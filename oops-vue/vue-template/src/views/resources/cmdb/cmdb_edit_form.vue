<template>
  <div class="cmdb-add">
    <!-- 修改 CMDB 弹窗 -->
    <el-form ref="cmdbForm" :inline="true" :model="cmdbForm" :rules="rules" label-width="100px" class="cmdbForm" size="small">
      <el-form-item label="SSH 端口号" prop="ssh_port">
        <el-input v-model="cmdbForm.ssh_port"/>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="cmdbForm.status" filterable placeholder="请搜索/选择 状态">
          <el-option
            v-for="status in serverStatus"
            :key="status.value"
            :label="status.label"
            :value="status.value"/>
        </el-select>
      </el-form-item>
      <el-form-item label="上架时间" prop="online_time">
        <el-date-picker
          v-model="cmdbForm.online_time"
          type="datetime"
          placeholder="请选择上架时间"/>
      </el-form-item>
      <el-form-item label="过保时间" prop="expired_time">
        <el-date-picker
          v-model="cmdbForm.expired_time"
          type="datetime"
          placeholder="请选择过保时间"/>
      </el-form-item>
      <el-form-item label="机房" prop="idc">
        <el-select v-model="cmdbForm.idc" filterable placeholder="请搜索/选择 机房" @change="editIdcChange">
          <el-option
            v-for="idc in idcList"
            :key="idc.id"
            :label="idc.cn_name"
            :value="idc.id">
            <span style="float: left">{{ idc.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ idc.id }}-{{ idc.cn_name }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="机柜" prop="cabinet">
        <el-select v-model="cmdbForm.cabinet" filterable placeholder="请搜索/选择 机柜">
          <el-option
            v-for="cabinet in cabinetList"
            :key="cabinet.id"
            :label="cabinet.label"
            :value="cabinet.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="环境" prop="env">
        <el-select v-model="cmdbForm.env" filterable placeholder="请搜索/选择 环境">
          <el-option
            v-for="env in serverEnv"
            :key="env.value"
            :label="env.label"
            :value="env.value"/>
        </el-select>
      </el-form-item>
    </el-form>
    <div class="cmdbFormButton">
      <el-button @click="resetForm('cmdbForm')">取 消</el-button>
      <el-button type="primary" @click="submitForm('cmdbForm')">确 定</el-button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'CmdbEditForm',
  props: {
    idcList: {
      required: true,
      type: Array
    },
    cabinetData: {
      required: true,
      type: Array
    },
    serverStatus: {
      required: true,
      type: Array
    },
    serverEnv: {
      required: true,
      type: Array
    },
    cmdbData: {
      required: true,
      type: Object,
      default: function() {
        return {
          ssh_port: '',
          status: '',
          online_time: '',
          expired_time: '',
          idc: '',
          cabinet: '',
          env: ''
        }
      }
    }
  },
  data: function() {
    return {
      cmdbForm: this.cmdbData,
      cabinetList: this.cabinetData,
      idcData: this.idcList,
      rules: {
        ssh_port: [
          { required: true, message: '请输入 SSH 端口号', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请选择状态', trigger: 'blur' }
        ],
        online_time: [
          { required: true, message: '请选择上架时间', trigger: 'blur' }
        ],
        expired_time: [
          { required: true, message: '请选择过保时间', trigger: 'blur' }
        ],
        idc: [
          { required: true, message: '请选择所属机房', trigger: 'blur' }
        ],
        cabinet: [
          { required: true, message: '请选择所在机柜', trigger: 'blur' }
        ],
        env: [
          { required: true, message: '请选择所属环境', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    cabinetData() {
      this.cabinetList = this.cabinetData
    },
    cmdbData() {
      this.cmdbForm = this.cmdbData
    }
  },
  methods: {
    // idc 选项变化后,相应的 机柜选项联动变化
    editIdcChange: function() {
      this.cabinetList = []
      this.cmdbForm.cabinet = ''
      var idc_id = this.cmdbForm.idc
      var cabinet_list = []
      this.idcList.find(function(idc) {
        if (idc.id === idc_id && idc.cabinets) {
          cabinet_list = idc.cabinets
          return true
        } else {
          cabinet_list = [{ 'id': 0, label: '该机房未查到机柜信息' }]
        }
      })
      this.cabinetList = cabinet_list
    },
    // 修改 CMDB 表单提交
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('commitEditCmdbObj', this.cmdbForm)
        } else {
          this.$message({
            message: 'Oh My God, 前端表单验证失败, 不能提交到后端',
            type: 'error'
          })
          return false
        }
      })
    },
    resetForm() {
      this.$refs.cmdbForm.resetFields()
      this.$emit('cancelEditCmdbObj')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .cmdbForm {
    width: 100%;
    /*text-align: center;*/
  }
  .cmdbFormButton {
    text-align: center;
  }
</style>
