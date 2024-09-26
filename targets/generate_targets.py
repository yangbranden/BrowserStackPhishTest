import requests
import os
import sys
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
CUSTOM_OFILE = None # "./targets/test"
SINGLE_FILE = True
ENTRIES_PER_FILE = 6 # my limit with 1 parallel thread is 6 (1 + 5 queued); see https://www.browserstack.com/docs/automate/selenium/queue-tests

if OUTPUT_MODE == Output.ALL:
    output_location = "./targets/all_targets"
elif OUTPUT_MODE == Output.ANDROID:
    output_location = "./targets/android"
elif OUTPUT_MODE == Output.IOS:
    output_location = "./targets/ios"
elif OUTPUT_MODE == Output.WINDOWS:
    output_location = "./targets/windows"
elif OUTPUT_MODE == Output.MACOSX:
    output_location = "./targets/macosx"
    
if CUSTOM_OFILE is not None:
    output_location = CUSTOM_OFILE

# OK WAIT I didn't realize this API was available
s = requests.Session()
s.auth = (os.environ.get("BROWSERSTACK_USERNAME"), os.environ.get("BROWSERSTACK_ACCESS_KEY"))

r = s.get("https://api.browserstack.com/automate/browsers.json")
output = json.loads(r.text)

selective_output = []

# Quick fix: fields cannot have value of null (skip if null)
for item in output:
    null_fields = [field for field in item if item[field] is None]
    for n in null_fields:
        item.pop(n)

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
        if item["os"] == "Windows":
            selective_output.append(item)
    output = selective_output
elif OUTPUT_MODE == Output.MACOSX:
    for item in output:
        if item["os"] == "OS X":
            selective_output.append(item)
    output = selective_output

# create the output directory; if it already exists, remove
if not SINGLE_FILE:
    if os.path.exists(output_location):
        for root, dirs, files in os.walk(output_location, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(output_location)
    os.makedirs(output_location)

if SINGLE_FILE:
    with open(f"{output_location}.yml", "w") as f:
        f.write("# =======================================\n")
        f.write("# FILE GENERATED BY generate_targets.py\n")
        f.write("# =======================================\n")
        yaml.dump(output, f, default_flow_style=False)
else:
    for i in range(0, len(output), ENTRIES_PER_FILE):
        batch = output[i:i+ENTRIES_PER_FILE]
        file_index = i // ENTRIES_PER_FILE
        with open(f"{output_location}/{file_index}.yml", "w") as f:
            f.write("# =======================================\n")
            f.write("# FILE GENERATED BY generate_targets.py\n")
            f.write("# =======================================\n")
            yaml.dump(batch, f, default_flow_style=False)