<template>
  <div class="cabinet-add">
    <!-- 添加弹窗 -->
    <el-form ref="cabinetForm" :model="cabinetForm" :rules="rules" label-width="100px" class="idcForm" size="small">
      <el-form-item label="机柜标签" prop="label">
        <el-input v-model="cabinetForm.label"/>
      </el-form-item>
      <el-form-item label="机柜描述" prop="description">
        <el-input v-model="cabinetForm.description"/>
      </el-form-item>
      <el-form-item label="机柜电源" prop="power">
        <el-input v-model="cabinetForm.power"/>
      </el-form-item>
      <el-form-item class="cabinetFormButton">
        <el-button @click="resetForm('cabinetForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('cabinetForm')">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'CabinetForm',
  props: {
    cabinetData: {
      required: true,
      type: Object,
      default: function() {
        return {
          label: '',
          description: '',
          power: ''
        }
      }
    }
  },
  data: function() {
    return {
      cabinetForm: this.cabinetData,
      rules: {
        label: [
          { required: true, message: '请输入 机柜标签', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入 机柜描述信息', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        power: [
          { required: true, message: '请输入 机柜电源信息', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    cabinetData() {
      this.cabinetForm = this.cabinetData
    }
  },
  methods: {
    submitForm: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('commitCabinetObj', this.cabinetForm)
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
      this.$refs.cabinetForm.resetFields()
      this.$emit('cancelCabinetObj')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .idcForm {
    .cabinetFormButton {
      text-align: center;
    }
  }
</style>
