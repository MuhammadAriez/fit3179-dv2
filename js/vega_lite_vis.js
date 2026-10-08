// Week 7: one variable holds the location of each chart's JSON file,
// then vegaEmbed draws that chart inside the div with the matching id.
//
// {"actions": false} hides the three-dot menu (Week 9).
// {"renderer": "svg"} draws the chart as SVG, so its text uses our Google font.

var embedOptions = {"actions": false, "renderer": "svg"};

// Panel 6: choropleth map
var vg_choropleth = "js/choropleth_map.vg.json";
vegaEmbed("#choropleth_map", vg_choropleth, embedOptions).then(function (result) {
  // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);


var vg_stacked_bar= "js/stacked_bar_chart.vg.json";
vegaEmbed("#stacked_bar_chart", vg_stacked_bar, embedOptions).then(function (result){

}).catch(console.error);


var vg_dumbbell= "js/dumbbell_chart.vg.json";
vegaEmbed("#dumbbell_chart", vg_dumbbell, embedOptions).then(function (result){

}).catch(console.error);

// Panel 10: slope graph
var vg_slope = "js/slope_chart.vg.json";
vegaEmbed("#slope_chart", vg_slope, embedOptions).then(function (result) {
}).catch(console.error);


// Panel 11: heatmap
var vg_heatmap = "js/heatmap.vg.json";
vegaEmbed("#heatmap", vg_heatmap, embedOptions).then(function (result) {
}).catch(console.error);


// Panel 7: proportional symbol map
var vg_symbol = "js/symbol_map.vg.json";
vegaEmbed("#symbol_map", vg_symbol, embedOptions).then(function (result) {
}).catch(console.error);

// Panel 8: lollipop chart
var vg_lollipop = "js/lollipop_chart.vg.json";
vegaEmbed("#lollipop_chart", vg_lollipop, embedOptions).then(function (result) {
}).catch(console.error);

// Panel 9: small-multiple maps
var vg_small_maps = "js/small_multiple_maps.vg.json";
vegaEmbed("#small_multiple_maps", vg_small_maps, embedOptions).then(function (result) {
}).catch(console.error);

// Panel 1: waffle chart
var vg_waffle = "js/waffle_chart.vg.json";
vegaEmbed("#waffle_chart", vg_waffle, embedOptions).then(function (result) {
}).catch(console.error);

// Panel 12: butterfly chart
var vg_butterfly = "js/butterfly_chart.vg.json";
vegaEmbed("#butterfly_chart", vg_butterfly, embedOptions).then(function (result) {
}).catch(console.error);

// Panel 13: treemap
var vg_treemap = "js/treemap.vg.json";
vegaEmbed("#treemap", vg_treemap, embedOptions).then(function (result) {
}).catch(console.error);