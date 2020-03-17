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

file_path = []
file_path.append(path + '/command/5/stdout.txt')
file_path.append(path + '/command/6/stdout.txt')

result['VAR_Apache24_WIN_Start'] = False
result['VAR_Apache24_WIN_Enable'] = False
result['VAR_Apache24_WIN_ServiceName'] = 'Apache2.4'
for path in file_path:
    if os.path.isfile(path):
        with open(path) as file_object:
            lines = file_object.readlines()
        for line in lines:
            if (re.match( '\s*Running\s+Apache2.4\s+Apache2.4\s*', line,re.I) != None):
                result['VAR_Apache24_WIN_Start'] = True
            elif (re.match( '\s*Auto\s*', line,re.I) != None):
                result['VAR_Apache24_WIN_Enable'] = True
    else:
        result = {}

print(json.dumps(result))
