<template>
  <div class="group-form">
    <!-- 添加弹窗 -->
    <el-form ref="groupForm" :model="groupForm" :rules="rules" label-width="100px" class="groupForm" size="small">
      <el-form-item label="用户组名" prop="name">
        <el-input v-model="group.name" placeholder="请输入用户组名"/>
      </el-form-item>
      <el-form-item class="groupFormButton">
        <el-button @click="resetForm('groupForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('groupForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'GroupForm',
  props: {
    groupForm: {
      required: true,
      type: Object,
      default: function() {
        return {
          name: ''
        }
      }
    }
  },
  data: function() {
    return {
      group: this.groupForm,
      rules: {
        name: [
          { required: true, message: '请输入用户组名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    groupForm: function() {
      this.group = this.groupForm
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('groupObj', this.group)
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
      this.$refs.groupForm.resetFields()
      this.$emit('cancelGroupObj')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .groupForm {
    margin: 0px auto;
    .groupFormButton {
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
