import json
import xml.etree.ElementTree as ET
import os

clearDocs = True
docsPath = "../DebugPages" # docs are stored here

chipsLocation = "Generated/chips.json" # chip json location
extraInfoPath = "../SecretInfo"

mdxTemplates = { # template file paths are put in a dictionary, will be replaced by the contents of the file
    "ExtraInfo": "templates/extrainfo.mdx",
    "Chips": "templates/chip.mdx"
}

ChipWarnings = {
    "Deprecated": """:::danger DEPRECATED

This chip has been deprecated. Please move to a different chip.

:::""",
    "Deprecating": """:::danger DEPRECATING

This chip is deprecating. Please avoid using it, as it will be replaced soon.

:::""",
    "BetaOnly": """:::caution BETA

This chip requires beta content to be enabled in the room. You can access the setting in "This Room -> Settings".

:::""",
    "RoomsV2Only": """:::caution ROOMS V2 ONLY

This chip is exclusive to Rooms V2. It will not show up in Rooms V1.

:::
""",
    "RoomsV1Only": """:::caution ROOMS V1 ONLY
    
This chip does not exist in Rooms V2.

:::
"""
}

topPlaceholder = """---
sidebar_position: ._index
tags: [Guide]
---
"""

chips = {} # json loaded chips
extraInfoDirs = []

with open(chipsLocation, "rt", encoding="UTF-8") as f:
    chips = json.load(f)

for templateName, templatePath in mdxTemplates.items(): # dict values are being replaced here
    with open(templatePath, "rt") as templFile:
        mdxTemplates[templateName] = templFile.read()

# print(mdxTemplates["Chips"])

def initializeExtraInfo(uuid: str, chip: dict) -> str:
    chipDirPath = chip["PaletteName"].replace("<", "[").replace(">", "]") + "@" + uuid
    completePath = extraInfoPath + "/" + chipDirPath
    for index, folderName in enumerate(extraInfoDirs):
        if uuid in folderName:
            if folderName != chipDirPath:
                os.rename(extraInfoPath + "/" + folderName, completePath)
            
            with open(completePath + "/tags.txt", "wt") as newTagsFile:
                newTagsFile.write(",".join(chip["Tags"]))

            del extraInfoDirs[index]
            return completePath
    
    os.mkdir(completePath)
    with open(completePath + "/extrainfo.mdx", "wt") as newEIFile, open(completePath + "/tags.txt", "wt") as newTagsFile:
        newEIFile.write(mdxTemplates["ExtraInfo"])
        newTagsFile.write(",".join(chip["Tags"]))
    return completePath

def GenerateDocFiles(uuid: str, chip: dict, extraInfoFolder: str):
    
    with open(f"{docsPath}/{uuid}.mdx", "wt") as docFile:
        ""

def Generate():
    global extraInfoDirs
    os.makedirs(extraInfoPath, exist_ok=True)
    extraInfoDirs = os.listdir(extraInfoPath)

    for chip_uuid, chip_content in chips.items():
        fldr = initializeExtraInfo(chip_uuid, chip_content)
        GenerateDocFiles(chip_uuid, chip_content, fldr)
Generate()