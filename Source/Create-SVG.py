from PIL import ImageFont
import sys
import json
import xml.etree.ElementTree as ET

fontSize = 18

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

#
myChips = {}
myPorts = {}
outputTarget = None
#

def getStringWidth(string: str, size: int):
    font = ImageFont.truetype("Ubuntu.ttf", size)
    return font.getlength(string)

def appendPort(svgObject: ET.Element, isInput: bool, portType: str, isList: bool, portName: str, posX: int, posY: int) -> int:
    
    return 0

def generateExec(svgObject: ET.Element, chip: dict):
    topBarWidth = getStringWidth(chip["ChipName"], fontSize) + 57 * 2
    x = topBarWidth / 2 + chipXOffset
    y = (topHeight + fontSize/1.5)/2
    title = ET.SubElement(svgObject, "text", {"text-anchor": "middle", "fill": "white", "font-size": "18px", "x": str(x), "y": str(y)})
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
            currentPortHeight = appendPort(svgObject, True, port["DataType"], port["IsList"], port["Name"], chipXOffset, outSpacing)
            outSpacing = outSpacing + currentPortHeight + verticalPadding
        
        newPathHeight = paddingFromTop + paddingFromBottom + max(totalInputSpacing, totalOutputSpacing)
        chipLength = max(minimalPadding, topBarWidth, largestInputText + largestOutputText + horizontalPortPadding)

        bottom.set("d", f"M{chipXOffset}, {topHeight} v{newPathHeight - 10} q0,10,10,10 h{chipLength - 20} q10,0,10,-10 v{-newPathHeight + 10} h{chipLength}")
        
        svgObject.set("height", str(41 + newPathHeight))
        svgObject.set()
        
        top = ET.SubElement(svgObject, "path")
        top.set("d", "")
    
def generateConst():
    ""
def generateVariableLike():
    ""

def setup(chipsDict: dict, portsDict: dict):
    myChips = chipsDict
    myPorts = portsDict

def Generate(UUID: str):
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="800", viewbox="0 0 800 800")
    returnval = ""
    chipToGenerate = myChips[UUID]
    match chipToGenerate["Model"]:
        case "Default":
            returnval = generateExec(svg, chipToGenerate)
        case "Variable":
            ""
        case "Constant":
            ""
        case _:
            ""

if __name__ == "__main__":
    try:
        # 1: uuid, 2: chips path, 3: ports path, 4: output target
        uuid = sys.argv[1]
        outputTarget = sys.argv[4]
        with open(sys.argv[2], encoding="utf8") as chips, open(sys.argv[3], encoding="utf8") as ports:
            myChips = json.loads(chips.read())
            myPorts = json.loads(ports.read())
        
        Generate(uuid)

    except Exception as ex:
        print("Invalid arguments were given!")
        print(ex)
        exit(1)