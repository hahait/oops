<template>
  <div class="interval-periodic-forms">
    <!-- 添加弹窗 -->
    <el-form ref="intervalPeriodicForm" :model="intervalPeriodicForm" :rules="rules" label-width="100px" class="intervalPeriodicForm" size="small">
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="时间间隔" prop="every">
              <el-input v-model.number="intervalPeriodicForm.every" placeholder="请输入正整数"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="时间单位" prop="period">
              <el-select v-model="intervalPeriodicForm.period" filterable placeholder="请选择时间单位" style="width: 100%">
                <el-option
                  v-for="s in periodList"
                  :key="s.value"
                  :label="s.label"
                  :value="s.value">
                  <span style="float: left">{{ s.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ s.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content" style="text-align:center;margin: 10px auto 0px;">
            <el-button size="small" @click="resetFormBtn('intervalPeriodicForm')" >取 消</el-button>
            <el-button size="small" type="primary" @click="submitFormBtn('intervalPeriodicForm')">确 定</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'IntervalPeriodicForm',
  props: {
    intervalPeriodicData: {
      required: true,
      type: Object,
      default: function() {
        return {
          every: '',
          period: ''
        }
      }
    }
  },
  data: function() {
    return {
      intervalPeriodicForm: this.intervalPeriodicData,
      periodList: [
        { 'value': 'seconds', 'label': '秒' },
        { 'value': 'minutes', 'label': '分钟' },
        { 'value': 'hours', 'label': '小时' },
        { 'value': 'days', 'label': '天' },
        { 'value': 'microseconds', 'label': '毫秒' }
      ],
      rules: {
        every: [
          { required: true, message: '请填写"时间间隔"', trigger: 'blur' },
          { type: 'number', message: '时间间隔必须为正整数', trigger: 'blur' }
        ],
        period: [
          { required: true, message: '请选择"时间单位"', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    intervalPeriodicData: function() {
      this.intervalPeriodicForm = this.intervalPeriodicData
    }
  },
  methods: {
    submitFormBtn: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('submitIntervalPeriodicForm', this.intervalPeriodicForm)
        } else {
          this.$message({
            message: 'Oh My God, 前端表单验证失败, 不能提交到后端',
            type: 'error'
          })
          return false
        }
      })
    },
    resetFormBtn: function() {
      this.$refs.intervalPeriodicForm.resetFields()
      this.$emit('cancelIntervalPeriodicForm')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.interval-periodic-forms {
  margin: 0px auto;
  .intervalPeriodicFormButton {
    text-align: center;
    .el-form-item__content {
      margin-left: 0px;
    }
  }
}
</style>
