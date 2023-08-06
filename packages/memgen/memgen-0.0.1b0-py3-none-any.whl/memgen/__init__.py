import sys

from memgen.parse_cli import parse_cli
from memgen.memgen import memgen


def main():
  args = parse_cli(sys.argv)

  memgen(args.input_pdbs, args.output_pdb, png=args.png,
      topology=args.topology,
      ratio=args.ratio,
      area_per_lipid=args.area_per_lipid,
      water_per_lipid=args.water_per_lipid,
      lipids_per_monolayer=args.lipids_per_monolayer,
      added_salt=args.added_salt,
      box_shape=args.box_shape,
      server=args.server
  )

from memgen.box_shape import BoxShape
