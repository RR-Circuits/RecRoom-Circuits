const { error } = require("console")
const fs = require("fs-extra")
const { join } = require("path")
const { exit } = require("process")
const https = require('follow-redirects').https
var SVGGen = ""

const TotalSteps = 5
var CurrentStep = 0

const GuidesCat = {
    "label": "Guides",
    "position": 2,
    "link": {
      "type": "generated-index",
      "description": "Guides for people!"
    }
  }

const GuideTemplate = `---
sidebar_position: ._index
tags: [Guide]
---

`

// read files
const ChipTemplate = fs.readFileSync("templates/chip.mdx", "utf-8")
const ExtraInfoTemplate = fs.readFileSync("templates/extrainfo.mdx", "utf-8")

// deprecation/beta messages
const DeprMsg = `:::danger DEPRECATED

This chip has been deprecated. Please move to a different chip.

:::`
const BetaMsg = `:::caution BETA

This chip requires beta content to be enabled in the room. You can access the setting in "This Room -> Settings".

:::`

var Currentindex = 1

function AddStep(prnt) {
    CurrentStep++
    console.log("[".concat(CurrentStep, "/", TotalSteps, "] ", prnt))
}
function BoolToYesNo(bl) {
    if(bl) return "✅"; else return "❌";
}
const DownloadFile = "Generated/Chips_OLD.json"

const sleep = s => new Promise(r => setTimeout(r, s*1000));

var oldJSON_raw
var OldJSON
var OldJSON_Clone
var entries

// Pre-defined port types, usually the non-yellow ports
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
    },
    "any": {
        "HasDefaultValue": false,
        "Model": "Data",
        "Color": "#F6EEE8",
    }
}

var NewChips = {}
const template = {
    "HasDefaultValue": false,
    "Model": "Data",
    "Color": "#F5C51F",
}

// Extract the data types from this JSON and put it in ports.json
async function RetrievePorts(){
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
function CheckHasFileName(arr, checkr) {
    for (const element of arr) {
        if (element.includes(checkr)) {
            return [true, element]
        }
    }
    return [false]
}

async function PrepareFiles() {
    const chps_rw = fs.readFileSync("Generated/chips.json", "utf-8")
    const chps = JSON.parse(chps_rw)
    const entries = Object.entries(chps)
    fs.mkdirSync(__dirname + '/../ExtraInfo/', {recursive: true}, function (err){
        if (err) console.log("error");
    })
    const ExtraInfoDir = fs.readdirSync(__dirname + '/../ExtraInfo/', {}, (err, files) => {
        if (err) {
            console.log(err)
        }
    })
    for(const [uuid, contents] of entries){
        var ExtraInfoFile = ""
        var TagsFile = ""
        const DirPath = __dirname + '/../ExtraInfo/'.concat(contents["PaletteName"].replace("<", "[").replace(">", "]"), "@", uuid)
        const FlNm = contents["PaletteName"].replace("<", "[").replace(">", "]").concat("@", uuid)
        const [Success, Element] = CheckHasFileName(ExtraInfoDir, uuid)

        if (Success) {
            if (Element != FlNm) {
                fs.renameSync(__dirname + '/../ExtraInfo/' + Element, DirPath)
            }
        } else {
            try {
                fs.mkdirSync(DirPath, {recursive: true}, function (err){
                    if (err) console.log("error");
                })
                fs.writeFileSync(DirPath.concat("/extrainfo.mdx"), ExtraInfoTemplate, { flag: "wx" })
                
               // fs.writeFileSync(__dirname + '/../ExtraInfo/'.concat(contents["ChipName"].replace("<", "[").replace(">", "]"), "@", uuid, ".md"), ExtraInfoTemplate, { flag: "wx" })
            } catch (error) {
                
            }
        }
        fs.writeFileSync(DirPath.concat("/tags.txt"), contents["Tags"].join(","))

        var NewChipFile = ChipTemplate
        var InputsStr = "| Input Name | Input Type |\n|-----------|-----------|"
        var OutputsStr = "| Output Name | Output Type |\n|-----------|-----------|"
        
        try {for(const func of contents["Functions"]) {
            for(const prt of func["Inputs"]) {
                let prtstr = "| ._name | ._type |"
                let newstr = ""
                if(prt["IsUnion"] === true) {
                    var joined = prt["DataType"].join(" , ")
                    newstr = "Any (".concat(joined, ")")
                } else {
                    newstr = prt["DataType"]
                }
                if (prt["IsList"]) {
                    newstr = "List&lt".concat(newstr, "&gt")
                }
                if (prt["Name"] == "") {
                    prt["Name"] = "*No name.*"
                }
                InputsStr = InputsStr.concat("\n", prtstr.replace("._name", prt["Name"]).replace("._type", newstr.replace("<", "&lt").replace(">", "&gt")))
            }

            for(const prt of func["Outputs"]) {
                let prtstr = "| ._name | ._type |"
                let newstr = ""
                if(prt["IsUnion"] === true) {
                    var joined = prt["DataType"].join(" , ")
                    newstr = "Union(".concat(joined, ")")
                } else {
                    newstr = prt["DataType"]
                } 
                if (prt["IsList"]) {
                    newstr = "List[".concat(newstr, "]")
                }
                if (prt["Name"] == "") {
                    prt["Name"] = "*No name.*"
                }
                OutputsStr = OutputsStr.concat("\n", prtstr.replace("._name", prt["Name"]).replace("._type", newstr))
            }
        }} catch (error) {
            console.log(error)
        }
        
        NewChipFile = NewChipFile
        .replace("._chipname", contents["PaletteName"]/*.replace("<", "[").replace(">", "]")*/)
        .replace("._istroll", BoolToYesNo(contents["TrollingRisk"]))
        .replace("._isbeta", BoolToYesNo(contents["IsBeta"]))
        .replace("._isrole", BoolToYesNo(contents["IsRoleAssignmentRisk"]))
        .replace("._uuid1", uuid).replace("._uuid2", uuid).replace("._uuid3", uuid)
        .replace("._inputs", InputsStr)
        .replace("._outputs", OutputsStr)
        .replace("._sidebarpos", Currentindex)
        .replace("._extrainfo", fs.readFileSync(DirPath.concat("/extrainfo.mdx"), "utf-8"))
        .replace("._tags", fs.readFileSync(DirPath.concat("/tags.txt"), "utf-8"))

        switch (contents["DeprecationStage"]) {
            case "Deprecated":
                NewChipFile = NewChipFile.replace("._depr", DeprMsg)
                break;
        
            default:
                if (contents["IsBeta"]) {
                    NewChipFile = NewChipFile.replace("._depr", BetaMsg)
                } else {
                    NewChipFile = NewChipFile.replace("._depr", "")
                }
                break;
        }
        if(contents["Description"] !== "") {
            NewChipFile = NewChipFile.replace("._chipdesc", contents["Description"].replace("<", "&lt").replace(">", "&gt"))
        } else NewChipFile = NewChipFile.replace("._chipdesc", "*No description.*")

        fs.writeFileSync(__dirname + '/../Circuits/docs/documentation/chips/'.concat(uuid, ".mdx"), NewChipFile);

        
        const returnedsvg = await SVGGen.Generate(uuid, require("./Generated/chips.json"), require("./Generated/ports.json"))

        fs.mkdirSync(__dirname + "/../Circuits/docs/documentation/chips/assets/", {recursive: true})
        fs.writeFileSync(__dirname + "/../Circuits/docs/documentation/chips/assets/".concat(uuid, ".svg"), returnedsvg)

        Currentindex++
    }
}

async function TranslateChipData(cut){
    for(const [uuid, chipd] of entries) {
        // Order: List<> removal -> Param checker
        var ThisChipModel = "Default"
        if (chipd["ReadonlyPaletteName"] == "Comment" || chipd["ReadonlyPaletteName"].toLowerCase().includes("variable")){
            ThisChipModel = "Variable"
        } else if (chipd["ReadonlyPaletteName"].toLowerCase().includes("constant") || chipd["ReadonlyPaletteName"] == "Player World UI") {
            ThisChipModel = "Constant"
        }
        let t = [] 
        for (const pth of chipd["NodeFilters"]) {
            t = t.concat(pth["FilterPath"])
        }
        const thischip = NewChips[uuid] = {
            ChipName: chipd["ReadonlyChipName"],
            PaletteName: chipd["ReadonlyPaletteName"],
            Description: chipd["Description"],
            //custom here
            Model: ThisChipModel,
            //
            IsBeta: chipd["IsBetaChip"],
            TrollingRisk: chipd["IsTrollingRisk"],
            IsRoleAssignmentRisk: chipd["IsRoleAssignmentRisk"],
            DeprecationStage: chipd["DeprecationStage"],
            Tags: t
        }
        for(const NodeDesc of chipd["NodeDescs"]){
            delete NodeDesc["Name"]
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
                delete port["Description"]
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
                delete port["Description"]
            }
            delete NodeDesc["ReadonlyTypeParams"]
        }
        thischip["Functions"] = chipd["NodeDescs"]
    }
}

async function PrepareDocs() {
    try {
        fs.mkdirSync(__dirname + "/../Guides/")
    }
    catch (err) {}
    fs.emptyDirSync(__dirname + "/../Circuits/docs/guides/")
    const DirFolders = fs.readdirSync(__dirname + "/../Guides/")
    fs.writeFileSync(__dirname + "/../Circuits/docs/guides/_category_.json", JSON.stringify(GuidesCat, null, 4))

    var GuideIndex = 1

    for (const fldr of DirFolders) {
        if (!fldr.includes("__ignore")) {
            const GuideContent = fs.readFileSync(__dirname + "/../Guides/" + fldr)
            fs.writeFileSync(__dirname + "/../Circuits/docs/guides/" + fldr, GuideTemplate.replace("._index", GuideIndex).concat(GuideContent))
        }
        GuideIndex++
    }
}

async function RestOfUpdate(){
    oldJSON_raw = fs.readFileSync(DownloadFile, "utf-8")
    OldJSON = JSON.parse(oldJSON_raw)["Nodes"]
    OldJSON_Clone = JSON.parse(oldJSON_raw)["Nodes"]
    entries = Object.entries(OldJSON_Clone)
    
    try {
        AddStep("Updating ports.json...")
        await RetrievePorts();
        fs.writeFileSync("Generated/ports.json", JSON.stringify(PortTypes, null, 4))

        AddStep("Translating chips...")
        await TranslateChipData();
        fs.writeFileSync("Generated/chips.json", JSON.stringify(NewChips, null, 4))
        fs.writeFileSync("Generated/generated.txt", Date.now().toString())
    }
    catch (err) {
        console.error(err)
        console.log("Something went wrong! Can't skip important steps!")
        exit(1)
    }
    try {
        SVGGen = require("./Create-SVG")
        AddStep("Preparing page files...")
        await PrepareFiles();
    }
    catch (err) {
        console.error(err)
        console.log("Couldn't create doc files!")
    }
    try {
        AddStep("Copying docs...")
        await PrepareDocs();
    }
    catch (err) {
        console.error(err)
        console.log("Unable to clone docs!")
    }

    

    console.log("Finished!")
    exit(0)
}
AddStep("Downloading chips...")
fs.mkdirSync("Generated", {recursive: true}, function (err){
    if (err) console.log("error");
})
const file = fs.createWriteStream("Generated/Chips_OLD.json");
const request = https.get("https://raw.githubusercontent.com/tyleo-rec/CircuitsV2Resources/master/misc/circuitsv2.json", function(response) {
    response.pipe(file);

    file.on("finish", () => {
        file.close()
        RestOfUpdate()
    })
})

/*
Script made by Funn Punn. Please don't modify this, I already had a hard time reading my own code.
Thanks!

^•ﻌ•^
*/
