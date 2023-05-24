const fs = require("fs-extra")
const d3 = require("d3")
const jsdom = require("jsdom")

const Chip_raw = fs.readFileSync("Generated/examplechip.json")
const Chip = JSON.parse(Chip_raw)
const Ports = JSON.parse(fs.readFileSync("Generated/ports.json"))
const Exec = ""
const DataNoDef = ""

const tempUUID = "ff1c2a15-4099-4aaa-afe3-c217b2fca15b"

//Padding
const PortHeight = 19
const MinimalPadding = 111
const VerticalPortPadding = 4
const HorizontalPortPadding = 2
const TopHeight = 41

const PaddingFromTop = 8
const PaddingFromBottom = 20

const chipxoffset = 20

//Padding

function AppendPort(ParentObject, IsInput, PortType, [posx, posy]) {
    const { HasDefaultValue, Model, Color } = Ports[PortType]
    switch (Model) {
        case "Exec":
            ParentObject.append("path")
                .attr("d", "M._posx,._posyh-16.465c-0.552,0,-1,0.448,-1,1v16c0,0.552,0.448,1,1,1h16.465c0.334,0,0.647,-0.167,0.832,-0.445l5.333,-8c0.224,-0.336,0.224,-0.774,0,-1.11l-5.333,-8c-0.185,-0.278,-0.498,-0.445,-0.832,-0.445z")
                .attr("fill", Color)
        case "Data":
            if (HasDefaultValue || !IsInput) {
                ParentObject.append("g")
                    .attr("filter", "url(#filter0_di_2556_19132)")
                    .append("rect")
                        .attr("x", posx)
                        .attr("y", posy)
                        .attr("width", 22)
                        .attr("height", "")
            } else {

            }

    }
}

const Template = new jsdom.JSDOM('<body></body>')
const NewChip = d3.select(Template.window.document.body).append("svg")
    .attr("width", 165)
    .attr("height", 165)

const Top = NewChip
    .append("rect")
        .attr("x", chipxoffset)
        .attr("y", 0)
        .attr("width", MinimalPadding)
        .attr("height", TopHeight)
        .attr("fill", "#525152")

const Bottom = NewChip 
        .append("rect")
            .attr("x", chipxoffset)
            .attr("y", TopHeight)
            .attr("width", Math.max(MinimalPadding, 0))
            .attr("fill", "#818081")

const Funcs = Chip[tempUUID]["Functions"][0]
var TotalInputSpacing = 0
var TotalOutputSpacing = 0

if (Funcs["Inputs"].length > 0) {
    TotalInputSpacing = (Funcs["Inputs"].length) * VerticalPortPadding - 1 + Funcs["Inputs"].length * PortHeight
}
if (Funcs["Outputs"].length > 0) {
    TotalOutputSpacing = (Funcs["Outputs"].length) * VerticalPortPadding - 1 + Funcs["Outputs"].length * PortHeight
}

var InSpacing = TopHeight + PaddingFromTop
var OutSpacing = TopHeight + PaddingFromTop

for (const port of Funcs["Inputs"]) {
    NewChip.append("path")
        .attr("d", Exec.replace("._posx", chipxoffset + 5).replace("._posy", InSpacing))
        .attr("fill", "#F55C1A")
    InSpacing = InSpacing + PortHeight + VerticalPortPadding
}
for (const port of Funcs["Outputs"]) {
    NewChip.append("path")
        .attr("d", Exec.replace("._posx", chipxoffset + 111 + 5).replace("._posy", OutSpacing))
        .attr("fill", "#F55C1A")
    OutSpacing = OutSpacing + PortHeight + VerticalPortPadding
}

Bottom.attr("height", PaddingFromTop + PaddingFromBottom + Math.max(TotalInputSpacing, TotalOutputSpacing))

fs.writeFileSync("Generated/TestElement.svg", Template.window.document.documentElement.innerHTML.replace("<head></head>", "").replace("<body>", "").replace("</body>", ""))