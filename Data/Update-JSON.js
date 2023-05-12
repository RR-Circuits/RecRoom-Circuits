const fs = require("fs")
const { exit } = require("process")
const { stringify } = require("querystring")
const https = require('follow-redirects').https

const ChipTemplate = fs.readFileSync("templates/chip.md", "utf-8")
const DeprMsg = `:::caution

This chip has been deprecated. Please use to a different chip.

:::`
const TotalSteps = 6
var CurrentStep = 0

function AddStep(prnt) {
    CurrentStep++
    console.log("[".concat(CurrentStep, "/", TotalSteps, "] ", prnt))
}

const DownloadFile = "Generated/Chips_OLD.json"

const sleep = s => new Promise(r => setTimeout(r, s*1000));

var oldJSON_raw
var OldJSON
var OldJSON_Clone
var entries
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

function PrepareFiles() {
    const entries = Object.entries(NewChips)
    for(const [uuid, contents] of entries){

        var NewChipFile = ChipTemplate
        var InputsStr = "| Port Name | Port Type |\n|-----------|-----------|"
        var OutputsStr = "| Port Name | Port Type |\n|-----------|-----------|"
        
        try {for(const prt of contents["Functions"][0]["Inputs"]) {
            var prtstr = ""
            if(prt["IsUnion"]) {
                var joined = prt["DataType"].join(" | ")
                var newstr = "Any (" + joined + ")"
                
                prtstr = "| ._name | ._type |".replace("._name", prt["Name"]).replace("._type", prt[newstr])
            } else {
                prtstr = "| ._name | ._type |".replace("._name", prt["Name"]).replace("._type", prt["DataType"])
            }
            InputsStr = InputsStr.concat("\n", prtstr)
        }} catch (error) {
            console.log(contents["ChipName"])
        }
        try {for(const prt of contents["Functions"][0]["Outputs"]) {
            var prtstr = ""
            if(prt["IsUnion"]) {
                var joined = prt["DataType"].join(" | ")
                var newstr = "Any (" + joined + ")"
                
                prtstr = "| ._name | ._type |".replace("._name", prt["Name"]).replace("._type", prt[newstr])
            } else {
                prtstr = "| ._name | ._type |".replace("._name", prt["Name"]).replace("._type", prt["DataType"])
            }
            OutputsStr = OutputsStr.concat("\n", prtstr)
        }} catch (error) {
            console.log(contents["ChipName"])
        }
        
        NewChipFile = NewChipFile.replace("._chipname", contents["ChipName"])
        .replace("._chipdesc", contents["Description"])
        .replace("._istroll", contents["TrollingRisk"])
        .replace("._isbeta", contents["IsBeta"])
        .replace("._inputs", InputsStr)
        .replace("._outputs", OutputsStr);

        fs.writeFileSync(__dirname + '/../Website/circuits/docs/documentation/chips/'+uuid+".md", NewChipFile)
    }
}

function TranslateChipData(){
    for(const [uuid, chipd] of entries) {
        // Order: List<> removal -> Param checker
        const thischip = NewChips[uuid] = {
            ChipName: chipd["ReadonlyChipName"],
            PaletteName: chipd["ReadonlyPaletteName"],
            Description: chipd["Description"],
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
function RestOfUpdate(){
    oldJSON_raw = fs.readFileSync(DownloadFile, "utf-8")
    OldJSON = JSON.parse(oldJSON_raw)["Nodes"]
    OldJSON_Clone = JSON.parse(oldJSON_raw)["Nodes"]
    entries = Object.entries(OldJSON_Clone)
    
    AddStep("Updating ports.json...")
    RetrievePorts();
    fs.writeFileSync("Generated/ports.json", JSON.stringify(PortTypes, null, 4))

    AddStep("Translating chips...")
    TranslateChipData();
    fs.writeFileSync("Generated/chips.json", JSON.stringify(NewChips, null, 4))

    AddStep("Generating info.txt...")
    fs.writeFileSync("Generated/info.txt", "Generated on " + new Date(Date.now()).toDateString())

    AddStep("Preparing page files...")
    PrepareFiles();

    AddStep("Testing file...")
    

    console.log("Finished!")
    exit(0)
}
AddStep("Downloading chips...")
const file = fs.createWriteStream("Generated/Chips_OLD.json");
const request = https.get("https://raw.githubusercontent.com/tyleo-rec/CircuitsV2Resources/master/misc/circuitsv2.json", function(response) {
    response.pipe(file);

    file.on("finish", () => {
        file.close()
        RestOfUpdate()
    })
})
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
