<template>
  <div class="taskperiodic-container">
    <!-- 添加按钮 -->
    <el-form :inline="true" class="periodic-add-form" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addCrontabPeriodicBtn">添加 Crontab </el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="small" @click="addIntervalPeriodicBtn">添加 Interval</el-button>
      </el-form-item>
    </el-form>
    <!-- 周期列表 -->
    <el-tabs type="border-card" value="crontab-periodic" stretch @tab-click="switchTabEvent">
      <el-tab-pane name="crontab-periodic">
        <span slot="label"><svg-icon icon-class="crontabperiodicconfig" /> Crontab 周期配置</span>
        <crontab-periodic-config
          :crontab-periodic-list="crontabPeriodicList"
          @editCrontabPeriodicBtn="editCrontabPeriodicBtn"
          @deleteCrontabPeriodicBtn="deleteCrontabPeriodicBtn"
        />
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCrontabCurrentPage" @SizeChange="ChangeCrontabPageSize"/>
      </el-tab-pane>
      <el-tab-pane name="interval-periodic">
        <span slot="label"><svg-icon icon-class="intervalperiodicconfig" /> Interval 周期配置</span>
        <interval-periodic-config
          :interval-periodic-list="intervalPeriodicList"
          @editIntervalPeriodicBtn="editIntervalPeriodicBtn"
          @deleteIntervalPeriodicBtn="deleteIntervalPeriodicBtn"
        />
        <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeIntervalCurrentPage" @SizeChange="ChangeIntervalPageSize"/>
      </el-tab-pane>
    </el-tabs>
    <!-- 添加/修改 crontab 周期弹框 -->
    <el-dialog
      :visible.sync="crontabPeriodicDialogVisible"
      width="40%"
      title="Crontab 周期配置信息"
      center>
      <crontab-periodic-form
        :crontab-periodic-data = "crontabPeriodicData"
        @submitCrontabPeriodicForm="submitCrontabPeriodic"
        @cancelCrontabPeriodicForm="cancelCrontabPeriodic"
      />
    </el-dialog>
    <!-- 添加/修改 interval 周期弹框 -->
    <el-dialog
      :visible.sync="intervalPeriodicDialogVisible"
      width="40%"
      title="Interval 周期配置信息"
      center>
      <interval-periodic-form
        :interval-periodic-data = "intervalPeriodicData"
        @submitIntervalPeriodicForm="submitIntervalPeriodic"
        @cancelIntervalPeriodicForm="cancelIntervalPeriodic"
      />
    </el-dialog>
  </div>
</template>

<script>
import MyPage from '@/components/Pagination'
import { getTaskCrontabPeriodicList, addTaskCrontabPeriodic, editTaskCrontabPeriodic, deleteTaskCrontabPeriodic } from '@/api/taskschedule/task_crontab_periodic'
import { getTaskIntervalPeriodicList, addTaskIntervalPeriodic, editTaskIntervalPeriodic, deleteTaskIntervalPeriodic } from '@/api/taskschedule/task_interval_periodic'
import CrontabPeriodicConfig from './crontab_periodic_config'
import IntervalPeriodicConfig from './interval_periodic_config'
import CrontabPeriodicForm from './crontab_periodic_form'
import IntervalPeriodicForm from './interval_periodic_form'

export default {
  name: 'TaskPeriodicManage',
  components: {
    MyPage,
    CrontabPeriodicConfig,
    IntervalPeriodicConfig,
    CrontabPeriodicForm,
    IntervalPeriodicForm
  },
  data: function() {
    return {
      listLoading: true,
      crontabPeriodicList: [],
      intervalPeriodicList: [],
      crontabPeriodicDialogVisible: false,
      intervalPeriodicDialogVisible: false,
      crontabPeriodicData: {},
      intervalPeriodicData: {},
      total: 0,
      params: {
        page: 1,
        page_size: 10
      }
    }
  },
  created() {
    this.fetchCrontabPeriodicData()
  },
  methods: {
    // 获取任务周期(crontab)列表
    fetchCrontabPeriodicData: function() {
      this.listLoading = true
      getTaskCrontabPeriodicList(this.params).then(res => {
        this.total = res.count
        this.crontabPeriodicList = res.results
        this.listLoading = false
      })
    },
    // 获取任务周期(interval)列表
    fetchIntervalPeriodicData: function() {
      this.listLoading = true
      getTaskIntervalPeriodicList(this.params).then(res => {
        this.total = res.count
        this.intervalPeriodicList = res.results
        this.listLoading = false
      })
    },
    // 添加 Crontab 周期按钮
    addCrontabPeriodicBtn: function() {
      this.crontabPeriodicData = {}
      this.crontabPeriodicDialogVisible = true
    },
    // 添加 Interval 周期按钮
    addIntervalPeriodicBtn: function() {
      this.intervalPeriodicData = {}
      this.intervalPeriodicDialogVisible = true
    },
    // 编辑 Crontab 周期按钮
    editCrontabPeriodicBtn: function(row) {
      const newCrontabValue = row
      this.crontabPeriodicData = { ...newCrontabValue }
      this.crontabPeriodicDialogVisible = true
    },
    // 编辑 Interval 周期按钮
    editIntervalPeriodicBtn: function(row) {
      const newIntervalValue = row
      this.intervalPeriodicData = { ...newIntervalValue }
      this.intervalPeriodicDialogVisible = true
    },
    // 删除 Crontab 周期按钮
    deleteCrontabPeriodicBtn: function(crontab_id) {
      deleteTaskCrontabPeriodic(crontab_id).then(
        () => {
          this.$message({
            message: `Good, Crontab 周期删除成功....`,
            type: 'success'
          })
          this.fetchCrontabPeriodicData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,Crontab 周期删除失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 删除 Interval 周期按钮
    deleteIntervalPeriodicBtn: function(interval_id) {
      deleteTaskIntervalPeriodic(interval_id).then(
        () => {
          this.$message({
            message: `Good, Interval 周期删除成功....`,
            type: 'success'
          })
          this.fetchIntervalPeriodicData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,Interval 周期删除失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 提交 Crontab 周期表单(添加和修改)
    submitCrontabPeriodic: function(crontab_data) {
      if (crontab_data.id) {
        const { id, ...data } = crontab_data
        editTaskCrontabPeriodic(id, data).then(
          () => {
            this.$message({
              message: 'Good,Crontab 配置信息更新成功',
              type: 'success'
            })
            this.crontabPeriodicData = {}
            this.crontabPeriodicDialogVisible = false
            this.fetchCrontabPeriodicData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh ,修改 Crontab 配置信息失败, 错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        addTaskCrontabPeriodic(crontab_data).then(
          () => {
            this.$message({
              message: 'Good, Crontab 周期创建成功',
              type: 'success'
            })
            this.crontabPeriodicData = {}
            this.crontabPeriodicDialogVisible = false
            this.fetchCrontabPeriodicData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh, Crontab 周期创建失败, 错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 提交 Interval 周期表单(添加和修改)
    submitIntervalPeriodic: function(interval_data) {
      if (interval_data.id) {
        const { id, ...data } = interval_data
        editTaskIntervalPeriodic(id, data).then(
          () => {
            this.$message({
              message: 'Good,Interval 配置信息更新成功',
              type: 'success'
            })
            this.intervalPeriodicData = {}
            this.intervalPeriodicDialogVisible = false
            this.fetchIntervalPeriodicData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh ,修改 Interval 配置信息失败, 错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        addTaskIntervalPeriodic(interval_data).then(
          () => {
            this.$message({
              message: 'Good, Interval 周期创建成功',
              type: 'success'
            })
            this.intervalPeriodicData = {}
            this.intervalPeriodicDialogVisible = false
            this.fetchIntervalPeriodicData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh, Interval 周期创建失败, 错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 取消提交 Crontab 周期表单
    cancelCrontabPeriodic: function() {
      this.crontabPeriodicData = {}
      this.crontabPeriodicDialogVisible = false
    },
    // 取消提交 Interval 周期表单
    cancelIntervalPeriodic: function() {
      this.intervalPeriodicData = {}
      this.intervalPeriodicDialogVisible = false
    },
    // 切换 tab 页
    switchTabEvent: function(tab, event) {
      if (tab.name === 'crontab-periodic') {
        this.params.page = 1
        this.fetchCrontabPeriodicData()
      } else {
        this.params.page = 1
        this.fetchIntervalPeriodicData()
      }
    },
    // Crontab 周期分页改变页码
    ChangeCrontabCurrentPage: function(val) {
      this.params.page = val
      this.fetchCrontabPeriodicData()
    },
    // Crontab 周期分页改变展示的数据行数
    ChangeCrontabPageSize: function(val) {
      this.params.page_size = val
      this.fetchCrontabPeriodicData()
    },
    // Interval 周期分页改变页码
    ChangeIntervalCurrentPage: function(val) {
      this.params.page = val
      this.fetchIntervalPeriodicData()
    },
    // Interval 周期分页改变展示的数据行数
    ChangeIntervalPageSize: function(val) {
      this.params.page_size = val
      this.fetchIntervalPeriodicData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .taskperiodic-container {
    margin: 20px 10px 10px;
    .periodic-add-form {
      margin-left: 8px;
      margin-bottom: 0px;
      text-align: left;
      .el-form-item:last-child {
        float: right;
      }
    }
    .appFormButton {
      width: 100%;
      text-align: center;
      margin-bottom: 0px;
    }
  }
</style>
