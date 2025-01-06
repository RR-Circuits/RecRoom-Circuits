# Script made by FunnPunn, so annoy him if this doesn't feel like working
from PIL import ImageFont
from cairosvg import svg2png
import sys
import json
import xml.etree.ElementTree as ET
import argparse

import traceback # please remove

fontSize = titleSize = 18

inlineFont = ".ubuntu {font-family: 'Ubuntu', sans-serif;}"

# chip values
portHeight = 19
minimalPadding = 111
verticalPadding = 6
horizontalPortPadding = 2
topHeight = 41

minimalReceiverHeight = 66

paddingFromTop = 8
paddingFromBottom = 4

chipXOffset = 72 # DefaultValue ports should be rendered, so this is why the chip is being moved to the right
# end

myChips = {}
myPorts = {}
#

def getStringWidth(string: str, size: int):
    """
    Gets the width of a string in pixels, using the ubuntu font and the given size.
    """
    font = ImageFont.truetype("fonts/Ubuntu.ttf", size)
    return font.getlength(string)

def appendPort(svgObject: ET.Element, isInput: bool, portType: str | list, isList: bool, portName: str, posX: int | float, posY: int | float, canHaveDefaultValue: bool | None = True) -> int | float:
    color = ""
    model = ""
    hasDefaultValue = False
    portOffset = 5
    currentPortHeight = 0
    portFontSize = 10

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
            port = ET.SubElement(svgObject, "path", {
                "class": f"{'input' if isInput else 'output'} exec"
            })
            port.set("d", f"M{posXrep},{posY}h-16.465c-0.552,0,-1,0.448,-1,1v16c0,0.552,0.448,1,1,1h16.465c0.334,0,0.647,-0.167,0.832,-0.445l5.333,-8c0.224,-0.336,0.224,-0.774,0,-1.11l-5.333,-8c-0.185,-0.278,-0.498,-0.445,-0.832,-0.445z")
            port.set("fill", color)
            currentPortHeight = 18
        case "Data":
            if hasDefaultValue and not isList and isInput and (canHaveDefaultValue == True or canHaveDefaultValue == None):
                rectGroup = ET.SubElement(svgObject, "g", {
                    "class": f"{'input' if isInput else 'output'} data {portType} {'list' if isList else 'nolist'} default",
                })
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
                    "class": f"{'input' if isInput else 'output'} data {portType} {'list' if isList else 'nolist'} nodefault",
                    "x": str(posX - (12 if isInput else 10)),
                    "y": str(posY),
                    "width": "22",
                    "height": "15",
                    "rx": "1",
                    "fill": color
                })
            
            currentPortHeight = 15
    Anchor = "start"
    portOffset = 16
    if isList:
        listText = ET.SubElement(svgObject, "text", {
            "x": str(posX),
            "y": str(posY + 1),
            "fill": "white",
            "font-size": f"{portFontSize}px",
            "font-weight": "bold",
            "class": "ubuntu"
        })
        listTextItem = ET.SubElement(listText, "tspan", {
            "x": str(posX - (5.5 if isInput else 3.5)),
            "dy": f"{portFontSize}",
            "class": "ubuntu",
            "style": "fill:none;fill-opacity:1;stroke:#000000;stroke-width:0.8px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:0.5;"
        })
        
        listTextItem.text = "[ ]"
    if not isInput:
        Anchor = "end"
        portOffset = -16
    portText = ET.SubElement(svgObject, "text", {
        "x": str(posX + portOffset),
        "y": str(posY + 14),
        "fill": "white",
        "text-anchor": Anchor,
        "font-size": f"{fontSize}px",
        "class": "ubuntu"
    })
    portText.text = portName
    return currentPortHeight

def generateExec(svgObject: ET.Element, chip: dict) -> ET.Element:
    topBarWidth = getStringWidth(chip["ChipName"], titleSize) + 57 * 2
    x = topBarWidth / 2 + chipXOffset
    y = (topHeight + fontSize/1.5)/2
    bottom = ET.SubElement(svgObject, "path", {
        "fill": "#818081",
        "class": "grabBase"
    })
    totalInputSpacing = 0
    totalOutputSpacing = 0
    largestInputText = 0
    largestOutputText = 0
    if len(chip["Functions"]) > 0:
        funcs = chip["Functions"][0]

        inSpacing = outSpacing = topHeight + paddingFromTop
        if len(funcs["Inputs"]) > 0:
            totalInputSpacing = len(funcs["Inputs"]) * verticalPadding - 1 + len(funcs["Inputs"]) * portHeight
        if len(funcs["Outputs"]) > 0:
            totalOutputSpacing = len(funcs["Outputs"]) * verticalPadding - 1 + len(funcs["Outputs"]) * portHeight
        
        for port in funcs["Inputs"]:
            strSize = getStringWidth(port["Name"], fontSize)
            if strSize > largestInputText:
                largestInputText = strSize
        
        for port in funcs["Outputs"]:
            strSize = getStringWidth(port["Name"], fontSize)
            if strSize > largestOutputText:
                largestOutputText = strSize

        for port in funcs["Inputs"]:
            currentPortHeight = appendPort(svgObject, True, port["DataType"], port["IsList"], port["Name"], chipXOffset, inSpacing)
            inSpacing = inSpacing + currentPortHeight + verticalPadding
            
        for port in funcs["Outputs"]:
            currentPortHeight = appendPort(svgObject, False, port["DataType"], port["IsList"], port["Name"], chipXOffset + max(minimalPadding, topBarWidth, largestInputText + largestOutputText + horizontalPortPadding + 40), outSpacing)
            outSpacing = outSpacing + currentPortHeight + verticalPadding
        
    newPathHeight = paddingFromTop + paddingFromBottom + max(totalInputSpacing, totalOutputSpacing)
    chipLength = max(minimalPadding, topBarWidth, largestInputText + largestOutputText + horizontalPortPadding + 40)

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

def generateReceiver(svgObject: ET.Element, chip: dict) -> ET.Element:
    chipXOffset = 0
    textWidth = 0

    darkShell = ET.SubElement(svgObject, "path", fill="#525152")
    lightShell = ET.SubElement(svgObject, "path", fill="#818081")
    darkShellWidth = max(textWidth - 25, 177.23)

    for line in chip["ChipName"].split("\n"):
        textWidth = getStringWidth(line, titleSize) if textWidth < getStringWidth(line, titleSize) else textWidth
    
    iconCircle = ET.SubElement(svgObject, "circle", {
        "cx": str(chipXOffset + 7.5),
        "cy": "35.5",
        "r": "2.5",
        "fill": "#F6EEE8"
    })
    iconRing1 = ET.SubElement(svgObject, "path", {
        "d": f"M{chipXOffset + 11.5},28.5c3.483,3.5,3.483,10.5,0,14",
        "stroke": "#F6EEE8",
        "fill-opacity": "0",
        "stroke-width": "3",
        "stroke-linecap": "round",
        "stroke-linejoin": "round"
    })
    iconRing2 = ET.SubElement(svgObject, "path", {
        "d": f"M{chipXOffset + 17.1125},25.5c3.483,3.5,3.483,16.5,0,20",
        "stroke": "#F6EEE8",
        "fill-opacity": "0",
        "stroke-width": "3",
        "stroke-linecap": "round",
        "stroke-linejoin": "round"
    })
    largestPortTextSize = 0
    newPortPlacement = 12

    for port in chip["Functions"][0]["Outputs"]:
        if getStringWidth(port["Name"], fontSize) > largestPortTextSize:
            largestPortTextSize = getStringWidth(port["Name"], fontSize)

    for port in chip["Functions"][0]["Outputs"]:
        returnedHeight = appendPort(svgObject, False, port["DataType"], port["IsList"], port["Name"], chipXOffset + darkShellWidth + largestPortTextSize + 43, newPortPlacement)
        newPortPlacement = newPortPlacement + returnedHeight + verticalPadding

    shellHeight = max(minimalReceiverHeight, newPortPlacement)
    darkShell.set(
        "d", f"M{chipXOffset}, 10 q0,-10,10,-10 h{darkShellWidth} v{shellHeight} h-{darkShellWidth} q-10,0,-10,-10 v-{shellHeight-20}"
    )
    lightShell.set(
        "d", f"M{chipXOffset + darkShellWidth + 5}, 0 h{largestPortTextSize + 30} q10,0,10,10 v{shellHeight-20} q0,10,-10,10 h-{largestPortTextSize + 30} v-{shellHeight}"
    )
    titleBox = ET.SubElement(svgObject, "text", {
            "x": str(52 + chipXOffset + textWidth/2),
            "y": "5",
            "text-anchor": "middle",
            "fill": "white",
            "font-size": f"{titleSize}px",
            "class": "ubuntu"
        })

    for line in chip["ChipName"].split("\n"):
        titleText = ET.SubElement(titleBox, "tspan", {
            "x": f"{chipXOffset + darkShellWidth/1.7}",
            "dy": f"{fontSize}px"
        })
        titleText.text = line

    svgObject.set("width", str(largestPortTextSize + 30 + darkShellWidth + 78))
    svgObject.set("height", str(shellHeight))
    svgObject.set("viewbox", f"0 0 {largestPortTextSize + 30 + darkShellWidth + 78} {shellHeight}")
    return svgObject

def generateSender(svgObject: ET.Element, chip: dict) -> ET.Element:
    textWidth = 0

    darkShell = ET.SubElement(svgObject, "rect", fill="#525152")
    lightShell1 = ET.SubElement(svgObject, "path", fill="#818081")
    lightShell2 = ET.SubElement(svgObject, "path", fill="#818081")
    titleBox = ET.SubElement(svgObject, "text", {
        "x": "0",
        "y": "0",
        "fill": "white",
        "font-size": f"{titleSize}px",
        "text-anchor": "middle",
        "class": "ubuntu"
    })
    baseLightShell1Width = 28
    minLightShell2Width = 60

    minShellHeight = 97

    largestInputPortTextSize = 0
    largestOutputPortTextSize = 0

    newInputPortPlacement = 10
    newOutputPortPlacement = 10


    for port in chip["Functions"][0]["Inputs"]:
        returnedPortHeight = appendPort(svgObject, True, port["DataType"], port["IsList"], port["Name"], chipXOffset, newInputPortPlacement)
        newInputPortPlacement = newInputPortPlacement + returnedPortHeight + verticalPadding
        nameLength = getStringWidth(port["Name"], fontSize)
        if nameLength > largestInputPortTextSize:
            largestInputPortTextSize = nameLength
        
    targetLightShell1Width = baseLightShell1Width + largestInputPortTextSize

    for line in chip["ChipName"].split("\n"):
        textWidth = getStringWidth(line, titleSize) if textWidth < getStringWidth(line, titleSize) else textWidth
    
    for line in chip["ChipName"].split("\n"):
        titleText = ET.SubElement(titleBox, "tspan", {
            "x": f"{chipXOffset + targetLightShell1Width + textWidth / 2 + 70 / 2}",
            "dy": f"{fontSize + 4}px",
            "text-anchor": "middle"
        })
        titleText.text = line

    targetDarkShellWidth = textWidth + 70

    darkShell.set("x", str(chipXOffset + targetLightShell1Width))
    darkShell.set("y", "0")
    darkShell.set("width", str(targetDarkShellWidth))

    for port in chip["Functions"][0]["Outputs"]:
        currentWidth = getStringWidth(port["Name"], fontSize)
        largestOutputPortTextSize = currentWidth if currentWidth > largestOutputPortTextSize else largestOutputPortTextSize
    
    for port in chip["Functions"][0]["Outputs"]:
        returnedPortHeight = appendPort(svgObject, False, port["DataType"], port["IsList"], port["Name"], chipXOffset + targetLightShell1Width + targetDarkShellWidth + largestOutputPortTextSize + minLightShell2Width, newOutputPortPlacement)
        newOutputPortPlacement = newOutputPortPlacement + returnedPortHeight + verticalPadding
    
    targetShellHeight = max(minShellHeight, newInputPortPlacement + paddingFromBottom, newOutputPortPlacement + paddingFromBottom)
    targetLightShell2Width = largestOutputPortTextSize + minLightShell2Width

    darkShell.set("height", str(targetShellHeight))
    lightShell1.set(
        "d", f"M{chipXOffset + 10}, 0 h{targetLightShell1Width - 10} v{targetShellHeight} h-{targetLightShell1Width - 10} q-10,0,-10,-10 v-{targetShellHeight - 20} q0,-10,10,-10"
    )
    lightShell2.set(
        "d", f"M{chipXOffset + targetLightShell1Width + targetDarkShellWidth}, 0 h{targetLightShell2Width-10} q10,0,10,10 v{targetShellHeight - 20} q0,10,-10,10 h-{targetLightShell2Width - 10} v-{targetShellHeight}"
    )
    
    iconCircle = ET.SubElement(svgObject, "circle", {
        "cx": str(chipXOffset + targetLightShell1Width + targetDarkShellWidth + 37.5),
        "cy": f"{targetShellHeight - paddingFromBottom*5}",
        "r": "2.5",
        "fill": "#F6EEE8"
    })
    iconRing1 = ET.SubElement(svgObject, "path", {
        "d": f"M{chipXOffset + targetLightShell1Width + targetDarkShellWidth + 41.5},{targetShellHeight - paddingFromBottom*5 - 7}c3.483,3.5,3.483,10.5,0,14",
        "stroke": "#F6EEE8",
        "fill-opacity": "0",
        "stroke-width": "3",
        "stroke-linecap": "round",
        "stroke-linejoin": "round"
    })
    iconRing2 = ET.SubElement(svgObject, "path", {
        "d": f"M{chipXOffset + targetLightShell1Width + targetDarkShellWidth + 47.1125},{targetShellHeight - paddingFromBottom*5 - 10}c3.483,3.5,3.483,16.5,0,20",
        "stroke": "#F6EEE8",
        "fill-opacity": "0",
        "stroke-width": "3",
        "stroke-linecap": "round",
        "stroke-linejoin": "round"
    })

    svgObject.set("width", str(2 * chipXOffset + targetLightShell1Width + targetDarkShellWidth + targetLightShell2Width))
    svgObject.set("height", str(targetShellHeight))

    return svgObject

def generateDefinition(svgObject: ET.Element, chip: dict):
    outerShell = ET.SubElement(svgObject, "rect", fill="#525152", rx="10")
    innerShell = ET.SubElement(svgObject, "rect", fill="#818081", rx="10")
    title = ET.SubElement(svgObject, "text", {
        "x": "0",
        "y": "0",
        "fill": "white",
        "font-size": f"{titleSize}px",
        "text-anchor": "middle",
        "class": "ubuntu"
    })

    textWidth = getStringWidth(chip["ChipName"], titleSize)

    largestPortText = 0
    newPortPlacement = 0
    offsetFromTop = 52

    for port in chip["Functions"][0]["Inputs"]:
        nameWidth = getStringWidth(port["Name"], fontSize)
        largestPortText = nameWidth if nameWidth > largestPortText else largestPortText
        returnedPortHeight = appendPort(svgObject, True, port["DataType"], port["IsList"], port["Name"], 50, newPortPlacement + offsetFromTop, False)
        newPortPlacement = newPortPlacement + returnedPortHeight + verticalPadding
    
    innerShellWidth = max(chipXOffset + largestPortText, textWidth)

    innerShell.set("x", "21")
    innerShell.set("y", "41")
    innerShell.set("width", str(innerShellWidth))
    innerShell.set("height", str(newPortPlacement - verticalPadding + 11*2))

    outerShell.set("x", "0")
    outerShell.set("y", "0"),
    outerShell.set("width", str(innerShellWidth + 44))
    outerShell.set("height", str(newPortPlacement - verticalPadding + 84))

    title.set("x", str((innerShellWidth + 44)/2))
    title.set("y", str(40/2 + titleSize/2))
    title.text = chip["ChipName"]
    
    svgObject.set("width", str(innerShellWidth + 44))
    svgObject.set("height", str(newPortPlacement - verticalPadding + 84))
    svgObject.set("viewbox", f"0 0 {innerShellWidth + 44} {newPortPlacement - verticalPadding + 84}")

    return svgObject

def setup_svg_generator(chipsDict: dict, portsDict: dict, iconsDict: dict):
    """
    Setup is required when using this script as a module.
    `chipsDict`: A dictionary of chips.
    `portsDict`: A dictionary of port data.
    """
    global myChips, myPorts
    myChips = chipsDict
    myPorts = portsDict
    myIcons = iconsDict

def generate_svg(UUID: str, returnPNGBytes: bool) -> bytes:
    global chipXOffset
    chipXOffset = 72
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="800", viewbox="0 0 800 800")
    ET.SubElement(ET.SubElement(svg, "defs"), "style").text = inlineFont
    returnval = None
    try:
        chipToGenerate = myChips[UUID]
        match chipToGenerate["Model"]:
            case "Default":
                returnval = ET.tostring(generateExec(svg, chipToGenerate))
            case "Variable":
                returnval = ET.tostring(generateVariableLike(svg, chipToGenerate))
            case "Constant":
                returnval = ET.tostring(generateConst(svg, chipToGenerate))
            case "Receiver":
                returnval = ET.tostring(generateReceiver(svg, chipToGenerate))
            case "Sender":
                returnval = ET.tostring(generateSender(svg, chipToGenerate))
            case "Definition":
                returnval = ET.tostring(generateDefinition(svg, chipToGenerate))
            case _:
                print("WARN: Chip model is unknown and an Exec will be returned. Expect strange results.")
                returnval = ET.tostring(generateExec(svg, chipToGenerate))
    except Exception as ex:
        print(traceback.format_exc())
        returnval = ET.tostring(generateVariableLike(svg, {
            "ChipName": "Couldn't generate image.",
            "Functions": [
                {
                    "Inputs": [],
                    "Outputs": []
                }
            ]
        }))

    if returnPNGBytes:
        return svg2png(bytestring=returnval, scale=2)
    else:
        return returnval

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("uuid")
    parser.add_argument("chipspath")
    parser.add_argument("portspath")
    parser.add_argument("imagetarget")
    parser.add_argument("-b", "--bitmap", action="store_true")

    args = parser.parse_args()

    with open(args.chipspath, encoding="utf-8") as chips, open(args.portspath, encoding="utf-8") as ports:
        myChips = json.load(chips)
        myPorts = json.load(ports)
        
    with open(args.imagetarget, "wb") as outputFile:
        outputFile.write(generate_svg(args.uuid, args.bitmap))