<template>
  <div class="zabbix-appconfig-container">
    <el-form :inline="true" :model="searchForm" size="small" class="zabbix-appconfig-form-inline">
      <el-form-item label="当前的应用">
        <el-select v-model="searchForm.app" filterable placeholder="请搜索或选择应用...." default-first-option>
          <el-option
            v-for="app in apps_list"
            :key="app.aid"
            :label="app.name"
            :value="app.aid">
            <span style="float: left">{{ app.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ app.aid }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button :plain="btnType !== 1" type="info" circle @click="commitOneHourTimeBtn">1h</el-button>
        <el-button :plain="btnType !== 2" type="info" circle @click="commitThreeHourTimeBtn">3h</el-button>
        <el-button :plain="btnType !== 3" type="info" circle @click="commitSixHourTimeBtn">6h</el-button>
        <el-button :plain="btnType !== 4" type="info" circle @click="commitTwelveHourTimeBtn">12h</el-button>
        <el-button :plain="btnType !== 5" type="info" circle @click="commitOneDayTimeBtn">1d</el-button>
        <el-button :plain="btnType !== 6" type="info" circle @click="commitThreeDayTimeBtn">3d</el-button>
      </el-form-item>
      <el-form-item>
        <el-popover
          v-model="showTimeVisible"
          width="350"
          trigger="click">
          <el-button slot="reference" :plain="btnType !== 7" type="info" icon="el-icon-date" circle @click="showTimeVisibleBtn"/>
          <el-form size="small" class="timeForm" label-position="right">
            <el-form-item label="起始时间">
              <el-date-picker
                v-model="searchForm.time_begin"
                type="datetime"
                format="yyyy-MM-dd HH:mm:ss"
                value-format="timestamp"
                align="center"
                placeholder="选择日期时间"/>
            </el-form-item>
            <el-form-item label="结束时间">
              <el-date-picker
                v-model="searchForm.time_end"
                type="datetime"
                format="yyyy-MM-dd HH:mm:ss"
                value-format="timestamp"
                placeholder="选择日期时间"/>
            </el-form-item>
            <el-button @click="closeTimeVisibleBtn">关闭</el-button>
            <el-button type="primary" @click="commitTimeSelectBtn">确 定</el-button>
          </el-form>
        </el-popover>
      </el-form-item>
      <el-form-item>
        <span style="color:#97a8be">自动刷新(1min)</span>
        <el-switch
          v-model="autoRefreshStatus"
          active-color="#13ce66"/>
        <el-button type="info" icon="el-icon-refresh" plain round @click="commitManuallyRefreshBtn">手动刷新</el-button>
      </el-form-item>
    </el-form>
    <div class="echarts-parts clearfix">
      <div class="cpu-charts mycharts">
        <mychart ref="myCpuChart" :options="polar" auto-resize theme="light"/>
      </div>
      <div class="load-charts mycharts">
        <mychart ref="myLoadChart" :options="polar" auto-resize theme="light"/>
      </div>
      <div class="memory-charts mycharts">
        <mychart ref="myMemoryChart" :options="polar" auto-resize theme="light"/>
      </div>
      <div class="tcp-total-charts mycharts">
        <mychart ref="myTcpTotalChart" :options="polar" auto-resize theme="light"/>
      </div>
      <div class="tcp-established-charts mycharts">
        <mychart ref="myTcpEstablishedChart" :options="polar" auto-resize theme="light"/>
      </div>
      <div class="tcp-closed-charts mycharts">
        <mychart ref="myTcpClosedChart" :options="polar" auto-resize theme="light"/>
      </div>
    </div>
    <el-dialog
      :visible.sync="echartsEnlargeDialogVisible"
      width="65%"
      class="echarts_enlarge_dialog"
      center>
      <mychart-enlarge :echarts-data="zabbixData" @getEnlargeLastData="getEnlargeLastData($event)"/>
    </el-dialog>
  </div>
</template>

<script>
import { getZabbixValueForServer, getMonitorRelateApps } from '@/api/monitor/monitor'
import MychartEnlarge from './echarts_enlarge'
import _ from 'lodash'

var date = new Date()
var default_time_end = Date.parse(date)
var default_time_begin = date.setTime(date.getTime() - 3600 * 1000)

/* eslint-disable */
export default {
  name: 'AppConfig',
  components: {
    MychartEnlarge
  },
  data: function() {
    var self = this;
    return {
      btnType: 0,
      searchForm: {
        item: '',
        app: '',
        time_begin: default_time_begin,
        time_end: default_time_end
      },
      showTimeVisible: false,
      echartsEnlargeDialogVisible: false,
      listLoading: true,
      zabbixData: {},
      zabbixCommonData: {},
      zabbixCpuData: {},
      zabbixLoadData: {},
      zabbixMemoryData: {},
      zabbixTcpTotalData: {},
      zabbixTcpEstablishedData: {},
      zabbixTcpClosedData: {},
      autoRefreshStatus: false,
      apps_list: [],
      polar: {
        title: {
          text: '',
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
            dataZoom:{
              yAxisIndex: false
            },
            restore: {
              icon: 'image://../../../src/icons/svg/echarts-restore.svg'
            },
            // dataView: {
            //   readOnly: true
            // },
            myRefresh: {
              show: true,
              title: '刷新',
              icon: 'image://../../../src/icons/svg/echarts-refresh.svg',
              onclick:() => {
                console.log('哈哈哈,我点了下 "刷新" 按钮....')
              }
            },
            myEnlarge: {
              show: true,
              title: '大图',
              icon: 'image://../../../src/icons/svg/echarts-enlarge.svg',
              onclick:() => {
                console.log('哈哈哈,我点了下 "放大" 按钮....')
              }
            },
          }
        },
        legend: {
          bottom: 0,
          data: []
        },
        grid: {
          top: '10%',
          left: '3%',
          right: '4%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLabel: {
            // rotate: 60,
            formatter: function(value, index) {
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
          data: []
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
          min: 0,
          max: 100,
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
        series: []
      }
    }
  },
  watch: {
    autoRefreshStatus() {
      if (this.autoRefreshStatus) {
        this.autoRefreshData()
      }
    },
    zabbixCpuData() {
      var self = this;
      var newOptions = {
        title: {
          text: 'CPU 利用率(%)'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('','cpu_idle')
                this.getCpuData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixCpuData
                this.zabbixData.title = 'CPU 利用率(%)'
                this.zabbixData.item = 'cpu_idle'
                this.zabbixData.y_min = 0
                this.zabbixData.y_max = 100
                this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixCpuData.x_data
        },
        series: this.zabbixCpuData.y_data,
        legend: {
          data: this.zabbixCpuData.legend_data
        }
      }
      this.$refs.myCpuChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myCpuChart.mergeOptions(newOptions, true);
    },
    zabbixLoadData() {
      var newOptions = {
        title: {
          text: '系统平均负载(5min)'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('', 'load_5m')
                this.getLoadData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixLoadData
                this.zabbixData.title = '系统平均负载(5min)'
                this.zabbixData.item = 'load_5m'
                this.zabbixData.y_min = 0
                this.zabbixData.y_max = function (value) {
                  return Math.floor(value.max) + 1
                },
                  this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixLoadData.x_data
        },
        yAxis: {
          max: function (value) {
            return Math.floor(value.max) + 1
          }
        },
        series: this.zabbixLoadData.y_data,
        legend: {
          data: this.zabbixLoadData.legend_data
        }
      }
      this.$refs.myLoadChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myLoadChart.mergeOptions(newOptions, true);
    },
    zabbixMemoryData() {
      var newOptions = {
        title: {
          text: '系统内存利用率(%)'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('','memory_free')
                this.getMemoryData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixMemoryData
                this.zabbixData.title = '系统内存利用率(%)'
                this.zabbixData.item = 'memory_free'
                this.zabbixData.y_min = 0
                this.zabbixData.y_max = 100
                this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixMemoryData.x_data
        },
        series: this.zabbixMemoryData.y_data,
        legend: {
          data: this.zabbixMemoryData.legend_data
        }
      }
      this.$refs.myMemoryChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myMemoryChart.mergeOptions(newOptions, true);
    },
    zabbixTcpTotalData() {
      var newOptions = {
        title: {
          text: 'TCP 连接总数(%)'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('','tcp_total')
                this.getTcpTotalData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixTcpTotalData
                this.zabbixData.title = 'TCP 连接总数(%)'
                this.zabbixData.item = 'tcp_total'
                this.zabbixData.y_min = function(value) {
                  return value.min - 20;
                },
                this.zabbixData.y_max = function(value) {
                  return value.max + 100;
                },
                this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixTcpTotalData.x_data
        },
        yAxis: {
          min: function(value) {
            return value.min - 20;
          },
          max: function(value) {
            return value.max + 100;
          },
        },
        series: this.zabbixTcpTotalData.y_data,
        legend: {
          data: this.zabbixTcpTotalData.legend_data
        }
      }
      this.$refs.myTcpTotalChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myTcpTotalChart.mergeOptions(newOptions, true);
    },
    zabbixTcpEstablishedData() {
      var newOptions = {
        title: {
          text: 'TCP 已连接总数'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('','tcp_established')
                this.getTcpEstablishedData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixTcpEstablishedData
                this.zabbixData.title = 'TCP 已连接总数'
                this.zabbixData.item = 'tcp_established'
                this.zabbixData.y_min = function(value) {
                  return value.min - 20;
                },
                this.zabbixData.y_max = function(value) {
                  return value.max + 50;
                },
                this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixTcpEstablishedData.x_data
        },
        yAxis: {
          min: function(value) {
            return value.min - 20;
          },
          max: function(value) {
            return value.max + 50;
          },
        },
        series: this.zabbixTcpEstablishedData.y_data,
        legend: {
          data: this.zabbixTcpEstablishedData.legend_data
        }
      }
      this.$refs.myTcpEstablishedChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myTcpEstablishedChart.mergeOptions(newOptions, true);
    },
    zabbixTcpClosedData() {
      var newOptions = {
        title: {
          text: 'TCP 已关闭总数'
        },
        toolbox: {
          feature: {
            myRefresh: {
              onclick: () => {
                this.commonTimeCalculate('','tcp_closed')
                this.getTcpClosedData()
              }
            },
            myEnlarge: {
              onclick: () => {
                this.zabbixData = this.zabbixTcpClosedData
                this.zabbixData.title = 'TCP 已关闭总数'
                this.zabbixData.item = 'tcp_closed'
                this.zabbixData.y_min = function(value) {
                  return value.min - 20;
                },
                this.zabbixData.y_max = function(value) {
                  return value.max + 100;
                },
                this.echartsEnlargeDialogVisible = true
              }
            }
          }
        },
        xAxis: {
          data: this.zabbixTcpClosedData.x_data
        },
        yAxis: {
          min: function(value) {
            return value.min - 100;
          },
          max: function(value) {
            return value.max + 100;
          }
        },
        series: this.zabbixTcpClosedData.y_data,
        legend: {
          data: this.zabbixTcpClosedData.legend_data
        }
      }
      this.$refs.myTcpClosedChart.clear()
      newOptions = _.merge({},this.polar,newOptions)
      this.$refs.myTcpClosedChart.mergeOptions(newOptions, true);
    }
  },
  // mounted() {
  //   window.vv = this;
  // },
  created() {
    this.fetchMonitorRelateApps()
  },
  methods: {
    // 获取监控项关联的所有 APP
    fetchMonitorRelateApps: function() {
      getMonitorRelateApps().then(res => {
        this.apps_list = res
      })
    },
    // 获取监控数据
    getZabbixData:async function(mychart_obj, item) {
      mychart_obj.showLoading(
        'default',
        {
          text:'获取数据中，请稍候...',
          color: '#67c23a',
          maskColor: 'rgba(255, 255, 255, 0)',
          textColor: '#c23531',
          zlevel: 0
        }
      )
      this.searchForm.item = item
      await getZabbixValueForServer(this.searchForm).then(
        (res) => {
          const legend_data = []
          res.y_data.forEach(y => {
            y['type'] = 'line'
            y['showSymbol'] = false
            legend_data.push(y.name)
          })
          res["legend_data"] = legend_data
          this.zabbixCommonData = res
          mychart_obj.hideLoading()
        }
      )
    },
    // 获取 cpu 信息
    getCpuData:async function() {
      await this.getZabbixData(this.$refs.myCpuChart, 'cpu_idle')
      this.zabbixCpuData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 获取 load 信息
    getLoadData:async function() {
      await this.getZabbixData(this.$refs.myLoadChart, 'load_5m')
      this.zabbixLoadData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 获取 memory 信息
    getMemoryData:async function() {
      await this.getZabbixData(this.$refs.myMemoryChart, 'memory_free')
      this.zabbixMemoryData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 获取 tcp total 信息
    getTcpTotalData:async function() {
      await this.getZabbixData(this.$refs.myTcpTotalChart, 'tcp_total')
      this.zabbixTcpTotalData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 获取 tcp established 信息
    getTcpEstablishedData:async function() {
      await this.getZabbixData(this.$refs.myTcpEstablishedChart, 'tcp_established')
      this.zabbixTcpEstablishedData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 获取 tcp closed 信息
    getTcpClosedData:async function() {
      await this.getZabbixData(this.$refs.myTcpClosedChart, 'tcp_closed')
      this.zabbixTcpClosedData =  this.zabbixCommonData
      this.zabbixCommonData = {}
    },
    // 自动刷新
    autoRefreshData: async function() {
      var self = this
      if (this.autoRefreshStatus) {
        this.searchForm.time_end = Date.parse(new Date())
        await this.getAllData()
        setTimeout(this.autoRefreshData,60000)
      }else{
        return
      }
    },
    // 获取上述 cpu/load/memory/tcp total/tcp established/tcp closed 信息
    getAllData: async function() {
      await this.getCpuData()
      await this.getLoadData()
      await this.getMemoryData()
      await this.getTcpTotalData()
      await this.getTcpEstablishedData()
      await this.getTcpClosedData()
    },
    // 显示 自定义时间弹框
    showTimeVisibleBtn: function() {
      this.showTimeVisible = true
    },
    // 自定义时间弹框中的关闭
    closeTimeVisibleBtn: function() {
      this.showTimeVisible = false
    },
    // 自定义时间弹框中的提交
    commitTimeSelectBtn: function() {
      this.btnType = 7
      this.getAllData()
    },
    // 通用 时间计算
    commonTimeCalculate: function(time,item) {
      if ( !this.searchForm.app ) {
        this.$message({
          message: 'Oh MyGod , 必须选择一个应用....',
          type: 'error',
          duration: 2000
        })
        return
      }
      this.searchForm.item = item?item:''
      this.searchForm.time_end = Date.parse(new Date())
      const date = new Date()
      this.searchForm.time_begin = time?date.setTime(date.getTime() - time):this.searchForm.time_begin
      if(!item) {
        console.log('我执行了这里....')
        this.getAllData()
      }
    },
    // 提交搜索最近1个小时的监控数据
    commitOneHourTimeBtn: function() {
      this.btnType = 1
      this.commonTimeCalculate(3600 * 1000)
    },
    // 提交搜索最近3个小时的监控数据
    commitThreeHourTimeBtn: function() {
      this.btnType = 2
      this.commonTimeCalculate(3600 * 1000 * 3)
    },
    // 提交搜索最近6个小时的监控数据
    commitSixHourTimeBtn: function() {
      this.btnType = 3
      this.commonTimeCalculate(3600 * 1000 * 6)
    },
    // 提交搜索最近12个小时的监控数据
    commitTwelveHourTimeBtn: function() {
      this.btnType = 4
      this.commonTimeCalculate(3600 * 1000 * 12)
    },
    // 提交搜索最近1天的监控数据
    commitOneDayTimeBtn: function() {
      this.btnType = 5
      this.commonTimeCalculate(3600 * 1000 * 24)
    },
    // 提交搜索最近3天的监控数据
    commitThreeDayTimeBtn: function() {
      this.btnType = 6
      this.commonTimeCalculate(3600 * 1000 * 24 * 3)
    },
    // 放大弹框中,点击 '刷新' 按钮
    getEnlargeLastData: function(item) {
      this.commonTimeCalculate('',item)
      if ( item === 'cpu_idle' ){
        this.getCpuData()
        this.zabbixData = this.zabbixCpuData
        this.zabbixData.title = 'CPU 利用率(%)'
        this.zabbixData.item = item
        this.zabbixData.y_min = 0
        this.zabbixData.y_max = 100
      } else if ( item === 'load_5m' ) {
        this.getLoadData()
        this.zabbixData = this.zabbixLoadData
        this.zabbixData.title = '系统平均负载(5min)'
        this.zabbixData.item = 'load_5m'
        this.zabbixData.y_min = 0
        this.zabbixData.y_max = ''
      } else if ( item === 'memory_free' ) {
        this.getMemoryData()
        this.zabbixData = this.zabbixMemoryData
        this.zabbixData.title = '系统内存利用率(%)'
        this.zabbixData.item = 'memory_free'
        this.zabbixData.y_min = 0
        this.zabbixData.y_max = 100
      } else if ( item === 'tcp_total' ) {
        this.getTcpTotalData()
        this.zabbixData = this.zabbixTcpTotalData
        this.zabbixData.title = 'TCP 连接总数(%)'
        this.zabbixData.item = 'tcp_total'
        this.zabbixData.y_min = function(value) {
          return value.min - 20;
        },
        this.zabbixData.y_max = function(value) {
          return value.max + 100;
        }
      } else if ( item === 'tcp_established' ) {
        this.getTcpEstablishedData()
        this.zabbixData = this.zabbixTcpEstablishedData
        this.zabbixData.title = 'TCP 已连接总数'
        this.zabbixData.item = 'tcp_established'
        this.zabbixData.y_min = function(value) {
          return value.min - 20;
        },
        this.zabbixData.y_max = function(value) {
          return value.max + 50;
        }
      } else{
        this.getTcpClosedData()
        this.zabbixData = this.zabbixTcpClosedData
        this.zabbixData.title = 'TCP 已关闭总数'
        this.zabbixData.item = 'tcp_closed'
        this.zabbixData.y_min = function(value) {
          return value.min - 20;
        },
        this.zabbixData.y_max = function(value) {
          return value.max + 100;
        }
      }
    },
    // 手动刷新
    commitManuallyRefreshBtn: function() {
      this.commonTimeCalculate()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .zabbix-appconfig-container {
    .zabbix-appconfig-form-inline {
      margin: 10px 30px 5px;
      text-align: left;
      .el-form-item:last-child {
        float: right;
      }
    }
    .echarts_enlarge_dialog {
      .el-dialog__header {
        padding-top: 0px;
      }
    }
    .echarts-parts {
      margin: 10px auto 30px;
      .mycharts {
        margin: 0px 2%;
        width: 45%;
        height: 400px;
        float: left;
        .echarts {
          width: 100%;
          min-height: 100%;
        }
      }
    }
  }
  .timeForm {
    text-align: center;
    margin: 10px;
  }
</style>
