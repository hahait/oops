<template>
  <div class="cmdb-container">
    <!-- 添加/搜索 CMDB -->
    <el-form :inline="true" class="cmdb-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addCmdbBtn">添加 CMDB </el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">点击搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 搜索 弹窗 -->
    <el-dialog
      :visible.sync="searchCmdbDialogVisible"
      title="搜索 CMDB 条件"
      width="55%"
      center>
      <el-form :inline="true" type="flex" justify="center" label-width="100px" class="searchForm" size="small">
        <el-form-item label="主机名">
          <el-input v-model="params.hostname" placeholder="主机名" />
        </el-form-item>
        <el-form-item label="实例 ID">
          <el-input v-model="params.instance_id" placeholder="实例 ID" />
        </el-form-item>
        <el-form-item label="管理 IP">
          <el-input v-model="params.ip" placeholder="管理 IP" />
        </el-form-item>
        <el-form-item label="公网 IP">
          <el-input v-model="params.public_ip" placeholder="公网 IP" />
        </el-form-item>
        <el-form-item label="服务器制造商">
          <el-select v-model="params.brand" filterable placeholder="请搜索/选择 服务器制造商" @change="searchBrandChange">
            <el-option
              v-for="brand in manufacturerList"
              :key="brand.id"
              :label="brand.name"
              :value="brand.name">
              <span style="float: left">{{ brand.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ brand.id }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="服务器型号">
          <el-select v-model="params.model" filterable placeholder="请搜索/选择 服务器型号">
            <el-option
              v-for="m in modelList"
              :key="m.id"
              :label="m.name"
              :value="m.name"/>
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="params.type" filterable placeholder="请搜索/选择 类型">
            <el-option
              v-for="type in serverTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="params.status" filterable placeholder="请搜索/选择 状态">
            <el-option
              v-for="status in serverStatus"
              :key="status.value"
              :label="status.label"
              :value="status.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="SN 码">
          <el-input v-model="params.sn_code" placeholder="SN 码" />
        </el-form-item>
        <el-form-item label="服务器环境">
          <el-select v-model="params.env" filterable placeholder="请搜索/选择 环境">
            <el-option
              v-for="env in serverEnv"
              :key="env.value"
              :label="env.label"
              :value="env.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="IDC">
          <el-select v-model="params.idc" filterable placeholder="请搜索/选择 机房" @change="searchIdcChange">
            <el-option
              v-for="idc in idcList"
              :key="idc.id"
              :label="idc.name"
              :value="idc.name">
              <span style="float: left">{{ idc.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ idc.id }}-{{ idc.cn_name }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="机柜">
          <el-select v-model="params.cabinet" filterable placeholder="请搜索/选择 机柜">
            <el-option
              v-for="cabinet in cabinetList"
              :key="cabinet.id"
              :label="cabinet.label"
              :value="cabinet.label"/>
          </el-select>
        </el-form-item>
        <el-form-item class="groupFormButton">
          <el-button @click="resetSearchForm('searchForm')">清空</el-button>
          <el-button type="primary" @click="submitSearchForm('searchForm')">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- CMDB 列表 -->
    <cmdb-list
      v-loading="listLoading"
      :cmdbs="cmdbList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @deleteCmdbObj="deleteCmdbObj"
      @editCmdbBtn="editCmdbBtn($event)"/>
    <!-- CMDB 修改弹窗 -->
    <el-dialog
      :visible.sync="editCmdbDialogVisible"
      :title="'修改 ' + cmdbData.hostname + ' 的 CMDB 信息'"
      width="55%"
      center>
      <cmdb-edit-form
        :idc-list="idcList"
        :cmdb-data="cmdbData"
        :cabinet-data="cabinetList"
        :server-status="serverStatus"
        :server-env="serverEnv"
        @commitEditCmdbObj="commitEditCmdbObj"
        @cancelEditCmdbObj="cancelEditCmdbObj"/>
    </el-dialog>
    <!-- 分页 -->
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
  </div>
</template>

<script>
import { getServerList, editServer, deleteServer } from '@/api/resources/cmdb'
import { getIdcList } from '@/api/resources/idc'
import { getManufacturerList } from '@/api/resources/manufacturer'
import CmdbList from './cmdb_list'
import CmdbEditForm from './cmdb_edit_form'
import MyPage from '@/components/Pagination/index'

export default {
  name: 'CMDB',
  components: {
    CmdbList,
    CmdbEditForm,
    MyPage
  },
  data: function() {
    return {
      cmdbList: [],
      idcList: [],
      cmdbData: [],
      manufacturerList: [],
      cabinetList: [{ id: 0, label: '请先选择IDC,联动更新 机柜信息' }],
      modelList: [{ id: 0, name: '请先选择服务器品牌,联动更新 服务器型号信息' }],
      listLoading: true,
      searchCmdbDialogVisible: false,
      editCmdbDialogVisible: false,
      total: 0,
      serverTypes: [
        { value: 'physical', label: '物理机' },
        { value: 'virtual', label: '虚拟机' },
        { value: 'cloud', label: '云主机' }
      ],
      serverStatus: [
        { value: 'Running', label: '运行中' },
        { value: 'Starting', label: '启动中' },
        { value: 'Stopping', label: '停止中' },
        { value: 'Stopped', label: '已下线' },
        { value: 'Maintenance', label: '维护中' }
      ],
      serverEnv: [
        { value: 'online', label: '生产' },
        { value: 'dev', label: '开发' },
        { value: 'test', label: '测试' },
        { value: 'gray', label: '预发布' }
      ],
      params: {
        page: 1,
        page_size: 10,
        hostname: '',
        instance_id: '',
        ip: '',
        public_ip: '',
        type: '',
        brand: '',
        model: '',
        idc: '',
        cabinet: '',
        status: '',
        env: '',
        sn_code: ''
      }
    }
  },
  created() {
    this.fetchData()
    this.fetchIdcData()
  },
  methods: {
    // 获取 CMDB 列表
    fetchData() {
      this.listLoading = true
      getServerList(this.params).then(res => {
        this.cmdbList = res.results
        this.total = res.count
        this.listLoading = false
      })
    },
    // 获取 IDC 列表
    fetchIdcData() {
      getIdcList({ page_size: 'all' }).then(res => {
        this.idcList = res
      })
    },
    // 获取服务器制造商列表
    fetchManufacturerData() {
      getManufacturerList({ page_size: 'all' }).then(res => {
        this.manufacturerList = res
      })
    },
    // 搜索中根据选择的IDC 联动显示机柜信息
    searchIdcChange: function() {
      this.cabinetList = []
      this.params.cabinet = ''
      var idc_name = this.params.idc
      var cabinet_list = []
      this.idcList.find(function(idc) {
        if (idc.name === idc_name && idc.cabinets) {
          cabinet_list = idc.cabinets
          return true
        } else {
          cabinet_list = [{ 'id': 0, label: '该机房未查到机柜信息' }]
        }
      })
      this.cabinetList = cabinet_list
    },
    // 搜索中根据选择的服务器品牌 联动显示服务器型号
    searchBrandChange: function() {
      this.modeltList = []
      this.params.model = ''
      var brand_name = this.params.brand
      var model_list = []
      this.manufacturerList.find(function(brand) {
        if (brand.name === brand_name && brand.models) {
          model_list = brand.models
          return true
        } else {
          model_list = [{ 'id': 0, name: '该服务器品牌未查到型号信息' }]
        }
      })
      this.modelList = model_list
    },
    // 添加 CMDB
    addCmdbBtn: function() {
      this.$message({
        dangerouslyUseHTMLString: true,
        showClose: true,
        message:
          '<div style="text-align: center"><h3>添加服务器建议</h3>' +
          '<p> 为了保证服务器信息能够持续及时准确的更新,以及持续稳定的为上层应用提供服务</p></br>' +
          '<p>建议在服务器上构建服务器信息定时上报的<b style="color: red"> 脚本或者客户端 </b></p></div>',
        type: 'warning'
      })
    },
    // 修改 CMDB 按钮
    editCmdbBtn: function(row) {
      const cmdb_data = {
        id: row.id,
        hostname: row.hostname,
        ssh_port: row.ssh_port,
        status: row.status,
        env: row.env,
        online_time: row.online_time,
        expired_time: row.expired_time,
        idc: row.idc.id,
        cabinet: row.cabinet.id
      }
      this.cabinetList = []
      this.cmdbData = cmdb_data
      var cabinet_list = []
      this.idcList.find(function(idc) {
        if (idc.id === row.idc.id && idc.cabinets) {
          cabinet_list = idc.cabinets
          return true
        } else {
          cabinet_list = [{ 'id': 0, label: '该机房未查到机柜信息' }]
        }
      })
      this.cabinetList = cabinet_list
      this.editCmdbDialogVisible = true
    },
    // 修改 CMDB 表单提交
    commitEditCmdbObj: function(form_data) {
      const { id, ...data } = form_data
      editServer(id, data).then(
        () => {
          this.$message({
            message: `Good,服务器 ${form_data.hostname} 信息更新成功`,
            type: 'success'
          })
          this.cmdbData = {}
          this.cabinetList = []
          this.editCmdbDialogVisible = false
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: `Oh , 更新服务器 ${form_data.hostname} 信息失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 取消 修改 CMDB 表单提交
    cancelEditCmdbObj: function() {
      this.cmdbData = {}
      this.cabinetList = []
      this.editCmdbDialogVisible = false
    },
    // 删除 CMDB
    deleteCmdbObj: function(row) {
      deleteServer(row.id).then(
        () => {
          this.$message({
            message: `Good, CMDB \< ${row.hostname} \> 删除成功 .....`,
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
            message: `Oh , CMDB \< ${row.hostname} \> 删除失败,错误信息: ` + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 搜索按钮
    searchSubmit: function() {
      this.listLoading = true
      this.fetchManufacturerData()
      this.listLoading = false
      this.searchCmdbDialogVisible = true
    },
    // 提交搜索表单
    submitSearchForm: function() {
      this.params.page = 1
      this.fetchData()
      this.searchCmdbDialogVisible = false
    },
    // 取消搜索表单提交（清空搜索条件）
    resetSearchForm: function() {
      this.params = {
        page: 1,
        page_size: 10,
        hostname: '',
        ip: '',
        type: '',
        brand: '',
        model: '',
        idc: '',
        cabinet: '',
        status: ''
      }
    },
    // 列表分页，改变当前页
    ChangeCurrentPage: function(val) {
      this.params.page = val
      this.fetchData()
    },
    // 列表分页，改变每页显示的行数
    ChangePageSize: function(val) {
      this.params.page_size = val
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .cmdb-container{
    .cmdb-form-inline {
      margin: 10px 30px 5px;
      text-align: right;
      .el-form-item:first-child {
        float: left;
      }
    }
    .searchForm, .cabinetDialogForm {
      width: 95%;
      text-align: center;
    }
  }
</style>
