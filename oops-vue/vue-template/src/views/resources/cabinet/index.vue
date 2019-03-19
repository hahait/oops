<template>
  <div class="idc-container">
    <!-- 添加/搜索 机柜 -->
    <el-form :inline="true" class="cabinet-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addCabinetButton">添加机柜 </el-button>
      </el-form-item>
    </el-form>
    <!-- 机柜列表 -->
    <cabinet-list
      v-loading="listLoading"
      :idc-cabinets="cabinetList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @cabinetEdit="editCabinetObj"
      @cabinetDelete="deleteCabinetObj"/>
    <!-- 添加/修改 机房 弹窗 -->
    <el-dialog
      :visible.sync="cabinetDialogVisible"
      width="40%"
      title="IDC 信息"
      center>
      <cabinet-form ref="cabinetForm" :cabinet-data="cabinetForm" class="cabinetDialogForm" @commitCabinetObj="commitCabinetObj($event)" @cancelCabinetObj="cancelCabinetObj"/>
    </el-dialog>
  </div>
</template>

<script>
import { getIdcObj } from '@/api/resources/idc'
import { addCabinet, editCabinet, deleteCabinet } from '@/api/resources/cabinet'
import MyPage from '@/components/Pagination/index'
import CabinetForm from './cabinet_form'
import CabinetList from './cabinet_list'

export default {
  name: 'Cabinet',
  components: {
    MyPage,
    CabinetForm,
    CabinetList
  },
  data: function() {
    return {
      cabinetList: {},
      listLoading: true,
      cabinetDialogVisible: false,
      cabinetForm: {}
    }
  },
  created() {
    this.getCabinetList()
  },
  methods: {
    // 机柜添加按钮
    addCabinetButton: function() {
      this.cabinetForm = {}
      this.cabinetDialogVisible = true
    },
    // 机柜 表单取消按钮
    cancelCabinetObj: function() {
      this.cabinetForm = {}
      this.cabinetDialogVisible = false
    },
    // 获取 机柜 列表
    getCabinetList: function() {
      const idc_id = this.$route.params.idc_id
      this.listLoading = true
      getIdcObj(idc_id).then(res => {
        this.cabinetList = res
        this.listLoading = false
      })
    },
    // 提交 添加/编辑 机柜表单
    commitCabinetObj: function(cabinet_str) {
      const cabinet_data = { idc: this.cabinetList.id, ...cabinet_str }
      if (!cabinet_str.id) {
        // 添加
        addCabinet(cabinet_data).then(
          () => {
            this.$message({
              message: 'Good,机柜添加成功....',
              type: 'success'
            })
            this.cabinetDialogVisible = false
            this.getCabinetList()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh ,添加机柜失败,错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        // 修改
        const { id, ...data } = cabinet_data
        editCabinet(id, data).then(
          () => {
            this.$message({
              message: 'Good,机柜修改成功....',
              type: 'success'
            })
            this.cabinetDialogVisible = false
            this.getCabinetList()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh ,添加修改失败,错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 编辑机柜按钮
    editCabinetObj: function(row) {
      const newCabinetabValue = row
      this.cabinetForm = { ...newCabinetabValue }
      this.cabinetDialogVisible = true
    },
    // 删除 机柜
    deleteCabinetObj: function(id) {
      deleteCabinet(id).then(
        () => {
          this.$message({
            message: 'Good,机柜删除成功....',
            type: 'success'
          })
          this.getCabinetList()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh ,添加删除失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .idc-container{
    .cabinet-form-inline {
      margin: 10px 30px 5px;
      text-align: right;
      .el-form-item:first-child {
        float: left;
      }
    }
    .cabinetDialogForm {
      width: 90%;
    }
  }
</style>
