const fs = require("fs")
const { exit } = require("process")
const { isatty } = require("tty")
const oldJSON_raw = fs.readFileSync("Chip/misc/circuitsv2.json")
const OldJSON = JSON.parse(oldJSON_raw)["Nodes"]
const OldJSON_Clone = JSON.parse(oldJSON_raw)["Nodes"]
const entries = Object.entries(OldJSON_Clone)
//init
var PortTypes = {
    "exec": {
        "HasDefaultValue": false,
        "Model": "Exec",
        "Color": "#F55C1A",
    },
    "string": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#784283",
    },
    "int": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#106522",
    },
    "float": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#186BDD",
    },
    "bool": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#EA2E50",
    },
    "color": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#004FB9",
    },
    "player": {
        "HasDefaultValue": true,
        "Model": "Data",
        "Color": "#F5C51F",
    }
}
var NewChips = {}
const template = {
    "HasDefaultValue": false,
    "Model": "Data",
    "Color": "#F5C51F",
}

function RetrievePorts(){
    for(const chip of Object.values(OldJSON)){
        for(const nodedesc of chip["NodeDescs"]){
            let HasParams = false
            if (Object.keys(nodedesc["ReadonlyTypeParams"]).length > 0) {
                HasParams = true
            }
            for(const param of Object.values(nodedesc["ReadonlyTypeParams"])){
                for(const splitstring of param.replace("(", "").replace(")", "").split(" | ")) {
                    if(PortTypes[splitstring.toLowerCase()] === undefined) {
                        PortTypes[splitstring.toLowerCase()] = template
                    }
                }
            }
            for(const port of nodedesc["Inputs"]){
                if(port["ReadonlyType"].includes("List<")){
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                }
                if(!HasParams){
                    if(PortTypes[port["ReadonlyType"].toLowerCase()] === undefined) {
                        PortTypes[port["ReadonlyType"].toLowerCase()] = template
                    }
                }
            }
            for(const port of nodedesc["Outputs"]){
                if(port["ReadonlyType"].includes("List<")){
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                }
                if(!HasParams){
                    if(PortTypes[port["ReadonlyType"].toLowerCase()] === undefined) {
                        PortTypes[port["ReadonlyType"].toLowerCase()] = template
                    }
                }
            }
        }
    }
}


function TranslateChipData(){
    for(const [uuid, chipd] of entries) {
        // Order: List<> removal -> Param checker
        const thischip = NewChips[uuid] = {
            ChipName: chipd["ReadonlyChipName"],
            PaletteName: chipd["ReadonlyPaletteName"],
            //custom here
            Model: "Default",
            //
            IsBeta: chipd["IsBetaChip"],
            TrollingRisk: chipd["IsTrollingRisk"],
            DeprecationStage: chipd["DeprecationStage"]
        }
        for(const NodeDesc of chipd["NodeDescs"]){
            const TempPortAssign = {}
            if(Object.keys(NodeDesc["ReadonlyTypeParams"]).length > 0){
                for(let [ParamKey, ParamValue] of Object.entries(NodeDesc["ReadonlyTypeParams"])) {
                    ParamValue = ParamValue.toLowerCase().replace("(", "").replace(")", "").split(" | ")
                    if(ParamValue.length < 2) {
                        TempPortAssign[ParamKey] = ParamValue[0]
                    } else TempPortAssign[ParamKey] = ParamValue;
                }
            }
            for(const port of NodeDesc["Inputs"]) {
                let IsList;
                let IsUnion;
                if(port["ReadonlyType"].includes("List<")) {
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                    IsList = true
                } else IsList = false; console.log(port["ReadonlyType"]);
                if(TempPortAssign[port["ReadonlyType"]] !== undefined) {
                    if(typeof(TempPortAssign[port["ReadonlyType"]]) == "string") {
                        IsUnion = false
                    } else {
                        IsUnion = true
                    }

                    port["ReadonlyType"] = TempPortAssign[port["ReadonlyType"]]
                    
                } else {
                    port["ReadonlyType"] = port["ReadonlyType"].toLowerCase()
                    IsUnion = false
                }
                port["DataType"] = port["ReadonlyType"]
                port["IsUnion"] = IsUnion
                port["IsList"] = IsList
                delete port["ReadonlyType"]
            }
            for(const port of NodeDesc["Outputs"]) {
                let IsList;
                let IsUnion;
                if(port["ReadonlyType"].includes("List<")) {
                    port["ReadonlyType"] = port["ReadonlyType"].replace("List<", "").replace(">", "")
                    IsList = true
                } else IsList = false;
                if(TempPortAssign[port["ReadonlyType"]] !== undefined) {
                    if(typeof(TempPortAssign[port["ReadonlyType"]]) == "string") {
                        IsUnion = false
                    } else {
                        IsUnion = true
                    }

                    port["ReadonlyType"] = TempPortAssign[port["ReadonlyType"]]
                    
                } else {
                    port["ReadonlyType"] = port["ReadonlyType"].toLowerCase()
                    IsUnion = false
                }
                port["DataType"] = port["ReadonlyType"]
                port["IsUnion"] = IsUnion
                port["IsList"] = IsList
                delete port["ReadonlyType"]
            }
            delete NodeDesc["ReadonlyTypeParams"]
        }
        thischip["Functions"] = chipd["NodeDescs"]
    }
}

console.log("[1/3] Updating ports.json...")
RetrievePorts();
fs.writeFileSync("Generated/ports.json", JSON.stringify(PortTypes, null, 4))

console.log("[2/3] Updating chips.json...")
TranslateChipData();
fs.writeFileSync("Generated/chips.json", JSON.stringify(NewChips, null, 4))
console.log("[3/3] Validating...")
console.log("Finished!")
exit(0)
/*
{
    NodeDescs: [
        {
            Inputs/Outputs: [
                {

                }
            ]
        }
    ]
}
*/
