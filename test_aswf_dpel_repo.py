#
# partcad-openusd-aswf-dpel, 2026
#
# Licensed under Apache License, Version 2.0.
#
"""Tests of the ASWF DPEL plugin, with the library answered from a table.

The archives are laid out as ALab's and Moore Lane's are, with made-up layers
in them, and are served with range requests as the library's are: they are read
a member a request, and never downloaded whole. Nothing here touches the
network.
"""

import base64
import importlib.util
import io
import os
import re
import runpy
import zipfile

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PLUGIN = os.path.join(_HERE, "aswf_dpel_repo.py")
_SPEC = importlib.util.spec_from_file_location("aswf_dpel_repo_under_test", _PLUGIN)
plugin = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(plugin)
ua = plugin.ua


def _usda(text=""):
    return ("#usda 1.0\n" + text).encode()


def _zip(members):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in members.items():
            z.writestr(name, data)
    return buf.getvalue()


ALAB = {
    "ALab/entry.usda": _usda("( subLayers = [@./entity/decor_jar01/decor_jar01.usda@] )\n"),
    "ALab/entity/decor_jar01/decor_jar01.usda": _usda(
        'def "jar" ( references = @../../fragment/geo/decor_jar01/pose.usdc@ ) {}\n'
        'def "hi" ( references = @fragment/geo/decor_jar01/render_high.usdc@ ) {}\n'
    ),
    "ALab/entity/decor_jar01/modelling/decor_jar01_modelling.usda": _usda(),
    "ALab/fragment/geo/decor_jar01/pose.usdc": _usda(),
    "ALab/fragment/tex/decor_jar01/albedo.exr": b"exr",
}
MOORE = {"Intel_mooreLane_v1_2_0/Intel_mooreLane/USD/MooreLane_ASWF_0623.usda": _usda("#" * 4000)}
TABLE = {plugin.ALAB: _zip(ALAB), plugin.MOORE_LANE: _zip(MOORE)}


class Wire:
    def __init__(self):
        self.asked = []

    def __call__(self, url, headers=None, method=None, timeout=120):
        headers = dict(headers or {})
        self.asked.append((url, headers.get("Range")))
        if url.startswith(plugin.BUCKET + "?"):
            assert "delimiter=%2F" in url, "the bucket is listed a folder at a time"
            body = (
                b"<ListBucketResult><IsTruncated>false</IsTruncated>"
                b"<Contents><Key>%s</Key><Size>2000000000</Size></Contents></ListBucketResult>" % plugin.LION.encode()
            )
            return ua.Response(200, {}, body, url)
        if url not in TABLE:
            return ua.Response(404, {}, b"", url)
        body = TABLE[url]
        if not headers.get("Range"):
            raise AssertionError("an archive of gigabytes is never asked for whole")
        start, end = (int(v) for v in re.match(r"bytes=(\d+)-(\d+)", headers["Range"]).groups())
        end = min(end, len(body) - 1)
        return ua.Response(
            206, {"Content-Range": "bytes %d-%d/%d" % (start, end, len(body))}, body[start : end + 1], url
        )


@pytest.fixture
def dpel(tmp_path, monkeypatch):
    monkeypatch.setenv("PARTCAD_OPENUSD_ASWF_DPEL_CACHE", str(tmp_path))

    def make(**parameters):
        made = plugin.AswfDpel({"parameters": parameters})
        made.http.request = Wire()
        return made

    return make


def test_a_child_package_per_scene(dpel):
    assert dpel().get("deps") == ["alab", "materialx-lion", "moore-lane"]


def test_alab_is_the_lab_and_each_of_its_entities(dpel):
    made = dpel()
    parts = made.get("alab/objects/part")
    assert sorted(parts) == sorted(["ALab"] + plugin.ALAB_ENTITIES)
    assert len(plugin.ALAB_ENTITIES) == len(set(plugin.ALAB_ENTITIES)) == 362
    assert parts["decor_jar01"]["license"] == "LicenseRef-ASWF-Digital-Assets-1.1"
    assert made.http.request.asked == [], "listing ALab reads not even its archive's directory"


def test_listing_and_searching_ask_nothing_of_the_library(dpel):
    made = dpel()
    for package in ("alab", "moore-lane", "materialx-lion"):
        assert made.get(package + "/objects/part")
    hits = made.get("alab/search/part?q=beaker")
    assert "chemistry_beaker01" in hits and "decor_jar01" not in hits
    # An entity is tagged with its kind, which a search finds it by.
    decor = made.get("alab/search/part?q=decor")
    assert len(decor) == ua.DEFAULT_LIMIT and all(name.startswith("decor_") for name in decor)
    jars = made.get("alab/search/part?q=decor+jar")
    assert "decor_jar01" in jars and all("jar" in name for name in jars)
    assert made.http.request.asked == []


def test_an_entity_is_read_out_of_the_archive_with_what_it_lacks_reported(dpel, capsys):
    made = dpel()
    data = base64.b64decode(made.get("alab/files/decor_jar01.usdz"))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        # A search path ('fragment/...') is looked for from the top of the lab.
        assert z.namelist() == ["entity/decor_jar01/decor_jar01.usda", "fragment/geo/decor_jar01/pose.usdc"]
    assert "render_high.usdc" in capsys.readouterr().err


def test_a_scene_too_large_is_refused_before_it_is_fetched(dpel, capsys):
    made = dpel(max_size_mb=0.001)
    assert ua.serve(made, "moore-lane/files/MooreLane.usdz") is None
    assert "Raise the plugin's 'max_size_mb'" in capsys.readouterr().err
    lion = dpel()
    assert ua.serve(lion, "materialx-lion/files/lion_statue.usdz") is None
    assert not any(url.endswith(plugin.LION) for url, _ in lion.http.request.asked)


def test_the_plugin_is_named_as_the_package_declares_it():
    with open(os.path.join(_HERE, "partcad.yaml")) as f:
        text = f.read()
    name = re.search(r"^name: (\S+)", text, re.M).group(1)
    assert re.search(r"^  aswf_dpel_repo:\n    type: basic\n    path: aswf_dpel_repo.py", text, re.M)
    assert plugin.AswfDpel.PLUGIN == name + ":aswf_dpel_repo"


def test_partcad_runs_it_and_reads_the_answer_from_output(tmp_path, monkeypatch):
    monkeypatch.setenv("PARTCAD_OPENUSD_ASWF_DPEL_CACHE", str(tmp_path))
    result = runpy.run_path(_PLUGIN, init_globals={"request": {"key": "meta", "parameters": {}}}, run_name="get")
    assert result["output"]["result"]["manufacturable"] is False
