#!/usr/bin/env bash

set -e

memgen example/dmpc.pdb example/dopc.pdb tmp/membrane1.pdb --ratio 1 4 \
    --area-per-lipid 65 --water-per-lipid 40 --lipids-per-monolayer 128 \
    --png tmp/membrane1.png --topology tmp/membrane1.top

[ -e tmp/membrane1.pdb ]
[ -e tmp/membrane1.png ]
[ -e tmp/membrane1.top ]

memgen -n 32 -a 85 -s 1000 -b hexagonal example/popc.pdb tmp/membrane2.pdb

[ -e tmp/membrane2.pdb ]
