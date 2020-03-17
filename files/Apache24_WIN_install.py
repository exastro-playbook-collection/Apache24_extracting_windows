import re
import json
import sys
import os

# main process
args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
result = {}

input_parameter_path = path + '/' + "input_parameter_install"
# Load json file
with open(input_parameter_path) as file_object:
    lines = file_object.readlines()

for line in lines:
    if 'VAR_Apache24_WIN_localpkg_src' in line:
        result['VAR_Apache24_WIN_localpkg_src'] = line.split(':',1)[1].strip()
    if 'VAR_Apache24_WIN_localpkg_dst' in line:
        result['VAR_Apache24_WIN_localpkg_dst'] = line.split(':',1)[1].strip()
    if 'VAR_Apache24_WIN_path' in line:
        result['VAR_Apache24_WIN_path'] = line.split(':',1)[1].strip()
    if 'VAR_Apache24_WIN_localpkg_VC_file' in line:
        result['VAR_Apache24_WIN_localpkg_VC_file'] = line.split(':',1)[1].strip()
    if 'VAR_Apache24_WIN_localpkg_Apache_file' in line:
        result['VAR_Apache24_WIN_localpkg_Apache_file'] = line.split(':',1)[1].strip()

result['VAR_Apache24_WIN_VC_INSTALL'] = True
result['VAR_Apache24_WIN_ServiceName'] = 'Apache2.4'
result['VAR_Apache24_WIN_localpkg_upload'] = True

print(json.dumps(result))
