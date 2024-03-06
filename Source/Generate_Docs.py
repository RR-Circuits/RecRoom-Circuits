import json
import shutil
import xml.etree.ElementTree as ET
import os
import Create_SVG
from distutils.dir_util import copy_tree

currentChipIndex = 1 # used for positioning

clearDocs = True

docsPath = "../Circuits/docs/chips" # docs are stored here
svgPath = "../Circuits/static/img/chip"
guidePath = "../Circuits/guides"
guideAssetPath = "../Circuits/static/guides"

guidesLocation = "../Guides"
chipsLocation = "Generated/chips.json" # chip json location
portsLocation = "Generated/ports.json"
extraInfoPath = "../ExtraInfo"

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
portDefs = {}

extraInfoDirs = []

with open(chipsLocation, "rt", encoding="UTF-8") as chps_f, open(portsLocation, "rt", encoding="UTF-8") as prts_f:
    chips = json.load(chps_f)
    portDefs = json.load(prts_f)

for templateName, templatePath in mdxTemplates.items(): # dict values are being replaced here
    with open(templatePath, "rt") as templFile:
        mdxTemplates[templateName] = templFile.read()

# print(mdxTemplates["Chips"])

def YesNo(state: bool):
    return "Yes" if state else "No"

def NoParse(string: str):
    return string.replace("<", "\<").replace(">", "\>").replace("{", "\{").replace("}", "\}")

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
    return outString

def generateDocFiles(uuid: str, chip: dict, extraInfoFolder: str):
    newDocString = mdxTemplates["Chips"]
    chipWarns = []
    avail = "Available everywhere"

    extraChipInfo = ""

    with open(extraInfoFolder + "/extrainfo.mdx") as extraFile:
        extraChipInfo = extraFile.read()

    ### HEADERS
    newDocString = newDocString.replace("._sidebarpos", str(currentChipIndex))
    newDocString = newDocString.replace("._tags", ",".join(chip["Tags"]))

    newDocString = newDocString.replace("._chipname", chip["PaletteName"])
    newDocString = newDocString.replace("._chipdesc", NoParse(chip["Description"]))

    treeItemCount = 0

    table = ET.Element("table")
    tableHead = ET.SubElement(table, "thead")
    tableHeadRow = ET.SubElement(tableHead, "tr")

    ET.SubElement(tableHeadRow, "th").text = "Inputs"
    ET.SubElement(tableHeadRow, "th").text = "Outputs"

    tableBody = ET.SubElement(table, "tbody")

    tableItems = []

    ### PORTS
    inTable = "| Input Name | Input Type |\n|-----------|-----------|"
    outTable = "| Output Name | Output Type |\n|-----------|-----------|"

    for func in chip["Functions"]:
        longestRow = func["Inputs"]
        if len(func["Inputs"]) < len(func["Outputs"]):
            longestRow = func["Outputs"]
        for _ in longestRow:
            tRow = ET.SubElement(tableBody, "tr")
            tableItems.append(ET.SubElement(tRow, "td"))
            tableItems.append(ET.SubElement(tRow, "td"))
        
        
        for idx, port in enumerate(func["Inputs"]):
            portCell = tableItems[idx * 2]
            portCell.text = NoParse(f"{formatPort(port)} | {port['Name'] if not port['Name'] == '' else '*No name.*'}")
            #inTable += f"\n| {port['Name'] if not port['Name'] == '' else '*No name.*'} | {formatPort(port)} |"
        for idx, port in enumerate(func["Outputs"]):
            portCell = tableItems[(idx * 2) + 1]
            portCell.text = NoParse(f"{formatPort(port)} | {port['Name'] if not port['Name'] == '' else '*No name.*'}")
            #outTable += f"\n| {port['Name'] if not port['Name'] == '' else '*No name.*'} | {formatPort(port)} |"

    newDocString = newDocString.replace("._ports", ET.tostring(table, encoding="unicode"))
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

    newDocString = newDocString.replace("._extrainfo", extraChipInfo)
    
    with open(f"{docsPath}/{uuid}.mdx", "wt") as docFile:
        docFile.write(newDocString)

def generateSVGs(uuid: str, chip: dict):
    newSVG = Create_SVG.generate_svg(uuid, False)

    with open(f"{svgPath}/{uuid}.svg", "wb") as SVGOutputFile:
        SVGOutputFile.write(newSVG)

def moveGuides():
    for possibleGuide in os.listdir(guidePath):
        if ".mdx" in possibleGuide:
            os.remove(f"{guidePath}/{possibleGuide}")

    for guideDir in os.listdir(guidesLocation):
        guideDirPath = f"{guidesLocation}/{guideDir}"
        if os.path.isdir(guideDirPath):
            shutil.copy(f"{guideDirPath}/doc.mdx", f"{guidePath}/{guideDir}.mdx")
            copy_tree(f"{guideDirPath}/assets", f"{guideAssetPath}/{guideDir}")

def Generate():
    global extraInfoDirs
    global currentChipIndex

    os.makedirs(extraInfoPath, exist_ok=True)
    extraInfoDirs = os.listdir(extraInfoPath)

    for chip_uuid, chip_content in chips.items():
        fldr = initializeExtraInfo(chip_uuid, chip_content)
        generateDocFiles(chip_uuid, chip_content, fldr)
        generateSVGs(chip_uuid, chip_content)
        currentChipIndex += 1
    
    moveGuides()

if __name__ == "__main__":
    Create_SVG.setup_svg_generator(chips, portDefs)
    Generate()