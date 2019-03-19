<template>
  <div class="user-add">
    <!-- 添加弹窗 -->
    <el-form ref="userForm" :model="userForm" :rules="rules" label-width="100px" class="userForm" size="small">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="userForm.username" placeholder="请输入用户名"/>
      </el-form-item>
      <el-form-item label="中文名" prop="cn_name">
        <el-input v-model="userForm.cn_name" placeholder="请输入用户中文名"/>
      </el-form-item>
      <el-form-item label="密码" prop="password" class="passwd-change-input">
        <el-input v-model="userForm.password" type="password" placeholder="请输入密码"/>
        <p style="font-size: 5px;margin: 0px"><span style="color:red">* </span>必须包含大/小写字母,数字及特殊字符!@#$%^&amp;*()_</p>
      </el-form-item>
      <el-form-item label="重复密码" prop="password_repeat">
        <el-input v-model="userForm.password_repeat" type="password" placeholder="请输入重复密码"/>
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="userForm.phone" placeholder="请输入手机号"/>
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-radio-group v-model="userForm.role">
          <el-radio
            v-for="(item, index) in role_list"
            :key="index"
            :label="index">{{ item }}</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="userForm.email" placeholder="请输入邮箱"/>
      </el-form-item>
      <el-form-item class="userFormButton">
        <el-button @click="resetForm('userForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('userForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'UserForm',
  props: {
    userForm: {
      required: true,
      type: Object,
      default: function() {
        return {
          username: '',
          cn_name: '',
          password: '',
          password_repeat: '',
          email: '',
          phone: '',
          role: ''
        }
      }
    }
  },
  data: function() {
    var validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.userForm.password_repeat !== '') {
          this.$refs.userForm.validateField('password_repeat')
        }
        callback()
      }
    }
    var validatePasswordRepaeat = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.userForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      role_list: {
        '0': 'Head',
        '1': 'Controller',
        '2': 'Manager',
        '3': 'Employee'
      },
      rules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        cn_name: [
          { required: true, message: '请输入中文名', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, validator: validatePassword, trigger: 'blur' },
          { min: 8, message: '密码长度至少8个字符，并且必须是同时包含大/小写、数字、字母和特殊字符', trigger: 'blur' }
        ],
        password_repeat: [
          { required: true, validator: validatePasswordRepaeat, trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择用户角色', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入用户手机还', trigger: 'blur' },
          { min: 11, max: 11, message: '手机号长度必须是11位字符', trigger: 'blur' }
        ],
        email: [
          { required: true, type: 'email', message: '请输入用户邮箱', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('userObj', this.userForm)
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
      this.$refs.userForm.resetFields()
      this.$emit('cancel-user-obj')
      // this.$nextTick(() => {
      //   console.log('表单中点了取消按钮,重置表单后: ', this.userForm)
      // })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .userForm {
    margin: 0px auto;
    .userFormButton {
      text-align: center;
    }
    .passwd-change-input {
      margin-bottom: 5px;
    }
  }
.el-select {
  width: 100%;
}
</style>
