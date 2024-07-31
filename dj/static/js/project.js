function createHeroGraph(selector, nodesData, linksData) {
    const width = 900, height = 800;
    const svg = d3.select(selector).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    const nodes = nodesData.sort((a, b) => a.size - b.size);
    const links = linksData;

    function raise() {
        d3.select(this).raise()
    }

    // Define patterns for each node image
    svg.append("defs")
        .selectAll("pattern")
        .data(nodes)
        .enter().append("pattern")
        .attr("id", d => `pattern-${d.id}`)
        .attr("patternUnits", "objectBoundingBox")
        .attr("width", 1)
        .attr("height", 1)
        .append("image")
        .attr("xlink:href", d => d.image)
        .attr("width", d => d.size)
        .attr("height", d => d.size)
        .attr("preserveAspectRatio", "xMidYMid slice");

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-550))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("class", "link");

    const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter().append("g")
        .attr("class", "node")
        .on("click", handleNodeClick)
        .on("mouseover", raise)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("circle")
        .attr("r", d => d.size / 2.2) // Adjust radius based on count
        .attr("fill", d => `url(#pattern-${d.id})`);

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);

    function ticked() {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("transform", d => `translate(${d.x},${d.y})`);
    }

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    function handleNodeClick(event, d) {
        // Reset previous highlights
        link.classed("highlighted-link", false);
        node.select("circle").style("stroke", '#b6b6b6');
        node.select("circle").style("opacity", '0.6');

        // Highlight the selected node
        d3.select(this).select("circle").classed("highlighted-node", true);
        // Highlight connected links and nodes
        link.filter(l => l.source.id === d.id || l.target.id === d.id)
            .classed("highlighted-link", true)
            .raise()
            .each(function (l) {
                d3.select(`#node-${l.source.id}`).raise();
                d3.select(`#node-${l.target.id}`).raise();
                d3.select(`#node-${l.source.id}`).select("circle").style("stroke", 'red');
                d3.select(`#node-${l.source.id}`).select("circle").style("opacity", '1');
                d3.select(`#node-${l.target.id}`).select("circle").style("stroke", 'red');
                d3.select(`#node-${l.target.id}`).select("circle").style("opacity", '1');
            });
    }

    // Add unique IDs to nodes for easier selection
    node.attr("id", d => `node-${d.id}`);
}

function createPieChart(selector, data) {
    const dataSorted = data.sort((a, b) => b.count - a.count);

    const pch_width = 700;
    const pch_height = 700;
    const radius = Math.min(pch_width, pch_height) / 3;
    const arc = d3.arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius - 1);

    const pie = d3.pie()
        .padAngle(1 / radius)
        .sort((a, b) => b.count - a.count)
        .value(d => d.count);

    const color = d3.scaleOrdinal()
        .domain(dataSorted.map(d => d.name))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), dataSorted.length).reverse());

    const pch_svg = d3.select(selector).append("svg")
        .attr("width", pch_width)
        .attr("height", pch_height)
        .attr("viewBox", [-pch_width / 2, -pch_height / 2, pch_width, pch_height])
        .attr("style", "max-width: 100%; height: auto;");

    pch_svg.append("g")
        .selectAll("path")
        .data(pie(dataSorted))
        .join("path")
        .attr("fill", d => color(d.data.name))
        .attr("d", arc)
        .append("title")
        .text(d => `${d.data.name}: ${d.data.count}`);

    pch_svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(pie(dataSorted))
        .join("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`);

    // Add circular images to the labels
    const defs = pch_svg.append("defs");

    dataSorted.forEach((d, i) => {
        defs.append("clipPath")
            .attr("id", `clip-${i}`)
            .append("circle")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("r", d.size / 4);
    });

    pch_svg.append("g")
        .selectAll("g")
        .data(pie(dataSorted))
        .enter()
        .append("g")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .call(image => image.filter(d => d.data.size > 40).append("image")
            .attr("xlink:href", d => d.data.image)
            .attr("width", d => d.data.size)
            .attr("height", d => d.data.size / 1.77)
            .attr("x", d => -0.50 * d.data.size - 9.12)  // Center the image horizontally
            .attr("y", d => -0.40 * d.data.size + 9.5)  // Center the image vertically
            .attr("clip-path", (d, i) => `url(#clip-${i})`));
}

function createBarChart(selector, dataChar) {

    const data = dataChar.sort((a, b) => b.count - a.count).slice(0, 8)
    // Specify the chart’s dimensions.
    const width = 450;
    const height = 250;
    const marginTop = 20;
    const marginRight = 0;
    const marginBottom = 40; // Increased to accommodate image height
    const marginLeft = 40;


    // Create the horizontal scale and its axis generator.
    const x = d3.scaleBand()
        .domain(d3.sort(data, d => -d.count).map(d => d.id))
        .range([marginLeft, width - marginRight])
        .padding(0.1);

    const xAxis = d3.axisBottom(x).tickSize(0);

    // Create the vertical scale.
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)]).nice()
        .range([height - marginBottom, marginTop]);

    // Create the SVG container and call the zoom behavior.
    const svg = d3.select(selector).append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto;");

    // Append the bars.
    svg.append("g")
        .attr("class", "bars")
        .attr("fill", "steelblue")
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", d => x(d.id))
        .attr("y", d => y(d.count))
        .attr("height", d => y(0) - y(d.count))
        .attr("width", x.bandwidth());

    // Append the axes.
    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis)
        .selectAll(".tick text").remove(); // Remove text labels

    // Add hero images to the x-axis
    svg.selectAll(".x-axis .tick")
        .append("svg:image")
        .attr("xlink:href", d => data.find(item => item.id === d).image)
        .attr("width", 50)
        .attr("height", 30)
        .attr("x", -25) // Center the image horizontally
        .attr("y", 10); // Adjust the vertical position of the images

    svg.append("g")
        .attr("class", "y-axis")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y))
        .call(g => g.select(".domain").remove());

    function zoom(svg) {
        const extent = [[marginLeft, marginTop], [width - marginRight, height - marginTop]];

        svg.call(d3.zoom()
            .scaleExtent([1, 8])
            .translateExtent(extent)
            .extent(extent)
            .on("zoom", zoomed));

        function zoomed(event) {
            x.range([marginLeft, width - marginRight].map(d => event.transform.applyX(d)));
            svg.selectAll(".bars rect").attr("x", d => x(d.id)).attr("width", x.bandwidth());
            svg.selectAll(".x-axis").call(xAxis);
            svg.selectAll(".x-axis image")
                .attr("x", d => x(d))
                .attr("width", x.bandwidth());
        }
    }

    return svg.node();
}

function fetchLeagueData(id) {
    const btnSeries = document.getElementById(`fetch-button-${id}`);

    console.log(id)
    fetch(`/leagues/${id}/series/`,)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // document.getElementById(`fetch-details-${id}`).innerText = data.error;
                btnSeries.classList.remove('btn-success');
                btnSeries.classList.add('btn-danger');
            } else {
                // document.getElementById(`fetch-details-${id}`).innerHTML = "OK";
                btnSeries.classList.remove('btn-danger');
                btnSeries.classList.add('btn-success');
            }
        })
        .catch(error => {
            console.error('Error fetching team data:', error);
            btnSeries.classList.remove('btn-success');
            btnSeries.classList.add('btn-danger');
        });
}

function showProgressBar(idSelector) {
    const divPr = document.getElementById(idSelector);
    divPr.classList.add('progress')
    divPr.innerHTML = '<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>'
    return divPr;
}

function removeProgressBar(progressBar) {
    if (progressBar) {
        progressBar.remove();
    }
}

async function fetchDataAndCreateCharts(query, idProgress) {
    const progressBar = showProgressBar(idProgress);

    function searchParamsToObj(url) {
        const paramsMap = Array
            .from(url.searchParams)
            .reduce((params, [key, val]) => params.set(key, val), new Map());
        return Object.fromEntries(paramsMap);
    }

    try {
        const url = new URL('/matches/heroes?' + query, window.location.origin);
        console.log(searchParamsToObj(url))
        // let leagueId, teamId, startDateTime, durationSeconds;
        // if (leagueId) url.searchParams.append('league_id', leagueId);
        // if (teamId) url.searchParams.append('team_id', teamId);
        // if (startDateTime) url.searchParams.append('start_date_time', startDateTime);
        // if (durationSeconds) url.searchParams.append('duration_seconds', durationSeconds);

        const response = await fetch(url);
        const data = await response.json();
        if (data.error) {
            console.error('Error fetching heroes data:', data.error);
            return null;
        } else {
            return data;
        }
    } catch (error) {
        console.error('Error fetching heroes data:', error);
        return null;
    } finally {
        removeProgressBar(progressBar);
    }
}

