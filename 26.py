import gzip
import json


def get_uk_text():
    with gzip.open("./jawiki-country.json.gz") as f:
        for line in f:
            json_dict = json.loads(line)
            if "イギリス" in json_dict["title"]:
                return json_dict["text"]


import re
doc = get_uk_text().split("\n")
rb = re.compile("^{{基礎情報(.+)")
rend = re.compile("^}}")
r = re.compile("^\|(.+) = (.+)")

enter = False
end = False
d = {}
for line in doc:
    if end:
        break
    if not enter:
        if rb.match(line):
            enter = True
            continue
    elif enter:
        for it in r.finditer(line):
            d[it.group(1)] = it.group(2)
            raw = it.group(2)
            replaced = raw
            for i in re.finditer(r"'{2}(\w+)'{2}", raw):
                replaced = raw.replace("'{}'".format(i.group(0)), i.group(1))
            d[it.group(1)] = replaced
        if rend.match(line):
            end = True
            continue
    else:
        pass

for k, v in d.items():
    print("{}: {}".format(k, v))
