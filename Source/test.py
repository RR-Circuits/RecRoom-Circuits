import Create_SVG
import json

chips = {}
ports = {}

with open("Generated/chips.json", encoding="utf8") as chipsfile, open("Generated/ports.json", encoding="utf8") as portsfile:
    chips = json.load(chipsfile)
    ports = json.load(portsfile)


Create_SVG.setup(chips, ports)
returns = Create_SVG.Generate("ff2d1f81-d76c-456f-acf0-af1861822681", True)
with open("Generated/OutSVG.png", "wb") as file:
    file.write(returns)