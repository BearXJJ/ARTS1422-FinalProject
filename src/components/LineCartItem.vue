<template>
  <svg ref="graphRef" class="line-cart-item"></svg>
</template>

<script setup>
  import {ref, onMounted} from 'vue';
  import * as d3 from 'd3';
  const props = defineProps({
    name: {
      type: String,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  });


  const graphRef = ref(null);
  let svg, mainGroup, text, lineCart;

  const data = props.data;
  onMounted(() => {
    svg = d3.select(graphRef.value);
    const innerWidth = svg.node().clientWidth;
    const cartWidth = innerWidth - 200;
    const innerHeight = svg.node().clientHeight;
    svg.attr('viewBox', `0 0 ${innerWidth} ${innerHeight+1}`);

    mainGroup = svg.append('g');

    text = mainGroup.append('text')
      .attr('id', 'text')
      .attr('x', 190) 
      .attr('y', innerHeight / 2 + 8)
      .attr('width', 200)
      .attr('text-anchor', 'end')
      .text(`${props.name}`)
      .style('font-size', '16px')
      .style('fill', 'black');

    lineCart = mainGroup.append('g')
      .attr('id', 'lineCart')
      .attr('transform', `translate(200, 0)`);
    
    const xScale = d3.scaleTime()
      .domain(d3.extent(data.map(d => d.time)))
      .range([0, cartWidth])
      .nice();
    const yScale = d3.scaleLinear()
      .domain(d3.extent(data.map(d => d.value)))
      .range([innerHeight, 0])
      .nice();
    const xAxis = d3.axisBottom(xScale).tickSize(0).ticks(0);
    lineCart.append('g')
      .attr('id', 'xAxisGroup')
      .call(xAxis)
      .attr('transform', `translate(0, ${innerHeight})`);
    const line = d3.line()
      .x(d => xScale(d.time))
      .y(d => yScale(d.value))
      .curve(d3.curveBasis);
    lineCart.append('path').datum(data)
      .attr('fill', 'none')
      .attr('d', line)
      .attr('stroke', '#0086FF')
      .attr('stroke-width', '2px');
  
  })

</script>

<style lang="less" scoped>

</style>
