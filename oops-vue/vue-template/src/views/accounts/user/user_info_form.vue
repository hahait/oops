<template>
  <div class="user-info-form">
    <!-- 修改用户信息弹窗 -->
    <el-form ref="userInfo" :model="userInfo" :rules="rules" label-width="100px" class="userInfo" size="small">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="userInfoForm.username" placeholder="请输入用户名" readonly disabled/>
      </el-form-item>
      <el-form-item label="中文名" prop="cn_name">
        <el-input v-model="userInfoForm.cn_name" placeholder="请输入用户中文名"/>
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="userInfoForm.phone" placeholder="请输入手机号"/>
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-radio-group v-model="userInfoForm.role">
          <el-radio v-for="(v,k) in role_list" :key="k" :label="k">{{ v }}</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="userInfoForm.email" placeholder="请输入邮箱"/>
      </el-form-item>
      <el-form-item class="userInfoFormButton">
        <el-button @click="resetForm('userInfo')">取 消</el-button>
        <el-button type="primary" @click="submitForm('userInfo')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'UserInfoForm',
  props: {
    userInfo: {
      required: true,
      type: Object,
      default: function() {
        return {
          username: '',
          cn_name: '',
          email: '',
          phone: '',
          role: ''
        }
      }
    }
  },
  data: function() {
    return {
      userInfoForm: this.userInfo,
      role_list: {
        '0': 'Head',
        '1': 'Controller',
        '2': 'Manager',
        '3': 'Employee'
      },
      rules: {
        cn_name: [
          { required: true, message: '请输入中文名', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
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
  watch: {
    userInfo: function() {
      this.userInfoForm = this.userInfo
    }
  },
  methods: {
    // 提交按钮事件
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const data = {
            'id': this.userInfoForm.id,
            'cn_name': this.userInfoForm.cn_name,
            'email': this.userInfoForm.email,
            'phone': this.userInfoForm.phone,
            'role': this.userInfoForm.role }
          this.$emit('changeUserInfo', data)
        } else {
          this.$message({
            message: 'Oh My God, 前端表单验证失败, 不能提交到后端',
            type: 'error'
          })
          return false
        }
      })
    },
    // 取消按钮事件
    resetForm() {
      this.$refs.userInfo.resetFields()
      this.$emit('cancelChangeUserInfo')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .userInfo {
    margin: 0px auto;
    .userInfoFormButton {
      text-align: center;
    }
  }
  .el-select {
    width: 100%;
  }
</style>
