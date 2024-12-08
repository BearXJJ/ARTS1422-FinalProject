<template>
  <div class="cluster-view">
    <div class="title">Cluster View</div>
  </div>
  <div class="attributeview-view">
    <div class="title">Attributes</div>
    <div class="gender_ratio_select-options">
      <div class="dropdown">
        <label for="gender_ratio_select-select">gender ratio</label>
        <select id="gender_ratio_select-select" v-model="gender_ratio_selectedFilter">
          <option value="filtera1">0<= Male < 25%</option>
          <option value="filtera2">25% <= Male < 50%</option>
          <option value="filtera3">50% <= Male < 75%</option>
          <option value="filtera4">75% <= Male <= 100%</option>
        </select>
      </div>
    </div>
    <div class="total_patent-options">
      <div class="dropdown">
        <label for="total_patent-select">total patent</label>
        <select id="total_patent-select" v-model="total_patent_selectedFilter">
          <option value="filterb1">1 <= total < 10</option>
          <option value="filterb2">10 <= total < 1000</option>
          <option value="filterb3">1000 <= total < 10000</option>
          <option value="filterb4">10000 <= total </option>
        </select>
      </div>
    </div>
    <div class="CPC_ratio-options">
      <div class="dropdown">
        <label for="CPC_ratio_select-select">CPC ratio</label>
        <select id="CPC_ratio_select-select" v-model="CPC_ratio_selectedFilter">
          <option value="filterc1">A</option>
          <option value="filterc2">B</option>
          <option value="filterc3">C</option>
          <option value="filterc4">D</option>
          <option value="filterc5">E</option>
          <option value="filterc6">F</option>
          <option value="filterc7">F</option>
          <option value="filterc8">G</option>
          <option value="filterc9">H</option>
        </select>
      </div>
    </div>
    <div class="emerging-options">
      <div class="dropdown">
        <label for="emerging-select">emerging</label>
        <select id="emerging-select" v-model="emerging_selectedFilter">
          <option value="filtere1">before 1990</option>
          <option value="filtere2">1990~1999</option>
          <option value="filtere3">2000~2009</option>
          <option value="filtere4">2010~2019</option>
          <option value="filtere5">after 2019</option>
        </select>
      </div>
    </div>
    <div class="total_cited-options">
      <div class="dropdown">
        <label for="total_cited-select">total cited</label>
        <select id="total_cited-select" v-model="total_cited_selectedFilter">
          <option value="filterd1">1 <= total < 10</option>
          <option value="filterd2">10 <= total < 1000</option>
          <option value="filterd3">1000 <= total < 10000</option>
          <option value="filterd4">10000 <= total </option>
        </select>
      </div>
    </div>
    <div class="cited_per_peo-options">
      <div class="dropdown">
        <label for="cited_per_peo-select">cited per people</label>
        <select id="cited_per_peo-select" v-model="cited_per_peo_selectedFilter">
          <option value="filterf1">1 <= total < 10</option>
          <option value="filterf2">10 <= total < 1000</option>
          <option value="filterf3">1000 <= total < 10000</option>
          <option value="filterf4">10000 <= total </option>
        </select>
      </div>
    </div>    
    <div class="cited_average-options">
      <div class="dropdown">
        <label for="cited_average-select">average cited</label>
        <select id="cited_average-select" v-model="cited_average_selectedFilter">
          <option value="filterg1">1 <= total < 10</option>
          <option value="filterg2">10 <= total < 1000</option>
          <option value="filterg3">1000 <= total < 10000</option>
          <option value="filterg4">10000 <= total </option>
        </select>
      </div>
    </div>   
    <div class="inventor_count-options">
      <div class="dropdown">
        <label for="inventor_count-select">inventor count</label>
        <select id="inventor_count-select" v-model="inventor_count_selectedFilter">
          <option value="filterh1">1 <= total < 10</option>
          <option value="filterh2">10 <= total < 1000</option>
          <option value="filterh3">1000 <= total < 10000</option>
          <option value="filterh4">10000 <= total </option>
        </select>
      </div>
    </div>    
    <div class="date-range">
      <label for="start_date">Start Date:</label>
      <input type="date" id="start_date" v-model="startDate" min="1990-01-01" max="2000-12-31">

      <label for="end_date">End Date:</label>
      <input type="date" id="end_date" v-model="endDate" min="1990-01-01" max="2000-12-31">
    </div>
    <div class="dimensionality-reduction">
      <label>Dimensionality Reduction</label>
      <div class="radio-group">
        <input type="radio" id="option1" value="t-SNE" v-model="selectedOption">
        <label for="option1">t-SNE</label>

        <input type="radio" id="option2" value="PCA" v-model="selectedOption">
        <label for="option2">PCA</label>

        <input type="radio" id="option3" value="UMAP" v-model="selectedOption">
        <label for="option3">UMAP</label>
      </div>
    </div>
    <div class="buttons">
      <label for="run_button">Run Button</label>
      <input @click="RunPage" type="checkbox" class="btn-check" id="run_button" v-model="runButton">

      <label for="clear_button">Clear Button</label>
      <input @click="ClearPage" type="checkbox" class="btn-check" id="clear_button" v-model="clearButton">
    </div>
  </div>

  <div class="reduction-view">
    <div class="title">Dimensionality Reduction</div>
    <div>
      <canvas ref="dotGridCanvas" width="450" height="300"></canvas>
    </div>
  </div>

  <div class="transpose-view">
    <div class="title">Transpose</div>
  </div>
</template>

<script setup>
import {ref, watch, onMounted} from 'vue';

const gender_ratio_selectedFilter = ref(null);
const total_patent_selectedFilter = ref(null);
const CPC_ratio_selectedFilter = ref(null);
const total_cited_selectedFilter = ref(null);
const emerging_selectedFilter = ref(null);
const cited_per_peo_selectedFilter = ref(null);
const cited_average_selectedFilter = ref(null);
const inventor_count_selectedFilter = ref(null);
const startDate = ref(null);
const endDate = ref(null);
const selectedOption = ref(null);
const runButton = ref(null);
const clearButton = ref(null);

watch(gender_ratio_selectedFilter, (newDt, oldDt) => {
  console.log('Gender ratio Changed:', newDt, oldDt);
});
watch(total_patent_selectedFilter, (newDt, oldDt) => {
  console.log('Total patent Changed:', newDt, oldDt);
});
watch(CPC_ratio_selectedFilter, (newDt, oldDt) => {
  console.log('CPC ratio Changed:', newDt, oldDt);
});
watch(total_cited_selectedFilter, (newDt, oldDt) => {
  console.log('total cited Changed:', newDt, oldDt);
});
watch(emerging_selectedFilter, (newDt, oldDt) => {
  console.log('Emerging Changed:', newDt, oldDt);
});
watch(cited_per_peo_selectedFilter, (newDt, oldDt) => {
  console.log('Cited per people Changed:', newDt, oldDt);
});
watch(cited_average_selectedFilter, (newDt, oldDt) => {
  console.log('Average Cited Changed:', newDt, oldDt);
});
watch(inventor_count_selectedFilter, (newDt, oldDt) => {
  console.log('Inventor count Changed:', newDt, oldDt);
});
watch(startDate, (newDt, oldDt) => {
  console.log('Start Date Changed:', newDt, oldDt);
});
watch(endDate, (newDt, oldDt) => {
  console.log('End Date Changed:', newDt, oldDt);
});

const handleOptionChange = (newOption) => {
  console.log('Selected option:', newOption);
};
watch(selectedOption, (newDt, oldDt) => {
  console.log('select Changed:', newDt, oldDt);
});

watch(runButton, (newDt, oldDt) => {
  console.log('Run Button Changed:', newDt, oldDt);
});
watch(clearButton, (newDt, oldDt) => {
  console.log('Clear Button Changed:', newDt, oldDt);
});

function RunPage(event){

}

function ClearPage(event) {
  event.preventDefault();
  clearButton.value = true;
  window.location.reload();
}

const dotGridCanvas = ref(null);

onMounted(() => {
  const ctx = dotGridCanvas.value.getContext('2d');
  const cellSize = 20; // 网格单元的大小
  const gridWidth = Math.floor(dotGridCanvas.value.width / cellSize);
  const gridHeight = Math.floor(dotGridCanvas.value.height / cellSize);

  // 绘制网格背景
  for (let x = 0; x <= gridWidth; x++) {
    ctx.moveTo(x * cellSize, 0);
    ctx.lineTo(x * cellSize, dotGridCanvas.value.height);
  }
  for (let y = 0; y <= gridHeight; y++) {
    ctx.moveTo(0, y * cellSize);
    ctx.lineTo(dotGridCanvas.value.width, y * cellSize);
  }
  ctx.strokeStyle = '#eee';
  ctx.stroke();

  // 绘制点
  ctx.fillStyle = '#333';
  for (let x = 0; x < gridWidth; x++) {
    for (let y = 0; y < gridHeight; y++) {
      // 这里可以根据需要决定是否绘制点
      ctx.beginPath();
      ctx.arc(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2, 5, 0, 2 * Math.PI);
      ctx.fill();
    }
  }
});
</script>

<style lang="less" scoped>
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
    display: flex;
    flex-direction: column;
    padding: 0px 5px;
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

  .buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px; 
    padding: 10px;
  }
  .btn-check {
    accent-color: #007BFF;
    transform: scale(1.5); 
    cursor: pointer;
  }
  label {
    cursor: pointer; 
  }
  
  .reduction-view {
    display: flex;
    flex-direction: column;  /* 垂直布局 */
    padding: 0px 5px;
  }


  .transpose-view {
    display: flex;
    flex-direction: column;  /* 垂直布局 */
    padding: 0px 5px;
  }

</style>
