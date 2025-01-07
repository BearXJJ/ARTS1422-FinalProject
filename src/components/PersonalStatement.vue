<template>
  <div class="personal-statement">
    <div class="content">
      <div v-if="!drawerOpen" class="dialog-box">
        <div class="title">Personal Statement</div>
        <textarea v-model="statementText"></textarea>
        <el-button @click="saveStatement" style="float: right;">Save Statement</el-button>
      </div>

      <div v-else class="result-drawer">
        <div class="title">Suggestion</div>
        <div style="font-size:15px" class="drawer-content">
          <p>{{ processedText }}</p>
          <el-button @click="closeDrawer" style="margin-top: 10px; float: right;">Return</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import eventBus from '../utils/eventbus';


const statementText = ref('');
const processedText = ref('');
const drawerOpen = ref(false);

const saveStatement = async () => {
  try {
    const response = await axios.post('http://localhost:3000/process-statement', {
      statementText: statementText.value,
    });
    console.log(response.data);
    if (response.data.success) {
      drawerOpen.value = true;
      processedText.value = response.data.processedText;
      eventBus.emit("lassoList", response.data.processList);
      eventBus.emit("year", 1990);
    } else {
      alert(response.data.message || 'Failed to process statement.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Error while processing statement.');
  }
};

const closeDrawer = () => {
  drawerOpen.value = false;
  statementText.value = ''; 
};
</script>

<style lang="less" scoped>

  .personal-statement {
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
  }

  .drawer-content p{
    margin-top: 5px;
    margin-left: 3px;
    height: 230px;
    overflow-y: scroll;
  }

  .dialog-box textarea{
    margin-top: 5px;
    width: 100%;
    height: 230px;
    resize: none;
  }

  .result-box, .result-drawer, .drawer-header {
    textarea {
      width: 100%;
      height: 80%;
      margin-bottom: 0px;
      resize: none;
    }
  
  }
  
</style>
