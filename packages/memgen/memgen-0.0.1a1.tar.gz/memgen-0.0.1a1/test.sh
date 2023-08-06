#!/usr/bin/env bash

set -e

memgen example/dmpc.pdb example/dopc.pdb membrane.pdb --ratio 1 4 --area-per-lipid 65 --water-per-lipid 40 --lipids-per-monolayer 128 --png membrane.png

[ -e membrane.pdb ]
[ -e membrane.png ]
