<template>
  <div class="monitor-item-form">
    <el-form ref="monitorItemForm" :model="itemForm" :rules="rules" label-width="100px" class="monitorItemForm" size="small">
      <el-form-item label="监控项名称" prop="item_name">
        <el-input v-model="itemData.item_name"/>
      </el-form-item>
      <el-form-item label="监控项 key" prop="item_key">
        <el-input v-model="itemData.item_key"/>
        <p style="font-size: 5px;margin: 0px">
          <span style="color:red">* </span>
          必须与 Zabbix 中定义的 item key 一致
        </p>
      </el-form-item>
      <el-form-item class="monitorItemFormButton">
        <el-button @click="resetForm('monitorItemForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('monitorItemForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'MonitorItemForm',
  props: {
    itemForm: {
      required: true,
      type: Object,
      default: function() {
        return {
          item_name: '',
          item_key: ''
        }
      }
    }
  },
  data: function() {
    return {
      itemData: this.itemForm,
      rules: {
        item_name: [
          { required: true, message: '请输入 监控项名称', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        item_key: [
          { required: true, message: '请输入 监控项 key', trigger: 'blur' },
          { min: 2, max: 220, message: '长度在 2 到 220 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    itemForm() {
      this.itemData = this.itemForm
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('commitItemObj', this.itemData)
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
      this.$refs.monitorItemForm.resetFields()
      this.$emit('cancelCommitForm')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.monitorItemForm {
  margin: 0px auto;
  .monitorItemFormButton {
    text-align: center;
  }
}
</style>
