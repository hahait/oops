<template>
  <div class="task-crontab-forms">
    <!-- 添加/修改弹窗 -->
    <el-form ref="crontabTaskForm" :model="crontabTaskForm" :rules="rules" label-width="120px" class="crontabTaskForm" size="small">
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="任务名称" prop="name">
              <el-input v-model="crontabTaskForm.name" placeholder="请输入名称"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="任务描述" prop="description">
              <el-input v-model="crontabTaskForm.description" type="textarea" placeholder="请输入描述信息"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="注册的task" prop="task">
              <el-select v-model="crontabTaskForm.task" filterable placeholder="请选择一个Task" style="width: 100%">
                <el-option
                  v-for="s in taskRegisteredList"
                  :key="s"
                  :label="s"
                  :value="s"/>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="调度策略" prop="schedule_policy" class="radio-form">
              <el-radio-group v-model="crontabTaskForm.schedule_policy">
                <el-radio label="Crontab">Crontab 调度</el-radio>
                <el-radio label="Interval">Interval 调度</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row v-if="crontabTaskForm.schedule_policy === 'Crontab'">
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="Crontab周期" prop="crontab">
              <el-select v-model="crontabTaskForm.crontab" filterable placeholder="请选择一个 Crontab 调度周期" style="width: 100%">
                <el-option
                  v-for="s in crontabPeriodicData"
                  :key="s.id"
                  :label="s.minute + ' ' + s.hour + ' ' + s.day_of_month + ' ' + s.month_of_year + ' ' + s.day_of_week"
                  :value="s.id">
                  <span style="float: left">{{ s.minute }} {{ s.hour }} {{ s.day_of_month }} {{ s.month_of_year }} {{ s.day_of_week }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">分 时 日 月 周</span>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row v-if="crontabTaskForm.schedule_policy === 'Interval'">
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="Interval周期" prop="interval">
              <el-select v-model="crontabTaskForm.interval" filterable placeholder="请选择一个 Interval 调度周期" style="width: 100%">
                <el-option
                  v-for="s in intervalPeriodicData"
                  :key="s.id"
                  :label="s.every + ' ' + s.period"
                  :value="s.id">
                  <span style="float: left">{{ s.every }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ s.period }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="位置参数" prop="args">
              <el-input v-model="crontabTaskForm.args" placeholder="请输入位置参数信息"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="关键字参数" prop="kwargs">
              <el-input v-model="crontabTaskForm.kwargs" placeholder="请输入关键字参数信息"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="过期时间" prop="expires">
              <el-date-picker
                v-model="crontabTaskForm.expires"
                type="datetime"
                placeholder="选择日期时间"
                style="width: 100%"
                default-time="00:00:00"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="状态" prop="enabled" class="radio-form">
              <el-radio-group v-model="crontabTaskForm.enabled">
                <el-radio label="True">激活</el-radio>
                <el-radio label="False">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content" style="text-align:center;margin: 10px auto 0px;">
            <el-button size="small" @click="resetFormBtn('crontabTaskForm')" >取 消</el-button>
            <el-button size="small" type="primary" @click="submitFormBtn('crontabTaskForm')">确 定</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'TaskCrontabForm',
  props: {
    crontabTaskData: {
      required: true,
      type: Object,
      default: function() {
        return {
          name: '',
          task: '',
          description: '',
          schedule_policy: '',
          crontab: '',
          interval: '',
          args: '[]',
          kwargs: '{}',
          expires: '',
          enabled: 'True'
        }
      }
    },
    crontabPeriodicData: {
      required: true,
      type: Array
    },
    intervalPeriodicData: {
      required: true,
      type: Array
    },
    taskRegisteredList: {
      required: true,
      type: Array
    }
  },
  data: function() {
    var validateCrontab = (rule, value, callback) => {
      if (!value && this.crontabTaskForm.schedule_policy === 'Crontab') {
        callback(new Error('请选择一个 Crontab 调度周期'))
      } else {
        callback()
      }
    }
    var validateInterval = (rule, value, callback) => {
      if (!value && this.crontabTaskForm.schedule_policy === 'Interval') {
        callback(new Error('请选择一个 Interval 调度周期'))
      } else {
        callback()
      }
    }
    return {
      crontabTaskForm: this.crontabTaskData,
      rules: {
        name: [
          { required: true, message: '名称(建议中文名)"', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        task: [
          { required: true, message: '请选择一个 "注册的 Task"', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '任务描述', trigger: 'blur' },
          { min: 3, max: 500, message: '长度在 3 到 500 个字符', trigger: 'blur' }
        ],
        schedule_policy: [
          { required: true, message: '请选择调度策略"', trigger: 'blur' }
        ],
        crontab: [
          { validator: validateCrontab, trigger: 'blur' }
        ],
        interval: [
          { validator: validateInterval, trigger: 'blur' }
        ],
        args: [
          { required: false, message: '任务的位置参数', trigger: 'blur' },
          { min: 0, max: 500, message: '长度在 3 到 500 个字符', trigger: 'blur' }
        ],
        kwargs: [
          { required: false, message: '任务的关键字参数', trigger: 'blur' },
          { min: 0, max: 500, message: '长度在 3 到 500 个字符', trigger: 'blur' }
        ],
        expires: [
          { required: false, message: '请选择过期时间', trigger: 'blur' }
        ],
        enabled: [
          { required: true, message: '请选择是否激活任务', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    crontabTaskData: function() {
      this.crontabTaskForm = this.crontabTaskData
    }
  },
  methods: {
    submitFormBtn: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('submitCrontabTaskForm', this.crontabTaskForm)
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
      this.$refs.crontabTaskForm.resetFields()
      this.$emit('cancelCrontabTaskForm')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.task-crontab-forms {
  margin: 0px auto;
  .radio-form {
    .el-radio:first-child  {
      width: 120px;
      margin-left: 50px;
    }
    .el-radio:last-child  {
      width: 120px;
      margin-left: 100px;
    }
  }
}
</style>
