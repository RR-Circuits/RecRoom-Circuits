import Create_SVG
import Translate_JSON
import json
import time

#with open("Generated/Chips_OLD.json", encoding="utf8") as file:
#    oldJSON = json.load(file)
#    chips, ports = Translate_JSON.ExtractChipJSON(oldJSON)
with open("Generated/chips.json", encoding="utf8") as chips, open("Generated/ports.json", encoding="utf8") as ports:
    chip = json.load(chips)
    port = json.load(ports)
    Create_SVG.setup_svg_generator(chip, port)

returned = Create_SVG.generate_svg("96a8fe50-bc37-458b-bac9-582d45314779", False)

with open("Generated/newtest.svg", "wb") as file:
    file.write(returned)