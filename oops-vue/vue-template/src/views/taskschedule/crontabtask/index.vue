<template>
  <div class="taskcrontab-manage-container">
    <!-- 搜索任务执行结果 -->
    <el-form :inline="true" class="task-crontab-manage-search-form" size="small">
      <el-form-item>
        <el-button type="primary" @click="addCrontabTaskBtn">添加 Task</el-button>
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.name" placeholder="名称" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.task" placeholder="task" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">点击搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 定时任务列表 -->
    <task-crontab-list
      :crontab-list="taskCrontabList"
      @editCrontabTaskBtn="editCrontabTaskBtn"
      @deleteCrontabTask="deleteCrontabTask"
      @nowExecCrontabTask="nowExecCrontabTask"
    />
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
    <!-- 添加/修改弹框 -->
    <el-dialog
      :visible.sync="taskCrontabDialogVisible"
      width="50%"
      title="定时任务信息"
      center>
      <task-crontab-form
        :crontab-task-data="taskCrontabInfo"
        :crontab-periodic-data="crontabPeriodicList"
        :interval-periodic-data="intervalPeriodicList"
        :task-registered-list="taskRegisteredList"
        @submitCrontabTaskForm="submitCrontabTaskForm"
        @cancelCrontabTaskForm="cancelCrontabTaskForm"
      />
    </el-dialog>
  </div>
</template>

<script>
import MyPage from '@/components/Pagination'
import { getTaskCrontabList, addTaskCrontab, editTaskCrontab, deleteTaskCrontab, execTaskNow } from '@/api/taskschedule/task_crontab_manage'
import { getTaskRegisteredList } from '@/api/taskschedule/task_registered'
import { getTaskCrontabPeriodicList } from '@/api/taskschedule/task_crontab_periodic'
import { getTaskIntervalPeriodicList } from '@/api/taskschedule/task_interval_periodic'
import TaskCrontabList from './task_crontab_list'
import TaskCrontabForm from './task_crontab_form'
import _ from 'lodash'

export default {
  name: 'TaskCrontabManage',
  components: {
    MyPage,
    TaskCrontabList,
    TaskCrontabForm
  },
  data: function() {
    return {
      listLoading: true,
      taskCrontabList: [],
      total: 0,
      taskCrontabInfo: {},
      taskCrontabDialogVisible: false,
      crontabPeriodicList: [],
      intervalPeriodicList: [],
      taskRegisteredList: [],
      params: {
        page: 1,
        page_size: 10,
        name: '',
        task: ''
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    // 获取应用列表
    fetchData: function() {
      this.listLoading = true
      getTaskCrontabList(this.params).then(res => {
        this.total = res.count
        this.taskCrontabList = res.results
        this.listLoading = false
      })
    },
    // 获取 Crontab 调度周期列表
    fetchCrontabPeriodicList: function() {
      getTaskCrontabPeriodicList({ page_size: 'all' }).then(res => {
        this.crontabPeriodicList = res
      })
    },
    // 获取 Interval 调度周期列表
    fetchIntervalPeriodicList: function() {
      getTaskIntervalPeriodicList({ page_size: 'all' }).then(res => {
        this.intervalPeriodicList = res
      })
    },
    // 获取注册的任务列表
    fetchTaskRegisteredList: async function() {
      await getTaskRegisteredList().then(res => {
        this.taskRegisteredList = res
      })
    },
    // 添加 Crontab 定时任务按钮
    addCrontabTaskBtn: async function() {
      this.fetchCrontabPeriodicList()
      this.fetchIntervalPeriodicList()
      await this.fetchTaskRegisteredList()
      this.taskCrontabInfo = { 'args': '[]', 'kwargs': '{}', 'enabled': 'True' }
      this.taskCrontabDialogVisible = true
    },
    // 编辑 crontab 定时任务按钮
    editCrontabTaskBtn: async function(row) {
      const newCrontabValue = row
      this.fetchCrontabPeriodicList()
      this.fetchIntervalPeriodicList()
      await this.fetchTaskRegisteredList()
      this.taskCrontabInfo = { ...newCrontabValue }
      this.taskCrontabDialogVisible = true
    },
    // 添加/编辑 Crontab 定时任务表单提交
    submitCrontabTaskForm: function(crontab_task_data) {
      if (crontab_task_data.id) {
        const { id, ...data } = crontab_task_data
        editTaskCrontab(id, data).then(
          () => {
            this.$message({
              message: `Good,任务: ${data.name} 信息更新成功`,
              type: 'success'
            })
            this.taskCrontabInfo = {}
            this.taskCrontabDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: `Oh ,任务: ${data.name} 配置信息失败, 错误信息: ` + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        addTaskCrontab(crontab_task_data).then(
          () => {
            this.$message({
              message: `Good, 任务: ${crontab_task_data.name}创建成功`,
              type: 'success'
            })
            this.taskCrontabInfo = {}
            this.taskCrontabDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: `Oh, 任务: ${crontab_task_data.data}创建失败, 错误信息: ` + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 取消 添加/编辑 表单提交
    cancelCrontabTaskForm: function() {
      this.taskCrontabInfo = {}
      this.taskCrontabDialogVisible = false
    },
    // 立即执行 任务
    nowExecCrontabTask: function(row) {
      const data = _.pick(row, ['task', 'args', 'kwargs'])
      execTaskNow(data).then(
        () => {
          this.$message({
            message: `Good,任务: ${data.task} 执行中...请稍后查看结果`,
            type: 'success'
          })
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,任务: ${data.task} 执行失败, 错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 删除 Crontab 定时任务按钮
    deleteCrontabTask: function(crontab_task_data) {
      deleteTaskCrontab(crontab_task_data.id).then(
        () => {
          this.$message({
            message: `Good, 任务: ${crontab_task_data.name} 删除成功....`,
            type: 'success'
          })
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,任务: ${crontab_task_data.name} 删除失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 搜索按钮
    searchSubmit: function() {
      this.params.page = 1
      this.fetchData()
    },
    // 分页改变页码
    ChangeCurrentPage: function(val) {
      this.params.page = val
      this.fetchData()
    },
    // 分页改变展示的数据行数
    ChangePageSize: function(val) {
      this.params.page_size = val
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .taskcrontab-manage-container {
    margin: 20px 10px 10px;
    .task-crontab-manage-search-form {
      margin: 10px 0px 0px 10px;
      text-align: right;
      .el-form-item:first-child {
        float: left;
      }
    }
    .appFormButton {
      width: 100%;
      text-align: center;
      margin-bottom: 0px;
    }
  }
</style>
