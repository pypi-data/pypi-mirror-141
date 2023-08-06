import os.path
from tempfile import TemporaryDirectory

from memgen import memgen


def test_memgen():
  with TemporaryDirectory() as temporary_dir:
    output_pdb = f"{temporary_dir}/membrane.pdb"
    output_png = f"{temporary_dir}/membrane.png"

    memgen(["example/dmpc.pdb", "example/dopc.pdb"], output_pdb, png=output_png,
        ratio=[1, 4], area_per_lipid=65, water_per_lipid=40, lipids_per_monolayer=128)

    assert(os.path.exists(output_pdb))
    assert(os.path.exists(output_png))
