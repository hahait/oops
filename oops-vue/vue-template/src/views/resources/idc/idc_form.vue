<template>
  <div class="idc-add">
    <!-- 添加弹窗 -->
    <el-form ref="idcForm" :model="idcForm" :rules="rules" label-width="100px" class="idcForm" size="small">
      <el-form-item label="IDC 简称" prop="name">
        <el-input v-model="idcForm.name"/>
      </el-form-item>
      <el-form-item label="中文名" prop="cn_name">
        <el-input v-model="idcForm.cn_name"/>
      </el-form-item>
      <el-form-item label="联系人" prop="contact_user">
        <el-input v-model="idcForm.contact_user"/>
      </el-form-item>
      <el-form-item label="电话" prop="phone">
        <el-input v-model="idcForm.phone"/>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="idcForm.email"/>
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="idcForm.address"/>
      </el-form-item>
      <el-form-item class="idcFormButton">
        <el-button @click="resetForm('idcForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('idcForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'IdcForm',
  props: {
    idcData: {
      required: true,
      type: Object,
      default: function() {
        return {
          name: '',
          cn_name: '',
          email: '',
          phone: '',
          address: '',
          contact_user: ''
        }
      }
    }
  },
  data: function() {
    return {
      idcForm: this.idcData,
      rules: {
        name: [
          { required: true, message: '请输入 IDC 简称', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        cn_name: [
          { required: true, message: '请输入 IDC 中文名', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        contact_user: [
          { required: false, message: '请输入 IDC 联系人姓名', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: false, message: '请输入 IDC 联系方式', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: false, type: 'email', message: '请输入 IDC 联系邮箱', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入 IDC 联系方式', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    idcData() {
      this.idcForm = this.idcData
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('idcObj', this.idcForm)
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
      this.$refs.idcForm.resetFields()
      this.$emit('cancel-idc-obj')
      // this.$nextTick(() => {
      //   console.log('表单中点了取消按钮,重置表单后: ', this.idcForm)
      // })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.idcForm {
  .idcFormButton {
    text-align: center;
  }
}
</style>
