<template>
  <el-container>
  <el-header>

      <el-row>
        <el-col :span="8" :offset="8"><div style="width: 300px; height: 35px;"><h2>舆情信息视图可视化</h2></div></el-col>
        <el-col :span="4" :offset="3"><div><p style=" width: 500px; height: 35px; ">当前时间是：{{ currentTime }}</p></div></el-col>
      </el-row>

  </el-header>
  <el-main>
    <el-row>
      <el-col :span="8"><div id="leftTwo2" style="width: 400px; height: 300px;"></div></el-col>
      <el-col :span="8"><div  id="mapContainer" style="margin-top: 60px; display: flex; width: 100%; height: 150px; border: 1px solid pink; margin-right: 20px;">
        <div style="margin-right: 50px; margin-left: 80px"><h3>舆情总数</h3><span style="margin-left: 7px;">{{ overview.total }}</span></div>
        <div style="margin-right: 20px;"><h3>舆情负面数量</h3><span style="margin-left: 28px;">{{ overview.negative }}</span></div>
      </div></el-col>
      <el-col :span="6"><div id="rightOne1" style="width: 500px; height: 300px;"></div></el-col>
    </el-row>
    <el-row>
      <el-col :span="8"><div id="leftOne1" style="width: 550px; height: 350px; "></div>
        </el-col>
      <el-col :span="8" :offset="3"><div id="rightTwo2" style="width: 600px; height: 300px;"></div></el-col>
    </el-row>
  </el-main>
</el-container>
</template>
<script>
import * as echarts from 'echarts'
import axios from 'axios'
export default {

  data () {
    return {
      currentTime: '', // 用于存储当前时间
      trends: [],
      overview: {
        total: 0,
        negative: 0
      },
      keywords: [
        {

        }
      ]
    }
  },
  mounted () {
    this.fetchData()
    // 在组件挂载后启动定时器
    setInterval(() => {
      this.updateTime()
    }, 1000)
  },
  methods: {
    // 初始化柱状图
    initBarChart (id, title, xData, yData, barColors) {
      const chart = echarts.init(document.getElementById(id))
      const option = {
        title: {
          text: title,
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: xData
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: yData,
            type: 'bar',
            itemStyle: {
              normal: {
                color: function (params) {
                  return barColors[params.dataIndex] || '#000' // 根据索引选择颜色
                }
              }
            }
          }
        ]
      }
      chart.setOption(option)
    },

    // 初始化折线图
    initLineChart (id, title, xData, yData) {
      const chart = echarts.init(document.getElementById(id))
      const option = {
        title: {
          text: title,
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: xData
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: yData,
            type: 'line'
          }
        ]
      }
      chart.setOption(option)
    },

    // 初始化饼图
    initPieChart (id, title, data) {
      const chart = echarts.init(document.getElementById(id))
      const option = {
        title: {
          text: title,
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '7%',
          left: 'center'
        },
        series: [
          {
            name: '正负面分析',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: data
          }
        ]
      }
      chart.setOption(option)
    },

    // 初始化带颜色渐变的柱状图
    initGradientBarChart (id, title, xData, yData, colors) {
      const chart = echarts.init(document.getElementById(id))
      const option = {
        title: {
          text: title,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: xData
        },
        series: [
          {
            type: 'bar',
            data: yData,
            itemStyle: {
              color: function (params) {
                return colors[params.dataIndex] || '#000' // 根据索引选择颜色
              }
            }
          }
        ]
      }
      chart.setOption(option)
    },

    // 初始化所有图表
    initAllCharts () {
    // 柱状图
      this.initBarChart('leftOne1', '正面负面柱状分析', ['正面', '负面'], [this.overview.total, this.overview.negative], ['#4CAF50', '#F44336'])

      // 折线图
      this.initLineChart('leftTwo2', '文章发布个数变化趋势', ['24-6', '24-7', '24-8', '24-9', '24-10', '24-11', '24-12'], [2036, 1359, 1365, 3265, 3120, 2365, 3369])

      // 饼图
      this.initPieChart('rightOne1', '舆情信息正负面', [
        { value: this.overview.total - this.overview.negative, name: '正面', itemStyle: { color: '#4CAF50' } },
        { value: this.overview.negative, name: '负面', itemStyle: { color: '#F44336' } }
      ])

      // 带颜色渐变的柱状图
      this.initGradientBarChart(
        'rightTwo2',
        '热词排名统计',
        [
          this.keywords[5].数据名称,
          this.keywords[4].数据名称,
          this.keywords[3].数据名称,
          this.keywords[2].数据名称,
          this.keywords[1].数据名称,
          this.keywords[0].数据名称
        ],
        [
          this.keywords[5].数值,
          this.keywords[4].数值,
          this.keywords[3].数值,
          this.keywords[2].数值,
          this.keywords[1].数值,
          this.keywords[0].数值
        ],
        ['#ff7f50', '#87cefa', '#da70d6', '#32cd32', '#6495ed', '#ff69b4']
      )
    },

    async fetchData () {
      try {
        const response = await axios.get('http://localhost:5000/api/data')
        const data = response.data

        // 分类数据
        this.trends = data.filter(item => item.分类 === '趋势分析')
        const overviewData = data.filter(item => item.分类 === '舆情总数' || item.分类 === '舆情负面数')
        this.overview.total = overviewData.find(item => item.数据名称 === '总数').数值
        this.overview.negative = overviewData.find(item => item.数据名称 === '负面数量').数值
        this.keywords = data.filter(item => item.分类 === '热词统计')

        console.log(this.overview.total)
        console.log(this.overview.negative)
        console.log(this.keywords)

        // 确保数据加载完成后初始化图表
        this.initAllCharts()
      } catch (error) {
        console.error('数据加载失败:', error)
      }
    },
    updateTime () {
      const date = new Date()
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      this.currentTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }
  }
}

</script>

<style>

</style>
