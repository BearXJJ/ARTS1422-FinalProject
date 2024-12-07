<template>
  <div class="container">
    <div class="title">Untitled</div>
    <div class="body">
      <div class="left">
        <cluter-view></cluter-view>
      </div>
      <div class="middle">
        <div class="middle-upper">
          <panoramic-view></panoramic-view>
        </div>
        <div class="middle-lower">
          <trend-view></trend-view>
        </div>
      </div>
      <div class="right">
        <div class="right-upper">
          <personal-statement></personal-statement>
        </div>
        <div class="right-lower">
          <comparison-view></comparison-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import CluterView from './components/ClusterView.vue'
  import PanoramicView from './components/PanoramicView.vue'
  import TrendView from './components/TrendView.vue'
  import PersonalStatement from './components/PersonalStatement.vue'
  import ComparisonView from './components/ComparisonView.vue'
</script>

<style lang="less" scoped>
  .container{
    width: 100vw;
    height: 100vh;
    background-color: rgb(179, 179, 179);
    .title{
      width: 100%;
      height: 40px;
      background-color: rgb(138, 138, 138);
      font-size: 20px;
      font-weight: 500;
      line-height: 40px;
      padding-left: 15px;
    }
    .body{
      display: flex;
      height: calc(100% - 40px);
      justify-content: space-evenly;
      align-items: center;
      .left{
        width: 25%;
        height: 99%;
        background-color: white;
        border-radius: 5px;
      }
      .middle{
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        width: 57%;
        height: 100%;
        .middle-upper{
          height: 65%;
          background-color: white;
          border-radius: 5px;
        }
        .middle-lower{
          height: 33.5%;
          background-color: white;
          border-radius: 5px;
        }
      }
      .right{
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        width: 17%;
        height: 100%;
        .right-upper{
          height: 33.5%;
          background-color: white;
          border-radius: 5px;
        }
        .right-lower{
          height: 65%;
          background-color: white;
          border-radius: 5px;
        }
      }
    }
  }
</style>
