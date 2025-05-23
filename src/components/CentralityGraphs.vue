<template>
  <div class="graph-container">
    <div id="chart1" class="graph"></div>
    <div id="chart2" class="graph"></div>
    <div id="chart3" class="graph"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'GraphComponent',
  props: ['value1'],
  data () {
    return {
      chart1: null,
      chart2: null,
      chart3: null,
      chartData: {
        series1: this.value1
      }

    }
  },
  watch: {
    value1 (newValue) {
      // 当 prop 'value' 发生变化时，更新图表数据
      this.updateChart(newValue)
    }
  },
  mounted () {
    this.initializeChart()
  },
  methods: {
    updateChart (newValue) {
      if (this.chart) {
        console.log(newValue)
        // 更新图表的数据
        this.chartData.series1 = newValue
        this.initializeChart()
      }
    },
    initializeChart () {
      // 初始化第一个图谱
      const chart1 = echarts.init(document.getElementById('chart1'))
      chart1.setOption({
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
              repulsion: 600,
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
            data: this.chartData.series1.nodes,
            edgeLabel: {
              show: false,
              margin: 8,
              valueAnimation: false
            },
            edgeSymbol: [
              null,
              null
            ],
            edgeSymbolSize: 10,
            links: this.chartData.series1.links,
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
            text: '\u6316\u6398\u51fa\u7684\u771f\u5b9e\u98ce\u9669\u793e\u56e2\u5173\u7cfb\u56fe\u8c31',
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

      })
      console.log(this.chartData.series1)
      // 初始化第二个图谱
      const chart2 = echarts.init(document.getElementById('chart2'))
      chart2.setOption({
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
              repulsion: 600,
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
            data: this.chartData.series1.nodes_b,
            edgeLabel: {
              show: false,
              margin: 8,
              valueAnimation: false
            },
            edgeSymbol: [
              null,
              null
            ],
            edgeSymbolSize: 10,
            links: this.chartData.series1.links_b,
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
            text: '\u6316\u6398\u51fa\u7684\u63a5\u8fd1\u4e2d\u5fc3\u6027\u5173\u7cfb\u56fe\u8c31',
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

      })

      // 初始化第三个图谱
      const chart3 = echarts.init(document.getElementById('chart3'))
      chart3.setOption({
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
              repulsion: 600,
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
            data: this.chartData.series1.nodes_c,
            edgeLabel: {
              show: false,
              margin: 8,
              valueAnimation: false
            },
            edgeSymbol: [
              null,
              null
            ],
            edgeSymbolSize: 10,
            links: this.chartData.series1.links_c,
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
            text: '\u6316\u6398\u51fa\u7684\u4ecb\u6570\u4e2d\u5fc3\u6027\u5173\u7cfb\u56fe\u8c31',
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

      })
    }
  }
}
</script>

<style scoped>
  .graph-container {
      display: flex;
      justify-content: space-between;
      margin: 0 auto;
  }
  .graph {
      width: 400px;
      height: 550px;
      border: 1px solid #ccc;
      margin-right: 10px;
  }
</style>
