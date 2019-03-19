<template>
  <div class="monitor-alert-container">
    <el-container>
      <el-header height="40px" style="text-align: left">
        <strong style="color: #48484c;">告警统计</strong>
        <span style="font-size: 10px;color: #97989a">(随搜索条件中的时间进行统计 [默认统计最近7天])</span>
      </el-header>
      <el-main>
        <div class="echarts-parts clearfix">
          <mychart ref="alertStatusChart" :options="polar" auto-resize theme="light"/>
          <mychart ref="alertLevelChart" :options="polar" auto-resize theme="light"/>
          <mychart ref="alertSourceChart" :options="polar" auto-resize theme="light"/>
          <mychart ref="alertTriggerChart" :options="polar" auto-resize theme="light"/>
        </div>
      </el-main>
    </el-container>
    <el-form :inline="true" class="alert-search-form" size="small">
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="searchSubmitBtn">请搜索</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="small" icon="el-icon-refresh" @click="refreshAlertBtn">请刷新</el-button>
      </el-form-item>
    </el-form>
    <el-tabs type="border-card" value="all-alert" stretch @tab-click="switchTabEvent">
      <el-tab-pane name="all-alert">
        <span slot="label"><svg-icon icon-class="allalert" /> 全部告警</span>
        <monitor-alert-list :alert-list="alertList" :tab-name="currentTab" @deleteMonitorAlert="deleteMonitorAlert"/>
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
      </el-tab-pane>
      <el-tab-pane name="zabbix-alert">
        <span slot="label"><svg-icon icon-class="linux" /> 系统告警 (zabbix)</span>
        <monitor-alert-list :alert-list="alertList" :tab-name="currentTab" @deleteMonitorAlert="deleteMonitorAlert"/>
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
      </el-tab-pane>
      <el-tab-pane name="cat-alert">
        <span slot="label"><svg-icon icon-class="appalert" /> 应用告警 (cat)</span>
        <monitor-alert-list :alert-list="alertList" :tab-name="currentTab" @deleteMonitorAlert="deleteMonitorAlert"/>
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
      </el-tab-pane>
      <el-tab-pane name="others-alert">
        <span slot="label"><svg-icon icon-class="othersalert" /> 其他告警( MQ..)</span>
        <monitor-alert-list :alert-list="alertList" :tab-name="currentTab" @deleteMonitorAlert="deleteMonitorAlert"/>
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
      </el-tab-pane>
    </el-tabs>
    <!-- 搜索 弹窗 -->
    <el-dialog
      :visible.sync="searchAlertDialogVisible"
      title="搜索告警"
      width="55%"
      center>
      <el-form :inline="true" type="flex" justify="center" label-width="100px" class="searchForm" size="small">
        <el-form-item label="告警标题">
          <el-input v-model="params.title" placeholder="告警标题" />
        </el-form-item>
        <el-form-item label="服务器 IP">
          <el-input v-model="params.server" placeholder="IP 地址" />
        </el-form-item>
        <el-form-item label="告警级别">
          <el-select v-model="params.level" filterable placeholder="请搜索/选择 告警级别">
            <el-option
              v-for="level in alertLevelList"
              :key="level"
              :label="level"
              :value="level"/>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="params.status" filterable placeholder="请搜索/选择 状态">
            <el-option
              v-for="status in alertStatusList"
              :key="status"
              :label="status"
              :value="status"/>
          </el-select>
        </el-form-item>
        <el-form-item label="起始时间">
          <el-date-picker
            v-model="params.start_time_begin"
            type="datetime"
            value-format="timestamp"
            align="center"
            placeholder="选择日期时间"/>
        </el-form-item>
        <el-form-item label="终止时间">
          <el-date-picker
            v-model="params.start_time_end"
            type="datetime"
            value-format="timestamp"
            align="center"
            placeholder="选择日期时间"/>
        </el-form-item>
        <el-form-item class="groupFormButton">
          <el-button @click="resetSearchForm">清空</el-button>
          <el-button type="primary" @click="submitSearchForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getMonitorAlertList, delMonitorAlert, getMonitorAlertStatistics } from '@/api/monitor/monitor'
import MyPage from '@/components/Pagination/index'
import MonitorAlertList from './alert_list'

var date = new Date()
var default_time_end = Date.parse(date)
var default_time_begin = date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)

/* eslint-disable */
export default {
  name: 'MonitorConfig',
  components: {
    MyPage,
    MonitorAlertList
  },
  data: function() {
    return {
      listLoading: false,
      searchAlertDialogVisible: false,
      alertList: [],
      alertStatistics: [],
      alertStatusStatistics: {},
      alertLevelStatistics: {},
      alertSourceStatistics: {},
      alertTriggerStatistics: {},
      currentTab: 'all-alert',
      total: 0,
      params: {
        page: 1,
        page_size: 10,
        source: '',
        start_time_begin: default_time_begin,
        start_time_end: default_time_end,
        level: '',
        statue: '',
        server: ''
      },
      alertLevelList: [
        'Info',
        'Warning',
        'Average',
        'High',
        'Disaster'
      ],
      alertStatusList: [
        'PROBLEM',
        'OK'
      ],
      polar: {
        title: {
          text: '',
          left: 'center',
          textStyle: {
            fontSize: 10,
          },
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: {
          name:'',
          type:'pie',
          radius: ['30%', '60%'],
          // roseType: true,
          label: {
            show: true,
            position: 'outside',
            fontSize: 13,
          },
          data:[]
        }
      },
      newOptions: {
        title: {
          text: ''
        },
        series: {
          name:'',
          data: []
        }
      },
    }
  },
  watch: {
    alertStatistics: function() {
      this.alertStatusStatistics = this.alertStatistics.alert_status_atatistics
      this.alertLevelStatistics = this.alertStatistics.alert_level_atatistics
      this.alertSourceStatistics = this.alertStatistics.alert_source_atatistics
      this.alertTriggerStatistics = this.alertStatistics.alert_trigger_atatistics
    },
    alertStatusStatistics: function() {
      this.newOptions.title.text = "告警状态统计"
      this.newOptions.series.name = "告警状态"
      this.newOptions.series.data = this.alertStatusStatistics
      this.$refs.alertStatusChart.mergeOptions(this.newOptions, false);
    },
    alertLevelStatistics: function() {
      this.newOptions.title.text = "告警级别统计"
      this.newOptions.series.name = "告警级别"
      this.newOptions.series.data = this.alertLevelStatistics
      this.$refs.alertLevelChart.mergeOptions(this.newOptions, false);
    },
    alertSourceStatistics: function() {
      this.newOptions.title.text = "告警来源统计"
      this.newOptions.series.name = "告警来源"
      this.newOptions.series.data = this.alertSourceStatistics
      this.$refs.alertSourceChart.mergeOptions(this.newOptions, false);
    },
    alertTriggerStatistics: function() {
      this.newOptions.title.text = "告警类别统计"
      this.newOptions.series.name = "告警类别"
      this.newOptions.series.data = this.alertTriggerStatistics
      this.$refs.alertTriggerChart.mergeOptions(this.newOptions, false);
    },
  },
  created: function() {
    this.fetchMonitorAlertList()
    this.fetchMonitorAlertStatistics()
  },
  methods: {
    // 获取 monitor item 列表
    fetchMonitorAlertList: function() {
      this.listLoading = true
      getMonitorAlertList(this.params).then(res => {
        this.total = res.count
        this.alertList = res.results
        this.listLoading = false
      })
    },
    // 获取告警统计
    fetchMonitorAlertStatistics: function() {
      getMonitorAlertStatistics(this.params).then(res => {
        this.alertStatistics = res
      })
    },
    // 切换 tab 页
    switchTabEvent(tab, event) {
      if (tab.name === 'zabbix-alert') {
        this.params.source = 'zabbix'
      } else if (tab.name === 'cat-alert') {
        this.params.source = 'cat'
      } else if (tab.name === 'others-alert') {
        this.params.source = 'others'
      } else {
        this.params.source = ''

      }
      this.params.page = 1
      this.currentTab = tab.name
      this.fetchMonitorAlertList()
    },
    // 搜索提交按钮
    searchSubmitBtn: function() {
      this.searchAlertDialogVisible = true
    },
    // 刷新按钮
    refreshAlertBtn: function() {
      this.params.page = 1
      this.params.start_time_end = Date.parse( new Date())
      this.fetchMonitorAlertList()
      this.fetchMonitorAlertStatistics()
    },
    // 提交搜索表单
    submitSearchForm: function() {
      this.params.page = 1
      this.fetchMonitorAlertList()
      this.fetchMonitorAlertStatistics()
      this.searchAlertDialogVisible = false
    },
    // 取消搜索表单提交（清空搜索条件）
    resetSearchForm: function() {
      this.params = {
        page: 1,
        page_size: 10,
        start_time_end: default_time_end,
        start_time_begin: default_time_begin
      }
    },
    // 删除告警
    deleteMonitorAlert: function(row) {
      delMonitorAlert(row.id).then(
        () => {
          this.$message({
            message: `Good,告警 ${row.title} 删除成功`,
            type: 'success'
          })
          this.fetchMonitorAlertList()
          this.fetchMonitorAlertStatistics()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `OH, 删除告警: ${row.title} 失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 列表分页，改变当前页
    ChangeCurrentPage: function(val) {
      this.params.page = val
      this.fetchMonitorAlertList()
    },
    // 列表分页，改变每页显示的行数
    ChangePageSize: function(val) {
      this.params.page_size = val
      this.fetchMonitorAlertList()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.monitor-alert-container {
  margin: 15px 10px 10px;

  .alert-search-form {
    margin: 20px 0px 0px 10px;
    text-align: right;
    .el-form-item:first-child {
      float: left;
    }
  }

  .groupFormButton {
    width: 100%;
    text-align: center;
    margin-bottom: 0px;
  }

  .el-container {
    margin-bottom: 40px;
    margin: 0px 10px;
    padding: 0px;
    border: 1px solid #e6e6e6;
    border-radius: 6px;
  }

  .el-header {
    background-color: #e6e6e6;
    text-align: center;
    line-height:40px;
    border-radius: 2px;
  }

  .el-main {
    text-align: center;
    line-height: 10%;
    padding: 10px 0px;
  }

  .el-tabs {
    margin: 0px 10px 20px;
    min-height: 90%;
    border-radius: 6px;
  }

  .echarts-parts {
    /*margin: 10px auto;*/
    .echarts {
      /*margin: 10px auto;*/
      width: 24%;
      height: 180px;
      float: left;
    }
  }

}
</style>
