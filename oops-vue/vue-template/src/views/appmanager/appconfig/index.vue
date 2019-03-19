<template>
  <div class="appconfig-container">
    <el-form :inline="true" class="app-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addAppBtn">添加应用 </el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">点击搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 搜索 弹窗 -->
    <el-dialog
      :visible.sync="searchAppDialogVisible"
      title="搜索 应用 条件"
      width="55%"
      center>
      <el-form :inline="true" type="flex" justify="center" label-width="100px" class="searchForm" size="small">
        <el-form-item label="应用名">
          <el-input v-model="params.name" placeholder="应用名" />
        </el-form-item>
        <el-form-item label="IP 地址">
          <el-input v-model="params.server" placeholder="IP 地址" />
        </el-form-item>
        <el-form-item label="端口">
          <el-input v-model="params.port" placeholder="IP 地址" />
        </el-form-item>
        <el-form-item label="管理组">
          <el-input v-model="params.manage_team" placeholder="管理组" />
        </el-form-item>
        <el-form-item label="环境">
          <el-select v-model="params.env" filterable placeholder="请搜索/选择 环境">
            <el-option
              v-for="env in envList"
              :key="env.value"
              :label="env.label"
              :value="env.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="部署方式">
          <el-select v-model="params.way" filterable placeholder="请搜索/选择 部署方式">
            <el-option
              v-for="way in wayList"
              :key="way.name"
              :label="way.label"
              :value="way.value"/>
          </el-select>
        </el-form-item>
        <el-form-item class="appFormButton">
          <el-button @click="resetSearchForm">清空</el-button>
          <el-button type="primary" @click="submitSearchForm">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- 应用列表 -->
    <apps-list
      :app-list="appList"
      @editAppConfigBasic="editAppConfigBasic"
      @editAppConfigServerBtn="editAppConfigServerBtn"
      @editAppConfigGroupBtn="editAppConfigGroupBtn"
      @deleteAppsConfig="deleteAppsConfig"
    />
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
    <!-- 应用基本信息添加/修改弹窗 -->
    <el-dialog
      :visible.sync="appsFormDialogVisible"
      width="55%"
      title="应用配置信息"
      center>
      <app-form
        :app-data="appFormData"
        @submitAppForm="submitAppForm"
        @cancelAppForm="cancelAppForm"/>
    </el-dialog>
    <!-- 应用的管理组弹窗 -->
    <el-dialog
      :visible.sync="appsGroupsFormDialogVisible"
      :title="'应用 ' + appRow.name + ' 的管理组信息'"
      width="50%"
      center>
      <app-groups
        :app="appRow"
        :get-app-group="appGroup"
        :group-list="groupList"
        @commitChangeAppGroups="commitChangeAppGroups"/>
    </el-dialog>
    <!-- 应用所属的服务器弹窗 -->
    <el-dialog
      :visible.sync="appsServersFormDialogVisible"
      :title="'应用 ' + appRow.name + ' 的服务器信息'"
      width="50%"
      center>
      <app-servers
        :app="appRow"
        :get-app-server="appServer"
        :server-list="serverList"
        @commitChangeAppServers="commitChangeAppServers"/>
    </el-dialog>
  </div>
</template>

<script>
import MyPage from '@/components/Pagination'
import { getAppConfigList, addAppConfig, editAppConfig, deleteAppConfig } from '@/api/appmanager/app'
import { getGroupList } from '@/api/accounts/group'
import { getServerForRelateList } from '@/api/resources/cmdb'
import AppsList from './app_list'
import AppForm from './app_form'
import AppGroups from './app_groups'
import AppServers from './app_servers'

export default {
  name: 'AppConfig',
  components: {
    MyPage,
    AppsList,
    AppForm,
    AppGroups,
    AppServers
  },
  data: function() {
    return {
      listLoading: true,
      searchAppDialogVisible: false,
      appsFormDialogVisible: false,
      appsGroupsFormDialogVisible: false,
      appsServersFormDialogVisible: false,
      appFormData: {},
      appRow: {},
      appGroup: [],
      appServer: [],
      serverList: [],
      groupList: [],
      appList: [],
      envList: [
        { 'value': 'dev', 'label': '开发' },
        { 'value': 'test', 'label': '测试' },
        { 'value': 'online', 'label': '生产' },
        { 'value': 'ops', 'label': '运维' },
        { 'value': 'gray', 'label': '预发布' }
      ],
      wayList: [
        { 'value': '0', 'label': 'tomcat' },
        { 'value': '1', 'label': 'jar' },
        { 'value': '3', 'label': 'node' },
        { 'value': '4', 'label': 'php' },
        { 'value': '5', 'label': '其他' }
      ],
      total: 0,
      params: {
        page: 1,
        page_size: 10,
        name: '',
        server: '',
        manage_team: '',
        env: '',
        way: '',
        port: ''
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
      getAppConfigList(this.params).then(res => {
        this.total = res.count
        this.appList = res.results
        this.listLoading = false
      })
    },
    // 获取用户组列表
    fetchGroupData: async function() {
      await getGroupList({ page_size: 'all' }).then(res => {
        this.groupList = res
      })
    },
    // 获取用户列表
    fetchUserData: async function() {
      this.listLoading = true
      await getServerForRelateList({ page_size: 'all' }).then(res => {
        this.serverList = res
        this.listLoading = false
      })
    },
    // 添加应用
    addAppBtn: function() {
      this.appFormData = {}
      this.appsFormDialogVisible = true
    },
    // 添加/修改 应用信息提交
    submitAppForm: function(app_data) {
      if (app_data.id) {
        delete app_data.server
        delete app_data.manage_team
        const { id, ...data } = app_data
        editAppConfig(id, data).then(
          () => {
            this.$message({
              message: `Good,应用 ${data.name} 配置信息更新成功`,
              type: 'success'
            })
            this.appFormData = {}
            this.appsFormDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: `Oh ,应用 ${data.name},配置信息修改失败, 错误信息: ` + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        addAppConfig(app_data).then(
          () => {
            this.$message({
              message: `Good,应用 ${app_data.name} 创建成功`,
              type: 'success'
            })
            this.appsFormDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: `Oh ,应用 ${app_data.name},创建失败, 错误信息: ` + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 应用信息取消提交
    cancelAppForm: function() {
      this.appFormData = {}
      this.appsFormDialogVisible = false
    },
    // 修改应用配置信息
    editAppConfigBasic: function(row) {
      const newAppconfigValue = row
      this.appFormData = { ...newAppconfigValue }
      this.appsFormDialogVisible = true
    },
    // 修改应用的所属服务器按钮
    editAppConfigServerBtn: async function(row) {
      const newAppRowValue = row
      this.appRow = { ...newAppRowValue }
      this.appServer = row.server.map(function(s) { return s.id })
      await this.fetchUserData()
      this.appsServersFormDialogVisible = true
    },
    // 修改应用的所属服务器
    commitChangeAppServers: function(server_data) {
      const { id, ...data } = server_data
      editAppConfig(id, data).then(
        () => {
          this.$message({
            message: `Good,应用 ${this.appRow.name} 关联服务器更新成功`,
            type: 'success'
          })
          this.appRow = {}
          this.appServer = []
          this.appsServersFormDialogVisible = false
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,应用 ${this.appRow.name} 关联服务器失败, 错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 修改应用所属组按钮
    editAppConfigGroupBtn: async function(row) {
      const newRowValue = row
      this.appRow = { ...newRowValue }
      this.appGroup = row.manage_team.map(function(group) { return group.id })
      await this.fetchGroupData()
      this.appsGroupsFormDialogVisible = true
    },
    // 修改应用所属组提交
    commitChangeAppGroups: function(group_data) {
      const { id, ...data } = group_data
      editAppConfig(id, data).then(
        () => {
          this.$message({
            message: `Good,应用 ${this.appRow.name} 关联管理组更新成功`,
            type: 'success'
          })
          this.appRow = {}
          this.appGroup = []
          this.appsGroupsFormDialogVisible = false
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh ,应用 ${this.appRow.name} 关联管理组失败, 错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 删除应用
    deleteAppsConfig: function(row) {
      deleteAppConfig(row.id).then(
        () => {
          this.$message({
            message: `Good,应用 ${row.name} 删除成功....`,
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
            message: `Oh ,应用 ${row.name} 删除失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 点击搜索
    searchSubmit: function() {
      this.searchAppDialogVisible = true
    },
    // 提交搜索表单
    submitSearchForm: function() {
      this.params.page = 1
      this.fetchData()
      this.searchAppDialogVisible = false
    },
    // 取消搜索表单提交（清空搜索条件）
    resetSearchForm: function() {
      this.params = {
        page: 1,
        page_size: 10,
        name: '',
        server: '',
        env: '',
        way: '',
        manage_team: ''
      }
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
.appconfig-container {
  margin: 20px 10px 10px;
  .app-form-inline {
    margin: 10px 10px 5px;
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
