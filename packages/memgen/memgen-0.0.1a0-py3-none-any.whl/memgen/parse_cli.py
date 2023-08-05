import argparse
from enum import Enum


class BoxShape(Enum):
    square = 'square'
    hexagonal = 'hexagonal'

    def __str__(self):
        return self.value


def parse_cli(argv):
    parser = argparse.ArgumentParser('memgen', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input_pdbs", nargs="+", help="PDB files with lipids.")
    parser.add_argument("output_pdb", help="Generated membrane.")

    parser.add_argument("-c", "--ratio", nargs="*", type=int,
            help=""" Lipid concentration ratio. For example: 1 4 (same as 20 80).
                     It means 20%% of the first lipid and 80%% of the second. """)
    parser.add_argument("-a", "--area-per-lipid", type=int, default=65, help="Area per lipid (Å²)")
    parser.add_argument("-w", "--water-per-lipid", type=int, default=35, help="Water molecules per lipid")
    parser.add_argument("-n", "--lipids-per-monolayer", type=int, default=64, help="Lipids per monolayer")
    parser.add_argument("-s", "--added-salt", type=int, default=0, help="Added salt (milli molar)")
    parser.add_argument("-b", "--box-shape", type=BoxShape, choices=list(BoxShape), default=BoxShape.square, help="Box shape")
    parser.add_argument("--png", help="A small thumbnail depicting generated membrane.")

    maintenance = parser.add_argument_group('Maintenance')
    maintenance.add_argument("--server", default="memgen.uni-saarland.de", help="Hostname of MemGen REST API server.")

    args = parser.parse_args(argv[1:])

    # Setting equal ratio of lipids if ratio not specified. For two lipids 1:1, for three 1:1:1 (33%/33%/33%) and so on.
    if len(args.input_pdbs) > 1 and args.ratio is None:
        args.ratio = [1] * len(args.input_pdbs)

    return args
