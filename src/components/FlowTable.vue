<template>
  <div class="flow-table">
    <el-table
      :data="tableData"
      :default-sort="{ prop: ['change_date', 'patent_count_sum', 'cited_count_sum'], order: 'descending' }"
      style="width: 100%"
      max-height="300"
    >
      <el-table-column prop="tag" label="Tag" width="75"
          :filters="[
            { text: 'To', value: 'To' },
            { text: 'From', value: 'From' },
          ]"
          :filter-method="filterTag"
          filter-placement="bottom-end">
        <template #default="scope">
          <el-tag
            :type="scope.row.tag === 'To' ? 'primary' : 'success'"
            disable-transitions>
            {{ scope.row.tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="corporation" label="Cop" width="90" sortable show-overflow-tooltip/>
      <el-table-column prop="patent_count_sum" label="P" width="60" sortable/>
      <el-table-column prop="cited_count_sum" label="C" width="60" sortable/>
      <el-table-column prop="change_date" label="Date" width="120" sortable/>
    </el-table>
  </div>
</template>

<script setup>
  import {ref, computed, onMounted, onBeforeUnmount} from 'vue'
  import eventBus from '../utils/eventbus';
  import talentFlow from '../assets/data/talent_flow.json'

  const selectedCompany = ref(null);
  const lassoList = ref([]);
  let tableData = ref([]);
  tableData = computed(() => {
    let xx = talentFlow.filter(d => lassoList.value.includes(d.from) && lassoList.value.includes(d.to))
                       .filter(d => d.change_date > '1989-10' && (d.from === selectedCompany.value || d.to === selectedCompany.value));
    xx.forEach(d => {
      if(d.from === selectedCompany.value){
        d.patent_count_sum = +d.patent_count_sum;
        d.cited_count_sum = +d.cited_count_sum;
        d.corporation = d.to;
        d.tag = 'To';
      }
      else{
        d.corporation = d.from;
        d.tag = 'From';
      }
    });
    return xx;
  })

  const filterTag = (value, row) => {
    return row.tag === value;
  }

  onMounted(() => {
    eventBus.on('lassoList', (data) => lassoList.value = data);
    eventBus.on('flow', (data) => selectedCompany.value = data);
  });

  onBeforeUnmount(() => {
    eventBus.off('lassoList', (data) => lassoList.value = data);
    eventBus.off('flow', (data) => selectedCompany.value = data);
  });

</script>

<style lang="less" scoped>
  .flow-table{
    padding: 0px 10px;
    width: 100%;
  }
</style>
