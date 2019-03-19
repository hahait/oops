<template>
  <div class="crontab-periodic-forms">
    <!-- 添加弹窗 -->
    <el-form ref="crontabPeriodicForm" :model="crontabPeriodicForm" :rules="rules" label-width="80px" class="crontabPeriodicForm" size="small">
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="分钟" prop="minute">
              <el-input v-model="crontabPeriodicForm.minute" placeholder="格式: *; 0~60; 10-25; */10; 10,15"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="时" prop="hour">
              <el-input v-model="crontabPeriodicForm.hour" placeholder="格式: *; 1~24; 14,18; 16-18; */6"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="日" prop="day_of_month">
              <el-input v-model="crontabPeriodicForm.day_of_month" placeholder="格式: *; 1~31; 10,15; 20-30; */10"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="月" prop="month_of_year">
              <el-input v-model="crontabPeriodicForm.month_of_year" placeholder="格式: *; 1~12; 8,10; 5-8; */2"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="周" prop="day_of_week">
              <el-input v-model="crontabPeriodicForm.day_of_week" placeholder="格式: *; 1~7; 2,3; 2-4"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content" style="text-align:center;">
            <el-button size="small" type="text">
              <a target="_blank" href="http://www.nncron.ru/help/EN/working/cron-format.htm" >
                Crontab 格式传送门
              </a>
            </el-button>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content" style="text-align:center;margin: 10px auto 0px;">
            <el-button size="small" @click="resetFormBtn" >取 消</el-button>
            <el-button size="small" type="primary" @click="submitFormBtn('crontabPeriodicForm')">确 定</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CrontabPeriodicForm',
  props: {
    crontabPeriodicData: {
      required: true,
      type: Object,
      default: function() {
        return {
          minute: '',
          hour: '',
          day_of_month: '',
          month_of_year: '',
          day_of_week: ''
        }
      }
    }
  },
  data: function() {
    return {
      crontabPeriodicForm: this.crontabPeriodicData,
      rules: {
        minute: [
          { required: true, message: '请填写"分钟"', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5个字符', trigger: 'blur' }
        ],
        hour: [
          { required: true, message: '请填写"时"', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ],
        day_of_month: [
          { required: true, message: '请填写"日"', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ],
        month_of_year: [
          { required: true, message: '请填写"月"', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ],
        day_of_week: [
          { required: true, message: '请填写"周"', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    crontabPeriodicData: function() {
      this.crontabPeriodicForm = this.crontabPeriodicData
    }
  },
  methods: {
    submitFormBtn: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('submitCrontabPeriodicForm', this.crontabPeriodicForm)
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
      this.$refs.crontabPeriodicForm.resetFields()
      this.$emit('cancelCrontabPeriodicForm')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.crontab-periodic-forms {
  margin: 0px auto;
  .crontabPeriodicFormButton {
    text-align: center;
    .el-form-item__content {
      margin-left: 0px;
    }
  }
}
</style>
