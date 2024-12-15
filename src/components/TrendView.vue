<template>
  <div class="trend-view">
    <div class="title">
      <div>Trend View</div>
      <div class="name">{{ selectedCompany }}</div>
    </div>
    <div class="graph-group">
      <line-cart-item class="item" v-for="(name, idx) in features" :key="idx" :name="name" :data="filterDataByKey(name)"></line-cart-item>
    </div>
    <div class="bottom">
      <div style="width: 200px"></div>
      <div class="ticks">
        <div>1990</div>
        <div>1995</div>
        <div>2000</div>
        <div>2005</div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, onMounted, reactive ,onBeforeUnmount} from 'vue';
  import axios from 'axios';
  import LineCartItem from './LineCartItem.vue';
  import eventBus from '../utils/eventbus';
  const features = ['gender ratio', 'average cited', 'total patent number',
              'total cited number', 'cited per people', 'inventor count'];

  let selectedCompany = ref("");

  const full_data = ref([]);
  const loadData = async () => {
    try {
      const response = await axios.get('http://localhost:3000/api/getOrganizationData');
      full_data.value = response.data; 
    } 
    catch (error) {
      console.error('请求数据失败:', error);
    }
  };

  onMounted(() => {
    loadData();
  });

  const data = ref([]);
  watch(full_data, (newData) => {
    const companyData = newData.find(d => d.organization_name === selectedCompany.value);
    data.value = companyData ? companyData.data : [];
  });
  watch(selectedCompany, (newCompany) => {
    console.log(newCompany)
    const companyData = full_data.value.find(d => d.organization_name === newCompany);
    data.value = companyData ? companyData.data : [];
  });

  // 替换所有空格为下划线
  const toSnakeCase = (str)=>{
    return str.replace(/\s+/g, '_'); 
  }

  const filterDataByKey = (key)=>{
    const d = reactive(data.value.map(item => ({
      time: item.time,
      value: item.detail[toSnakeCase(key)]
    })));
    return d;
  }

  onMounted(() => {
    eventBus.on('trend', (data) => selectedCompany.value = data);
  });

  onBeforeUnmount(() => {
    eventBus.off('trend', (data) => selectedCompany.value = data);
  });


</script>

<style lang="less" scoped>
  .trend-view{
    height: 100%;
    padding: 0px 10px;
    .title{
      display: flex;
      justify-content: space-between;
      height: 30px;
      line-height: 30px;
      border-bottom: 2px solid rgb(179, 179, 179);
      .name{
        margin-right: 5px;
      }
    }
    .graph-group{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      margin-top:10px;
      height: calc(100% - 70px);
      .item{
        height: calc(100%/7);
      }
    }
    .bottom{
      display: flex;
      height: 30px;
      .ticks{
        display: flex;
        justify-content: space-between;
        flex-grow: 1;
        line-height: 30px;
        font-size: 12px;
      }
    }
  }
</style>
