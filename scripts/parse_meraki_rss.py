#!/usr/bin/env python3
"""Parse Meraki Community RSS using stdlib only (no lxml). Emits JSON for Ansible."""

import json
import sys
import xml.etree.ElementTree as ET


def parse_rss(path):
    tree = ET.parse(path)
    descriptions = []
    links = []
    for item in tree.getroot().iter("item"):
        desc_el = item.find("description")
        link_el = item.find("link")
        desc = (desc_el.text or "") if desc_el is not None else ""
        link = (link_el.text or "") if link_el is not None else ""
        descriptions.append({"description": desc.strip()})
        links.append({"link": link.strip()})
    return {"descriptions": descriptions, "links": links}


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: parse_meraki_rss.py <rss.xml>", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(parse_rss(sys.argv[1])))


if __name__ == "__main__":
    main()
