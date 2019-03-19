<template>
  <div class="zabbix-montorconfig-container">
    <!-- 添加/搜索 机房 -->
    <el-form :inline="true" class="monitor-item-search-form" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addMonitorItemButton">添加监控项</el-button>
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.item_name" placeholder="监控项名称" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.item_key" placeholder="监控项 key" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">搜索</el-button>
      </el-form-item>
    </el-form>
    <monitor-item-list
      v-loading="listLoading"
      :items="itemsList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @changeMonitorItem="changeMonitorItem"
      @bindApp="bindApp"
      @deleteMonitorItem="deleteMonitorItem"
      @bindServersInfo="showServersBindInfo($event)"/>
    <!-- 分页 -->
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
    <!-- 监控项添加/修改 -->
    <el-dialog
      :visible.sync="monitorItemDialogVisible"
      width="40%"
      title="监控项信息"
      center>
      <monitor-item-form :item-form="monitorItemForm" class="monitorItemDialogForm" @commitItemObj="commitItemObj($event)" @cancelCommitForm="cancelCommitItemForm"/>
    </el-dialog>
    <!-- 监控项关联应用 -->
    <el-dialog
      :visible.sync="monitorItemRelateAppDialogVisible"
      :title="'监控项: < '+item.item_name+' > 关联应用'"
      width="50%"
      center>
      <monitor-item-relate-apps
        :item="item"
        :apps="apps"
        class="monitorItemRelateAppsDialogForm"
        @commitMonitorItemRelateAppsBtn="commitMonitorItemRelateApps"/>
    </el-dialog>
    <!-- 查看监控项关联的服务器列表 -->
    <el-dialog
      :visible.sync="viewMonitorItemRelateServersDialogVisible"
      :title="'查看监控项 <' + selectItemRelateServersParams.item_key + '> 关联的服务器列表'"
      width="70%"
      center>
      <el-form :inline="true" size="small" style="margin: 0px 30px;text-align: right;">
        <el-form-item>
          <el-input v-model="selectItemRelateServersParams.server" placeholder="服务器管理 IP" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchItemRelateServersSubmit">搜索</el-button>
        </el-form-item>
      </el-form>
      <monitor-item-relate-servers :items-relate-servers="itemsRelateServersList"/>
      <my-page
        :total="itemRelateServersTotal"
        :page_size="selectItemRelateServersParams.page_size"
        :current_page="selectItemRelateServersParams.page"
        @CurrentChange="changeItemRelateServersCurrentPage"
        @SizeChange="changeItemRelateServersPageSize"/>
    </el-dialog>
  </div>
</template>

<script>
import { getMonitorItemList, addMonitorItem, deleteMonitorItem, editMonitorItem, getMonitorItemBindServerList } from '@/api/monitor/monitor'
import { getAppConfigSimpleList } from '@/api/appmanager/app'
import MonitorItemList from './monitor_item_list'
import MonitorItemForm from './monitor_item_form'
import MonitorItemRelateApps from './monitor_item_relate_app'
import MyPage from '@/components/Pagination/index'
import MonitorItemRelateServers from './monitor_item_relate_servers'
// import _ from 'lodash'

/* eslint-disable */
export default {
  name: 'MonitorConfig',
  components: {
    MonitorItemList,
    MyPage,
    MonitorItemForm,
    MonitorItemRelateApps,
    MonitorItemRelateServers
  },
  data: function() {
    return {
      listLoading: false,
      monitorItemDialogVisible: false,
      monitorItemRelateAppDialogVisible: false,
      viewMonitorItemRelateServersDialogVisible: false,
      item: {},
      apps: [],
      itemsList: [],
      total: 0,
      params: {
        page: 1,
        page_size: 10,
        itme_name: '',
        itme_key: ''
      },
      monitorItemForm: {},
      itemRelateServersTotal: 0,
      itemsRelateServersList: [],
      selectItemRelateServersParams: {
        page: 1,
        page_size: 10,
        server: '',
        itme_key: ''
      }
    }
  },
  created: function() {
    this.fetchMonitorItemList()
  },
  methods: {
    // 获取 monitor item 列表
    fetchMonitorItemList: function() {
      this.listLoading = true
      getMonitorItemList(this.params).then(res => {
        this.total = res.count
        this.itemsList = res.results
        this.listLoading = false
      })
    },
    // 获取监控项 关联的服务器列表
    fetchItemRelateServersInfo: function() {
      this.listLoading = true
      getMonitorItemBindServerList(this.selectItemRelateServersParams).then(
        (res) => {
          this.itemRelateServersTotal = res.count
          this.itemsRelateServersList = res.results
          this.listLoading = false
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `OH, 获取监控项: ${this.selectItemRelateServersParams.item_key} 绑定的服务器列表失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 获取应用列表
    fetchAppList: async function() {
      await getAppConfigSimpleList({ page_size: 'all' }).then(res => {
        this.apps = res
      })
    },
    // 添加监控项按钮
    addMonitorItemButton: function() {
      this.monitorItemDialogVisible = true
    },
    // 搜索提交
    searchSubmit: function() {
      this.params.page = 1
      this.fetchMonitorItemList()
    },
    // 搜索监控项关联的主机信息 提交
    searchItemRelateServersSubmit: function() {
      this.selectItemRelateServersParams.page = 1
      this.fetchItemRelateServersInfo()
    },
    // 添加/更新 监控项 提交
    commitItemObj: function(item_data) {
      if(!item_data.id) {
        addMonitorItem(item_data).then(
          () => {
            this.$message({
              message: 'Good , 监控项添加成功',
              type: 'success'
            })
            this.monitorItemDialogVisible = false
            this.monitorItemForm = {}
            this.fetchMonitorItemList()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'OH,添加失败,信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        const { id, ...data } = item_data
        editMonitorItem(id, data).then(
          () => {
            this.$message({
              message: `Good, 监控项: ${item_data.item_name} 更新成功`,
              type: 'success'
            })
            this.monitorItemForm = {}
            this.monitorItemDialogVisible = false
            this.fetchMonitorItemList()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: `OH,监控项: ${item_data.item_name} 更新失败, 信息: ` + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 添加 监控项 取消
    cancelCommitItemForm: function() {
      this.monitorItemForm = {}
      this.monitorItemDialogVisible = false
    },
    // 编辑 监控项
    changeMonitorItem: function(row) {
      const newValue = row
      this.monitorItemForm = { ...newValue }
      this.monitorItemDialogVisible = true
    },
    // 监控项绑定应用 按钮
    bindApp: async function(row) {
      this.item = row
      await this.fetchAppList()
      this.monitorItemRelateAppDialogVisible = true
    },
    // 修改 监控项关联应用 提交
    commitMonitorItemRelateApps: function(relate_apps_list) {
      const { id, item_name, ...data } = relate_apps_list
      editMonitorItem(id, data).then(
        () => {
          this.$message({
            message: `Good , 监控项 ${item_name} 关联应用成功`,
            type: 'success'
          })
          this.monitorItemRelateAppDialogVisible = false
          this.item = {}
          this.fetchMonitorItemList()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `OH,监控项 ${item_name} 关联应用失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 删除 监控项
    deleteMonitorItem: function(row) {
      deleteMonitorItem(row.id).then(
        () => {
          this.$message({
            message: `Good,监控项 ${row.item_name} 删除成功`,
            type: 'success'
          })
          this.fetchMonitorItemList()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `OH, 删除监控项: ${item_name} 失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 查看 监控项 实际绑定的服务器
    showServersBindInfo: function(item_key) {
      this.selectItemRelateServersParams.item_key = ''
      this.selectItemRelateServersParams.server = ''
      this.selectItemRelateServersParams.item_key = item_key
      this.fetchItemRelateServersInfo()
      this.viewMonitorItemRelateServersDialogVisible = true
    },
    // 列表分页，改变当前页
    ChangeCurrentPage: function(val) {
      this.params.page = val
      this.fetchMonitorItemList()
    },
    // 查看监控项关联服务器列表分页，改变当前页
    changeItemRelateServersCurrentPage: function(val) {
      this.selectItemRelateServersParams.page = val
      this.fetchItemRelateServersInfo()
    },
    // 列表分页，改变每页显示的行数
    ChangePageSize: function(val) {
      this.params.page_size = val
      this.fetchMonitorItemList()
    },
    // 查看监控项关联服务器列表分页，改变每页显示的行数
    changeItemRelateServersPageSize: function(val) {
      this.selectItemRelateServersParams.page_size = val
      this.fetchItemRelateServersInfo()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.zabbix-montorconfig-container {
  margin: 20px 10px 10px;
  .monitor-item-search-form {
    margin: 10px 30px 5px;
    text-align: right;
    .el-form-item:first-child {
      float: left;
    }
  }
  .monitorItemDialogForm, .monitorItemRelateAppsDialogForm {
    width: 90%;
  }
}
</style>
