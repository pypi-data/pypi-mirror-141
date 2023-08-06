from memgen.parse_cli import parse_cli, BoxShape


def test_minimal_example():
    """ Minimal example. Single lipid, with default settings. """

    cmd = 'memgen example/dmpc.pdb membrane.pdb'

    assert vars(parse_cli(cmd.split())) == {
      'input_pdbs': ['example/dmpc.pdb'],
      'output_pdb': 'membrane.pdb',
      'ratio': None,
      'area_per_lipid': 65,
      'water_per_lipid': 35,
      'lipids_per_monolayer': 64,
      'added_salt': 0,
      'box_shape': BoxShape.square,
      'png': None,
      'server': 'memgen.uni-saarland.de'
    }


def test_kitchen_sink_example():
    """ Two lipids and all possible options set. """

    cmd = """ memgen 
              example/dmpc.pdb example/dopc.pdb membrane.pdb --ratio 1 4
              --area-per-lipid 55 --water-per-lipid 30 --lipids-per-monolayer 75 --added-salt 5
              --box-shape hexagonal
              --png membrane.png
              --server localhost:3000 """

    assert vars(parse_cli(cmd.split())) == {
      'input_pdbs': ['example/dmpc.pdb', 'example/dopc.pdb'],
      'output_pdb': 'membrane.pdb',
      'ratio': [1, 4],
      'area_per_lipid': 55,
      'water_per_lipid': 30,
      'lipids_per_monolayer': 75,
      'added_salt': 5,
      'box_shape': BoxShape.hexagonal,
      'png': 'membrane.png',
      'server': 'localhost:3000'
    }
