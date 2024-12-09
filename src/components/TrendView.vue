<template>
  <div class="trend-view">
    <div class="title">
      <div>Trend View</div>
      <div class="name">International Business Machine Coporation</div>
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
  import LineCartItem from './LineCartItem.vue';
  import data from '../assets/data/data-trend.json'
  const features = ['gender ratio', 'CPC ratio', 'average cited', 'total patent number',
              'total cited number', 'cited per people', 'inventor count'];

  // 替换所有空格为下划线
  const toSnakeCase = (str)=>{
    return str.replace(/\s+/g, '_'); 
  }

  const filterDataByKey = (key)=>{
    return data.map(item => ({
      time: item.time,
      value: item.detail[toSnakeCase(key)]
    }));
  }

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
