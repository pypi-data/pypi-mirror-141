import base64
import http.client
import json
from typing import List, Optional

from memgen.parse_cli import BoxShape
from memgen.defaults import Defaults


def jupyter_display(png):
  if png is None:
    return None

  try:
    from IPython.display import Image

    return Image(filename=png)
  except ImportError as e:
    pass


def memgen(
    input_pdbs: List[str],
    output_pdb: str,
    ratio: Optional[List[int]] = None,
    area_per_lipid: int = Defaults.area_per_lipid,
    water_per_lipid: int = Defaults.water_per_lipid,
    lipids_per_monolayer: int = Defaults.lipids_per_monolayer,
    box_shape: BoxShape = Defaults.box_shape,
    png: Optional[str] = None,
    server: str = Defaults.server
):
  print(f'Submitting "{", ".join(input_pdbs)}" to "{server}". Please wait...')

  encoded_input_pdbs_content = []

  for input_pdb in input_pdbs:
    with open(input_pdb, 'rb') as fp:
      encoded_input_pdbs_content.append(str(base64.b64encode(fp.read()), 'ascii'))

  connection = http.client.HTTPConnection(server)

  connection.request('POST', '/api/submit', json.dumps({
    'pdbs': encoded_input_pdbs_content,
    'ratio': ratio,
    'areaPerLipid': area_per_lipid,
    'waterPerLipid': water_per_lipid,
    'lipidsPerMonolayer': lipids_per_monolayer
  }), {'Content-type': 'application/json'})

  res = connection.getresponse()

  res_body = json.loads(res.read().decode())

  if res.status == 200:
    with open(output_pdb, 'wb') as pdb_fp:
      pdb_fp.write(base64.b64decode(res_body['pdb']))

    if png:
      with open(png, 'wb') as png_fp:
        png_fp.write(base64.b64decode(res_body['png']))

    if png:
      print(f'Output saved as "{output_pdb}" and "{png}".')
    else:
      print(f'Output saved as "{output_pdb}".')

    return jupyter_display(png)
  else:
    print(f"Server response: {res_body['error']}")
    print(f'Saving error output as "{output_pdb}-out.log" and "{output_pdb}-out.log".')

    with open(f'{output_pdb}-out.log', 'w') as std_out_fp:
      std_out_fp.write(res_body['stdOut'])

    with open(f'{output_pdb}-err.log', 'w') as std_err_fp:
      std_err_fp.write(res_body['stdErr'])

    exit(1)
