nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
      .duration(350)
      .reduceXTicks(reduce_x_ticks)   //If 'false', every single x-axis tick label will be rendered.
      .rotateLabels(0)      //Angle to rotate x-axis labels.
      .showControls(true)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
      .groupSpacing(0.1)    //Distance between each group of bars.
      //.forceY([0,24])
      .height(450)
      .width(960)
    ;

    //chart.xAxis
    //    .tickFormat(d3.format(',f'));

    chart.yAxis
        .tickFormat(d3.format(',f'));
        
    d3.select('.stats__chart svg')
        .datum(my_data)
        .transition()
        .duration(500)
        .call(chart)
        .style({ 'height': 450, 'width': 960 });

    nv.utils.windowResize(chart.update);

    console.log(chart);

    return chart;
});
