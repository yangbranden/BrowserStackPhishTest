import requests
import os
import json
import yaml
from enum import Enum

class Output(Enum):
    ALL = 0
    ANDROID = 1
    IOS = 2
    WINDOWS = 3
    MACOSX = 4

OUTPUT_MODE = Output.ALL

if OUTPUT_MODE == Output.ALL:
    output_file = "all_targets.yml"
elif OUTPUT_MODE == Output.ANDROID:
    output_file = "android.yml"
elif OUTPUT_MODE == Output.IOS:
    output_file = "ios.yml"
elif OUTPUT_MODE == Output.WINDOWS:
    output_file = "windows.yml"
elif OUTPUT_MODE == Output.MACOSX:
    output_file = "macosx.yml"

# OK WAIT I didn't realize this API was available
s = requests.Session()
s.auth = (os.environ.get("BROWSERSTACK_USERNAME"), os.environ.get("BROWSERSTACK_ACCESS_KEY"))

r = s.get("https://api.browserstack.com/automate/browsers.json")
output = json.loads(r.text)

selective_output = []
if OUTPUT_MODE == Output.ANDROID:
    for item in output:
        if item["os"] == "android":
            selective_output.append(item)
    output = selective_output
elif OUTPUT_MODE == Output.IOS:
    for item in output:
        if item["os"] == "ios":
            selective_output.append(item)
    output = selective_output
elif OUTPUT_MODE == Output.WINDOWS:
    for item in output:
        if item["os"] == "windows":
            selective_output.append(item)
    output = selective_output
elif OUTPUT_MODE == Output.MACOSX:
    for item in output:
        if item["os"] == "OS X":
            selective_output.append(item)
    output = selective_output

with open(output_file, "w") as f:
    f.write("# =======================================\n")
    f.write("# THIS FILE WAS GENERATED BY generate_targets.py\n")
    f.write("# =======================================\n")
    yaml.dump(output, f, default_flow_style=False)