#
# partcad-openusd-aswf-dpel, 2026
#
# Licensed under Apache License, Version 2.0.
#
"""A PartCAD 'basic' repository plugin that serves the ASWF Digital Production Example Library's USD as parts.

Published as ``//pub/collection/openusd/aswf-dpel/assets``. The Academy Software
Foundation's Digital Production Example Library (https://dpel.aswf.io) hosts
two of the scenes openusd.org's Downloads page lists among its "Additional
Assets", and one more in USD:

    alab           Animal Logic's ALab: the lab as one scene ('ALab'), and each
                   of its 362 entities - a jar, a beaker, a book - as a part
    moore-lane     Intel's 4004 Moore Lane: a house, as one scene
    materialx-lion the MaterialX lion statue, as one part

Each is ``type: usd``, built by PartCAD's own part type of that name from a USDZ the
plugin packs of the asset's own layers (see usd_assets.py). The archives are
gigabytes - ALab's is 9.9 GB, Moore Lane's 8 GB - and their server takes
range requests, so an asset costs the members it is made of, read out of the
archive with a request each, and the archive's directory, read once and kept.
Listing and searching cost nothing: what each package holds is written down
here, for the release of it this plugin reads.

Moore Lane and the lion are larger than the 512 MB a part's file may be by
default; the plugin says so, and its 'max_size_mb' takes them.

PartCAD runs this script once per key (via runpy) with the key in
``request["key"]``; the answer goes in ``output``.
"""

import importlib.util
import os
import sys

# When this plugin's answers stopped meaning what they meant before. PartCAD
# keys everything it caches of this package on it, so raise it with any change
# to what is answered - here, or in usd_assets.py.
#
# v1: ALab 2.1.0, Moore Lane 1.2.0 and the MaterialX lion, as PartCAD 'usd' parts.
CACHE_VERSION = 1


def _shared():
    """usd_assets.py, beside this script, under a name of this plugin's own."""
    name = "_partcad_openusd_aswf_dpel_usd_assets"
    if name not in sys.modules:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usd_assets.py")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


ua = _shared()

SITE = "https://dpel.aswf.io/"
# The library's files, behind CloudFront; the bucket behind it lists them.
FILES = "https://dpel-assets.aswf.io/"
BUCKET = "https://aswf-dpel-assets.s3.amazonaws.com/"
DPEL_LICENSE = "LicenseRef-ASWF-Digital-Assets-1.1"

ALAB = FILES + "usd-alab/alab-v2.1.0.zip"
MOORE_LANE = FILES + "4004-moore-lane/intel_moorelane_v1_2_0.zip"
LION = "materialx-teapot-lion/lion_statue_hq.usd"

# ALab 2.1.0's entities: 'entity/<name>/<name>.usda' each, as its archive's
# directory has them. Named here so that listing and searching ALab reads not
# even that directory, which is megabytes of a 9.9 GB archive.
ALAB_ENTITIES = """
alab_set01 book_encyclopedia01 book_magazine01 books_encyclopedias01 books_magazines01 books_magazines02
chemistry_beaker01 chemistry_beaker02 chemistry_beaker03 chemistry_beaker_rack01 chemistry_beaker_stand01
chemistry_bottle01 chemistry_bottle02 chemistry_bottle03 chemistry_flask_stand01 chemistry_kipps_apparatus01
chemistry_magnetic_stirrer01 chemistry_microscope01 chemistry_test_tube01 chemistry_test_tube02
chemistry_test_tube03 construction_cinder_block01 decor_basket01 decor_beach_umbrella01 decor_beachball01
decor_blender01 decor_board_games01 decor_bonsai_jar01 decor_book_open01 decor_book_open02 decor_bottle_cap01
decor_bottle_soda01 decor_bottle_soda02 decor_can_half01 decor_can_half02 decor_can_half03 decor_can_half04
decor_choko_experiment01 decor_clip01 decor_cooler_box01 decor_cricket_ball01 decor_cricket_bat01
decor_cstand_clamp01 decor_cstand_ground01 decor_dish_rack01 decor_firecracker01 decor_flask_pump01
decor_foam_hand01 decor_glass01 decor_hair_dryer_torch01 decor_hazard_sign01 decor_helmet_head01 decor_jar01
decor_jar02 decor_jar03 decor_kerosene_lamp01 decor_macrame_hangar01 decor_mat01 decor_medical_screen01
decor_mug_coffee01 decor_mug_coffee02 decor_mug_coffee03 decor_necklace_curly01 decor_paper_notea01
decor_paper_notea02 decor_paper_notea03 decor_paper_notea04 decor_paper_noteb01 decor_paper_noteb02
decor_paper_noteb03 decor_paper_notec01 decor_paper_notec02 decor_paper_notec03 decor_paper_noted01
decor_paper_notee01 decor_paper_notef01 decor_paper_notef02 decor_paper_notef03 decor_paper_notef04
decor_paper_notef05 decor_paper_notef06 decor_paper_notef07 decor_paper_notef08 decor_paper_notef09
decor_paper_notef10 decor_paper_noteg01 decor_paper_noteh01 decor_paper_noteh02 decor_paper_notei01
decor_paper_notej01 decor_paper_notek01 decor_paper_notel01 decor_paper_notem01 decor_paper_noten01
decor_paper_noteo01 decor_paper_rolled01 decor_paper_rolled02 decor_party_lights01 decor_piggy_bank01
decor_pitch_experiment01 decor_plant_small01 decor_plant_small02 decor_plant_small03 decor_plant_small04
decor_planter01 decor_plastic_label01 decor_plastic_label02 decor_plastic_label03 decor_plastic_label04
decor_plastic_label05 decor_plastic_label06 decor_plastic_label07 decor_plastic_label08 decor_plastic_label09
decor_plastic_label10 decor_postera01 decor_posterb01 decor_pot01 decor_rocket_disk01 decor_seeding_tray01
decor_sheets_car01 decor_sheets_inspiration01 decor_sheets_planning01 decor_sheets_projector01
decor_soccer_ball01 decor_spray_can01 decor_spray_can02 decor_string01 decor_suitcase02 decor_suitcase03
decor_tennis_ball01 decor_tennis_racket01 decor_thumb_tack01 decor_toolbox01 decor_toy_dino01 decor_toy_dino02
decor_toy_penguin01 decor_tripod_head01 decor_tripod_tabletop01 decor_wooden_box01 dmp_skydome_alab01
electronics_audio_generator01 electronics_cabling electronics_cabling02 electronics_cabling03
electronics_cabling04 electronics_cabling05 electronics_camera01 electronics_camera02 electronics_car_battery01
electronics_ham_cabling01 electronics_ham_cabling02 electronics_ham_equipment01 electronics_ham_equipment02
electronics_ham_equipment03 electronics_ham_equipment04 electronics_ham_microphone01 electronics_lightmeter01
electronics_oscilloscope01 electronics_portable_tv01 electronics_powerpoint01 electronics_speaker01
electronics_spoolrack electronics_tape_recorder01 electronics_tesla_coil01 electronics_turntable01
electronics_wire_spool01 electronics_wire_spool02 electronics_wire_spool04 electronics_wire_spool05
electronics_wire_spool06 furniture_bench01 furniture_bench_seat01 furniture_blackboard01 furniture_lawn_chair02
furniture_lbracket01 furniture_lbracket02 furniture_organizer_drawers01 furniture_parts_cabinet01
furniture_parts_cabinet02 furniture_shelving01 furniture_sink01 furniture_wooden_shelf01 furniture_workbench01
lab_electronics01 lab_garage01 lab_hydrophonics01 lab_inspiration01 lab_planning01 lab_projector01 lab_remi01
lab_remi_body01 lab_remi_head01 lab_structure01 lab_workbench01 plant_choko_bud01 plant_choko_bud02
plant_choko_flower01 plant_choko_flower02 plant_choko_flower03 plant_choko_flower04 plant_choko_leaf01
plant_choko_leaf02 plant_choko_leaf03 plant_choko_leaf04 plant_choko_leaf05 plant_choko_leaf06
proc_dev_circuit_board_large01 proc_dev_circuit_board_large02 proc_dev_circuit_board_large03
proc_dev_circuit_board_medium01 proc_dev_circuit_board_medium02 proc_dev_circuit_board_medium03
proc_dev_circuit_board_medium04 proc_dev_circuit_board_small01 proc_dev_circuit_board_small02
proc_dev_circuit_board_small03 proc_dev_circuit_buzzer01 proc_dev_circuit_buzzer02 proc_dev_circuit_cable01
proc_dev_circuit_cable02 proc_dev_circuit_capacitor01 proc_dev_circuit_capacitor02 proc_dev_circuit_capacitor03
proc_dev_circuit_diode01 proc_dev_circuit_diode02 proc_dev_circuit_diode03 proc_dev_circuit_diode04
proc_dev_circuit_diode05 proc_dev_circuit_fuse01 proc_dev_circuit_fuse02 proc_dev_circuit_motherboard_large01
proc_dev_circuit_motherboard_large02 proc_dev_circuit_motherboard_large03 proc_dev_circuit_motherboard_medium01
proc_dev_circuit_motherboard_medium02 proc_dev_circuit_motherboard_medium03
proc_dev_circuit_motherboard_medium04 proc_dev_circuit_motherboard_small01 proc_dev_circuit_motherboard_small02
proc_dev_circuit_motherboard_small03 proc_dev_circuit_resistor01 proc_dev_circuit_resistor02
proc_dev_circuit_resistor03 proc_dev_circuit_resistor04 proc_dev_circuit_resistor05 proc_dev_circuit_resistor06
proc_dev_circuit_resistor07 proc_dev_circuit_resistor08 proc_dev_circuit_resistor09 proc_dev_circuit_resistor10
proc_dev_circuit_solder01 proc_dev_circuit_solder02 proc_dev_circuit_solder03 proc_dev_circuit_tranformer01
proc_dev_circuit_tranformer02 stationary_crayon_box01 stationary_notepad01 stationary_paper01 stationary_paper02
stationary_paper03 stationary_pencil01 stationary_pencil02 stationary_pencil03 stationary_protractor_box01
stationary_set_square01 stationary_set_square02 stationary_slide_rule01 stoat01 stoat_backpack01 stoat_body01
stoat_outfit01 structure_barrier01 structure_base01 structure_board01 structure_brick01 structure_brick02
structure_brick03 structure_brick04 structure_brick_broken01 structure_brick_broken02 structure_brick_broken03
structure_door01 structure_door_garage01 structure_hydroponics01 structure_roof structure_wall_back01
structure_wall_cabling01 structure_wall_fibro01 structure_wall_fibro02 structure_wall_fibro03
structure_wall_fibro04 structure_wall_fibro05 structure_wall_front01 structure_wall_left01
structure_wall_right01 structure_window_casement01 structure_window_louvered01 structure_window_louvered02
test202009demo_ll_leaf01_sm01 test_beast_generic01 tool_board01 tool_bolt01 tool_chisel01 tool_chisel02
tool_chisel03 tool_earmuffs01 tool_fertilizer_can01 tool_fishing_rod01 tool_garden_hose01 tool_hammer01
tool_hook_small01 tool_level01 tool_magnifying_lamp01 tool_oxy_tank01 tool_oxy_torch01 tool_pliers01
tool_power_cable01 tool_power_cable02 tool_power_cord01 tool_pvc_cap01 tool_retro_plug01 tool_retro_plug02
tool_retro_plug03 tool_saw01 tool_scraper01 tool_screw01 tool_screw02 tool_screwdriver01 tool_screwdriver02
tool_screwdriver03 tool_screwdriver04 tool_screwdriver_holder01 tool_shovel01 tool_soldering_iron01 tool_vice01
tool_washer01 tool_wrench_boxend01 tool_wrench_boxend02 tool_wrench_boxend03 tool_wrench_boxend04
tool_wrench_boxend05 tool_wrench_boxend06 tool_wrench_boxend07 tool_wrench_combination01
tool_wrench_combination02 tool_wrench_combination03 tool_wrench_combination04 toy_box01 toy_box02 toy_box03
toy_box04 toy_curly_surgery toy_fun_coil vegetation_bonsai01 vegetation_bonsai_branch01
vegetation_bonsai_branch02 vegetation_bonsai_branch03 vegetation_bonsai_trunk01 vegetation_bonsai_twig01
vegetation_bonsai_twig02 vegetation_bonsai_twig03
""".split()

COLLECTIONS = {
    "alab": ("Animal Logic's ALab: a laboratory, as one scene and as each of its entities.", SITE + "alab/"),
    "moore-lane": ("Intel's 4004 Moore Lane: a house, as one scene.", SITE + "4004-moore-lane/"),
    "materialx-lion": ("The MaterialX lion statue, in USD.", SITE),
}


class AswfDpel(ua.Source):
    NAME = "openusd-aswf-dpel"
    TITLE = "the ASWF Digital Production Example Library"
    URL = SITE
    DESC = (
        "The USD of the Academy Software Foundation's Digital Production Example Library (dpel.aswf.io): "
        "Animal Logic's ALab and each of its entities, Intel's 4004 Moore Lane, and the MaterialX lion."
    )
    LICENSE = DPEL_LICENSE
    VERSION = CACHE_VERSION
    REPOSITORY = "partcad-collection-openusd-aswf-dpel"
    PLUGIN = "//pub/collection/openusd/aswf-dpel:aswf_dpel_repo"

    def collections(self):
        return {name: ua.Collection(name, desc, url) for name, (desc, url) in COLLECTIONS.items()}

    def assets(self, collection):
        if collection == "alab":
            store = ua.ZipStore(self.http, ALAB, "alab-v2.1.0.zip", prefix="ALab")
            found = {
                "ALab": ua.Asset("ALab", store, "entry.usda", desc="ALab: the whole laboratory, every entity in "
                                 "place.", url=SITE + "alab/", license=DPEL_LICENSE, author="Animal Logic")
            }  # fmt: skip
            for name in ALAB_ENTITIES:
                # Its kind, the first word of its name ('decor', 'tool', 'chemistry'), is what it is tagged.
                found[ua.safe_id(name)] = ua.Asset(
                    name, store, "entity/%s/%s.usda" % (name, name),
                    desc="%s, an entity of ALab." % name.replace("_", " "), url=SITE + "alab/",
                    license=DPEL_LICENSE, author="Animal Logic", tags=[name.split("_")[0].rstrip("0123456789")],
                )  # fmt: skip
            return found
        if collection == "moore-lane":
            store = ua.ZipStore(
                self.http, MOORE_LANE, "intel_moorelane_v1_2_0.zip", prefix="Intel_mooreLane_v1_2_0/Intel_mooreLane"
            )
            return {
                "MooreLane": ua.Asset(
                    "MooreLane", store, "USD/MooreLane_ASWF_0623.usda",
                    desc="4004 Moore Lane: the house, its point instances and its lights. Its geometry alone is "
                    "1.1 GB: raise the plugin's 'max_size_mb' to take it.",
                    url=SITE + "4004-moore-lane/", license=DPEL_LICENSE, author="Intel",
                ),
            }  # fmt: skip
        if collection == "materialx-lion":
            # The bucket is listed a folder at a time, and only once the lion is built.
            store = ua.S3Store(self.http, BUCKET)
            return {
                "lion_statue": ua.Asset(
                    "lion_statue", store, LION,
                    desc="A lion statue, the MaterialX project's. 2 GB: raise the plugin's 'max_size_mb' to take it.",
                    url=SITE, license=DPEL_LICENSE,
                ),
            }  # fmt: skip
        return {}


def get(key):
    return ua.serve(AswfDpel(globals().get("request")), key)


# Last, so that everything above is defined when PartCAD runs this.
if __name__ == "get":
    output = {"result": get(request["key"])}  # noqa: F821 - injected by the runtime
else:
    output = {}
