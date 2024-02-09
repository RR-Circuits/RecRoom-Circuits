import json
#import Create_SVG
import os

chipsLocation = "Generated/chips.json"
extraInfoPath = "../ExtraInfo"
templatePath = "templates"

extraInfoTemplateText = ""
chipTemplateText = ""

deprecatednMsg = """:::danger DEPRECATED

This chip has been deprecated. Please move to a different chip.

:::"""
deprecatingMsg = """:::danger DEPRECATED

This chip has been deprecated. Please move to a different chip.

:::"""

betaMsg = """:::caution BETA

This chip requires beta content to be enabled in the room. You can access the setting in "This Room -> Settings".

:::"""

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