<template>
  <div class="panoramic-view">
    <div class="title">
      <div>Panoramic View</div>
      <div class="legend">
        <div class="color-block" :style="{backgroundColor: color['A']}"></div>
        <div class="color-legend">A</div>
        <div class="color-block" :style="{backgroundColor: color['B']}"></div>
        <div class="color-legend">B</div>
        <div class="color-block" :style="{backgroundColor: color['C']}"></div>
        <div class="color-legend">C</div>
        <div class="color-block" :style="{backgroundColor: color['D']}"></div>
        <div class="color-legend">D</div>
        <div class="color-block" :style="{backgroundColor: color['E']}"></div>
        <div class="color-legend">E</div>
        <div class="color-block" :style="{backgroundColor: color['F']}"></div>
        <div class="color-legend">F</div>
        <div class="color-block" :style="{backgroundColor: color['G']}"></div>
        <div class="color-legend">G</div>
        <div class="color-block" :style="{backgroundColor: color['H']}"></div>
        <div class="color-legend">H</div>
        <div class="color-block" :style="{backgroundColor: color['Y']}"></div>
        <div class="color-legend">Y</div>
        </div>
      <div class="icon">
        <span :class="['iconfont', 'icon-fangdajing', {active: toolUsing === 1}]"
              @click="() => toolUsing = 1"></span>
        <span :class="['iconfont', 'icon-duibi', {active: toolUsing === 2}]"
              @click="() => toolUsing = 2"></span>
      </div>
    </div>
    <svg ref="graphRef" class="graph"></svg>
  </div>
</template>

<script setup>
  import {ref, onMounted} from 'vue';
  import * as d3 from 'd3';
  import {getMaxClass, generateAcronym, groupTalentFlow} from '../utils/utils'
  import eventBus from '../utils/eventbus';
  import talent_flow from '../assets/data/talent_flow.json'

  const lassoList = ["!j Incorporated", "(Shahram) Sean Malek", ".Decimal, Inc.", "01Click, L.L.C.", "061428 CORP.", "1-800 CONTACTS, INC.", "1-800 Concrete, Inc.", "1020, Inc.", "10Tales, Inc.", "10X GENOMICS, INC.", "12 Sigma Technologies", "12 Technologies, Inc.", "128 Technology, Inc.", "140 Proof, Inc.", "15 Seconds of Fame, Inc.", "168 Productions, LLC", "170 Systems Inc.", "1776 Media Network, Inc.", "1914 Holding Company", "1997 Irrevocable Trust for Gregory P. Benson", "19th Hole Cart LLC", "1Co, Inc.", "International Business Machines Corporation", "Raytheon Company", "Honeywell International Inc."]

  const graphRef = ref(null);
  let svg, maingroup, circles, texts, lines, donutGroup, donuts;
  let simulation;
  let MAXCOO;
  let onDrag = false, toolUsing = ref(1);
  const minOpacity = 0.1; 
  const color ={"A":'#ffadad', "B":'#ffd6a5', "C":'#fdffb6', "D":'#caffbf', "E":'#9bf6ff', "F":'#a0c4ff', "G":'#bdb2ff', "H":'#ffc6ff', "Y":'#cce3de'};

  const radius = d => Math.sqrt(Math.sqrt(d.total_patent_number))*10;
  const linkStrength = d => d.coo / 100;

  const clickEvent = (event, d) => {
    if(onDrag) return;
    if(toolUsing.value === 1){
      eventBus.emit('trend', d.name);
      eventBus.emit('flow', d.name);
    }
    if(toolUsing.value === 2){
      eventBus.emit('comparison', d.name);
    }
  }

  const mouseOverEvent = (event, data, d) => {
    if(onDrag) return;
    let t = d3.transition().duration(500)
    let relatedLinks = data.links.filter(l => l.source.name === d.name || l.target.name === d.name);
    relatedLinks = relatedLinks.map(l => l.source.name).concat(relatedLinks.map(l => l.target.name));
    relatedLinks = [...new Set(relatedLinks)]
    d3.selectAll('.links')
      .filter(l => l.source.name === d.name || l.target.name === d.name)
      .transition().duration(500).ease(d3.easeLinear)
      .attr('opacity', l => Math.pow(l.coo / MAXCOO, 2))
      .on('start', function repeat(){
        d3.select(this).attr('stroke-dashoffset', 0);
        d3.active(this).attr('stroke-dashoffset', l => l.coo * 4).transition().on('start', repeat);
      });
    d3.selectAll('.links')
      .filter(l => l.source.name != d.name && l.target.name != d.name)
      .transition(t)
      .attr('opacity', 0);
    d3.selectAll('.circles, .text, .donut-group')
      .filter(l => relatedLinks.includes(l.name) || d.name === l.name)
      .transition(t)
      .attr('opacity', 1);
    d3.selectAll('.circles')
      .filter(l => relatedLinks.includes(l.name) || d.name === l.name)
      .transition(t)
      .attr('fill', "#ebebeb");
    d3.selectAll('.circles, .text')
      .filter(l => !relatedLinks.includes(l.name) && d.name !== l.name)
      .transition(t)
      .attr('opacity', minOpacity);
    d3.selectAll('.donut-group')
      .filter(l => !relatedLinks.includes(l.name) && d.name !== l.name)
      .transition(t)
      .attr('opacity', 0);
  }

  const mouseOutEvent = (event, d) => {
    if(onDrag) return;
    let t = d3.transition().duration(500)
    d3.selectAll('.links, .donut-group')
      .transition(t)
      .attr('opacity', 0);
    d3.selectAll('.circles, .text')
      .transition(t)
      .attr('opacity', 1);
    d3.selectAll('.circles')
      .attr('fill', d => color[getMaxClass(d)]);
  }

  const init = (data) => {
    // 渲染连接线
    lines = maingroup.selectAll('.links').data(data.links).join('line')
      .attr('class', 'links')
      .attr('stroke', 'black')
      .attr('opacity', 0)
      .attr('stroke-width', 5)
      .attr('stroke-dasharray', d => d.coo * 2)
      .attr('stroke-dashoffset', 0);

    // 渲染节点
    circles = maingroup.selectAll('.circles').data(data.nodes).join('circle')
      .attr('class', 'circles')
      .attr('opacity', 1)
      .attr('r', radius)
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('fill', d => color[getMaxClass(d)])
      .on('mouseover', (event, d) => mouseOverEvent(event, data, d))
      .on('mouseout', (event, d) => mouseOutEvent(event, d))
      .on('click', (event, d) => clickEvent(event, d));

    // 渲染节点文本
    texts = maingroup.selectAll('.text').data(data.nodes).join('text')
      .attr('class', 'text')
      .attr('opacity', 1)
      .attr('x', d => d.x)
      .attr('y', d => d.y)
      // .attr('font-size', d => radius(d) > 50 ? radius(d) : 10)
      .attr('font-size', 12)
      .attr('text-anchor', 'middle')
      .attr('dy', 4)
      .attr("pointer-events", "none")
      .attr('fill', 'black')
      // .text(d => d.name);
      .text(d => generateAcronym(d.name));

    // 渲染节点外圈
    const getPath = (data)=>{
      const classData = Object.entries(data.class_ratio).map(([key, value]) => ({
        className: key,
        classRatio: value
      }))
      const pie = d3.pie().value(d => d.classRatio);
      const arcData = pie(classData);
      const arc = d3.arc().innerRadius(radius(data)).outerRadius(radius(data) + 10);

      return arcData.map((d, i) => ({
        path: arc(d),
        color: color[d.data.className]
      }));
    }

    donutGroup = maingroup.selectAll('.donut-group').data(data.nodes).join('g')
      .attr('class', 'donut-group')
      .attr('opacity', 0)
      .attr('transform', d => `translate(${d.x}, ${d.y})`)
      .lower();
      
    donuts = donutGroup.selectAll('.donut').data(d => getPath(d)) .join('path')
      .attr('class', 'donut')
      .attr('d', d => d.path) 
      .attr('fill', d => d.color);

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
    donutGroup
      .attr('transform', d => `translate(${d.x}, ${d.y})`);
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

    d3.json('organization_time_to2020.json').then(data => {

      let nodes = data.filter(d => lassoList.includes(d.organization_name))
      nodes = nodes.map(node => ({
        name: node.organization_name,
        total_patent_number: node.data.filter(d => d.time === 1998)[0].detail.total_patent_number,
        class_ratio: node.data.filter(d => d.time === 1998)[0].detail.CPC_ratio,
      }))

      let links = talent_flow.filter(d => d.change_date > '1998-10' && lassoList.includes(d.from) && lassoList.includes(d.to));
      links = groupTalentFlow(links);
      console.log(links)
      data = {
        nodes: nodes,
        links: links
      };

      MAXCOO = d3.max(data.links, d => d.coo);

      data.nodes.forEach(n => {
        n.x = svg.node().clientWidth / 2 + Math.random() * 10;
        n.y = svg.node().clientHeight / 2 + Math.random() * 10;
      });

      init(data);

      const forceNode = d3.forceManyBody()
        .strength(-30)
        .distanceMax(50);
      const forceLink = d3.forceLink(data.links)
        .id(d => d.name)
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

    .legend{
      display: flex;
      flex-direction: row;
      align-items: center;
      margin-top: 3px;
      .color-block{
        height: 15px;
        width: 15px;
        border-radius: 3px;
        border: 1px solid #8f8f8f;
        margin-left: 15px;
      }
      .color-legend{
        font: 15px "Noto-Sans-Italic";
        color: #333533;
        margin-left: 5px;
      }
    }

    .icon{
      .iconfont{
        font-size: 20px;
        margin-left: 10px;
      }
      .active{
        color: red;
      }
    }
  }

  .graph {
    flex-grow: 1;
  }
</style>
