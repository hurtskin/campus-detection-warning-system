<template>
  <div id="eee0c4fc11b949579f7251952016e291" class="chart-container" style="width:900px; height:700px;"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  props: ['value'],
  data () {
    return {
      chart: null, // 用于存储 ECharts 实例
      nodes: this.value.nodes,
      links: this.value.links
    }
  },
  watch: {
    value (newValue) {
      // 当 prop 'value' 发生变化时，更新图表数据
      this.updateChart(newValue)
    }
  },
  mounted () {
    // 在组件挂载后初始化图表
    this.initializeChart()
    console.log('1')
  },
  methods: {
    initializeChart () {
      // 初始化 ECharts 实例
      this.chart = echarts.init(
        document.getElementById('eee0c4fc11b949579f7251952016e291'),
        'white',
        { renderer: 'canvas' }
      )
      console.log(this.nodes)
      // 设置图表的初始配置
      const option = {
        animation: true,
        animationThreshold: 2000,
        animationDuration: 1000,
        animationEasing: 'cubicOut',
        animationDelay: 0,
        animationDurationUpdate: 300,
        animationEasingUpdate: 'cubicOut',
        animationDelayUpdate: 0,
        aria: {
          enabled: false
        },
        color: [
          '#5470c6',
          '#91cc75',
          '#fac858',
          '#ee6666',
          '#73c0de',
          '#3ba272',
          '#fc8452',
          '#9a60b4',
          '#ea7ccc'
        ],
        series: [
          {
            type: 'graph',
            layout: 'force',
            symbolSize: 10,
            circular: {
              rotateLabel: false
            },
            force: {
              repulsion: 100,
              gravity: 0.2,
              edgeLength: 30,
              friction: 0.6,
              layoutAnimation: true
            },
            label: {
              show: true,
              margin: 8,
              fontSize: 10,
              valueAnimation: false
            },
            lineStyle: {
              show: true,
              width: 1,
              opacity: 1,
              curveness: 0.1,
              type: 'solid'
            },
            roam: true,
            draggable: true,
            focusNodeAdjacency: true,
            data: this.nodes, // 使用传入的节点数据
            edgeLabel: {
              show: false,
              margin: 8,
              valueAnimation: false
            },
            edgeSymbol: [null, null],
            edgeSymbolSize: 10,
            links: this.links, // 使用传入的链接数据
            rippleEffect: {
              show: true,
              brushType: 'stroke',
              scale: 2.5,
              period: 4
            }
          }
        ],
        legend: [
          {
            data: [],
            selected: {},
            show: true,
            padding: 5,
            itemGap: 10,
            itemWidth: 25,
            itemHeight: 14,
            backgroundColor: 'transparent',
            borderColor: '#ccc',
            borderRadius: 0,
            pageButtonItemGap: 5,
            pageButtonPosition: 'end',
            pageFormatter: '{current}/{total}',
            pageIconColor: '#2f4554',
            pageIconInactiveColor: '#aaa',
            pageIconSize: 15,
            animationDurationUpdate: 800,
            selector: false,
            selectorPosition: 'auto',
            selectorItemGap: 7,
            selectorButtonGap: 10
          }
        ],
        tooltip: {
          show: true,
          trigger: 'item',
          triggerOn: 'mousemove|click',
          axisPointer: {
            type: 'line'
          },
          showContent: true,
          alwaysShowContent: false,
          showDelay: 0,
          hideDelay: 100,
          enterable: false,
          confine: false,
          appendToBody: false,
          transitionDuration: 0.4,
          textStyle: {
            fontSize: 14
          },
          borderWidth: 0,
          padding: 5,
          order: 'seriesAsc'
        },
        title: [
          {
            show: true,
            text: '热血高校人物关系图谱',
            target: 'blank',
            subtarget: 'blank',
            left: 'center',
            padding: 5,
            itemGap: 10,
            textAlign: 'auto',
            textVerticalAlign: 'auto',
            triggerEvent: false,
            textStyle: {
              fontSize: 20
            }
          }
        ]
      }

      // 设置图表的配置项
      this.chart.setOption(option)
    },
    updateChart (newValue) {
      if (this.chart) {
        console.log(newValue)
        // 更新图表的数据
        this.chart.setOption({
          series: [
            {
              data: newValue.nodes,
              links: newValue.links
            }
          ]
        })
        console.log('更新完成')
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 900px;
  height: 500px;
}
</style>
