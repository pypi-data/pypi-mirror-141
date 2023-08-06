#!/usr/bin/env bash

set -e

memgen example/dmpc.pdb example/dopc.pdb membrane1.pdb --ratio 1 4 --area-per-lipid 65 --water-per-lipid 40 --lipids-per-monolayer 128 --png membrane1.png

[ -e membrane1.pdb ]
[ -e membrane1.png ]

memgen -n 32 -a 85 -s 1000 -b hexagonal example/popc.pdb membrane2.pdb

[ -e membrane2.pdb ]
