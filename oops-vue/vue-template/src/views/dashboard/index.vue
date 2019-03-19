<template>
  <div class="dashboard-container">
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="5">
        <div class="grid-content server_statistics">
          <div class="grid-head clearfix">
            <div class="grid_left">
              <strong> {{ serverTotalCount }}</strong>
              <p>服务器总数</p>
            </div>
            <div class="grid_right">
              <svg-icon icon-class="linux" />
            </div>
          </div>
          <div class="grid_foot">
            <span >今日增加: {{ serverTodayAddCount }} </span>
            <a href="#" style="float: right;margin-right: 2px">详情 <svg-icon icon-class="right_arrow" style="color: white"/></a>
          </div>
        </div>
      </el-col>
      <el-col :span="5">
        <div class="grid-content apps_statistics">
          <div class="grid-head clearfix">
            <div class="grid_left">
              <strong> {{ appTotalCount }}</strong>
              <p>应用总数</p>
            </div>
            <div class="grid_right">
              <svg-icon icon-class="android" />
            </div>
          </div>
          <div class="grid_foot">
            <span >今日增加: {{ appTodayAddCount }} </span>
            <a href="#" style="float: right;margin-right: 2px">详情 <svg-icon icon-class="right_arrow" style="color: white"/></a>
          </div>
        </div>
      </el-col>
      <el-col :span="5">
        <div class="grid-content workform_statistics">
          <div class="grid-head clearfix">
            <div class="grid_left">
              <strong> {{ workformTotalCount }}</strong>
              <p>工单总数</p>
            </div>
            <div class="grid_right" style="padding-left: 2px">
              <svg-icon icon-class="workform" />
            </div>
          </div>
          <div class="grid_foot">
            <span >今日增加: {{ workformTodayAddCount }} </span>
            <a href="#" style="float: right;margin-right: 2px">详情 <svg-icon icon-class="right_arrow" style="color: white"/></a>
          </div>
        </div>
      </el-col>
      <el-col :span="5">
        <div class="grid-content publish_statistics">
          <div class="grid-head clearfix">
            <div class="grid_left">
              <strong> {{ publishTotalCount }}</strong>
              <p>发布总数</p>
            </div>
            <div class="grid_right" style="padding-left: 3px">
              <svg-icon icon-class="publish" />
            </div>
          </div>
          <div class="grid_foot">
            <span >今日增加: {{ publishTodayAddCount }} </span>
            <a href="#" style="float: right;margin-right: 2px">详情 <svg-icon icon-class="right_arrow" style="color: white"/></a>
          </div>
        </div>
      </el-col>
      <el-col :span="5">
        <div class="grid-content alert_statistics">
          <div class="grid-head clearfix">
            <div class="grid_left">
              <strong> {{ alertTotalCount }}</strong>
              <p>告警总数</p>
            </div>
            <div class="grid_right" style="padding-left: 3px">
              <svg-icon icon-class="dashboard-alert" />
            </div>
          </div>
          <div class="grid_foot">
            <span >今日增加: {{ alertTodayAddCount }}  </span>
            <a href="#" style="float: right;margin-right: 2px">详情 <svg-icon icon-class="right_arrow" style="color: white"/></a>
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="mycarousel">
      <my-carousel
        :server-detail="serverDetail"
        :alert-seven-days-detail="alertSevenDaysDetail"
        :alert-today-detail="alertTodayDetail"
        :app-detail="appDetail"
        :publish-seven-days-detail="publishSevenDaysDetail"
        :publish-today-detail="publishTodayDetail"
        :workform-seven-days-detail="workformSevenDaysDetail"
        :workform-today-detail="workformTodayDetail"
      />
    </div>
  </div>
</template>

<script>
import { getDashboardCountStatistics, getDashboardSevenDaysStatistics } from '@/api/dashboard/statistics'
import MyCarousel from './mycarousel'

export default {
  name: 'Dashboard',
  components: {
    MyCarousel
  },
  data: function() {
    return {
      listLoading: false,
      countStatisticsData: {},
      sevenDaysData: {},
      serverTotalCount: '',
      serverTodayAddCount: '',
      serverDetail: {},
      appTotalCount: '',
      appTodayAddCount: '',
      appDetail: {},
      alertTotalCount: '',
      alertTodayAddCount: '',
      alertTodayDetail: [],
      alertSevenDaysDetail: {},
      publishTotalCount: '',
      publishTodayAddCount: '',
      publishTodayDetail: [],
      publishSevenDaysDetail: {},
      workformTotalCount: '',
      workformTodayAddCount: '',
      workformTodayDetail: [],
      workformSevenDaysDetail: {}
    }
  },
  created() {
    this.fetchDashboardCountStatistics()
    this.fetchDashboardSevenDaysStatistics()
  },
  methods: {
    fetchDashboardCountStatistics: function() {
      this.listLoading = true
      getDashboardCountStatistics().then(
        res => {
          this.countStatisticsData = res
          this.serverTotalCount = res.cmdb_statistics.total_count
          this.serverTodayAddCount = res.cmdb_statistics.today_add_count
          this.serverDetail = res.cmdb_statistics
          this.alertTotalCount = res.alert_count_statistics.total_count
          this.alertTodayAddCount = res.alert_count_statistics.today_add_count
          this.alertTodayDetail = res.alert_count_statistics.today_add_detail
          this.appTotalCount = res.app_statistics.total_count
          this.appTodayAddCount = res.app_statistics.today_add_count
          this.appDetail = res.app_statistics
          this.publishTotalCount = res.publish_count_statistics.total_count
          this.publishTodayAddCount = res.publish_count_statistics.today_add_count
          this.publishTodayDetail = res.publish_count_statistics.today_add_detail
          this.workformTotalCount = res.workform_count_statistics.total_count
          this.workformTodayAddCount = res.workform_count_statistics.today_add_count
          this.workformTodayDetail = res.workform_count_statistics.today_add_detail
          this.listLoading = false
        }
      )
    },
    fetchDashboardSevenDaysStatistics: function() {
      getDashboardSevenDaysStatistics().then(
        res => {
          this.sevenDaysData = res
          this.alertSevenDaysDetail = res.alert_seven_days_statistics
          this.appSevenDaysDetail = res.app_seven_days_statistics
          this.publishSevenDaysDetail = res.publish_seven_days_statistics
          this.workformSevenDaysDetail = res.workform_seven_days_statistics
        }
      )
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard-container {
  margin: 30px;
  .row-bg {
    background-color: white;
    .grid-content {
      height: 120px;
      margin: 0px 10px;
      border-radius: 10px;
      color: white;
      .grid-head {
        height: 80%;
        .grid_left {
          width: 60%;
          padding: 15px 10px 10px;
          float: left;
          strong {
            font-size: 32px;
          }
          p {
            margin-top: 15px;
            margin-bottom: 5px;
            font-size: 15px;
          }
        }
        .grid_right {
          float: left;
          width: 40%;
          padding-left: 10px;
          .svg-icon {
            width: 4em;
            height: 4em;
            vertical-align: -4.15em;
          }
          .svg-icon:hover {
            width: 4.5em;
            height: 4.5em;
            vertical-align: -4.45em;
          }
        }
      }
      .grid_foot {
        font-size: 10px;
        padding: 5px 10px;
        background-color: rgba(0,0,0,0.1);
        border-bottom-right-radius: 8px;
        border-bottom-left-radius: 8px;
      }
    }
    .server_statistics {
      background-color: #00c0ef !important;
      .svg-icon {
        color: #10a5de
      }
      .svg-icon:hover {
        color: #3ca5ce
      }
    }
    .apps_statistics {
      background-color: #00a65a !important;
      .svg-icon {
        color: #5cca79
      }
      .svg-icon:hover {
        color: #4ed872
      }
    }
    .workform_statistics {
      background-color: #f39c12 !important;
      .svg-icon {
        color: #a7934b
      }
      .svg-icon:hover {
        color: #9a863e
      }
    }
    .publish_statistics {
      background-color: #f312d7 !important;
      .svg-icon {
        color: #c331b1
      }
      .svg-icon:hover {
        color: #b916a5
      }
    }
    .alert_statistics {
      background-color: #dd4b39 !important;
      .svg-icon {
        color: #c52424
      }
      .svg-icon:hover {
        color: #a01515
      }
    }
  }
  .mycarousel {
    margin: 10px 10px;
    border: 2px solid #e6e6e6;
    border-radius: 10px;
  }
}
</style>
