import json
import sys
import copy
import pathlib
import os

portTemplate = {
    "HasDefaultValue": False,
    "Model": "Data",
    "Color": "#F5C51F",
}

portTypes = {
    "exec": {
        "HasDefaultValue": False,
        "Model": "Exec",
        "Color": "#F55C1A",
    },
    "string": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#784283",
    },
    "int": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#106522",
    },
    "float": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#186BDD",
    },
    "bool": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#EA2E50",
    },
    "color": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#004FB9",
    },
    "player": {
        "HasDefaultValue": True,
        "Model": "Data",
        "Color": "#F5C51F",
    },
    "any": {
        "HasDefaultValue": False,
        "Model": "Data",
        "Color": "#F6EEE8",
    },
    "(t0, t1)": {
        "HasDefaultValue": False,
        "Model": "Data",
        "Color": "#F6EEE8",
    }
}

# strict: lowercase name must match any of these keys (event receiver, "event receiver")
# includes: lowercase name must include any of the keys (event sender, studio "event sender")

autoAssignModels = [
    {
        "key": "event receiver",
        "result": "Receiver",
        "pattern": "strict"
    },
    {
        "key": "event sender",
        "result": "Sender",
        "pattern": "includes"
    },
    {
        "key": "event definition",
        "result": "Definition",
        "pattern": "strict"
    },
    {
        "key": "data table",
        "result": "Definition",
        "pattern": "strict"
    },
    {
        "key": "constant",
        "result": "Constant",
        "pattern": "includes"
    },
    {
        "key": "data table",
        "result": "Constant",
        "pattern": "strict"
    },
    {
        "key": "variable",
        "result": "Variable",
        "pattern": "includes"
    },
    {
        "key": "comment",
        "result": "Variable",
        "pattern": "strict"
    }
]

def getPorts(jsonSourcet: dict) -> dict:
    for UUID, chip in jsonSourcet["Nodes"].items():
        for nodedesc in chip["NodeDescs"]:
            hasParams = len(nodedesc["ReadonlyTypeParams"].keys()) > 0
            for param in nodedesc["ReadonlyTypeParams"].values():
                for splitString in param.replace("(", "").replace(")", "").split(" | "):
                    if not (splitString.lower() in portTypes):
                        portTypes[splitString.lower()] = portTemplate
        
            for port in nodedesc["Inputs"]:
                if "List<" in port["ReadonlyType"]:
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                if (not hasParams):
                    if not (port["ReadonlyType"].lower() in portTypes):
                        portTypes[port["ReadonlyType"].lower()] = portTemplate

            for port in nodedesc["Outputs"]:
                if "List<" in port["ReadonlyType"]:
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                if (not hasParams):
                    if not (port["ReadonlyType"].lower() in portTypes):
                        portTypes[port["ReadonlyType"].lower()] = portTemplate
    return portTypes

def translateChip(jsonSourceb: dict) -> dict:
    newDict = {}
    for uuid, chip in jsonSourceb["Nodes"].items():
        thisChipModel = "Default"
        for check in autoAssignModels:
            match check["pattern"]:
                case "strict":
                    if chip["ReadonlyPaletteName"].lower() == check["key"]: thisChipModel = check["result"]
                case "includes":
                    if check["key"] in chip["ReadonlyPaletteName"].lower(): thisChipModel = check["result"]
        tags = []
        for nodeFilter in chip["NodeFilters"]:
            tags = tags + nodeFilter["FilterPath"]
        thisChip = {
            "ChipName": chip["ReadonlyChipName"],
            "PaletteName": chip["ReadonlyPaletteName"],
            "Description": chip["Description"],
            "Model": thisChipModel,
            "IsBeta": chip["IsBetaChip"],
            "RoomsV1": chip["IsValidInRoom1"],
            "RoomsV2": chip["IsValidInRoom2"],
            "TrollingRisk": chip["IsTrollingRisk"],
            "IsRoleAssignmentRisk": chip["IsRoleAssignmentRisk"],
            "DeprecationStage": chip["DeprecationStage"],
            "Tags": tags
        }
        for nodeDesc in chip["NodeDescs"]:
            #del nodeDesc["Name"]
            tempPortAssign = {}
            if len(nodeDesc["ReadonlyTypeParams"]) > 0:
                for paramKey, paramValue in nodeDesc["ReadonlyTypeParams"].items():
                    paramValue = paramValue.lower().replace("(", "").replace(")", "").split(" | ")
                    if len(paramValue) < 2:
                        tempPortAssign[paramKey] = paramValue[0]
                    else:
                        tempPortAssign[paramKey] = paramValue
            for port in nodeDesc["Inputs"]:
                isList = False
                isUnion = False
                if "List<" in port["ReadonlyType"]:
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                    isList = True
                if port["ReadonlyType"] in tempPortAssign:
                    if isinstance(tempPortAssign[port["ReadonlyType"]], str):
                        isUnion = False
                    else:
                        isUnion = True
                    
                    port["ReadonlyType"] = tempPortAssign[port["ReadonlyType"]]
                port["DataType"] = port["ReadonlyType"].lower() if isinstance(port["ReadonlyType"], str) else port["ReadonlyType"]
                port["IsUnion"] = isUnion
                port["IsList"] = isList
                    
                del port["ReadonlyType"]
                del port["Description"]
            
            for port in nodeDesc["Outputs"]:
                isList = False
                isUnion = False
                if "List<" in port["ReadonlyType"]:
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                    isList = True
                if port["ReadonlyType"] in tempPortAssign:
                    if isinstance(tempPortAssign[port["ReadonlyType"]], str):
                        isUnion = False
                    else:
                        isUnion = True
                    
                    port["ReadonlyType"] = tempPortAssign[port["ReadonlyType"]]
                port["DataType"] = port["ReadonlyType"].lower() if isinstance(port["ReadonlyType"], str) else port["ReadonlyType"]
                port["IsUnion"] = isUnion
                port["IsList"] = isList
                    
                del port["ReadonlyType"]
                del port["Description"]
            
            del nodeDesc["ReadonlyTypeParams"]
        thisChip["Functions"] = chip["NodeDescs"]
        newDict[uuid] = thisChip
    return newDict

def ExtractChipJSON(jsonSrc: dict) -> ():
    """
    Returns a tuple of dicts that use FunnPunn's format.
    First item is the chips dict.
    Second item is the ports dict.
    """
    chipClone = copy.deepcopy(jsonSrc)
    portsClone = copy.deepcopy(jsonSrc)

    return (translateChip(chipClone), getPorts(portsClone))

if __name__ == "__main__":
    jsonSource = sys.argv[1]
    outputChipsTarget = sys.argv[2]
    outputPortsTarget = sys.argv[3]

    oldJSON = {}

    with open(jsonSource, encoding="utf8") as jsonSourceFile:
        oldJSON = json.load(jsonSourceFile)
    
    chps, prts = ExtractChipJSON(oldJSON)
    
    generated_path = pathlib.Path("./Generated/")
    if not generated_path.exists():
        os.mkdir(generated_path)

    with open(outputChipsTarget, "wt") as chipsFile, open(outputPortsTarget, "wt") as portsFile:
        json.dump(chps, chipsFile, indent=(4 if len(sys.argv) > 4 else None))
        json.dump(prts, portsFile, indent=(4 if len(sys.argv) > 4 else None))
