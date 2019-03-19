<template>
  <div class="apps-form">
    <!-- 添加弹窗 -->
    <el-form ref="appForm" :model="appForm" :rules="rules" label-width="100px" class="appForm" size="small">
      <el-row>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="应用名" prop="name">
              <el-input v-model="appForm.name" placeholder="请输入应用名"/>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="端口号" prop="ports">
              <el-input v-model="appForm.ports" placeholder="请填写应用监听的端口号"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="环境" prop="env">
              <el-select v-model="appForm.env" filterable placeholder="请选择应用所属环境">
                <el-option
                  v-for="e in envList"
                  :key="e.value"
                  :label="e.label"
                  :value="e.value"/>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="类型" prop="type">
              <el-select v-model="appForm.type" filterable placeholder="请选择应用类型">
                <el-option
                  v-for="t in typeList"
                  :key="t.value"
                  :label="t.label"
                  :value="t.value"/>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="状态" prop="status">
              <el-select v-model="appForm.status" filterable placeholder="请选择应用状态">
                <el-option
                  v-for="s in statusList"
                  :key="s.value"
                  :label="s.label"
                  :value="s.value"/>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="11">
          <div class="grid-content">
            <el-form-item label="部署方式" prop="manage_team">
              <el-select v-model="appForm.way" filterable placeholder="请选择应用部署方式">
                <el-option
                  v-for="w in wayList"
                  :key="w.value"
                  :label="w.label"
                  :value="w.value"/>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="描述" prop="describe">
              <el-input v-model="appForm.describe" placeholder="请填写应用功能性描述"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="部署路径" prop="path">
              <el-input v-model="appForm.path" placeholder="请填写应用部署路径"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="日志路径" prop="log_path">
              <el-input v-model="appForm.log_path" placeholder="请填写应用日志目录"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="启动脚本" prop="start_script">
              <el-input v-model="appForm.start_script" placeholder="请填写应用启动脚本"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="发布脚本" prop="ansible_playbook">
              <el-input v-model="appForm.ansible_playbook" placeholder="请填写应用的发布脚本"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="22">
          <div class="grid-content">
            <el-form-item label="git 仓库" prop="git">
              <el-input v-model="appForm.git" placeholder="请填写应用的git仓库"/>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content appFormButton">
            <el-button size="small" @click="resetFormBtn" >取 消</el-button>
            <el-button size="small" type="primary" @click="submitFormBtn('appForm')">确 定</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'AppForm',
  props: {
    appData: {
      required: true,
      type: Object,
      default: function() {
        return {
          name: '',
          env: '',
          describe: '',
          path: '',
          ansible_playbook: '',
          start_script: '',
          log_path: '',
          git: '',
          ports: '',
          way: '',
          type: '',
          status: ''
        }
      }
    }
  },
  data: function() {
    return {
      appForm: this.appData,
      envList: [
        { 'value': 'dev', 'label': '开发' },
        { 'value': 'test', 'label': '测试' },
        { 'value': 'online', 'label': '生产' },
        { 'value': 'ops', 'label': '运维' },
        { 'value': 'gray', 'label': '预发布' }
      ],
      wayList: [
        { 'value': '0', 'label': 'tomcat' },
        { 'value': '1', 'label': 'jar' },
        { 'value': '3', 'label': 'node' },
        { 'value': '4', 'label': 'php' },
        { 'value': '5', 'label': '其他' }
      ],
      statusList: [
        { 'value': '0', 'label': '运行中' },
        { 'value': '1', 'label': '待上线' },
        { 'value': '2', 'label': '已停服' }
      ],
      typeList: [
        { 'value': '0', 'label': '核心应用' },
        { 'value': '1', 'label': '一般应用' },
        { 'value': '2', 'label': '中间件' },
        { 'value': '3', 'label': '其他' }
      ],
      rules: {
        name: [
          { required: true, message: '请输入应用名', trigger: 'blur' },
          { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
        ],
        ports: [
          { required: true, message: '请输入应用监听的端口号', trigger: 'blur' },
          { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
        ],
        env: [
          { required: true, message: '请选择应用所属环境', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择应用类型', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请选择应用状态', trigger: 'blur' }
        ],
        way: [
          { required: true, message: '请选择应用部署方式', trigger: 'blur' }
        ],
        describe: [
          { required: true, message: '请简单描述下应用的功能', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入应用部署路径', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        log_path: [
          { required: false, message: '请输入应用的日志路径', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        start_script: [
          { required: true, message: '请输入应用的启动脚本', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        ansible_playbook: [
          { required: false, message: '请输入应用的发布脚本', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ],
        git: [
          { required: false, message: '请输入应用的仓库地址', trigger: 'blur' },
          { min: 3, max: 200, message: '长度在 3 到 200 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    appData: function() {
      this.appForm = this.appData
    }
  },
  methods: {
    submitFormBtn: function(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$emit('submitAppForm', this.appData)
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
      this.$refs.appForm.resetFields()
      this.$emit('cancelAppForm')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .appForm {
    margin: 0px auto;
    .appFormButton {
      text-align: center;
    }
  }
  .el-select {
    width: 100%;
  }
</style>
