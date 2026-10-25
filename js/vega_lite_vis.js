// Week 7: one variable holds the location of each chart's JSON file,
// then vegaEmbed draws that chart inside the div with the matching id.
//
// {"actions": false} hides the three-dot menu (Week 9).
// {"renderer": "svg"} draws the chart as SVG, so its text uses our Google font.

var embedOptions = {"actions": false, "renderer": "svg"};

// Figure 1: Pictogram
var vg_pictogram = "js/01_pictogram.vg.json";
vegaEmbed("#pictogram", vg_pictogram, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 2: Sankey diagram
var vg_sankey = "js/02_sankey_diagram.vg.json";
vegaEmbed("#sankey_diagram", vg_sankey, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 3: Dumbbell chart
var vg_dumbbell = "js/03_dumbbell_chart.vg.json";
vegaEmbed("#dumbbell_chart", vg_dumbbell, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 4: 100% stacked bar chart
var vg_stacked_bar = "js/04_stacked_bar_chart.vg.json";
vegaEmbed("#stacked_bar_chart", vg_stacked_bar, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 5: Choropleth map
var vg_choropleth = "js/05_choropleth_map.vg.json";
vegaEmbed("#choropleth_map", vg_choropleth, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 6: Proportional symbol map
var vg_symbol = "js/06_symbol_map.vg.json";
vegaEmbed("#symbol_map", vg_symbol, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 7: Hexagon bin map
var vg_bin_map = "js/07_bin_map.vg.json";
vegaEmbed("#bin_map", vg_bin_map, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 8: Lollipop chart
var vg_lollipop = "js/08_lollipop_chart.vg.json";
vegaEmbed("#lollipop_chart", vg_lollipop, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 9: Small-multiple maps and line chart
var vg_small_maps = "js/09_small_multiple_maps.vg.json";
vegaEmbed("#small_multiple_maps", vg_small_maps, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 10: Slope chart
var vg_slope = "js/10_slope_chart.vg.json";
vegaEmbed("#slope_chart", vg_slope, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 11: Heatmap
var vg_heatmap = "js/11_heatmap.vg.json";
vegaEmbed("#heatmap", vg_heatmap, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 12: Butterfly chart
var vg_butterfly = "js/12_butterfly_chart.vg.json";
vegaEmbed("#butterfly_chart", vg_butterfly, embedOptions).then(function (result) {
}).catch(console.error);

// Figure 13: Treemap
var vg_treemap = "js/13_treemap.vg.json";
vegaEmbed("#treemap", vg_treemap, embedOptions).then(function (result) {
}).catch(console.error);
