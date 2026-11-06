# The ASWF Digital Production Example Library's USD for PartCAD

Serves the USD of the Academy Software Foundation's [Digital Production Example
Library](https://dpel.aswf.io) - which hosts two of the "Additional Assets" [openusd.org's Downloads
page](https://openusd.org/release/dl_downloads.html) lists, Animal Logic's ALab and Intel's 4004 Moore
Lane - as PartCAD parts, published as `//pub/collection/openusd/aswf-dpel/assets`:

| Package | What it is | Parts |
| --- | --- | --- |
| `assets/alab` | [ALab](https://dpel.aswf.io/alab/), Animal Logic's laboratory (2.1.0) | `ALab`, the whole lab, and each of its 362 entities, by name: `decor_jar01`, `chemistry_beaker01`, `book_encyclopedia01`, ... |
| `assets/moore-lane` | [4004 Moore Lane](https://dpel.aswf.io/4004-moore-lane/), Intel's house (1.2.0) | `MooreLane` |
| `assets/materialx-lion` | The MaterialX lion statue | `lion_statue` |

```shell
pc list parts //pub/collection/openusd/aswf-dpel/assets/alab
pc search parts -P //pub/collection/openusd/aswf-dpel/assets/alab -k beaker
pc inspect //pub/collection/openusd/aswf-dpel/assets/alab:decor_jar01
```

**Range requests, not downloads.** The archives are gigabytes - ALab's is 9.9 GB, Moore Lane's 8 GB -
and their server takes range requests. So listing and searching read nothing of them - the plugin
knows what each holds - and building an asset reads the archive's directory once (ALab's lists 14
thousand files, and took 18 seconds) and then the files the asset is made of, out of the archive a
request each: an ALab jar is 74 files and 2 MB.

**Moore Lane and the lion are large**: 1.1 GB of geometry and 1.9 GB. A part's file may be 512 MB
unless the plugin's `max_size_mb` says otherwise, and the plugin refuses them saying so, before it
has fetched more than it had to find that out. Take them on a machine with the memory for it.

**The library's licence.** Everything here is under the [ASWF Digital Assets License
v1.1](https://dpel.aswf.io/alab/alab-license/): for education, research, software and hardware
development, benchmarking and demonstration; a redistribution keeps its notice, and an image
published of it carries its copyright. Read it before you use what you build from this.

**No geometry is vendored.** Every asset is fetched from dpel-assets.aswf.io the first time a part of
it is built, and kept by PartCAD from then on.

**Nothing here is manufacturable.** These are scenes made to be rendered; the package says
`manufacturable: false`, and so does the plugin of what it serves.

Requires PartCAD 0.9.6 or newer: the first release whose `//builtin` has the `usd` part type.

## Listing, searching, building

**Listing and searching download no asset.** `pc list parts` and `pc search parts` are answered from
what the plugin itself knows each package holds - ALab 2.1.0's 362 entities by name - without a request
of any kind. Building an entity reads ALab's directory, a few MB of the 9.9 GB archive, once, and then
the entity's own files. What a part is made of is fetched when the part is built - by `pc inspect`, `pc
render`, `pc export`, or an assembly that places it - and then only that asset's own files, and kept.

`pc search parts -k <words>` is answered by the plugin, from the same catalog: a part matches when
every word is in its name, its description, its author, its tags or its package's name, and the ones
whose name matches come first. Each package answers with at most 20, or what `--limit` says (up to
100); search a package and every one below it with `-P '<package>...'`.

## What a part is

Every part here is `type: usd`: PartCAD's own part type for OpenUSD, in its `//builtin`, which reads a
stage with Pixar's USD library (`usd-core`), installed into the sandbox that builds the part and
nowhere else. The plugin's part is the file, and the part type makes the shape of it.

- **The file.** A part's file is a USDZ package of the asset, which the plugin makes when the part is
  built. An asset published as a `.usdz` is served as it is. One published as `.usd`, `.usda` or
  `.usdc` layers is a root layer that names others by relative path - sublayers, references,
  payloads - and the plugin follows those names (in a text layer its `@asset paths@`, in a binary one
  its token table) and packs the root and everything it reaches into a USDZ, root first, as the format
  wants it. Textures are left out unless the plugin's `textures` says otherwise: PartCAD builds
  geometry. A file an asset names that the source does not have is reported, and the asset is served
  without it.
- **The shape.** What is built is the stage's default prim - what a reference to the asset brings
  in - and every mesh it shows: through native instancing and point instancers, of the purpose asked
  for, visible ones only, in millimetres (by the stage's `metersPerUnit`) with Z up. A cube, sphere,
  cylinder, cone or capsule is meshed; curves, points and volumes are not surfaces, and are left out
  and counted. Up to 20 000 triangles, each triangle is a face, and two that share an edge share it:
  the part is drawn as lines, written to STEP, and made the solid it bounds where it closes. Past
  that, the triangles of each colour are one mesh: fast at any size, drawn shaded (`pc render --style
  shaded`) and written as STL, 3MF or glTF, but with no edges for a line drawing. Each face is drawn in
  the colour its material's `diffuseColor`, or else its `displayColor`, gives. The part is a surface
  as USD describes it - what a renderer draws - and PartCAD says so when it is not a solid.
- **The size.** It is what the asset says it is, by its `metersPerUnit`: an asset authored in the
  wrong units comes out as large, or as small, as it says.
- **The other reader.** `reader=cadmpeg` reads the same file with cadmpeg instead, PartCAD's
  converter for CAD formats, which reads USD from its 0.6.8 release on: what a render shows, at the
  stage's static values. It does no point instancer (the City Set's buildings, the chess set's pawns
  are left out), no `purpose` but `render` and no `time` but `default`, and a prim it reads as an
  exact surface (a cube, a sphere) is counted and left out rather than meshed. It is there as a
  second opinion and a fallback; `usd-core` is the reader to use.

Every part takes the part type's parameters, in its name (`King;purpose=proxy`) or in the `with` of
an enrich of it:

| Parameter | Default | What it is |
| --- | --- | --- |
| `reader` | `usd-core` | What reads the stage: `usd-core`, or `cadmpeg` (see above). |
| `prim` | the default prim | Build only what is under this prim; `/` is the whole stage. |
| `purpose` | `render` | `render`: what a final render draws; `proxy`: the stand-ins a viewer draws; `all`: both, and guides. |
| `surface` | `auto` | `faces`: a face per triangle; `mesh`: a mesh per colour; `auto`: `faces` up to 20 000 triangles. |
| `time` | `default` | The time code to read animated geometry at, skinning a character to it. `default` is what a viewer opens the stage at (its start time code, else its earliest sample), unposed. |
| `maxTriangles` | 5000000 | The most triangles the part may be: a scene of more is refused, saying so. |

PartCAD's own documentation of the part type is
[the `usd` part type](https://partcad.readthedocs.io/en/latest/config_parts.html#usd-files).

ALab's entities name meshes of two kinds, `pose` and `render_high`; the 2.1.0 archive has the first
and not the second, which is in the separate "techvars" archive, so an entity is built of its pose
meshes and the plugin says which files it went without.

## Parameters of the plugin

| Parameter | Default | What it is |
| --- | --- | --- |
| `textures` | `false` | Whether a part's USDZ carries the asset's textures too. ALab's are 4K EXR. |
| `max_size_mb` | `512` | The most a part's USDZ may be, in MB. |

Each is yours to set without touching this package, in your own `~/.partcad/config.yaml` under
`parameters`, by the plugin's name (`//pub/collection/openusd/aswf-dpel:aswf_dpel_repo`), or in a
package of your own, as an enrich of the plugin and a package it serves.

## Caching

The plugin keeps what the library answered under `~/.cache/partcad-openusd-aswf-dpel/` (or
`$PARTCAD_OPENUSD_ASWF_DPEL_CACHE`): each archive's directory for a week, and each file it read out of
one for good. Delete the directory to start over. PartCAD keeps every answer the plugin gives, files
included.

Every request says what it is: `User-Agent: Mozilla/5.0 (compatible; PartCAD-openusd-aswf-dpel/<version>;
+https://github.com/partcad/partcad-collection-openusd-aswf-dpel)`.

## Status

Run against dpel-assets.aswf.io: listing and searching the three packages make no request.
Building an entity read ALab's directory (14 190 files, 18 seconds) and then its own members: the jar
(92 by 92 by 145 mm) and a beaker (67 by 60 by 77 mm) were packed and read back by the part type with
usd-core 26.11; Moore Lane and the lion were refused for their size, as they should be.

Through PartCAD's own `usd` part type, run from the change that adds it to `//builtin` before its
release, with all six `partcad-collection-openusd-*` packages in one workspace: `pc list packages -r`
listed their 17 packages, and `pc search parts -P '<workspace>...'` answered across all of them in
about two seconds, each collection searching its own catalog; `pc info` built `chemistry_beaker01` (67
by 60 by 77 mm, a closed solid of 16 324 mm³), and refused the lion (1864 MB), saying how to take it.

The library holds more than this - Noa and the Airship, from AWS - but in Maya, not USD; and the
Pixar-listed scenes are what it is here for.

## Layout

| Path | Purpose |
| --- | --- |
| `partcad.yaml` | `//pub/collection/openusd/aswf-dpel`; the `assets` external dependency and the `aswf_dpel_repo` repository that serves it. |
| `aswf_dpel_repo.py` | The repository plugin: where the library keeps its archives. |
| `usd_assets.py` | What every OpenUSD collection plugin shares, byte for byte: following a USD asset's layers, packing a USDZ, reading remote archives, buckets and listings a piece at a time, searching a catalog, the keys PartCAD asks. |
| `shared.sha256` | The digests of the shared files and their tests. They are the same in every `partcad-collection-openusd-*` repository - pixar, usd-wg, apple, nvidia, aswf-dpel and disney-moana - and a test fails when one here differs: change them in all of them. |
| `test_*.py` | The tests. Nothing in them touches the network. |

```shell
python -m pytest
```

When what the plugin answers changes - here or in `usd_assets.py` - raise `CACHE_VERSION` in
`aswf_dpel_repo.py`: PartCAD keys everything it caches of this package on it, and an unchanged version
is answered from what it cached before.

## Licensing

The code here is Apache-2.0 (`LICENSE`). The assets are under the ASWF Digital Assets License v1.1:
ALab © Animal Logic (now Netflix Animation Studios), 4004 Moore Lane © Intel Corporation. Nothing of
them is in this repository.
