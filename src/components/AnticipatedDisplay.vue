<template>
  <div>
    <el-divider></el-divider>
    <div style="display: flex; justify-content: space-around;">
      <div class="buttonq">
       <el-badge :value="countTotalSentiments()" class="item" type="primary">
           <el-button size="small" @click="submit3">总量/条</el-button>
       </el-badge>
  </div>
  <div class="buttonq">
       <el-badge :value="countPositiveSentiments()" class="item" type="success">
           <el-button size="small" @click="submit1">正面/条</el-button>
       </el-badge>
  </div>
  <div class="buttonq">
       <el-badge :value="countPassiveSentiments()" class="item" type="danger">
           <el-button size="small" @click="submit2">负面/条</el-button>
       </el-badge>
  </div>
    </div>
    <el-divider></el-divider>
    <div id="charts" v-if="label == 0" style="width: 500px; height: 500px; margin: 30px 0 0 45px;" ></div>
    <div v-if="label != 0">
      <el-table :data="anticipatedData" style="width: 100%">
      <el-table-column width="100px" prop="label" label="情感">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.sentiment_code == '积极' && (label == 3 || label == 1)">正面</el-tag>
          <el-tag v-else-if="scope.row.sentiment_code == '消极' && (label == 3 || label == 2)" type="danger">负面</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="text" label="文本">
        <template slot-scope="scope">
          <div v-if="scope.row.sentiment_code == '积极' && (label == 3 || label == 1)">{{scope.row.text}}</div>
          <div v-else-if="scope.row.sentiment_code == '消极' && (label == 3 || label == 2)" type="danger">{{scope.row.text}}</div>
        </template>
      </el-table-column>
    </el-table>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  props: ['parentMessage'],
  data () {
    return {
      anticipatedData: this.parentMessage,
      label: 0
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    countPositiveSentiments () {
      return this.anticipatedData.filter(item => item.sentiment_code === '积极').length
    },
    countPassiveSentiments () {
      return this.anticipatedData.filter(item => item.sentiment_code === '消极').length
    },
    countTotalSentiments () {
      return this.countPositiveSentiments() + this.countPassiveSentiments()
    },
    submit3 () {
      this.label = 3
    },
    submit2 () {
      this.label = 2
    },
    submit1 () {
      this.label = 1
    },
    initChart () {
      const myChart = echarts.init(document.getElementById('charts'))
      const data = [
        { value: this.countPositiveSentiments(), name: '正面', isPositive: true },
        { value: this.countPassiveSentiments(), name: '负面', isPositive: false }
      ]
      const option = {
        title: {
          text: '饼状图展示',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: data.map(item => {
              return {
                value: item.value,
                name: item.name,
                itemStyle: {
                  color: item.isPositive ? '#b9d3ee' : '#ff6347'
                }
              }
            }),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      myChart.setOption(option)
    }

  }

}
</script>

<style scoped>
</style>
