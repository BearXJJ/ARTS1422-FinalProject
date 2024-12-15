<template>
  <div class="cluster-view">
    <div class="title">Cluster View</div>
  </div>
  <div class="attributeview-view">
    <div class="title">Attributes</div>

    <div style="font-size:8px" class="buttons">
      <label for="gender_ratio_button">Gender Ratio</label>
      <input type="checkbox" class="btn-check" id="gender_ratio_button" v-model="filters.gender_ratio">

      <label for="total_patent_button">Total Patent</label>
      <input type="checkbox" class="btn-check" id="total_patent_button" v-model="filters.total_patent">

      <label for="cited_per_peo_button">Cited per People</label>
      <input type="checkbox" class="btn-check" id="cited_per_peo_button" v-model="filters.cited_per_people">

      <label for="emerging_button">Emerging</label>
      <input type="checkbox" class="btn-check" id="emerging_button" v-model="filters.emerging">
    </div>

    <div style="font-size:8px" class="buttons">
      <label for="total_cited_button">Total Cited</label>
      <input type="checkbox" class="btn-check" id="total_cited_button" v-model="filters.total_cited">

      <label for="CPC_ratio_button">CPC Ratio</label>
      <input type="checkbox" class="btn-check" id="CPC_ratio_button" v-model="filters.cpc_ratio">

      <label for="cited_average_button">Cited Average</label>
      <input type="checkbox" class="btn-check" id="cited_average_button" v-model="filters.cited_average">

      <label for="inventor_count_button">Inventor Count</label>
      <input type="checkbox" class="btn-check" id="inventor_count_button" v-model="filters.inventor_count">
    </div>

    <div style="font-size:8px" class="date-range">
      <label for="small_button">Exclude</label>
      <input type="checkbox" class="btn-check" id="small_button" v-model="filters.small_exclude">

      <label for="start_year">Start</label>
      <select id="start_year" v-model="filters.start_year">
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>

      <label for="end_date">End</label>
      <input type="text" id="end_date" v-model="filters.end_year" disabled>
    </div>

    <div style="font-size:8px" class="dimensionality-reduction">
      <label>Dimensionality Reduction</label>
      <div class="radio-group">
        <input type="radio" id="option1" value="t-SNE" v-model="filters.reduction_method">
        <label for="option1">t-SNE</label>

        <input type="radio" id="option2" value="PCA" v-model="filters.reduction_method">
        <label for="option2">PCA</label>

        <input type="radio" id="option3" value="UMAP" v-model="filters.reduction_method">
        <label for="option3">UMAP</label>
      </div>
    </div>

    <div style="font-size:8px" class="button_down">
      <button @click="RunPage">Run page</button>
      <button @click="ClearPage">Clear page</button>
    </div>
  </div>

  <div class="reduction-view">
    <div class="title">Dimensionality Reduction</div>
    <div>
      <svg ref="scatterplot"></svg>
    </div>
  </div>

  <div class="transpose-view">
    <div class="title">Transpose</div>
  </div>
  <FlowTable></FlowTable>
</template>

<script setup>
import * as d3 from 'd3';
import {ref, watch, onMounted} from 'vue';
import axios from 'axios';
import eventBus from '../utils/eventbus';
import FlowTable from './FlowTable.vue';



const scatterplot = ref(null);

const filters = ref({
  gender_ratio: false,
  total_patent: false,
  cited_per_people: false,
  emerging: false,
  total_cited: false,
  cpc_ratio: false,
  cited_average: false,
  inventor_count: false,
  small_exclude: true,
  start_year: 1990,
  end_year: 2020,
  reduction_method: 't-SNE',
});

const years = Array.from({ length: 31 }, (_, i) => 1990 + i);

const RunPage = async () => {
  try {
    // const response = await axios.post('http://localhost:5000/run-filter', filters.value);
    // console.log(response);
    const data = await d3.csv('now.csv');

    data.forEach(d => {
      d.x = +d.x; 
      d.y = +d.y;
      d.id = d.organization_name;
    });

    drawReductionView(data);
  } catch (error) {
    console.error('Error running page:', error);
    alert('Failed to run the page.');
  }
};

const ClearPage = () => {
  location.reload();
  filters.value = {
    gender_ratio: false,
    total_patent: false,
    cited_per_people: false,
    emerging: false,
    total_cited: false,
    cpc_ratio: false,
    cited_average: false,
    inventor_count: false,
    small_exclude: true,
    start_year: 1990,
    end_year: 2020,
    reduction_method: 't-SNE',
  };
  
};

const drawReductionView = (data) => {
  const width = 300;
  const height = 150;
  const margin = { top: 0, right: 0, bottom: 0, left: 0 };

  const xExtent = d3.extent(data, d => d.x);
  const yExtent = d3.extent(data, d => d.y);
  const xBuffer = 0; 
  const yBuffer = 0; 

  const xScale = d3.scaleLinear()
                  .domain([xExtent[0] - xBuffer, xExtent[1] + xBuffer])
                  .range([margin.left, width - margin.right])
                  .nice();

  const yScale = d3.scaleLinear()
                  .domain([yExtent[0] - yBuffer, yExtent[1] + yBuffer])
                  .range([height - margin.bottom, margin.top])
                  .nice();

  const colorScale = d3.scaleOrdinal()
                      .domain([1])
                      .range(["orange"]);

  const svg = d3.select(scatterplot.value);

  const circles = svg.selectAll("circle")
    .data(data)
    .enter().append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 3)
    .attr("fill", d => colorScale(d.cluster));

  let lassoPath = [];
  let isLassoing = false;
  let selectedData = data.map(d => d.id);

  svg.on("mousedown", (event) => {
    isLassoing = true;
    lassoPath = [];
    const [x, y] = d3.pointer(event);
    lassoPath.push({ x, y });
    svg.append("path")
    .attr("class", "lasso-path")
    .attr("stroke", "gray")
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", "4 4")
    .attr("fill", "none");
  });

  // 绘制套索
  svg.on("mousemove", (event) => {
    if (!isLassoing) return;
    const [x, y] = d3.pointer(event);
    lassoPath.push({ x, y });
    svg.select(".lasso-path")
      .attr("d", d3.line().x(d => d.x).y(d => d.y)(lassoPath));
  });

  svg.on("mouseup", () => {
    if (!isLassoing) return;
    isLassoing = false;
    svg.select(".lasso-path")
      .attr("d", d3.line()
        .x(d => d.x)
        .y(d => d.y)([...lassoPath, lassoPath[0]]));
    // 检查路径内部的数据点
    selectedData = data.filter(d => isInsideLasso(d));

    selectedData = selectedData.map(d => d.id);
    svg.select(".lasso-path").remove();
    lassoPath = [];

    console.log(selectedData)

    eventBus.emit('lassoList', selectedData);
    eventBus.emit('year', filters.value.start_year);

  });

  // 判断点是否在套索路径内
  const isInsideLasso = (point)=>{
    let isInside = false;
    let n = lassoPath.length;
    for (let i = 0, j = n - 1; i < n; j = i++) {
      const xi = lassoPath[i].x, yi = lassoPath[i].y;
      const xj = lassoPath[j].x, yj = lassoPath[j].y;
      const intersect = ((yi > yScale(point.y)) !== (yj > yScale(point.y))) &&
        (xScale(point.x) < (xj - xi) * (yScale(point.y) - yi) / (yj - yi) + xi);
      if (intersect) isInside = !isInside;
    }
    return isInside;
  }
}

</script>

<style lang="less" scoped>
  .date-range {
    display: flex;
    align-items: center;
    gap: 10px; 

    select, input[type="text"] {
      padding: 5px; 
      width: 60px; 
      height: auto; 
      border: 1px solid #ccc; 
      border-radius: 2px; 
      background-color: #f9f9f9;  
    }

    input[type="text"][disabled] {
    }
  }
  .title {
    height: 30px;
    line-height: 30px;
    border-bottom: 0.5px solid rgb(179, 179, 179);
  }
  .cluster-view {
    display: flex;
    flex-direction: column;
    padding: 0px 5px;
  }
  .attributeview-view {
    width: 100%;
    height: 25%;
    position: relative;
  }
  .svg-container {
    width: 100%;
    height: 25%;
    position: relative;
  }
  .radio-group {
    display: flex;
    align-items: center;
    gap: 10px; 
  }
  .radio-group label {
    margin: 0; 
  }
  input[type="radio"] {
    margin-right: 5px;  
  }

  


</style>
