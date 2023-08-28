import Create_SVG
import Translate_JSON
import json
import time

chips = {}
ports = {}

start = time.time()

with open("Generated/Chips_OLD.json", encoding="utf8") as file:
    oldJSON = json.load(file)
    chips, ports = Translate_JSON.ExtractChipJSON(oldJSON)
end = time.time()
print(end - start)
Create_SVG.setup_svg_generator(chips, ports)

returned = Create_SVG.generate_svg("89599e52-1537-4696-91ea-fca1eb0ba26a", True)

with open("Generated/newtest.png", "wb") as file:
    file.write(returned)