<template>
  <div id="cce7cd855bf84a029d19000b394d3e62" class="chart-container" style="width:900px; height:500px;"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  props: ['value'],
  data () {
    return {
      chart: null,
      chartData: {
        series: this.value.series,
        legend: [
          {
            data: [
              'community 1',
              'community 2'
            ],
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
        xAxis: this.value.xAxis,
        yAxis: this.value.yAxis,
        title: [
          {
            show: true,
            text: this.value.title.text,
            target: 'blank',
            subtarget: 'blank',
            padding: 5,
            itemGap: 10,
            textAlign: 'auto',
            textVerticalAlign: 'auto',
            triggerEvent: false
          }
        ]
      }
    }
  },
  watch: {
    value (newValue) {
      // 当 prop 'value' 发生变化时，更新图表数据
      this.updateChart(newValue)
    }
  },
  mounted () {
    this.initializeChart()
  },
  methods: {
    initializeChart () {
      this.chart = echarts.init(
        document.getElementById('cce7cd855bf84a029d19000b394d3e62'), 'white', { renderer: 'canvas' }
      )
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
            type: this.chartData.series[0].type,
            name: this.chartData.series[0].name,
            symbolSize: this.chartData.series[0].symbolSize,
            data: this.chartData.series[0].data,
            itemStyle: this.chartData.series[0].itemStyle,
            label: {
              show: false,
              margin: 8
            },
            rippleEffect: {
              show: true,
              brushType: 'stroke',
              scale: 2.5,
              period: 4
            }
          },
          {
            type: this.chartData.series[1].type,
            name: this.chartData.series[1].name,
            symbolSize: this.chartData.series[1].symbolSize,
            data: this.chartData.series[1].data,
            itemStyle: this.chartData.series[1].itemStyle,
            label: {
              show: false,
              margin: 8
            },
            rippleEffect: {
              show: true,
              brushType: 'stroke',
              scale: 2.5,
              period: 4
            }
          }
        ],
        legend: this.chartData.legend,
        tooltip: this.chartData.tooltip,
        xAxis: this.chartData.xAxis,
        yAxis: this.chartData.yAxis,
        title: this.chartData.title

      }
      this.chart.setOption(option)
    },
    updateChart (newValue) {
      this.chartData.series = newValue.series
      this.chartData.xAxis = newValue.xAxis
      this.chartData.yAxis = newValue.yAxis
      this.initializeChart()
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
