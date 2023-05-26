const SVGGen = require("./Create-SVG")
const fs = require("fs-extra")
const SuggJSON = JSON.parse(fs.readFileSync("Generated/suggestions.json", "utf-8"))

fs.writeFileSync("Generated/OutSVG.svg", SVGGen.Generate("mltry", SuggJSON))