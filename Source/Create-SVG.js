const fs = require("fs-extra")
const d3 = require("d3")
const jsdom = require("jsdom")

const Chip_raw = fs.readFileSync("Generated/chips.json")
const Chip = JSON.parse(Chip_raw)
const Ports = JSON.parse(fs.readFileSync("Generated/ports.json"))
const Exec = ""
const DataNoDef = ""

//Padding
const PortHeight = 19
const MinimalPadding = 111
const VerticalPortPadding = 6
const HorizontalPortPadding = 2
const TopHeight = 41

const PaddingFromTop = 8
const PaddingFromBottom = 4

const chipxoffset = 160

//Padding

function AppendPort(ParentObject, IsInput, PortType, [posx, posy]) {
    const PType = Ports[PortType]
    var Color = "#F6EEE8"
    var Model = "Data"
    var HasDefaultValue = false
    var portoffset = 5
    try {
        Color = PType["Color"]
        Model = PType["Model"]
        HasDefaultValue = Ports[PortType]["HasDefaultValue"]
    }
    catch (err) {
        
    }
    if (Model == "Exec") {
        ParentObject.append("path")
            .attr("d", "M._posx,._posyh-16.465c-0.552,0,-1,0.448,-1,1v16c0,0.552,0.448,1,1,1h16.465c0.334,0,0.647,-0.167,0.832,-0.445l5.333,-8c0.224,-0.336,0.224,-0.774,0,-1.11l-5.333,-8c-0.185,-0.278,-0.498,-0.445,-0.832,-0.445z".replace("._posx", posx + portoffset).replace("._posy", posy))
            .attr("fill", Color)
        return 18
    } else if (Model == "Data") {
        if (HasDefaultValue && IsInput) {
            ParentObject.append("g")
                .attr("filter", "url(#filter0_di_2556_19132)")
                .append("rect")
                    .attr("x", posx - 12)
                    .attr("y", posy)
                    .attr("width", 22)
                    .attr("height", "15")
                    .attr("rx", "1")
                    .attr("fill", Color)

            const g2 = ParentObject.append("g")
                .attr("filter", "url(#filter1_di_2556_19132)")
            const TempWidth = 30
            g2.append("rect")
                .attr("x", posx - 24 - TempWidth - 12)
                .attr("y", posy - 4)
                .attr("width", 15 + TempWidth)
                .attr("height", 23)
                .attr("rx", "1")
                .attr("fill", Color)

            g2.append("rect")
                .attr("x", posx - 20 - TempWidth - 12)
                .attr("y", posy + 0.001)
                .attr("width", 7 + TempWidth)
                .attr("height", 15)
                .attr("rx", "1")
                .attr("fill", "#818081")

            ParentObject.append("g")
                .attr("filter", "url(#filter2_di_2556_19132)")
                .append("rect")
                    .attr("x", posx - 9 - 12)
                    .attr("y", posy + 4)
                    .attr("width", 9)
                    .attr("height", 7)
                    .attr("fill", Color)

        } else {
            ParentObject.append("rect")
                .attr("x", posx - 12)
                .attr("y", posy)
                .attr("width", "22")
                .attr("height", "15")
                .attr("rx", "1")
                .attr("fill", Color)
        }
    return 15
    }
}

function GenerateSVG (tempUUID) {
    const Template = new jsdom.JSDOM('<body></body>')
    const NewChip = d3.select(Template.window.document.body).append("svg")
        .attr("width", 400)
        .attr("height", 400)

    const Top = NewChip
        .append("path")
            .attr("d",
                "M._posx, ._posy v-31 q0,-10,10,-10 h91 q10,0,10,10 v31 h-111".replace("._posx", chipxoffset).replace("._posy", TopHeight)
            )
            .attr("fill", "#525152")

    const Bottom = NewChip 
            .append("path")
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
        const returnedwidth = AppendPort(NewChip, true, port["DataType"], [chipxoffset, InSpacing])
        InSpacing = InSpacing + returnedwidth + VerticalPortPadding
    }
    for (const port of Funcs["Outputs"]) {
        const returnedwidth = AppendPort(NewChip, false, port["DataType"], [chipxoffset + 111, OutSpacing])
        OutSpacing = OutSpacing + returnedwidth + VerticalPortPadding
    }

    const NewPathHeight = ("height", PaddingFromTop + PaddingFromBottom + Math.max(TotalInputSpacing, TotalOutputSpacing))

    Bottom.attr("d",
        "M._posx, ._posy v._heightsubten q0,10,10,10 h._chipwdsubten q10,0,10,-10 v._negheig h._chipyw".replace("._posx", chipxoffset).replace("._posy", TopHeight).replace("._heightsubten", NewPathHeight - 10).replace("._chipwdsubten", MinimalPadding - 20).replace("._chipyw", MinimalPadding).replace("._negheig", 0-NewPathHeight + 10)
    )

    return (Template.window.document.documentElement.innerHTML.replace("<head></head>", "").replace("<body>", "").replace("</body>", ""))
}

module.exports ={
    Generate: GenerateSVG
}