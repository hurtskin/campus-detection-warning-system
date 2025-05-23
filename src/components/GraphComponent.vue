<template>
  <div>
    <div class="card" style="width: 1200px; height: 700px;" >
    <div id="mynetwork" class="card-body"></div>
    <!-- <div v-if="number === 0" ><el-empty description="无与其相关数据"></el-empty></div> -->
    </div>
  </div>

</template>

<script>
require('vis-network/dist/dist/vis-network.min.css')
const vis = require('vis-network/dist/vis-network.min')

export default {
  name: 'GraphComponent',
  props: ['value1', 'value2'],
  data () {
    return {
      edges: this.value1, // 初始化为父组件传递的 value1
      nodes: this.value2, // 初始化为父组件传递的 value2
      network: null,
      container: null,
      options: null,
      data: null
    }
  },
  watch: {
    value1 (newEdges) {
      this.handleValuesChange(newEdges, this.value2)
    },
    value2 (newNodes) {
      this.handleValuesChange(this.value1, newNodes)
    }
  },

  methods: {
    handleValuesChange (newEdges, newNodes) {
    // 在这里处理 value1 和 value2 的变化
      this.edges = newEdges
      this.nodes = newNodes
      this.drawGraph()
    },
    drawGraph () {
      const container = document.getElementById('mynetwork')
      // 判断 nodes 和 edges 是否都存在有效数据
      if (!this.nodes || !this.edges || this.nodes.length === 0 || this.edges.length === 0) {
        if (this.network) {
          this.network.destroy() // 销毁现有图像
          this.network = null // 重置 network 对象
        }
        const imagePath = require('@/assets/NoData.png')
        container.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: gray;">
        <img src="${imagePath}" alt="No Data" style="width: 150px; height: auto; margin-bottom: 10px;">
        <p style="font-size: 16px;">暂无相关数据</p>
      </div>
    `
        return
      }

      // 创建 vis.DataSet 对象
      this.nodes = new vis.DataSet(this.nodes)
      this.edges = new vis.DataSet(this.edges)

      // 配置图表
      this.data = { nodes: this.nodes, edges: this.edges }
      this.options = {
        nodes: { font: { size: 14, align: 'center' }, borderWidth: 2 },
        edges: { color: { inherit: true }, smooth: { type: 'continuous' } },
        physics: { barnesHut: { gravitationalConstant: -2000, centralGravity: 0.4, springLength: 200 }, minVelocity: 0.04 }
      }

      // 初始化 vis network
      if (this.network) {
        this.network.destroy() // 如果图表已经存在，销毁并重新绘制
      }

      this.network = new vis.Network(container, this.data, this.options)

      // 监听节点拖动事件
      this.network.on('dragStart', (params) => {
        const nodeId = params.nodes[0] // 获取当前被拖动的节点
        if (nodeId) {
          this.network.setOptions({
            physics: { enabled: true } // 启用物理引擎
          })
        }
      })

      this.network.on('dragEnd', (params) => {
        const nodeId = params.nodes[0] // 获取拖动结束的节点
        if (nodeId) {
          // 禁用物理引擎并固定所有节点的位置
          const positions = this.network.getPositions()
          Object.keys(positions).forEach((id) => {
            this.nodes.update({
              id,
              x: positions[id].x,
              y: positions[id].y
            })
          })

          this.network.setOptions({
            physics: { enabled: false } // 禁用物理引擎
          })
        }
      })

      this.network.on('stabilizationIterationsDone', () => {
        this.network.setOptions({
          physics: { enabled: false } // 禁用物理引擎
        })
      })
    }
  },
  mounted () {
    // 初始挂载时绘制图表
    this.drawGraph()
  }
}
</script>

<style scoped>
#mynetwork {
  width: 100%;
  height: 750px;
  background-color: #ffffff;
  border: 1px solid lightgray;
  position: relative;
  float: left;
}
</style>
