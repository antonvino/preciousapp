nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
      .duration(350)
      .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
      .rotateLabels(0)      //Angle to rotate x-axis labels.
      .showControls(true)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
      .groupSpacing(0.1)    //Distance between each group of bars.
      .forceY([0,24])
      .height(300)
    ;

    //chart.xAxis
    //    .tickFormat(d3.format(',f'));

    chart.yAxis
        .tickFormat(d3.format(',f'));
        
    d3.select('#chart svg')
        .datum(my_data)
        .call(chart)
        .style({ 'height': 300 });

    nv.utils.windowResize(chart.update);

    return chart;
});