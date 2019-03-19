<template>
  <div class="user-info-change-form">
    <!-- 修改用户信息弹窗 -->
    <el-form ref="myselfInfo" :model="myselfInfo" :rules="rules" label-width="100px" class="myselfInfo" size="small">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="myselfInfoData.username" placeholder="请输入用户名" readonly disabled/>
      </el-form-item>
      <el-form-item label="中文名" prop="cn_name">
        <el-input v-model="myselfInfoData.cn_name" placeholder="请输入用户中文名"/>
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="myselfInfoData.phone" placeholder="请输入手机号"/>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="myselfInfoData.email" placeholder="请输入邮箱"/>
      </el-form-item>
      <el-form-item class="userInfoFormButton">
        <el-button @click="resetForm('myselfInfo')">取 消</el-button>
        <el-button type="primary" @click="submitForm('myselfInfo')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'MyselfChangeForm',
  props: {
    myselfInfo: {
      required: true,
      type: Object,
      default: function() {
        return {
          username: '',
          cn_name: '',
          email: '',
          phone: ''
        }
      }
    }
  },
  data: function() {
    return {
      myselfInfoData: this.myselfInfo,
      rules: {
        cn_name: [
          { required: true, message: '请输入中文名', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
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
    myselfInfo: function() {
      this.myselfInfoData = this.myselfInfo
    }
  },
  methods: {
    // 确认按钮事件
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const data = {
            'id': this.myselfInfoData.id,
            'cn_name': this.myselfInfoData.cn_name,
            'email': this.myselfInfoData.email,
            'phone': this.myselfInfoData.phone }
          this.$emit('commitChangeMyselfInfo', data)
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
      this.$refs.myselfInfo.resetFields()
      this.$emit('cancelChangeMyselfInfo')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .myselfInfo {
    margin: 0px auto;
    .userInfoFormButton {
      text-align: center;
    }
  }
</style>
