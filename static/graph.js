(function() {
	window.addEventListener("load", function() {

		var svg = d3.select("svg"),
			width = +parseInt(svg.style("width")),
			height = +parseInt(svg.style("height")),
			transform = d3.zoomIdentity;;

	    // console.log(width + " " + height);

	    var container = svg.append("g");

	    var simulation = d3.forceSimulation()
		    .force("link", d3.forceLink().id(function(d) { return d.name; }).distance(100).strength(0.007))
		    .force("charge", d3.forceManyBody())
		    .force("center", d3.forceCenter(width / 2, height / 2));

		var link = container.append("g")
			.attr("class", "links")
			.selectAll("line")
			.data(graph.edges)
			.enter().append("line")
			.style("stroke-width", 5)

		var node = container.append("g")
			.attr("class", "nodes")
			.selectAll("circle")
			.data(graph.nodes)
			.enter().append("circle")
			.style("r", 13)
			.style("fill", "#000")
			.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended));

		node.append("title")
			.text(function(d) { return d.name; });

		simulation
			.nodes(graph.nodes)
			.on("tick", ticked);

		simulation.force("link")
			.links(graph.edges);

		svg.call(d3.zoom()
			.scaleExtent([1/10, 5])
			.on("zoom", zoomed));
		
		function ticked() {
			link
		        .attr("x1", function(d) { return d.source.x; })
		        .attr("y1", function(d) { return d.source.y; })
		        .attr("x2", function(d) { return d.target.x; })
		        .attr("y2", function(d) { return d.target.y; });
		    node
		        .attr("cx", function(d) { return d.x; })
		        .attr("cy", function(d) { return d.y; });
		}

		function zoomed() {
        	container.attr("transform", d3.event.transform);
        }

		function dragstarted(d) {
			if (!d3.event.active) simulation.alphaTarget(0.3).restart();
			d.fx = d.x;
			d.fy = d.y;
		}
		
		function dragged(d) {
			d.fx = d3.event.x;
			d.fy = d3.event.y;
		}

		function dragended(d) {
			if (!d3.event.active) simulation.alphaTarget(0);
			d.fx = null;
		 	d.fy = null;
		}
	});
})();