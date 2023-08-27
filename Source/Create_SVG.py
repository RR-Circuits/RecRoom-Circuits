from PIL import ImageFont
from cairosvg import svg2png
import sys
import json
import xml.etree.ElementTree as ET

fontSize = titleSize = 18

# chip values
portHeight = 19
minimalPadding = 111
verticalPadding = 6
horizontalPortPadding = 2
topHeight = 41

paddingFromTop = 8
paddingFromBottom = 4

chipXOffset = 72 # DefaultValue ports should be rendered, so this is why the chip is being moved to the right
# end

myChips = {}
myPorts = {}
outputTarget = None
#

def getStringWidth(string: str, size: int):
    """
    Gets the width of a string in pixels, using the ubuntu font and the given size.
    """
    font = ImageFont.truetype("Ubuntu.ttf", size)
    return font.getlength(string)
def appendPort(svgObject: ET.Element, isInput: bool, portType: str | list, isList: bool, portName: str, posX: int | float, posY: int | float) -> int | float:
    color = ""
    model = ""
    hasDefaultValue = False
    portOffset = 5
    currentPortHeight = 0
    if isinstance(portType, list):
        color = "#F6EEE8"
        model = "Data"
        hasDefaultValue = False
    else:
        portData = myPorts[portType]
        color = portData["Color"]
        model = portData["Model"]
        hasDefaultValue = portData["HasDefaultValue"]

    match model:
        case "Exec":
            posXrep = posX + portOffset + (2 if not isInput else 0)
            port = ET.SubElement(svgObject, "path")
            port.set("d", f"M{posXrep},{posY}h-16.465c-0.552,0,-1,0.448,-1,1v16c0,0.552,0.448,1,1,1h16.465c0.334,0,0.647,-0.167,0.832,-0.445l5.333,-8c0.224,-0.336,0.224,-0.774,0,-1.11l-5.333,-8c-0.185,-0.278,-0.498,-0.445,-0.832,-0.445z")
            port.set("fill", color)
            currentPortHeight = 18
        case "Data":
            if hasDefaultValue and not isList and isInput:
                rectGroup = ET.SubElement(svgObject, "g")
                ET.SubElement(rectGroup, "rect", {
                    "x": str(posX - 12),
                    "y": str(posY),
                    "width": "22",
                    "height": "15",
                    "fill": color,
                    "rx": "1"
                })

                ET.SubElement(rectGroup, "rect", {
                    "x": str(posX - 66),
                    "y": str(posY - 3),
                    "width": "45",
                    "height": "21",
                    "rx": "1",
                    "fill": color
                })

                ET.SubElement(rectGroup, "rect", {
                    "x": str(posX - 62),
                    "y": str(posY + 1.001),
                    "width": "37",
                    "height": "13",
                    "rx": "1",
                    "fill": "#818081"
                })

                ET.SubElement(rectGroup, "rect", {
                    "x": str(posX - 21),
                    "y": str(posY + 4),
                    "width": "9",
                    "height": "7",
                    "rx": "1",
                    "fill": color
                })
            else:
                ET.SubElement(svgObject, "rect", {
                    "x": str(posX - (12 if isInput else 10)),
                    "y": str(posY),
                    "width": "22",
                    "height": "15",
                    "rx": "1",
                    "fill": color
                })
            currentPortHeight = 15
    Anchor = "start"
    portOffset = 38
    if not isInput:
        Anchor = "end"
        portOffset = -16
    portText = ET.SubElement(svgObject, "text", {
        "x": str(posX + portOffset),
        "y": str(posY + 12.5),
        "fill": "white",
        "text-anchor": Anchor,
        "font-size": "medium",
        "class": "ubuntu"
    })
    portText.text = portName
    return currentPortHeight

def generateExec(svgObject: ET.Element, chip: dict) -> ET.Element:
    topBarWidth = getStringWidth(chip["ChipName"], titleSize) + 57 * 2
    x = topBarWidth / 2 + chipXOffset
    y = (topHeight + fontSize/1.5)/2
    bottom = ET.SubElement(svgObject, "path", fill="#818081")
    
    if len(chip["Functions"]) > 0:
        funcs = chip["Functions"][0]
        totalInputSpacing = 0
        totalOutputSpacing = 0
        largestInputText = 0
        largestOutputText = 0

        inSpacing = outSpacing = topHeight + paddingFromTop
        if len(funcs["Inputs"]) > 0:
            totalInputSpacing = len(funcs["Inputs"]) * verticalPadding - 1 + len(funcs["Inputs"]) * portHeight
        if len(funcs["Outputs"]) > 0:
            totalOutputSpacing = len(funcs["Outputs"]) * verticalPadding - 1 + len(funcs["Outputs"]) * portHeight
        
        for port in funcs["Inputs"]:
            strSize = getStringWidth(port["Name"], fontSize)
            if strSize > largestInputText:
                largestInputText = strSize
            currentPortHeight = appendPort(svgObject, True, port["DataType"], port["IsList"], port["Name"], chipXOffset, inSpacing)
            inSpacing = inSpacing + currentPortHeight + verticalPadding
            

        
        for port in funcs["Outputs"]:
            strSize = getStringWidth(port["Name"], fontSize)
            if strSize > largestOutputText:
                largestOutputText = strSize
            currentPortHeight = appendPort(svgObject, False, port["DataType"], port["IsList"], port["Name"], chipXOffset + max(minimalPadding, topBarWidth), outSpacing)
            outSpacing = outSpacing + currentPortHeight + verticalPadding
        
        newPathHeight = paddingFromTop + paddingFromBottom + max(totalInputSpacing, totalOutputSpacing)
        chipLength = max(minimalPadding, topBarWidth, largestInputText + largestOutputText + horizontalPortPadding)

        bottom.set("d", f"M{chipXOffset}, {topHeight} v{newPathHeight - 10} q0,10,10,10 h{chipLength - 20} q10,0,10,-10 v{-newPathHeight + 10} h{chipLength}")
        
        svgObject.set("width", str(chipLength + 2 * chipXOffset))
        svgObject.set("height", str(41 + newPathHeight))
        svgObject.set("viewbox", f"0 0 {chipLength + 2 * chipXOffset} {41 + newPathHeight}")
        
        top = ET.SubElement(svgObject, "path")
        top.set("d", f"M{chipXOffset}, {topHeight} v-31 q0,-10,10,-10 h{chipLength - 20} q10,0,10,10 v31 h-{chipLength}")
        top.set("fill", "#525152")

        title = ET.SubElement(svgObject, "text", {
            "text-anchor": "middle",
            "fill": "white",
            "font-size": f"{titleSize}px",
            "x": str(chipLength/2 + chipXOffset),
            "y": str(y),
            "class": "ubuntu"
        })
        title.text = chip["ChipName"]
        return svgObject
    
def generateConst(svgObject: ET.Element, chip: dict) -> ET.Element:
    chipXOffset = 0
    svgObject.set("height", "48")
    textWidth = getStringWidth(chip["ChipName"], titleSize)
    chipLength = textWidth + 70

    outerShell = ET.SubElement(svgObject, "rect", {
        "x": str(chipXOffset),
        "y": "0",
        "width": str(chipLength),
        "height": "48",
        "rx": "10",
        "fill": "#525152"
    })
    innerShell = ET.SubElement(svgObject, "rect", {
        "x": str(chipXOffset + chipLength - 14),
        "y": "13.5",
        "width": "14",
        "height": "21",
        "fill": "#3F3F3F"
    })
    outputPort = chip["Functions"][0]["Outputs"][0]
    appendPort(svgObject, False, outputPort["DataType"], outputPort["IsList"], "", chipXOffset + chipLength, 16.5)
    title = ET.SubElement(svgObject, "text", {
        "x": str(chipLength/2 + chipXOffset),
        "y": str(21 + fontSize / 2),
        "fill": "white",
        "text-anchor": "middle",
        "font-size": f"{titleSize}px",
        "class": "ubuntu"
    })
    svgObject.set("viewbox", f"0 0 {chipLength + 22} 48")
    svgObject.set("width", str(chipLength + 22))
    title.text = chip["ChipName"]

    return svgObject
def generateVariableLike(svgObject: ET.Element, chip: dict) -> ET.Element:
    textWidth = getStringWidth(chip["ChipName"], titleSize) + 22
    chipLength = max(textWidth + 50, 51)

    outerShell = ET.SubElement(svgObject, "rect", {
        "x": str(chipXOffset),
        "y": "0",
        "width": str(chipLength),
        "height": "76",
        "rx": "10",
        "fill": "#818081"
    })

    innerShell = ET.SubElement(svgObject, "rect", {
        "x": str(chipXOffset + 20),
        "y": "15",
        "width": str(max(textWidth + 10, 11)),
        "height": "46",
        "rx": "10",
        "fill": "#525152"
    })

    standardOffset = 17
    inSpacing = 0
    outSpacing = 0

    funcs = chip["Functions"][0]
    
    for port in funcs["Inputs"]:
        returnedHight = appendPort(svgObject, True, port["DataType"], port["IsList"], "", chipXOffset, standardOffset + inSpacing)
        inSpacing = inSpacing + returnedHight + verticalPadding
    
    for port in funcs["Outputs"]:
        returnedHight = appendPort(svgObject, False, port["DataType"], port["IsList"], "", chipXOffset + chipLength, standardOffset + outSpacing)
        outSpacing = outSpacing + returnedHight + verticalPadding
    
    title = ET.SubElement(svgObject, "text", {
            "x": str(chipLength / 2 + chipXOffset),
            "y": str(35 + fontSize / 2),
            "text-anchor": "middle",
            "fill": "white",
            "font-size": f"{titleSize}px",
            "class": "ubuntu"
        })
    title.text = chip["ChipName"]

    svgObject.set("viewbox", f"0 0 {chipLength + 2 * chipXOffset} 76")
    svgObject.set("width", str(chipLength + 2 * chipXOffset))
    svgObject.set("height", "76")
    
    return svgObject

def setup(chipsDict: dict, portsDict: dict):
    """
    Setup is required when using this script as a module.
    ChipsDict: A dictionary of chips.
    portsDict: A dictionary of port data.
    """
    global myChips
    global myPorts
    myChips = chipsDict
    myPorts = portsDict

def Generate(UUID: str, returnPNGBytes: bool):
    global chipXOffset
    chipXOffset = 72
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="800", viewbox="0 0 800 800")
    returnval = ""
    chipToGenerate = myChips[UUID]
    match chipToGenerate["Model"]:
        case "Default":
            returnval = ET.tostring(generateExec(svg, chipToGenerate))
        case "Variable":
            returnval = ET.tostring(generateVariableLike(svg, chipToGenerate))
        case "Constant":
            returnval = ET.tostring(generateConst(svg, chipToGenerate))
        case _:
            ""
    if returnPNGBytes:
        return svg2png(bytestring=returnval)
    else:
        return returnval

if __name__ == "__main__":
    try:
        # 1: uuid, 2: chips path, 3: ports path, 4: output target
        uuid = sys.argv[1]
        outputTarget = sys.argv[4]
        with open(sys.argv[2], encoding="utf8") as chips, open(sys.argv[3], encoding="utf8") as ports:
            myChips = json.load(chips)
            myPorts = json.load(ports)
        
        with open(outputTarget, "wb") as outputFile:
            outputFile.write(Generate(uuid, False))
        

    except Exception as ex:
        print("An error occured!")
        print(ex)
        exit(1)