<template>
  <div class="cluster-view">
    <div class="title">Cluster View</div>
  </div>
  <div class="attributeview-view">
    
    <div class="buttons">
      <div class = "button_type">
        <label for="gender_ratio_button">Gender Ratio</label>
        <input type="checkbox" class="btn-check" id="gender_ratio_button" v-model="filters.gender_ratio">
      </div>

      <div class = "button_type">
        <label for="total_patent_button">Total Patent</label>
        <input type="checkbox" class="btn-check" id="total_patent_button" v-model="filters.total_patent">
      </div>
    </div>
    <div class="buttons">
      <div class = "button_type">
        <label for="cited_per_peo_button">Cited per People</label>
        <input type="checkbox" class="btn-check" id="cited_per_peo_button" v-model="filters.cited_per_people">
      </div>

      <div class = "button_type">
        <label for="emerging_button">Emerging</label>
        <input type="checkbox" class="btn-check" id="emerging_button" v-model="filters.emerging">
      </div>
    </div>

    <div class="buttons">
      <div class = "button_type">
        <label for="total_cited_button">Total Cited</label>
        <input type="checkbox" class="btn-check" id="total_cited_button" v-model="filters.total_cited">
      </div>

      <div class = "button_type">
        <label for="CPC_ratio_button">CPC Ratio</label>
        <input type="checkbox" class="btn-check" id="CPC_ratio_button" v-model="filters.cpc_ratio">
      </div>
    </div>
    <div class="buttons">
      <div class = "button_type">
        <label for="cited_average_button">Cited Average</label>
        <input type="checkbox" class="btn-check" id="cited_average_button" v-model="filters.cited_average">
      </div>

      <div class = "button_type">
        <label for="inventor_count_button">Inventor Count</label>
        <input type="checkbox" class="btn-check" id="inventor_count_button" v-model="filters.inventor_count">
      </div>
    </div>
    <div class="buttons">
      <div class = "button_exclude">
        <label for="small_button">Exclude Small Corporation</label>
        <input type="checkbox" class="btn-check" id="small_button" v-model="filters.small_exclude">
      </div>
    </div>

    <div class="time_range">
      <div class = "button_type">
        <label for="start_year">Start</label>
        <select id="start_year" class = "input_win" v-model="filters.start_year">
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

      <div class = "button_type">
        <label for="end_date">End</label>
        <input type="text" class = "input_win" id="end_date" v-model="filters.end_year" disabled>
      </div>
    </div>

    <div class="dimensionality-reduction">
      <label style="font-weight: 600;">Dimensionality Reduction</label>
      <div class="dim_ele">
        <div class = "button_dim">
          <input class = 'select_dim' type="radio" id="option1" value="t-SNE" v-model="filters.reduction_method">
          <label class = "select_text" for="option1">t-SNE</label>
        </div>

        <div class = "button_dim">
          <input class = 'select_dim' type="radio" id="option2" value="PCA" v-model="filters.reduction_method">
          <label class = "select_text" for="option2">PCA</label>
        </div>

        <div class = "button_dim">
          <input class = 'select_dim' type="radio" id="option3" value="UMAP" v-model="filters.reduction_method">
          <label class = "select_text" for="option3">UMAP</label>
        </div>
      </div>
    </div>

    <div class="button_down">
      <div class="button_type">
        <el-button style= "height:20px; margin-left: 30px;" @click="RunPage">Run</el-button>
      </div>
      <div class="button_type">
        <el-button style= "height:20px; margin-left: 30px;" @click="ClearPage">Clear</el-button>
      </div>
    </div>
  </div>

  <div class="reduction-view">
    <div class="title"></div>
    <div class = "svg_c" >
      <svg ref="scatterplot"></svg>
    </div>
  </div>

  <div class="transpose-view">
    <div class="title"></div>
    <FlowTable></FlowTable>
  </div>
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
    const response = await axios.post('http://localhost:3000/run-filter', filters.value);
    console.log(response);
    const data = await d3.csv('now.csv');
    console.log("Loaded Data:", data);

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
  const width = 420;
  const height = 280;
 
  const margin = { top: 0, right: 0, bottom: 0, left: 0 };

  const xExtent = d3.extent(data, d => d.x);
  const yExtent = d3.extent(data, d => d.y);

  const xScale = d3.scaleLinear()
    .domain([xExtent[0], xExtent[1]])
    .range([0, width-5])
    .nice();

  const yScale = d3.scaleLinear()
    .domain([yExtent[0], yExtent[1]])
    .range([height-5, 0])
    .nice();

  const colorScale = d3.scaleOrdinal()
    .domain([1])
    .range(["orange"]);

  const svg = d3.select(scatterplot.value);

  svg
  .attr('height', height)
  .attr('width', width);

  const circles = svg.selectAll("circle")
    .data(data)
    .enter().append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 2)
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
    selectedData = data.filter(d => isInsideLasso(d));
    // selectedData = (selectedData.length===0)? data : selectedData;
    console.log(selectedData);
    selectedData = selectedData.map(d => d.id);
    console.log(selectedData);
    eventBus.emit('lassoList', selectedData);
    eventBus.emit('year', filters.value.start_year);
    svg.select(".lasso-path").remove();
    lassoPath = [];
  });

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

<style lang = "less" scoped>
  .title {
    height: 30px;
    line-height: 30px;
    border-bottom: 2px solid rgb(179, 179, 179);
  }
  .cluster-view {
    display: flex;
    flex-direction: column;
    padding: 0px 5px;
  }
  .attributeview-view {
    width: 100%;
    height: 25%;
    font-size: 22px;
    .dimensionality-reduction{
      font-size:12px;
      // font-weight:bold;
      margin-left:11px;
      margin-top: 5px;
    }
    .dim_ele{
      // transform: translateY(5px);
      margin-top: 10px;
    }
    .buttons{
      height:12%;
      align-items:flex-end;
    }
    .button_type{
      font-size:12px;
      display: inline-block;
      width: 45%;
      height: 25px;
      line-height: 20px;
      margin-left:10px;
      transform:translateY(3px)
    }
    
    .btn-check{
      margin-left:5px;
      transform:translateY(3px)
    }
    .input_win{
      text-align:center;
      margin-left:5px;
      width: 40%;
    }
    .button_exclude{
      font-size:12px;
      width: 90%;
      height: 20px;
      margin-left:10px;
      margin-top:8px;
      transform:translateY(3px)
    }
    .time_range{
      transform: translateY(-5px);
      height: 30px;
    }
    .button_dim{
      width:30%;
      height:10%;
      font-size:12px;
      display: inline-block;
      margin-left:10px;

    }
    .select_dim{
      margin-right:2px;
      transform: translateY(2px);
    }
    .button_down{
      margin-left: 15px;
    }
    .button_t3{
      display: inline-block;
      width: 170px;
      height: 35px;
      line-height: 35px;
    }
  }
  .reduction-view {
    width: 100%;
    height: 30%;
    .svg_c{
      width: 100%;
      height: 100%;
    }
    .svg{
      width: 100%;
      height: 100%;
    }
  }
  .transpose-view{
    width: 100%;
    height: 25%;
  }
  


</style>
