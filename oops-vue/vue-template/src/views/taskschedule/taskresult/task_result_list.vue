<template>
  <div class="task-result-list">
    <!-- 任务执行结果列表 -->
    <el-table
      :data="resultList"
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
        label="任务ID"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.uuid }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayStatus(scope.row.state).type" size="small">{{ humanDisplayStatus(scope.row.state).value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="位置参数"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-popover
            :title="'任务 ' + scope.row.uuid + ' 位置参数'"
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
            :title="'任务 ' + scope.row.uuid + ' 关键字参数'"
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
        label="执行结果"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-popover
            :title="'任务 ' + scope.row.uuid + ' 执行结果'"
            placement="top"
            width="800"
            trigger="click">
            {{ scope.row.result }}
            <el-button slot="reference" type="text" size="mini" plain>
              点击查看
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        label="异常信息"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <el-popover
            :title="'任务 ' + scope.row.uuid + ' 异常信息'"
            placement="top"
            width="800"
            trigger="click">
            {{ scope.row.traceback }}
            <el-button slot="reference" type="text" size="mini" plain>
              点击查看
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        label="开始执行时间"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span>{{ scope.row.started }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="执行耗时(s)"
        align="center"
        min-width="8%">
        <template slot-scope="scope">
          <span>{{ scope.row.runtime }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="执行的Worker"
        align="center"
        min-width="12%">
        <template slot-scope="scope">
          <span>{{ scope.row.worker }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'TaskResultList',
  props: {
    'resultList': {
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
    humanDisplayStatus: function(status) {
      if (status === 'SUCCESS') {
        return { type: 'success', value: '成功' }
      } else if (status === 'FAILURE') {
        return { type: 'danger', value: '失败' }
      } else if (status === 'STARTED') {
        return { type: '', value: '已开始执行' }
      } else if (status === 'REVOKED') {
        return { type: 'warning', value: '已被撤销' }
      } else {
        return { type: 'info', value: status }
      }
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
</style>
