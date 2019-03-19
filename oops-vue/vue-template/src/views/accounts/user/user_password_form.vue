<template>
  <div class="change-user-password">
    <!-- 修改密码弹窗 -->
    <el-form ref="changeUserPasswordForm" :model="changeUserPasswordForm" :rules="rules" label-width="100px" class="changeUserPasswordForm" size="small">
      <el-form-item label="密码" prop="password" class="passwd-change-input">
        <el-input v-model="userPasswordData.password" type="password" placeholder="请输入密码"/>
        <p style="font-size: 5px;margin: 0px"><span style="color:red">* </span>必须包含大/小写字母,数字及特殊字符!@#$%^&amp;*()_</p>
      </el-form-item>
      <el-form-item label="重复密码" prop="password_repeat">
        <el-input v-model="userPasswordData.password_repeat" type="password" placeholder="请输入重复密码"/>
      </el-form-item>
      <el-form-item class="changeUserPasswordFormButton">
        <el-button @click="resetForm('changeUserPasswordForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('changeUserPasswordForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'UserPasswordForm',
  props: {
    changeUserPasswordForm: {
      required: true,
      type: Object,
      default: function() {
        return {
          id: '',
          password: '',
          password_repeat: ''
        }
      }
    }
  },
  data: function() {
    var validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.changeUserPasswordForm.password_repeat !== '') {
          this.$refs.changeUserPasswordForm.validateField('password_repeat')
        }
        callback()
      }
    }
    var validatePasswordRepaeat = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.changeUserPasswordForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      userPasswordData: this.changeUserPasswordForm,
      rules: {
        password: [
          { required: true, validator: validatePassword, trigger: 'blur' },
          { min: 8, message: '密码长度至少8个字符，并且必须是同时包含大/小写、数字、字母和特殊字符', trigger: 'blur' }
        ],
        password_repeat: [
          { required: true, validator: validatePasswordRepaeat, trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    changeUserPasswordForm: function() {
      this.userPasswordData = this.changeUserPasswordForm
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('changeUserPassword', this.changeUserPasswordForm)
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
      this.$refs.changeUserPasswordForm.resetFields()
      this.$emit('cancelChangeUserPassword')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .changeUserPasswordForm {
    margin: 0px auto;
    .changeUserPasswordFormButton {
      text-align: center;
      margin-bottom: 10px;
    }
    .passwd-change-input {
      margin-bottom: 5px;
    }
  }
  .el-select {
    width: 100%;
  }
</style>
