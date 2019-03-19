<template>
  <mychart ref="mychartEnlarge" :options="options" auto-resize theme="light" class="mychartEnlarge" style="width: 100%;min-height: 90%;"/>
</template>

<script>
/* eslint-disable */
export default {
  name: 'MychartEnlarge',
  props: {
    'echartsData': {
      type: Object,
      required: true,
      default: function () {
        return {
          legend_data: [],
          x_data: [],
          y_data: []
        }
      }
    }
  },
  computed:{
    options: function() {
      return {
        title: {
          text: this.echartsData.title,
          left: 'center',
          textStyle: {
            fontSize: 15
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        toolbox: {
          show: true,
          orient: 'horizontal',
          right: 20,
          feature: {
            saveAsImage: {},
            dataZoom: {
              yAxisIndex: false
            },
            restore: {
              icon: 'image://../../../src/icons/svg/echarts-restore.svg'
            },
            myRefresh: {
              show: true,
              title: '刷新',
              icon: 'image://../../../src/icons/svg/echarts-refresh.svg',
              onclick: () => {
                this.getLastData(this.echartsData.item)
              }
            }
          }
        },
        legend: {
          bottom: 0,
          data: this.echartsData.legend_data
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLabel: {
            formatter: function (value, index) {
              var mytime = value.split(' ')
              return mytime[1]
            },
            showMaxLabel: true,
            showMinLabel: true,
            color: '#4b4b4c'
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dotted'
            }
          },
          splitArea: {
            show: true
          },
          axisLine: {
            lineStyle: {
              color: '#909399'
            }
          },
          data: this.echartsData.x_data
        },
        dataZoom: [
          {
            type: 'inside',
            xAxisIndex: [0],
            filterMode: 'filter',
            minValueSpan: 5
          }
        ],
        yAxis: {
          type: 'value',
          min: this.echartsData.y_min ,
          max: this.echartsData.y_max,
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dotted'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#909399'
            }
          },
          axisLabel: {
            showMaxLabel: true,
            showMinLabel: true,
            color: '#4b4b4c'
          }
        },
        series: this.echartsData.y_data
      }
    }
  },
  watch: {
    echartsData() {
      var newOptions = {
        xAxis: {
          data: this.echartsData.x_data
        },
        series: this.echartsData.y_data,
        legend: {
          data: this.echartsData.legend_data
        }
      }
      this.$refs.mychartEnlarge.mergeOptions(newOptions, false);
    }
  },
  methods: {
    getLastData: function(item) {
      this.$emit('getEnlargeLastData',item)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
