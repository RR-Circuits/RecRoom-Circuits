const fs = require("fs-extra")
const d3 = require("d3")
const jsdom = require("jsdom")
const StringWidth = require("string-pixel-width")
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

const chipxoffset = 72

const FontSize = 18

//Padding
function GetStringWidth (str) {
    return StringWidth(str, {size: FontSize})
}

function AppendPort(ParentObject, IsInput, PortType, [posx, posy], PortName) {
    const PType = Ports[PortType]
    var Color = "#F6EEE8"
    var Model = "Data"
    var HasDefaultValue = false
    var portoffset = 5

    var prtheight = 0
    try {
        Color = PType["Color"]
        Model = PType["Model"]
        HasDefaultValue = Ports[PortType]["HasDefaultValue"]
    }
    catch (err) {
        
    }
    if (Model == "Exec") {
        var posxrep = posx + portoffset
        if (!IsInput) {
            posxrep = posxrep + 2
        }
        const testpath = ParentObject.append("path")
            .attr("d", "M._posx,._posyh-16.465c-0.552,0,-1,0.448,-1,1v16c0,0.552,0.448,1,1,1h16.465c0.334,0,0.647,-0.167,0.832,-0.445l5.333,-8c0.224,-0.336,0.224,-0.774,0,-1.11l-5.333,-8c-0.185,-0.278,-0.498,-0.445,-0.832,-0.445z".replace("._posx", posxrep).replace("._posy", posy))
            .attr("fill", Color)
        prtheight = 18
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
            const testrect = ParentObject.append("rect")
                .attr("x", posx - 12)
                .attr("y", posy)
                .attr("width", "22")
                .attr("height", "15")
                .attr("rx", "1")
                .attr("fill", Color)
            if (!IsInput) {
                testrect.attr("x", posx - 10)
            }
        }

    prtheight = 15
    }
    var Anch = "start"
    if (!IsInput) {Anch = "end"; portoffset = -16} else {portoffset = 16}

    ParentObject.append("svg:text")
        .attr("x", posx + portoffset)
        .attr("y", posy+12.5)
        .text(PortName)
        .attr("fill", "white")
        .attr("text-anchor", Anch)
        .attr("font-size", "medium")
        .attr("class", "uwuntu")
    
    return [prtheight]
}

function GenerateSVG (tempUUID) {
    const Template = new jsdom.JSDOM('<body></body>')
    const NewChip = d3.select(Template.window.document.body).append("svg")
        .attr("width", 800)
        .attr("height", 800)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("viewbox", "0 0 800 800")

    const Title = NewChip
        .append("svg:text")
            .attr("x", 10)
            .attr("y", 20)
            .text(Chip[tempUUID]["ChipName"])
            .attr("fill", "white")
            .attr("text-anchor", "middle")
            .attr("font-size", "18px")
            .attr("class", "uwuntu")

    const TopBarWidth = GetStringWidth(Title.text()) + 57 * 2
    Title.attr("x", TopBarWidth/2 + chipxoffset).attr("y", (TopHeight+FontSize)/2)
    const Bottom = NewChip 
            .append("path")
                .attr("fill", "#818081")

    const Funcs = Chip[tempUUID]["Functions"][0]
    var TotalInputSpacing = 0
    var TotalOutputSpacing = 0

    var LargestInputText = 0
    var LargestOutputText = 0

    var InSpacing = TopHeight + PaddingFromTop
    var OutSpacing = TopHeight + PaddingFromTop
    
    try {
        if (Funcs["Inputs"].length > 0) {
            TotalInputSpacing = (Funcs["Inputs"].length) * VerticalPortPadding - 1 + Funcs["Inputs"].length * PortHeight
        }
        if (Funcs["Outputs"].length > 0) {
            TotalOutputSpacing = (Funcs["Outputs"].length) * VerticalPortPadding - 1 + Funcs["Outputs"].length * PortHeight
        }
        
        for (const port of Funcs["Inputs"]) {
            if (GetStringWidth(port["Name"]) > LargestInputText) {
                LargestInputText = GetStringWidth(port["Name"])
            }
        }
        for (const port of Funcs["Outputs"]) {
            if (GetStringWidth(port["Name"]) > LargestOutputText) {
                LargestOutputText = GetStringWidth(port["Name"])
            }
        }

        for (const port of Funcs["Inputs"]) {
            const RtrnVL = AppendPort(NewChip, true, port["DataType"], [chipxoffset, InSpacing], port["Name"])
            const returnedwidth = RtrnVL[0]
            const namelen = RtrnVL[1]
            InSpacing = InSpacing + returnedwidth + VerticalPortPadding
        }
        for (const port of Funcs["Outputs"]) {
            const RtrnVL = AppendPort(NewChip, false, port["DataType"], [chipxoffset + Math.max(MinimalPadding, TopBarWidth, LargestInputText + LargestOutputText + HorizontalPortPadding), OutSpacing], port["Name"])
            const returnedwidth = RtrnVL[0]
            const namelen = RtrnVL[1]
            OutSpacing = OutSpacing + returnedwidth + VerticalPortPadding
        }
    } catch (err) {}

    const NewPathHeight = (PaddingFromTop + PaddingFromBottom + Math.max(TotalInputSpacing, TotalOutputSpacing))

    const ChipLen = Math.max(MinimalPadding, TopBarWidth, LargestInputText + LargestOutputText + HorizontalPortPadding)

    Bottom.attr("d",
        "M._posx, ._posy v._heightsubten q0,10,10,10 h._chipwdsubten q10,0,10,-10 v._negheig h._chipyw".replace("._posx", chipxoffset).replace("._posy", TopHeight).replace("._heightsubten", NewPathHeight - 10).replace("._chipwdsubten", ChipLen - 20).replace("._chipyw", ChipLen).replace("._negheig", 0-NewPathHeight + 10)
    )
    NewChip.attr("height", 41 + NewPathHeight)
    NewChip.attr("viewbox", "0 0 800 ".concat(41 + NewPathHeight))
    const Top = NewChip
        .append("path")
            .attr("d",
                "M._posx, ._posy v-31 q0,-10,10,-10 h._horsub20 q10,0,10,10 v31 h-._horr".replace("._posx", chipxoffset).replace("._posy", TopHeight).replace("._horsub20", ChipLen - 20).replace("._horr", ChipLen)
            )
            .attr("fill", "#525152")
    Title.raise()
    Title.attr("x", ChipLen/2 + chipxoffset)
    return (Template.window.document.documentElement.innerHTML.replace("<head></head>", "").replace("<body>", "").replace("</body>", ""))
}

module.exports ={
    Generate: GenerateSVG
}