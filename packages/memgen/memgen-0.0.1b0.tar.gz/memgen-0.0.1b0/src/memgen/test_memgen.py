import os.path
from tempfile import TemporaryDirectory

from memgen import memgen
from memgen.box_shape import BoxShape


def test_two_lipids():
  with TemporaryDirectory() as temporary_dir:
    output_pdb = f"{temporary_dir}/membrane.pdb"
    output_png = f"{temporary_dir}/membrane.png"
    output_topology = f"{temporary_dir}/membrane.top"

    memgen(["example/dmpc.pdb", "example/dopc.pdb"], output_pdb, png=output_png, topology=output_topology,
        ratio=[1, 4], area_per_lipid=65, water_per_lipid=40, lipids_per_monolayer=128)

    assert(os.path.exists(output_pdb))
    assert(os.path.exists(output_png))

def test_hexagon_with_salt():
  with TemporaryDirectory() as temporary_dir:
    output_pdb = f"{temporary_dir}/membrane.pdb"
    output_png = f"{temporary_dir}/membrane.png"

    memgen(["example/popc.pdb"], output_pdb, png=output_png,
        area_per_lipid=85, lipids_per_monolayer=32,
        added_salt=1000, box_shape=BoxShape.hexagonal)

    assert(os.path.exists(output_pdb))
    assert(os.path.exists(output_png))
