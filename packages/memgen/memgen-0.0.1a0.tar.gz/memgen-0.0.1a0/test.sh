#!/usr/bin/env bash

memgen example/dmpc.pdb example/dopc.pdb membrane.pdb --ratio 1 4 --area-per-lipid 55 --water-per-lipid 30 --lipids-per-monolayer 75 --added-salt 5 --box-shape hexagonal --png membrane.png --server localhost:3000
