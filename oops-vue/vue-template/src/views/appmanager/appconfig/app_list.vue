<template>
  <div class="app-list">
    <!-- 用户组列表 -->
    <el-table
      :data="appList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="部署路径">
              <span>{{ props.row.path }}</span>
            </el-form-item>
            <el-form-item label="发布脚本">
              <span>{{ props.row.ansible_playbook }}</span>
            </el-form-item>
            <el-form-item label="启动脚本">
              <span>{{ props.row.start_script }}</span>
            </el-form-item>
            <el-form-item label="日志路径">
              <span>{{ props.row.log_path }}</span>
            </el-form-item>
            <el-form-item label="管理组">
              <span v-for="mg in props.row.manage_team" :key="mg.id">{{ mg.name }}<br></span>
            </el-form-item>
            <el-form-item label="创建时间">
              <span>{{ props.row.create_time }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="应用名"
        align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="服务器IP"
        align="center">
        <template slot-scope="scope">
          <span v-for="ip in scope.row.server" :key="ip.id">{{ ip.manager_ip }}<br></span>
        </template>
      </el-table-column>
      <el-table-column
        label="描述"
        align="center"
        width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.describe }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="环境"
        align="center">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayEnv(scope.row.env).type" size="small">{{ humanDisplayEnv(scope.row.env).value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayStatus(scope.row.status).type" size="small">{{ humanDisplayStatus(scope.row.status).value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="类型"
        align="center">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayType(scope.row.type).type" size="small">{{ humanDisplayType(scope.row.type).value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="开启的端口"
        align="center">
        <template slot-scope="scope">
          <span v-html="humanDisplayPorts(scope.row.ports)"/>
        </template>
      </el-table-column>
      <el-table-column
        label="最后更新时间"
        align="center"
        width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.last_update_time }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-dropdown size="small" trigger="click" placement="bottom-start">
            <el-button type="primary" size="mini" plain>
              编辑<i class="el-icon-arrow-down el-icon--right"/>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="appConfigBasicEdit(scope.row)">修改基本信息</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="appConfigGroupEditBtn(scope.row)">修改管理组</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="appConfigServerEditBtn(scope.row)">修改所属服务器</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="appConfigDelete(scope.row)">删除应用</el-button>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'AppsList',
  props: {
    'appList': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {

    }
  },
  methods: {
    // 修改应用基本信息
    appConfigBasicEdit: function(row) {
      this.$emit('editAppConfigBasic', row)
    },
    // 修改应用所属服务器
    appConfigServerEditBtn: function(row) {
      this.$emit('editAppConfigServerBtn', row)
    },
    // 修改应用管理组
    appConfigGroupEditBtn: function(row) {
      this.$emit('editAppConfigGroupBtn', row)
    },
    // 删除用户组
    appConfigDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该应用: \< ${row.name} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteAppsConfig', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 人性化显示端口
    humanDisplayPorts: function(ports) {
      if (ports) {
        return ports.replace(/;/g, '<br>')
      } else {
        return ''
      }
    },
    // 人性化显示状态
    humanDisplayStatus: function(status) {
      if (status === '0') {
        return { type: 'success', value: '运行中' }
      } else if (status === '1') {
        return { type: 'warning', value: '待上线' }
      } else {
        return { type: 'danger', value: '已停服' }
      }
    },
    // 人性化显示环境
    humanDisplayEnv: function(env) {
      if (env === 'online') {
        return { type: 'danger', value: '生产' }
      } else if (env === 'gray') {
        return { type: 'warning', value: '灰度' }
      } else if (env === 'dev') {
        return { type: 'info', value: '开发' }
      } else if (env === 'test') {
        return { type: 'info', value: '测试' }
      } else {
        return { type: 'info', value: '运维' }
      }
    },
    // 人性化显示类型
    humanDisplayType: function(type) {
      if (type === '0') {
        return { type: 'danger', value: '核心应用' }
      } else if (type === '1') {
        return { type: 'warning', value: '一般应用' }
      } else if (type === '2') {
        return { type: 'success', value: '中间件' }
      } else {
        return { type: 'info', value: '其他' }
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .app-list {
    margin: 0px 10px 10px;
    .el-table__body-wrapper .el-table__body {
      min-width: 100%;
    }
    .el-table__header-wrapper .el-table__header {
      min-width: 100%;
    }
    .demo-table-expand {
      font-size: 0;
    }
    .demo-table-expand label {
      width: 90px;
      color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
    }
  }
</style>
