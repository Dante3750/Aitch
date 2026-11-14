"""Builds content/selectors.js from EasyList's generic hiding list (simple selectors only)."""
import os, re, json, sys
src, out = sys.argv[1], sys.argv[2]
simple = re.compile(r'^##((?:[a-zA-Z][\w-]*)?(?:[.#][\w-]+)*(?:\[[\w-]+(?:[\^*$]?="[^"\\]*")?\])*)$')
sels = {m.group(1) for l in open(src, encoding='utf-8') if (m := simple.match(l.strip())) and m.group(1)}
sels |= {l.strip() for l in open(os.path.join(os.path.dirname(__file__), 'extra_selectors.txt')) if l.strip()}
sels = sorted(sels)
open(out, 'w').write("// Generated from EasyList (GPLv3 / CC BY-SA 3.0). Do not edit by hand.\n"
    "globalThis.DANTEHELP_SELECTORS = " + json.dumps(sels, separators=(',', ':')) + ";\n")
print(len(sels), "selectors")
