import Create_SVG
import json
import xml.etree.ElementTree as et

rt = et.Element("OfficialChips", {
    "version": "0.0.0"
})

rt.attrib = {}

chips = {}
ports = {}

with open("Generated/chips.json") as cFile, open("Generated/ports.json") as pFile:
    chips = json.load(cFile)
    ports = json.load(pFile)

Create_SVG.setup_svg_generator(chips, ports)
i = True
for chipID in chips.keys():
    et.register_namespace("", "http://www.w3.org/2000/svg")
    newSVG = et.fromstring(Create_SVG.generate_svg(chipID, False))
    newSVG.attrib = {
        "id": chipID
    }
    newSVG.tag = "ChipEntry"
    if i:
        print(newSVG)
        i = False
    newSVG.remove(newSVG.find("{http://www.w3.org/2000/svg}defs"))
    rt.append(newSVG)

with open("Generated/FullTree.xml", "wt") as Ft:
    #inefficient af
    outStr = et.tostring(rt, encoding="unicode").replace(":ns0", "").replace("ns0:", "")
    Ft.write(outStr)