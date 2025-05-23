<template>
  <div class="box" style="display: flex;">
        <div ><GraphComponent v-if="edges && nodes" :value1="edges" :value2="nodes" ></GraphComponent></div>
        <el-card class="page-container">
          <div style="height: 300px;">
            <el-input v-model="text" placeholder="请输入知识图谱索引内容"></el-input>
            <div style="display: flex; margin-left: 37px;" >
              <div style="margin: 10px 5px 0px 10px;">
              <el-button @click="reset">重置</el-button>
            </div>
            <div style="margin: 10px 5px 0px 10px;">
              <el-button type="primary" @click="getKnowledge">搜索</el-button>
            </div>

            </div>

          </div>

        </el-card>

  </div>
</template>

<script>
import GraphComponent from '@/components/GraphComponent.vue'
import axios from 'axios'
export default {
  components: {
    GraphComponent
  },
  data () {
    return {
      edges: null,
      nodes: null,
      number: 1,
      text: ''
    }
  },
  methods: {
    reset () {
      this.text = ''
    },
    getKnowledge () {
      try {
        axios.post('http://localhost:5000/get_neo4j', { text: this.text }, {
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(response => {
          const { edges, nodes } = response.data
          this.edges = edges && edges.length > 0 ? edges : []
          this.nodes = nodes && nodes.length > 0 ? nodes : []
          console.log(response.data)
        })
      } catch (error) {
        console.error('POST 请求出错:', error)
        throw error
      }
    }
  },
  created () {
    this.getKnowledge()
  }
}
</script>

<style lang="less" scoped>
.el-input{
  width: 200px;
}
.page-container {
    min-height: 300px;
    box-sizing: border-box;
    margin-left: 10px;
}
</style>
