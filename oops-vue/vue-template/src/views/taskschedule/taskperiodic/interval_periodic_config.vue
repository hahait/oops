<template>
  <div class="interval-periodic-list">
    <!-- 任务周期(interval) 列表 -->
    <el-table
      :data="intervalPeriodicList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column
        label="时间间隔"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.every }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="时间单位"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.period }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        min-width="12%">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            plain
            @click="intervalPeriodicEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            plain
            @click="intervalPeriodicDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'IntervalPeriodicConfig',
  props: {
    'intervalPeriodicList': {
      type: Array,
      required: true
    }
  },
  methods: {
    intervalPeriodicEdit: function(row) {
      console.log('此时 intervalPeriodicList: ', this.intervalPeriodicList)
      this.$emit('editIntervalPeriodicBtn', row)
    },
    intervalPeriodicDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该 Interval 周期吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteIntervalPeriodicBtn', row.id)
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
.interval-periodic-list {
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
