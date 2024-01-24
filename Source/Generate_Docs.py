import json
#import Create_SVG
import os

chipsLocation = "Generated/chips.json"
extraInfoPath = "../ExtraInfo"
templatePath = "templates"

extraInfoTemplateText = ""
chipTemplateText = ""

chips = {}

with open(chipsLocation, "rt", encoding="UTF-8") as f, open(""):
    chips = json.load(f)

with open(templatePath + "/chips.mdx", "rt") as chipTemplate, open(templatePath + "/extrainfo.mdx", "rt") as extraInfoTemplate:
    chipTemplateText = chipTemplate.read()
    extraInfoTemplateText = extraInfoTemplate.read()

def generateDocs():
    os.makedirs(extraInfoPath, exist_ok=True)
    extraInfoDirs = os.listdir(extraInfoPath)

    for uuid, chip in chips.items():
        chipDirPath = chip["PaletteName"].replace("<", "[").replace(">", "]") + "@" + "" + uuid
        
        for folderName in extraInfoDirs:
            if uuid in folderName and folderName != chipDirPath:
                os.rename(extraInfoPath + "/" + folderName, extraInfoPath + "/" + chipDirPath)

generateDocs()