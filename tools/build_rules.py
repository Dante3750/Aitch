"""Builds rules/ads.json from EasyList network-rule files plus tools/extra_domains.txt.

Usage: python3 tools/build_rules.py rules/ads.json easylist_*.txt

Plain ad-server domains are packed into a few big rules. Path rules and
exceptions (@@) are converted one-to-one. Anything Chrome/Firefox
declarativeNetRequest cannot express (regex, $rewrite, $csp, $popup...) is skipped.
"""
import os, re, json, sys

out, sources = sys.argv[1], sys.argv[2:]
PLAIN = re.compile(r'^\|\|([a-z0-9.-]+\.[a-z]{2,})\^(\$third-party)?$')
TYPES = {"script": "script", "image": "image", "stylesheet": "stylesheet",
         "subdocument": "sub_frame", "xmlhttprequest": "xmlhttprequest", "media": "media",
         "font": "font", "object": "object", "ping": "ping", "websocket": "websocket",
         "other": "other"}
SUB = ["sub_frame", "script", "image", "xmlhttprequest", "media", "ping",
       "stylesheet", "font", "websocket", "object", "other"]
DOMAIN_OK = re.compile(r'^[a-z0-9.-]+\.[a-z0-9-]+$')

def convert(line):
    """Returns ('domain', d) | ('rule', action, condition) | None."""
    allow = line.startswith("@@")
    if allow:
        line = line[2:]
    m = PLAIN.match(line)
    if m and not allow:
        return ("domain", m.group(1))
    pattern, _, opts = line.partition("$") if "$" in line else (line, "", "")
    # '$' can appear inside a pattern; only treat the last one as the options marker
    if "$" in line:
        i = line.rfind("$")
        pattern, opts = line[:i], line[i + 1:]
    if not pattern or (pattern.startswith("/") and pattern.endswith("/") and len(pattern) > 1):
        return None  # regex rule
    if not pattern.isascii() or pattern.startswith("||*") or len(pattern) < 4:
        return None
    cond, inc, exc, action = {"urlFilter": pattern}, [], [], "allow" if allow else "block"
    for o in filter(None, opts.split(",")):
        neg, name = o.startswith("~"), o.lstrip("~")
        if name == "third-party":
            cond["domainType"] = "firstParty" if neg else "thirdParty"
        elif name in TYPES:
            (exc if neg else inc).append(TYPES[name])
        elif name.startswith("domain="):
            yes, no = [], []
            for d in name[7:].split("|"):
                target = no if d.startswith("~") else yes
                d = d.lstrip("~")
                if not DOMAIN_OK.match(d):
                    return None
                target.append(d)
            if yes: cond["initiatorDomains"] = yes
            if no: cond["excludedInitiatorDomains"] = no
        elif name == "document" and allow and not neg:
            action, inc = "allowAllRequests", ["main_frame", "sub_frame"]
        elif name == "match-case":
            cond["isUrlFilterCaseSensitive"] = True
        else:
            return None  # generichide, rewrite, csp, popup, ...
    if action == "allowAllRequests":
        cond["resourceTypes"] = ["main_frame", "sub_frame"]
    elif inc:
        cond["resourceTypes"] = sorted(set(inc))
    elif exc:
        cond["excludedResourceTypes"] = sorted(set(exc) | {"main_frame"})
    return ("rule", action, cond)

domains, converted, skipped, seen = set(), [], 0, set()
for src in sources:
    for line in open(src, encoding="utf-8"):
        line = line.strip()
        if not line or line[0] in "![" or "##" in line or "#@#" in line or "#?#" in line:
            continue
        r = convert(line)
        if r is None:
            skipped += 1
        elif r[0] == "domain":
            domains.add(r[1])
        else:
            key = json.dumps(r, sort_keys=True)
            if key not in seen:
                seen.add(key)
                converted.append(r)

extra = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra_domains.txt")
domains |= {l.strip() for l in open(extra) if l.strip()}
domains = sorted(domains)

rules, CHUNK = [], 1000
for i in range(0, len(domains), CHUNK):
    rules.append({"id": len(rules) + 1, "priority": 1, "action": {"type": "block"},
                  "condition": {"requestDomains": domains[i:i + CHUNK],
                                "domainType": "thirdParty", "resourceTypes": SUB}})
PRIORITY = {"block": 1, "allow": 2, "allowAllRequests": 3}
for _, action, cond in converted:
    rules.append({"id": len(rules) + 1, "priority": PRIORITY[action],
                  "action": {"type": action}, "condition": cond})

json.dump(rules, open(out, "w"), separators=(",", ":"))
n = lambda a: sum(1 for r in converted if r[1] == a)
print(f"{len(domains)} ad-server domains, {n('block')} path rules, "
      f"{n('allow') + n('allowAllRequests')} exceptions, {skipped} skipped, {len(rules)} rules total")
