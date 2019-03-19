<template>
  <div class="task-result-list">
    <!-- 任务执行结果列表 -->
    <el-table
      :data="crontabList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column
        label="任务名"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="task"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.task }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayStatus(scope.row.enabled).type" size="small">{{ humanDisplayStatus(scope.row.enabled).value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="调度周期"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <span>{{ scope.row.schedule_period }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="位置参数"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-popover
            :title="'任务 ' + scope.row.name + ' 位置参数'"
            placement="top"
            width="800"
            trigger="click">
            {{ scope.row.args }}
            <el-button slot="reference" type="text" size="mini" plain>
              点击查看
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        label="关键字参数"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-popover
            :title="'任务 ' + scope.row.name + ' 关键字参数'"
            placement="top"
            width="800"
            trigger="click">
            {{ scope.row.kwargs }}
            <el-button slot="reference" type="text" size="mini" plain>
              点击查看
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        label="过期时间"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <span>{{ scope.row.expires }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="最后一次运行时间"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.last_run_at }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="运行次数"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <span>{{ scope.row.total_run_count }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <el-dropdown size="small" trigger="click" placement="bottom-start">
            <el-button type="primary" size="mini" plain>
              编辑<i class="el-icon-arrow-down el-icon--right"/>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-button size="mini" type="text" class="primary-color-btn" plain @click="taskCrontabEditBtn(scope.row)">修改信息</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button size="mini" type="text" class="warning-color-btn" plain @click="taskCrontabNowExecBtn(scope.row)">立即执行</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button size="mini" type="text" class="danger-color-btn" plain @click="taskCrontabDeleteBtn(scope.row)">删除任务</el-button>
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
  name: 'TaskCrontabList',
  props: {
    'crontabList': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
    }
  },
  methods: {
    // 人性化显示状态
    humanDisplayStatus: function(enabled) {
      if (enabled === 'True') {
        return { type: 'success', value: '已激活' }
      } else {
        return { type: 'danger', value: '已禁用' }
      }
    },
    // Crontab 定时任务编辑按钮
    taskCrontabEditBtn: function(row) {
      this.$emit('editCrontabTaskBtn', row)
    },
    // 立即执行 任务
    taskCrontabNowExecBtn: function(row) {
      this.$confirm(`<p style="margin:20px">你确定要立即执行任务: <b style="color:red;">"${row.name}" 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('nowExecCrontabTask', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消执行'
        })
      })
    },
    // Crontab 定时任务删除按钮
    taskCrontabDeleteBtn: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该任务: ${row.name} 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteCrontabTask', row)
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
.el-popover {
  background-color: #d2d2da;
}
.el-popover__title {
  text-align: center;
}
.task-result-list {
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
.primary-color-btn {
  color: #409eff
}
.warning-color-btn {
  color: #e6a23c
}
.danger-color-btn {
  color: #f56c6c
}
</style>
