<template>
  <div class="idc-container">
    <!-- 添加/搜索 机房 -->
    <el-form :inline="true" class="idc-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addIdcButton">添加 IDC </el-button>
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.name" placeholder="机房名称" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 机房列表 -->
    <idc-list
      v-loading="listLoading"
      :idcs="idcList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @idcEdit="editIdcObj"
      @idcDelete="deleteIdcObj"/>
    <!-- 分页 -->
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
    <!-- 添加/修改 机房 弹窗 -->
    <el-dialog
      :visible.sync="idcDialogVisible"
      width="40%"
      title="IDC 信息"
      center>
      <idc-form ref="idcForm" :idc-data="idcForm" class="idcDialogForm" @idcObj="commitIdcObj($event)" @cancel-idc-obj="cancelIdcObj"/>
    </el-dialog>
  </div>
</template>

<script>
import { getIdcList, addIdc, editIdc, deleteIdc } from '@/api/resources/idc'
import IdcList from './idc_list'
import MyPage from '@/components/Pagination/index'
import IdcForm from './idc_form'

export default {
  name: 'Idc',
  components: {
    IdcList,
    MyPage,
    IdcForm
  },
  data: function() {
    return {
      idcList: [],
      listLoading: true,
      total: 0,
      idcDialogVisible: false,
      cabinetDialogVisible: false,
      params: {
        page: 1,
        page_size: 10,
        name: ''
      },
      idcForm: {},
      cabinetForm: {}
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    // IDC 添加按钮
    addIdcButton: function() {
      this.idcDialogVisible = true
    },
    // IDC 表单取消按钮
    cancelIdcObj: function() {
      this.idcForm = {}
      this.idcDialogVisible = false
    },
    // 获取 IDC 列表
    fetchData() {
      this.listLoading = true
      getIdcList(this.params).then(res => {
        this.idcList = res.results
        this.total = res.count
        this.listLoading = false
      })
    },
    // 搜索提交
    searchSubmit: function() {
      this.params.page = 1
      this.fetchData()
    },
    // 添加 IDC
    commitIdcObj: function(idc_str) {
      delete idc_str['cabinets']
      if (idc_str.id) {
        const { id, ...data } = idc_str
        console.log('idc_str: ', idc_str)
        editIdc(id, data).then(
          () => {
            this.$message({
              message: 'Good,IDC 更新成功',
              type: 'success'
            })
            // 数据驱动的方式清空表单的值
            this.idcForm = {}
            this.idcDialogVisible = false
            // 组件引用的方式清空表单的值(使用表单提供的事件)
            this.$refs['idcForm'].$refs['idcForm'].resetFields()
            this.fetchData()
          }
        )
      } else {
        addIdc(idc_str).then(
          () => {
            this.$message({
              message: 'Good,IDC 创建成功',
              type: 'success'
            })
            this.idcDialogVisible = false
            this.$refs['idcForm'].$refs['idcForm'].resetFields()
            this.fetchData()
          }
        )
      }
    },
    // 编辑 IDC
    editIdcObj: function(row) {
      const newValue = row
      this.idcForm = { ...newValue }
      this.idcDialogVisible = true
    },
    // 删除 IDC
    deleteIdcObj: function(id) {
      deleteIdc(id).then(
        () => {
          this.$message({
            message: 'Good,IDC 删除成功',
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
            message: 'Oh , 删除IDC失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 添加机柜信息按钮
    addIdcCabinetBtn: function(row) {
      this.cabinetForm = row
      this.cabinetDialogVisible = true
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
.idc-container{
  .idc-form-inline {
    margin: 10px 30px 5px;
    text-align: right;
    .el-form-item:first-child {
      float: left;
    }
  }
  .idcDialogForm, .cabinetDialogForm {
    width: 90%;
  }
}
</style>
