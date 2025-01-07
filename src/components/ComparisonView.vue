<template>
  <div class="comparison-view">
    <div class="title">Comparison View</div>
    <el-scrollbar class="scrollbar">
      <div class="scrollbar-flex-content">
        <div 
         v-for="(item, index) in displayedCompanies " 
         :key="index" 
         class="scrollbar-item"
         :style="{ backgroundColor: color(index) }"
        >
          <span class="item-text">{{ item }}</span>
          <button @click="removeCompany(index)" class="remove-button">
            <i class="fas fa-times"></i> 
          </button>
        </div>
      </div>
    </el-scrollbar>
    <svg ref="graphRef" class="graph"></svg>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount} from 'vue';
import * as d3 from 'd3';
import eventBus from '../utils/eventbus';

const graphRef = ref(null);
// 选中的org
const displayedCompanies = ref([]);

// 固定年份
const year = 1989;
const cpcKeys = ["A","B","E","F","G","H","Y"];
const color_2 ={"A":'#ffadad', "B":'#ffd6a5', "C":'#fdffb6', "D":'#caffbf', "E":'#9bf6ff', "F":'#a0c4ff', "G":'#bdb2ff', "H":'#ffc6ff', "Y":'#cce3de'};

const Selected_list = ref([]);

let svg, g, yScale, xScale, ySubgroup, customColors, color, tooltip;
let width, height, margin, innerWidth, innerHeight;
let orgs, filteredOrgs;

orgs = d3.json('../../public/organization_time_to2020.json');
// console.log(orgs)

// 监听事件，当公司被选中时
eventBus.on('comparison', (companyName) => {
  // console.log(companyName);
  if (!displayedCompanies.value.includes(companyName)) {
    if (displayedCompanies.value.length < 3) {
      displayedCompanies.value.push(companyName);
      updateChart();
    } else {
      console.warn('已选择3家公司，无法再添加更多。');
    }
  }
  // console.log('Updated displayedCompanies:', displayedCompanies.value);
})

// bus.on
// orgs = await d3.json('../../public/organization_time_to2020.json');
// filteredOrgs = orgs.filter(d => Selected_list.includes(d.organization_name));

// 按钮 删除函数
function removeCompany(index) {
  displayedCompanies.value.splice(index, 1);
  updateChart();
  // console.log('Updated displayedCompanies:', displayedCompanies.value);
}

// 初始化
onMounted(async () => {
  svg = d3.select(graphRef.value);
  width = svg.node().clientWidth;
  height = svg.node().clientHeight;
  margin = { top: 0, right: 0, bottom: 0, left: 0 };
  innerWidth = width - margin.left - margin.right;
  innerHeight = height - margin.top - margin.bottom;

  g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // 创建tooltip
  tooltip = d3.select('body')
    .append('div')
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('opacity', 0)
    .style('background', '#fff')
    .style('border', '1px solid #ccc')
    .style('padding', '5px')
    .style('border-radius', '4px')
    .style('font-size','12px');

  // 定义颜色比例尺
  // 修改了前3个
  customColors = ['#ffd6a5','#a0c4ff', '#ffc6ff', '#caffbf', '#FF33FF', '#FF6F33', '#33FFFF', '#FF3399', '#3399FF', '#FF6633'];
  color = d3.scaleOrdinal(customColors);
  // color = d3.scaleOrdinal(d3.schemeCategory10);
});

async function updateChart(){
  if (displayedCompanies.value.length === 0) {
    // 没有公司，清空图表
    g.selectAll('.metricGroup').remove();
    // g.selectAll('.metricGroup').remove(text.metric-label);
    return;
  }

  // 获取数据
  const metrics_original = await fetchAndTransformData(displayedCompanies.value);
  // if (metrics_original.length === 0) {
  //   g.selectAll('.metricGroup').remove();
  //   return;
  // }

  // 数据处理
  const metrics_processed = metrics_original.map(d => {
    if (d.metric === 'emerging') {
      d.values = d.values.map(val => {
        const yearVal = parseInt(val.toString().split('-')[0], 10) || 0;
        return yearVal - 1979;
      });
      // 对emerging再做归一化
      const maxVal = d3.max(d.values);
      if (maxVal > 0) {
        d.values = d.values.map(v => v / maxVal);
      }
    } else if (d.metric !== 'class_ratio') {
      // 对普通metric归一化
      d.values = d.values.map(val => +val);
      const maxVal = d3.max(d.values);
      if (maxVal > 0) {
        d.values = d.values.map(v => v / maxVal);
      }
    } 
    // 对class_ratio不做归一化，它们已经是比例。
    return d;
  });

  // 确定尺度
  const maxVal = d3.max(metrics_processed.flatMap(d => d.values)) || 0;
  // const maxVal = d3.max(metrics_processed.flatMap(d => d.metric === 'CPC_distribution' 
  // ? d.values.flatMap(v => v)  // 所有分类值对比 
  // : d.values
  // )) || 0;

  xScale = d3.scaleLinear()
    .domain([0, maxVal])
    .range([0, innerWidth]);

  yScale = d3.scaleBand()
    .domain(metrics_processed.map(d => d.metric))
    .range([0, innerHeight])
    .padding(0.5);

  // 根据公司数量动态创建子分组尺度
  ySubgroup = d3.scaleBand()
    .domain(d3.range(displayedCompanies.value.length)) // 0到公司数量-1的数组
    .range([0, yScale.bandwidth()])
    .padding(0.05);

  // 数据绑定
  const metricGroups = g.selectAll('.metricGroup')
    .data(metrics_processed, d => d.metric);

  // 进入选择集
  // 使用join保持图形元素并对更新进行动画处理
  const metricGroupsEnter = metricGroups.enter()
    .append('g')
    .attr('class', 'metricGroup')
    .attr('transform', d => `translate(0,${yScale(d.metric)})`);

  metricGroupsEnter.append('text')
    .attr('class','metric-label')
    .attr('font-size','10px')
    .attr('x', xScale(0))
    .attr('y', -1)
    .attr('text-anchor', 'left');

  // update + enter合并，并对transform动画
  const metricGroupsMerged = metricGroups.merge(metricGroupsEnter)
    .transition()
    .duration(0)
    .attr('transform', d => `translate(0,${yScale(d.metric)})`);

  metricGroups.exit().remove();

  // 更新metric-label文本
  metricGroupsMerged.select('.metric-label')
    .text(d => {
      const formattedText = d.metric.replace(/_/g, ' ');
      return formattedText.charAt(0).toUpperCase() + formattedText.slice(1);
      });

  // 对每个metric绘制rect或stack
  metricGroupsMerged.on('end', function(d) {
    const metricGroup = d3.select(this);

    if (d.metric === 'class_ratio') {
      // 堆叠数据
      const stack = d3.stack().keys(d3.range(cpcKeys.length));
      const stackedInput = d.values.map((arr) => {
        const obj = {};
        arr.forEach((val, idx) => {
          obj[idx] = val;
        });
        return obj;
      });
      const stackedData = stack(stackedInput);

      // 公司group
      const companiesGroup = metricGroup.selectAll('g.companyGroup')
        .data(d.values, (dd, i) => i);

      const companiesGroupEnter = companiesGroup.enter()
        .append('g')
        .attr('class', 'companyGroup')
        .attr('transform', (dd,i) => `translate(0,${ySubgroup(i)})`);

      const companiesGroupMerged = companiesGroup.merge(companiesGroupEnter)
        .transition()
        .duration(0)
        .attr('transform', (dd,i) => `translate(0,${ySubgroup(i)})`);

      companiesGroup.exit().transition().duration(0).remove();

      // 对每个公司绘制堆叠段
      companiesGroupMerged.on('end', function(companyData, companyIndex){
        const companyG = d3.select(this);
        const companyLayers = stackedData.map(layer => layer[companyIndex]);

        const segments = companyG.selectAll('rect.cpc-segment')
            // .data(companyLayers)
            .data(companyLayers.map((layerValue, i) => {
             return {value: layerValue, cpcIndex: i}; 
            }), d => d.cpcIndex);

        const segmentsEnter = segments.enter()
          .append('rect')
          .attr('class','cpc-segment')
          .attr('y',0)
          // .attr('x', seg => xScale(seg[0]))
          .attr('x', seg => xScale(seg.value[0]))
          .attr('height', ySubgroup.bandwidth())
          .attr('width',0) // 初始width为0, 动画中展开
          // .attr('fill', (seg, idx) => color(idx))
          .attr('fill', (seg) => {
            // console.log('cpc',cpcKeys[seg.cpcIndex])
            return color_2[cpcKeys[seg.cpcIndex]]
          })
          // .attr('fill', (seg) => color_2[cpcKeys[seg.cpcIndex]])

          .on('mouseover', function(event, seg){
            const cpcIndex = seg.cpcIndex;
            const cpcKey = cpcKeys[cpcIndex];
            const originalValue = d.originalValues[companyIndex][cpcIndex];
            const name = displayedCompanies.value[companyIndex];
            // console.log('name', name)

          //   const originalValue = d.originalValues[companyIndex][cpcIndex];
          //   const cpcKey = cpcKeys[seg.idx];
          //   const name = displayedCompanies.value[companyIndex];

          //   // 高亮同一公司
          //   // companyG.selectAll('rect').attr('opacity', 0.6);
          //   // d3.select(this).attr('opacity',1);

            tooltip
              .style('opacity', 0.8)
              .html(`<strong>【${d.metric.replace(/_/g, ' ').charAt(0).toUpperCase() + d.metric.replace(/_/g, ' ').slice(1)}】</strong><br/>
                    Company: ${name}<br/>
                    Class: ${cpcKey}<br/>
                    Proportion: ${originalValue}`)
              .style('left', (event.pageX - 120) + 'px')
              .style('top', (event.pageY - 80) + 'px');
          })
          .on('mousemove', function(event) {
            tooltip
              .style('left', (event.pageX - 120) + 'px')
              .style('top', (event.pageY - 80) + 'px');
          })
          .on('mouseout', function() {
            companyG.selectAll('rect').attr('opacity', 1);
            // tooltip.style('opacity', 0);
            tooltip.style('left', (event.pageX - 20000) + 'px');
            tooltip.style('top', (event.pageY + 20000) + 'px');

          });

        // update + enter
        segmentsEnter.merge(segments)
          .transition()
          .duration(1000)
          .attr('x', seg => xScale(seg.value[0]))
          .attr('width', seg => xScale(seg.value[1]) - xScale(seg.value[0]))
          .attr('height', ySubgroup.bandwidth());


        segments.exit().transition().duration(500).attr('width',0).remove();
      });

    } else {
      // 普通metric
      const bars = metricGroup.selectAll('rect.bar')
        .data(d.values.map((val,i) => ({val, metric:d.metric, idx:i})), d => d.idx);

      const barsEnter = bars.enter()
        .append('rect')
        .attr('class','bar')
        .attr('y', d => ySubgroup(d.idx))
        .attr('x', xScale(0))
        .attr('width',0)
        .attr('height', ySubgroup.bandwidth())
        // .attr('fill', (dd,i) => color(i))
        .attr('fill', (dd,i) => color(i))
        .on('mouseover', function(event, dd) {
          const idx = dd.idx;
          g.selectAll('.bar').attr('opacity', data => data && data.idx===idx ? 1 : 0.6);

          const originalData = metrics_original.find(m => m.metric === dd.metric);
          const originalValue = originalData.originalValues[dd.idx];
          const name = displayedCompanies.value[dd.idx];

          tooltip
            .style('opacity', 0.8)
            .html(`<strong >【${dd.metric.replace(/_/g, ' ').charAt(0).toUpperCase() + d.metric.replace(/_/g, ' ').slice(1)}】</strong>
              <br/>Organization: ${name}
              <br/>Value: ${originalValue}`)
            .style('left', (event.pageX - 160) + 'px')
            .style('top', (event.pageY - 65) + 'px');
        })
        .on('mousemove', function(event) {
          tooltip.style('left', (event.pageX - 160) + 'px')
                 .style('top', (event.pageY - 65) + 'px');
        })
        .on('mouseout', function() {
          g.selectAll('.bar').attr('opacity', 1);
          // tooltip.style('opacity', 0);
          tooltip.style('left', (event.pageX - 20000) + 'px')
                 .style('top', (event.pageY + 20000) + 'px');
        });

      barsEnter.merge(bars)
        .transition()
        .duration(1000)
        .attr('width', dd => xScale(dd.val))
        .attr('y', d => ySubgroup(d.idx))
        .attr('height', ySubgroup.bandwidth());

      bars.exit().transition().duration(500)
        .attr('width',0)
        .remove();
    }
  });
}

// 获取整合organization数据
async function fetchAndTransformData(companyNames) {
  // if(!filteredOrgs){
  //  orgs = await d3.json('../../public/organization_time_to2020.json');
   const data = await orgs;
   filteredOrgs = data.filter(d => Selected_list.value.includes(d.organization_name));
  // }
  // const orgs = await d3.json('../../year-test.json');

  // 过滤 orgs 数据，仅保留在 Selected 中的公司
  // 对每家公司获取detailA(或B、C...)，再整合
  // 首先获取所有公司数据对象
  // const companiesData = companyNames.map(name => orgs.find(d => d.organization_name === name));
  const companiesData = companyNames.map(name => filteredOrgs.find(d => d.organization_name === name));


  // 检查是否有公司不存在数据
  if (companiesData.some(c => !c)) {
    console.error('无法在数据中找到某些公司。');
    return [];
  }

  // 获取metric列表
  const metricsList = [
    'total_patent_number','total_cited_number','inventor_count','average_cited',
    'cited_per_people','emerging','gender_ratio','class_ratio'
  ];
  
    // const metricsList = [
    //   'class_ratio', 'total_patent_number','total_cited_number','inventor_count','average_cited',
    //   'cited_per_people','emerging','gender_ratio'
    // ];

  function getDetailByYear(company, year) {
    const record = company.data.find(d => d.time === year);
    // return record.detail
    return record ? record.detail : null;
  }

  // 获取所有公司的detail数据
  const details = companiesData.map(c => getDetailByYear(c, year));
  if (details.some(d => !d)) {
    console.error('指定年份的数据在其中一个公司中不存在。');
    return [];
  }

  // 构造最终数据结构
  // { metric: 'total_patent_number', values: [comp1Val, comp2Val,...], originalValues: [...] }
  const transformed = metricsList.map(metric => {
      if (metric === 'class_ratio') {
        const companyCPC = details.map(detail => cpcKeys.map(k => detail.CPC_ratio?.[k] ?? 0));
        return {
          metric: 'class_ratio',
          values: companyCPC,
          originalValues: companyCPC.map(arr => [...arr]) // 复制一份用于tooltip显示原值
        };
      } else {
        const values = details.map(detail => detail[metric]);
        return { metric, values: [...values], originalValues: [...values] };
      }
  });
  // console.log("metric:",transformed)
  return transformed;

}

  onMounted(() => {
      eventBus.on('lassoList', (data) => Selected_list.value = data);
    });

  onBeforeUnmount(() => {
    eventBus.off('lassoList', (data) => Selected_list.value = data);
  });


</script>

<style lang="less" scoped>
.comparison-view {
  height: 100%;
  padding: 0px 10px;
  .scrollbar{
    height:10%
  }
  .graph {
    width: 100%;
    height: 87%;
  }
}
.title {
  height: 30px;
  line-height: 30px;
  border-bottom: 2px solid rgb(179, 179, 179);
}

.scrollbar-flex-content {
  display: flex;
  height: 40px;
}
.scrollbar-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60%; 
  max-width: 130px; 
  min-width: 130px; 
  height: 100%;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  // background: #f9f9f9;
  // background: red;


  .item-text {
  color: black; /* 设置文字颜色为黑色 */
  font-size: 10px; /* 设置字体大小 */
  // font-weight: bold;
  flex-grow: 1;
  }
  .remove-button {
    margin-left: 5px;
    margin-right: 5px;
    width: 12px;
    height: 12px;
    border: none;
    border-radius: 20%;
    background-color: transparent;
    color: black;
    font-size: 10px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .remove-button:hover {
    color: white;
    background-color: #808080;
  }
  // .tooltip-topic {
  //   font-size: 16px;
  //   font-weight: bold;
  // }
  // :deep(.strong) {
  // font-size: 30px;
  // font-weight: bold;
  // }
}
</style>