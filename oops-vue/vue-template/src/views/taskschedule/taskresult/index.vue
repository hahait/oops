<template>
  <div class="taskresult-container">
    <!-- 搜索任务执行结果 -->
    <el-form :inline="true" class="task-result-search-form" size="small">
      <el-form-item>
        <el-input v-model="params.name" placeholder="任务名称" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.uuid" placeholder="任务ID" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.args" placeholder="任务位置参数" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.kwargs" placeholder="任务关键字参数" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.result" placeholder="任务执行结果" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">点击搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 任务执行结果列表 -->
    <task-result-list :result-list="taskResultList"/>
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
  </div>
</template>

<script>
import MyPage from '@/components/Pagination'
import { getTaskResultList } from '@/api/taskschedule/taskresult'
import TaskResultList from './task_result_list'

export default {
  name: 'TaskResult',
  components: {
    MyPage,
    TaskResultList
  },
  data: function() {
    return {
      listLoading: true,
      taskResultList: [],
      total: 0,
      params: {
        page: 1,
        page_size: 10,
        name: '',
        uuid: '',
        args: '',
        kwargs: '',
        result: ''
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
      getTaskResultList(this.params).then(res => {
        this.total = res.count
        this.taskResultList = res.results
        this.listLoading = false
      })
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
  .taskresult-container {
    margin: 20px 10px 10px;
    .task-result-search-form {
      margin: 10px 0px 0px 10px;
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
