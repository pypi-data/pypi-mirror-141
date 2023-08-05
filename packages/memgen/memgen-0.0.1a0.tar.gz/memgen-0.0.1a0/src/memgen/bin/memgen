#!/usr/bin/env python3

import base64
import http.client
import json
import sys

from memgen.parse_cli import parse_cli

args = parse_cli(sys.argv)

print(f'Submitting "{", ".join(args.input_pdbs)}" to "{args.server}". Please wait...')

input_pdbs_content = []
encoded_input_pdbs_content = []

for input_pdb in args.input_pdbs:
  with open(input_pdb, 'rb') as fp:
    encoded_input_pdbs_content.append(str(base64.b64encode(fp.read()), 'ascii'))

connection = http.client.HTTPConnection(args.server)

connection.request('POST', '/api/submit', json.dumps({
  'pdbs': encoded_input_pdbs_content,
  'ratio': args.ratio,
  'areaPerLipid': args.area_per_lipid,
  'waterPerLipid': args.water_per_lipid,
  'n': args.lipids_per_monolayer
}), {'Content-type': 'application/json'})

res = connection.getresponse()

res_body = json.loads(res.read().decode())

if res.status == 200:
  with open(args.output_pdb, 'wb') as pdb_fp:
    pdb_fp.write(base64.b64decode(res_body['pdb']))

  if args.png:
    with open(args.png, 'wb') as png_fp:
      png_fp.write(base64.b64decode(res_body['png']))

  if args.png:
    print(f'Output saved as "{args.output_pdb}" and "{args.png}".')
  else:
    print(f'Output saved as "{args.output_pdb}".')
else:
  print(f"Server response: {res_body['error']}")
  print(f'Saving error output as "{args.output_pdb}-out.log" and "{args.output_pdb}-out.log".')

  with open(f'{args.output_pdb}-out.log', 'w') as std_out_fp:
    std_out_fp.write(res_body['stdOut'])

  with open(f'{args.output_pdb}-err.log', 'w') as std_err_fp:
    std_err_fp.write(res_body['stdErr'])

  exit(1)
