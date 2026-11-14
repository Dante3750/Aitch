"""Builds rules/ads.json from EasyList's ad-server list plus tools/extra_domains.txt."""
import os, re, json, sys
src, out = sys.argv[1], sys.argv[2]
pat = re.compile(r'^\|\|([a-z0-9.-]+\.[a-z]{2,})\^(\$third-party)?$')
doms = set()
skipped = 0
for line in open(src, encoding='utf-8'):
    line = line.strip()
    if not line or line[0] in '![': continue
    m = pat.match(line)
    if m: doms.add(m.group(1))
    else: skipped += 1
doms |= {l.strip() for l in open(os.path.join(os.path.dirname(__file__), 'extra_domains.txt')) if l.strip()}
doms = sorted(doms)
TYPES = ["sub_frame","script","image","xmlhttprequest","media","ping","stylesheet","font","websocket","other"]
rules, CH = [], 1000
for i in range(0, len(doms), CH):
    rules.append({"id": i//CH + 1, "priority": 1, "action": {"type": "block"},
        "condition": {"requestDomains": doms[i:i+CH], "domainType": "thirdParty", "resourceTypes": TYPES}})
json.dump(rules, open(out, 'w'), separators=(',', ':'))
print(len(doms), "domains,", len(rules), "rules,", skipped, "skipped")
