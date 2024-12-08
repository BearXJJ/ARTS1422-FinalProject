<script setup>
  import {ref, onMounted} from 'vue';
  import * as d3 from 'd3';

  const graphRef = ref(null);
  let svg, maingroup, circles, texts, lines;
  let simulation;
  let MAXCOO, color;
  let onDrag = false;

  const radius = d => Math.sqrt(d.total_patent_num)*10;
  const linkStrength = d => d.coo / 100;

  const init = (data) => {
    // 渲染连接线
    lines = maingroup.selectAll('.links').data(data.links).join('line').attr('class', 'links')
      .attr('stroke', 'black')
      .attr('opacity', 0)
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', d => d.coo * 2)
      .attr('stroke-dashoffset', 0);

    // 渲染节点
    circles = maingroup.selectAll('.circles').data(data.nodes).join('circle')
      .attr('class', 'circles')
      .attr('opacity', 1)
      .attr('r', radius)
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('fill', (d, i) => color(i))
      .on('mouseover', (event, d) => {
        if(onDrag) return;
        let t = d3.transition().duration(500)
        let relatedLinks = data.links.filter(l => l.source.index === d.index || l.target.index === d.index);
        relatedLinks = relatedLinks.map(l => l.source.index).concat(relatedLinks.map(l => l.target.index));
        relatedLinks = [...new Set(relatedLinks)]
        d3.selectAll('.links')
          .filter(l => l.source.index === d.index || l.target.index === d.index)
          .transition().duration(500).ease(d3.easeLinear)
          .attr('opacity', l => Math.pow(l.coo / MAXCOO, 2))
          .on('start', function repeat(){
            d3.select(this).attr('stroke-dashoffset', 0);
            d3.active(this).attr('stroke-dashoffset', l => l.coo * 4).transition().on('start', repeat);
          });
        d3.selectAll('.links')
          .filter(l => l.source.index != d.index && l.target.index != d.index)
          .transition(t)
          .attr('opacity', 0);
        d3.selectAll('.circles, .text')
          .filter(l => relatedLinks.includes(l.index))
          .transition(t)
          .attr('opacity', 1);
        d3.selectAll('.circles, .text')
          .filter(l => !relatedLinks.includes(l.index))
          .transition(t)
          .attr('opacity', 0);
      })
      .on('mouseout', (event, d) => {
        if(onDrag) return;
        let t = d3.transition().duration(500)
        d3.selectAll('.links')
          .transition(t)
          .attr('opacity', 0);
        d3.selectAll('.circles, .text')
          .transition(t)
          .attr('opacity', 1);
      })

    // 渲染节点文本
    texts = maingroup.selectAll('.text').data(data.nodes).join('text')
      .attr('class', 'text')
      .attr('opacity', 1)
      .attr('x', d => d.x)
      .attr('y', d => d.y)
      // .attr('font-size', d => radius(d) > 50 ? radius(d) : 10)
      .attr('font-size', 16)
      .attr('text-anchor', 'middle')
      .attr('dy', 4)
      .attr("pointer-events", "none")
      .attr('fill', 'black')
      .text(d => d.name);


  };

  const ticked = () => {
    lines
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);
    circles
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);
    texts
      .attr('x', d => d.x)
      .attr('y', d => d.y);
  };

  // 定义边界力
  const forceBoundary = (nodes, width, height) => {
    nodes.forEach(node => {
      const r = radius(node)+20;
      if(node.x - r < 0) node.x = r;
      if(node.x + r > width) node.x = width - r;
      if (node.y - r < 0) node.y = r;
      if (node.y + r > height) node.y = height - r;
    });
  };

  // 定义拖拽方法
  const dragstarted = (event) => {
    onDrag = true;
    if (!event.active) simulation.alphaTarget(0.99).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  };

  const dragged = (event) => {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  };

  const dragended = (event) => {
    onDrag = false;
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  };

  const drag = d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);

  // 加载数据并初始化力导向图
  onMounted(() => {
    svg = d3.select(graphRef.value);
    svg.attr('viewBox', `0 0 ${svg.node().clientWidth} ${svg.node().clientHeight}`);

    maingroup = svg.append('g')
      .attr('id', 'maingroup')
      .attr('transform', 'translate(0, 0) scale(1)');

    d3.json('test-data.json').then(data => {
      MAXCOO = d3.max(data.links, d => d.coo);
      color = d3.scaleSequential(d3.interpolateRainbow).domain([0, data.nodes.length - 1]);

      data.nodes.forEach(n => {
        n.x = svg.node().clientWidth / 2 + Math.random() * 10;
        n.y = svg.node().clientHeight / 2 + Math.random() * 10;
      });

      init(data);

      const forceNode = d3.forceManyBody()
        .strength(-30)
        .distanceMax(50);
      const forceLink = d3.forceLink(data.links)
        .id(d => d.index)
        .strength(linkStrength)
        .distance(400);

      simulation = d3.forceSimulation(data.nodes)
        .force("link", forceLink)
        .force("charge", forceNode)
        .force("collide", d3.forceCollide().radius(d => radius(d) + 5))
        .force("boundary", () => forceBoundary(data.nodes, svg.node().clientWidth, svg.node().clientHeight))
        .on("tick", ticked);

      circles.call(drag);
    });

  });

</script>

<template>
  <div class="panoramic-view">
    <div class="title">
      <div>Panoramic View</div>
      <div class="icon">
        <span class="iconfont icon-fangdajing"></span>
        <span class="iconfont icon-duibi"></span>
      </div>

    </div>
    <svg ref="graphRef" class="graph"></svg>
  </div>
</template>

<style lang="less" scoped>
  @import '../assets/icon/iconfont.css';
  .panoramic-view {
    height: 100%;
    padding: 0px 10px;
    display: flex;
    flex-direction: column;
  }

  .title {
    display: flex;
    justify-content: space-between;
    height: 30px;
    line-height: 30px;
    border-bottom: 2px solid rgb(179, 179, 179);
    .icon{
      .iconfont{
        font-size: 20px;
        margin-left: 10px;
      }
    }
  }

  .graph {
    flex-grow: 1;
    width: 100%;
    height: 100%;
  }
</style>
