<template>
  <div class="my-carousel">
    <el-carousel :interval="1000" :autoplay="true" :initial-index="0" indicator-position="none" arrow="always" height="300px">
      <el-carousel-item class="server-carousel">
        <el-row :gutter="10">
          <el-col :span="12">
            <div class="grid-content">
              <mychart ref="mServer" :options="getCmdbDetail1Options()" auto-resize theme="light"/>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="grid-content">
              <mychart ref="myServer" :options="getCmdbDetail2Options()" auto-resize theme="light"/>
            </div>
          </el-col>
        </el-row>
      </el-carousel-item>
      <el-carousel-item class="app-carousel">
        <el-row :gutter="10">
          <el-col :span="12">
            <div class="grid-content-left">
              <mychart ref="myApp" :options="getAppDetail1Options()" auto-resize theme="light"/>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="grid-content-right">
              <mychart ref="myApp" :options="getAppDetail2Options()" auto-resize theme="light"/>
            </div>
          </el-col>
        </el-row>
      </el-carousel-item>
      <el-carousel-item class="workform-carousel">
        <el-row :gutter="10">
          <el-col :span="10">
            <div class="grid-content-left">
              <mychart ref="myWorkfrom" :options="getAlertStatisticsDetailOption()" auto-resize theme="light"/>
            </div>
          </el-col>
          <el-col :span="14">
            <div class="grid-content-right">
              <p>今日工单</p>
              <el-table
                :data="alertTodayDetail"
                stripe
                border
                size="mini"
                highlight-current-row
                max-height="200"
                style="min-width: 100%;">
                <el-table-column
                  label="标题"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.title }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="详情"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.detail }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="来源"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.source }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="状态"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.status }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-col>
        </el-row>
      </el-carousel-item>
      <el-carousel-item class="publish-carousel">
        <el-row :gutter="10">
          <el-col :span="10">
            <div class="grid-content-left">
              <mychart ref="myPublish" :options="getAlertStatisticsDetailOption()" auto-resize theme="light"/>
            </div>
          </el-col>
          <el-col :span="14">
            <div class="grid-content-right">
              <p>今日发布</p>
              <el-table
                :data="alertTodayDetail"
                stripe
                border
                size="mini"
                highlight-current-row
                max-height="200"
                style="min-width: 100%;">
                <el-table-column
                  label="标题"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.title }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="详情"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.detail }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="来源"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.source }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="状态"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.status }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-col>
        </el-row>
      </el-carousel-item>
      <el-carousel-item class="alert-carousel">
        <el-row :gutter="10">
          <el-col :span="10">
            <div class="grid-content-left">
              <mychart ref="myAlert" :options="getAlertStatisticsDetailOption()" auto-resize theme="light"/>
            </div>
          </el-col>
          <el-col :span="14">
            <div class="grid-content-right">
              <p>今日告警</p>
              <el-table
                :data="alertTodayDetail"
                stripe
                border
                size="mini"
                highlight-current-row
                max-height="200"
                style="min-width: 100%;">
                <el-table-column
                  label="标题"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.title }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="详情"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.detail }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="来源"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.source }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  label="状态"
                  align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.status }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-col>
        </el-row>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'MyCarousel',
  props: {
    serverDetail: {
      type: Object,
      required: true
    },
    appDetail: {
      type: Object,
      required: true
    },
    alertSevenDaysDetail: {
      type: Object,
      required: true
    },
    alertTodayDetail: {
      type: Array,
      required: true
    },
    publishSevenDaysDetail: {
      type: Object,
      required: true
    },
    publishTodayDetail: {
      type: Array,
      required: true
    },
    workformSevenDaysDetail: {
      type: Object,
      required: true
    },
    workformTodayDetail: {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      option: {
        color: ['#3398DB'],
        title: {
          text: '',
          left: 'center',
          textStyle: {
            fontSize: 15
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          top: 40,
          left: '3%',
          right: '4%',
          bottom: 10,
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: [],
          axisTick: {
            alignWithLabel: true
          },
          splitLine: {
            show: true,
            interval: 0,
            lineStyle: {
              type: 'dotted'
            }
          }
        },
        yAxis: {
          type: 'value',
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dotted'
            }
          }
        },
        series: {
          name: '',
          type: 'bar',
          barWidth: '40%',
          data: []
        }
      },
      optionServerAndApp: {
        title: {
          text: '',
          left: 'center',
          padding: [5, 10, 10, 10],
          textStyle: {
            fontSize: 15
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },

        series: [
          {
            name: '',
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '30%'],
            label: {
              normal: {
                position: 'inner'
              }
            },
            data: []
          },
          {
            name: '',
            type: 'pie',
            radius: ['40%', '55%'],
            label: {
              normal: {
                formatter: '{a|{a}}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                backgroundColor: '#eee',
                borderColor: '#aaa',
                borderWidth: 1,
                borderRadius: 4,
                rich: {
                  a: {
                    color: '#999',
                    lineHeight: 20,
                    align: 'center'
                  },

                  hr: {
                    borderColor: '#aaa',
                    width: '100%',
                    borderWidth: 0.5,
                    height: 0
                  },
                  b: {
                    fontSize: 12,
                    lineHeight: 20
                  },
                  per: {
                    color: '#eee',
                    backgroundColor: '#c5c2c2',
                    padding: [2, 4],
                    borderRadius: 2
                  }
                }
              }
            },
            data: []
          }
        ]
      }
    }
  },
  methods: {
    getCmdbDetail1Options: function() {
      var newOptions = {
        title: {
          text: '服务器统计(品牌 and 状态)'
        },
        series: [
          {
            name: '状态',
            data: this.serverDetail.cmdb_by_status
          },
          {
            name: '品牌',
            data: this.serverDetail.cmdb_by_manufacturer
          }
        ]
      }
      newOptions = _.merge({}, this.optionServerAndApp, newOptions)
      return newOptions
    },
    getCmdbDetail2Options: function() {
      var newOptions = {
        title: {
          text: '服务器统计(机房 and 环境)'
        },
        series: [
          {
            name: '环境',
            data: this.serverDetail.cmdb_by_env
          },
          {
            name: '机房',
            data: this.serverDetail.cmdb_by_idc
          }
        ]
      }
      newOptions = _.merge({}, this.optionServerAndApp, newOptions)
      return newOptions
    },
    getAppDetail1Options: function() {
      var newOptions = {
        title: {
          text: '应用统计(管理组 and 状态)'
        },
        series: [
          {
            name: '状态',
            data: this.appDetail.app_by_status
          },
          {
            name: '管理组',
            data: this.appDetail.app_by_team
          }
        ]
      }
      newOptions = _.merge({}, this.optionServerAndApp, newOptions)
      return newOptions
    },
    getAppDetail2Options: function() {
      var newOptions = {
        title: {
          text: '应用统计(类型 and 环境)'
        },
        series: [
          {
            name: '环境',
            data: this.appDetail.app_by_env
          },
          {
            name: '类型',
            data: this.appDetail.app_by_type
          }
        ]
      }
      newOptions = _.merge({}, this.optionServerAndApp, newOptions)
      return newOptions
    },
    getAlertStatisticsDetailOption: function() {
      var newOptions = {
        title: {
          text: '告警周统计'
        },
        xAxis: {
          data: this.alertSevenDaysDetail.x_data
        },
        series: {
          name: '告警数',
          data: this.alertSevenDaysDetail.y_data
        }
      }
      newOptions = _.merge({}, this.option, newOptions)
      return newOptions
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.my-carousel {
  .grid-content-left {
    font-size: 14px;
    text-align: center;
    height: 300px;
    margin: 0;
  }
  .grid-content-right {
    font-size: 14px;
    text-align: center;
    height: 300px;
    margin: 0;
    p {
      font-size: 15px;
      font-weight: bold;
      margin: 5px auto 10px;
    }
  }
  .echarts {
    width: 100%;
    height: 300px;
  }
}
</style>
