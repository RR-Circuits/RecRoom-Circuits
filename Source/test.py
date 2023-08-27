import Create_SVG
import json

chips = {}
ports = {}

with open("Generated/chips.json", encoding="utf8") as chipsfile, open("Generated/ports.json") as portsfile:
    chips = json.load(chipsfile)
    ports = json.load(portsfile)


Create_SVG.setup(chips, ports)
returns = Create_SVG.Generate("0ccb153c-dd08-4f22-80fd-9d8c5940928c", True, True)
with open("Generated/OutSVG.png", "wb") as file:
    file.write(returns)