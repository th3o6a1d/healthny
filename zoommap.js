function ZoomMap(geography, layers, dataset) {

    function getItem(area) {
      var area = new Number(area)
      var area = Math.floor(area / 100)
      var result = $.grep(dataset.data, function (e) {
          return e.id == area;
      });
      try {
          return result[0].value
      } catch (e) {
          // console.log('Could not load area ' + area);
      }
    }

    tooltip = d3.select("body").append("div").attr("class", "tooltip").style("position", "absolute").style("z-index", "10").style("opacity", 0);

    function zipmouseover(d) {
        $('#info').html(dataset.labels.id + ": "+ d.id + "<br>" + dataset.labels.value + ": " + getItem(d.id))
    };

    function mouseover(d) {
        var bedcount = ""
        if (d.beds) {
            bedcount = "<tr>Beds: " + d.beds + "</tr>"
        }
        return tooltip.html(d.hospital + "<br>" + bedcount).transition().duration(100).style("opacity", 0.80);
    };

    function mousemove(d) {
        var o, x, y;
        if (typeof event !== "undefined" && event !== null) {
            x = event.pageX;
            y = event.pageY;
        } else {
            o = $('body').offset();
            x = o.left + (d.xy[0] * .75);
            y = o.top + (d.xy[1] * .75) + 67;
        }
        return tooltip.style("top", (y - 10) + "px").style("left", (x + 10) + "px");
    };

    function mouseout() {
        return tooltip.transition().delay(100).style("opacity", 0).each("end", function () {
            return tooltip.style("top", "0px").style("left", "0px");
        });
    };
    var largest = 0
    for (i = 0; i < dataset.data.length; i++) {
        var value = dataset.data[i].value
        if (value > largest) {
            largest = value;
        }
    };
    var width = 1000,
        height = 600,
        centered;
    var quantize = d3.scale.quantize().domain([0, largest]).range(d3.range(9).map(function (i) {
        return "q" + i + "-9";
    }));

    var projection = d3.geo.mercator().scale(4500).translate([width / 2, height / 2]).center([-76.0, 43.0])
    var path = d3.geo.path().projection(projection);
    var svg = d3.select("body").append("svg").attr("width", width).attr("height", height);
    svg.append("rect").attr("class", "background").attr("id", "canvas").attr("width", width).attr("height", height);
    svg.append("div").attr("class", "scroll-left").attr("id", "info").attr("width", 300).attr("height", 200);
    var g = svg.append("g");
    var target = document.getElementById('info')
    var spinner = new Spinner().spin(target);

    d3.json(geography, function (error, ny) {
        g.append("g").attr("id", "zipcode").selectAll("path").data(topojson.feature(ny, ny.objects.ny).features).enter().append("path").attr("d", path).on("click", clicked).on("mouseover", zipmouseover).attr("title", function (d) {
            return d.id
        }).attr("class", function (d) {
            return quantize(getItem(d.id));
        })
        for (var i = 0; i < layers.length; i++) { 
          d3.json(layers[i], function (hosps) {
              node = g.append("g").attr("id", "hosps").selectAll("path").data(hosps).enter().append("g").attr("class", "node").attr("transform", function (d) {
                  return "translate(" + projection([d.coordinates[1], d.coordinates[0]]) + ")";
              });
              node.append("circle").attr("r", function (d) {
                  if (d.beds > 300) {
                      return 2 * d.beds / 625
                  } else {
                      return 2
                  };
              }).attr("fill", "red").attr("opacity", 0.5).on("mouseover", mouseover).on("mouseout", mouseout).on("mousemove", mousemove)
              node.append("text").attr("id", function (d) {
                  return "hosp" + d.id;
              }).attr("dy", "-.85em").text(function (d) {
                  return d.hospital;
              }).attr("class", "hidden").attr("text-anchor", "middle")
              spinner.stop();
          });
        };
    });

    function clicked(d) {
        var x, y, k;
        if (d && centered !== d) {
            var centroid = path.centroid(d);
            x = centroid[0];
            y = centroid[1];
            k = 11;
            g.selectAll("text").transition().duration(750).attr("transform", "scale(" + k / 50 + ")")
            g.selectAll("circle").transition().duration(750).attr("transform", "scale(" + k / 50 + ")")
            centered = d;
        } else {
            x = width / 2;
            y = height / 2;
            k = 1;
            g.selectAll("text").transition().duration(750).attr("transform", "scale(" + k + ")")
            g.selectAll("circle").transition().duration(750).attr("transform", "scale(" + k + ")")
            centered = null;
        }
        g.selectAll("path").classed("active", centered &&
            function (d) {
                return d === centered;
            });
        g.transition().duration(750).attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")").style("stroke-width", 1.5 / k + "px");
    }
};