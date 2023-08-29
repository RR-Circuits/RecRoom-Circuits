import Create_SVG
import Translate_JSON
import json
import time

with open("Generated/chips.json", encoding="utf8") as chips, open("Generated/ports.json", encoding="utf8") as ports:
    chip = json.load(chips)
    port = json.load(ports)
    Create_SVG.setup_svg_generator(chip, port)
uuid = ""
returned = Create_SVG.generate_svg(uuid, False)

with open("Generated/newtest.svg", "wb") as file:
    file.write(returned)

returned = Create_SVG.generate_svg(uuid, True)

with open("Generated/newtest.png", "wb") as file:
    file.write(returned)