import json
import xml.etree.ElementTree as ET
import os

currentChipIndex = 1 # used for positioning

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

def YesNo(state: bool):
    return "Yes" if state else "No"

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

def formatPort(port: dict) -> str:
    outString = ""
    if port["IsUnion"]:
        outString = f'Any ({", ".join(port["DataType"])})'
    else:
        outString = port["DataType"]
    if port["IsList"]:
        outString = f"List<{outString}>"
    
    outString = outString.replace("<", "&lt").replace(">", "&gt") # avoid JSX parsing attempts
    return outString

def generateDocFiles(uuid: str, chip: dict, extraInfoFolder: str):
    newDocString = mdxTemplates["Chips"]
    chipWarns = []
    avail = "Available everywhere"

    ### HEADERS
    newDocString = newDocString.replace("._sidebarpos", str(currentChipIndex))
    newDocString = newDocString.replace("._tags", ",".join(chip["Tags"]))

    newDocString = newDocString.replace("._chipname", chip["PaletteName"])
    newDocString = newDocString.replace("._chipdesc", chip["Description"])

    ### PORTS
    inTable = "| Input Name | Input Type |\n|-----------|-----------|"
    outTable = "| Output Name | Output Type |\n|-----------|-----------|"

    for func in chip["Functions"]:
        for port in func["Inputs"]:
            inTable += f"\n| {port['Name'] if not port['Name'] == '' else '*No name.*'} | {formatPort(port)} |"
        for port in func["Outputs"]:
            outTable += f"\n| {port['Name'] if not port['Name'] == '' else '*No name.*'} | {formatPort(port)} |"

    newDocString = newDocString.replace("._inputs", inTable).replace("._outputs", outTable)
    ### PORTS END

    ### WARNS
    newDocString = newDocString.replace("._uuid", uuid)
    if chip["IsBeta"]:
        chipWarns.append(ChipWarnings["BetaOnly"])
    if chip["RoomsV1"]:
        if not chip["RoomsV2"]:
            chipWarns.append(ChipWarnings["RoomsV1Only"])
            avail = "Rooms V1 only"
    elif chip["RoomsV2"]:
        chipWarns.append(ChipWarnings["RoomsV2Only"])
        avail = "Rooms V2 only"

    chipWarns = "\n".join(chipWarns)

    newDocString = newDocString.replace("._warns", chipWarns).replace("._avail", avail)
    ### PROPERTIES
    newDocString = newDocString.replace("._istroll", YesNo(chip["TrollingRisk"]))
    newDocString = newDocString.replace("._isbeta", YesNo(chip["IsBeta"]))
    newDocString = newDocString.replace("._isrole", YesNo(chip["IsRoleAssignmentRisk"]))
    
    with open(f"{docsPath}/{uuid}.mdx", "wt") as docFile:
        docFile.write(newDocString)

def Generate():
    global extraInfoDirs
    global currentChipIndex
    
    os.makedirs(extraInfoPath, exist_ok=True)
    extraInfoDirs = os.listdir(extraInfoPath)

    for chip_uuid, chip_content in chips.items():
        fldr = initializeExtraInfo(chip_uuid, chip_content)
        generateDocFiles(chip_uuid, chip_content, fldr)
        currentChipIndex += 1

Generate()