class RiskVisualizer {
  constructor(selector, data) {
    this.container = d3.select(selector);
    this.data = data;
    this.init();
  }

  init() {
    this.width = 800;
    this.height = 400;
    this.svg = this.container.append("svg")
      .attr("width", this.width)
      .attr("height", this.height);

    this.createScales();
    this.drawAxes();
    this.drawBubbles();
  }

  createScales() {
    this.xScale = d3.scaleLinear()
      .domain([0, d3.max(this.data, d => d.severity)])
      .range([50, this.width - 30]);

    this.yScale = d3.scaleBand()
      .domain(this.data.map(d => d.file_type))
      .range([30, this.height - 20]);
  }

  drawBubbles() {
    this.svg.selectAll("circle")
      .data(this.data)
      .enter()
      .append("circle")
      .attr("cx", d => this.xScale(d.severity))
      .attr("cy", d => this.yScale(d.file_type))
      .attr("r", d => Math.sqrt(d.count) * 3)
      .style("fill", "#ff4444")
      .style("opacity", 0.7);
  }
}
