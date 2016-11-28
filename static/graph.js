(function() {
	window.addEventListener("load", function() {
		
		var toggle = 0;
		var svg = d3.select("svg"),
			width = +parseInt(svg.style("width")),
			height = +parseInt(svg.style("height")),
			transform = d3.zoomIdentity;;

	    // console.log(width + " " + height);

	    svg.attr("pointer-events", "all")
	    
	    var fisheye = d3.fisheye()
	    	.radius(200)
	    	.power(4);

	    svg.attr("pointer-events", "all");

	    var container = svg.append("g")
	    	.call(d3.zoom().scaleExtent([1/10, 5]).on("zoom", zoomed))
	    	.append("g");

	    container.append("rect")
	    	.attr("width", width)
	    	.attr("height", height)
	    	.attr("fill", "white")

	    // container.attr("pointer-events", "all")

	    var simulation = d3.forceSimulation()
		    .force("link", d3.forceLink().id(function(d) { return d.name; }).distance(175).strength(0.007))
		    .force("charge", d3.forceManyBody())
		    .force("center", d3.forceCenter(width / 2, height / 2));

		var link = container.selectAll("line")
			.data(graph.edges)
			.enter().append("line")
			.attr("class", "links")
			.style("stroke-width", 5)
			.attr("x1", function(d) { return d.source.x; })
	    	.attr("y1", function(d) { return d.source.y; })
	    	.attr("x2", function(d) { return d.target.x; })
	    	.attr("y2", function(d) { return d.target.y; });

		var node = container.selectAll("circle")
			.data(graph.nodes)
			.enter().append("circle")
			.attr("class", "nodes")
			.attr("cx", function(d) { return d.x })
			.attr("cy", function(d) { return d.y })
			.attr("r", 13)
			.style("fill", "#000")
			.on("click", connectedNodes);
			// .on("mout", showAll);
			// .call(d3.drag()
			// 	.on("start", dragstarted)
			// 	.on("drag", dragged)
			// 	.on("end", dragended));

		node.append("title")
			.text(function(d) { return d.name; });

		container.on("mousemove", function() {
	    	fisheye.center(d3.mouse(this));

	    	node
				.each(function(d) { d.display = fisheye(d); })
				.attr("cx", function(d) { return d.display.x; })
				.attr("cy", function(d) { return d.display.y; })
				.attr("r", function(d) { return d.display.z * 13; });

	    	link
	            .attr("x1", function(d) { return d.source.display.x; })
	            .attr("y1", function(d) { return d.source.display.y; })
	            .attr("x2", function(d) { return d.target.display.x; })
	            .attr("y2", function(d) { return d.target.display.y; });
    	});	

		simulation
			.nodes(graph.nodes)
			.on("tick", ticked);

		simulation.force("link")
			.links(graph.edges);

		// simulation.tick()

		// container.call(d3.zoom()
		// 	.scaleExtent([1/10, 5])
		// 	.on("zoom", zoomed));

		var linkedByIndex = {};
		for (i = 0; i < graph.nodes.length; i++) {
		    linkedByIndex[i + "," + i] = 1;
		};
		graph.edges.forEach(function (d) {
		    linkedByIndex[d.source.index + "," + d.target.index] = 1;
		});

		function neighboring(a, b) {
		    return linkedByIndex[a.index + "," + b.index];
		}

		function connectedNodes() {
		    if (toggle == 0) {
		        d = d3.select(this).node().__data__;
		        node.style("opacity", function (o) {
		            return neighboring(d, o) | neighboring(o, d) ? 1 : 0.15;
	        	});
		        toggle = 1;
		    } else {
		        node.style("opacity", 1);;
		        toggle = 0;
		    }
		}

		function showAll() {
			node.style("opacity", 1);;
		}

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

		// function dragstarted(d) {
		// 	if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		// 	d.fx = d.x;
		// 	d.fy = d.y;
		// }

		// function dragged(d) {
		// 	d.fx = d3.event.x;
		// 	d.fy = d3.event.y;
		// }

		// function dragended(d) {
		// 	if (!d3.event.active) simulation.alphaTarget(0);
		// 	d.fx = null;
		//  	d.fy = null;
		// }
	});
})();