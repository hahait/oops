<template>
  <div class="alert-list">
    <!-- 表格内容 -->
    <el-table
      :data="alerts"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="标题"
        align="center"
        min-width="30%">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column
        v-if="tabName === 'all-alert'"
        label="来源"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.source }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="级别"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <el-tag :type="humanizeDisplayLevel(scope.row.level)" :color="humanizeDisplayLevelColor(scope.row.level)" size="small">{{ scope.row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <el-tag :type="humanizeDisplayStatus(scope.row.status)" size="small">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="详情"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <el-popover
            placement="top"
            width="600"
            trigger="hover">
            {{ scope.row.detail }}
            <el-button slot="reference" type="text" size="mini">点击查看</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        v-if="tabName === 'zabbix-alert'"
        label="关联的服务器"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.server }}</span>
        </template>
      </el-table-column>
      <el-table-column
        v-else
        label="关联的应用"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span v-if="scope.row.source === 'zabbix'">{{ scope.row.server }}</span>
          <span v-else>{{ scope.row.server }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="告警时间"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span>{{ scope.row.start_time }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="结束时间"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span>{{ scope.row.end_time }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <el-button type="danger" plain round size="mini" @click="deleteMonitorAlertBtn(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'MonitorAlertList',
  props: {
    'tabName': {
      type: String,
      required: true,
      default: ''
    },
    'alertList': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      alerts: this.alertList
    }
  },
  watch: {
    alertList: function() {
      this.alerts = this.alertList
    }
  },
  methods: {
    humanizeDisplayStatus: function(status) {
      if (status === 'OK') {
        return ''
      } else {
        return 'danger'
      }
    },
    humanizeDisplayLevel: function(level) {
      if (level === 'Info') {
        return 'info'
      } else if (level === 'Warning') {
        return 'warning'
      } else if (level === 'Average') {
        return 'danger'
      } else if (level === 'High') {
        return 'danger'
      } else {
        return 'danger'
      }
    },
    humanizeDisplayLevelColor: function(level) {
      if (level === 'High') {
        return '#f5cde1'
      } else if (level === 'Disaster') {
        return '#f99fb8'
      } else {
        return ''
      }
    },
    changeMonitorAlertBtn: function(row) {
      console.log(row)
    },
    deleteMonitorAlertBtn: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该监控项: \< ${row.title} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteMonitorAlert', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.alert-list {
  margin: 5px 0px 10px;
}

.el-popover {
  background-color: #adaeaf;
  padding: 5px;
}

.el-popper[x-placement^=top] .popper__arrow::after {
  border-top-color: #adaeaf;
}
</style>
