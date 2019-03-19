<template>
  <div class="crontab-periodic-list">
    <!-- 任务周期(crontab) 列表 -->
    <el-table
      :data="crontabPeriodicData"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column
        label="分钟"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.minute }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="小时"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.hour }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="日"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.day_of_month }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="月"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.month_of_year }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="周"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.day_of_week }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="时区"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span>{{ scope.row.timezone }}</span>
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
            @click="crontabPeriodicEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            plain
            @click="crontabPeriodicDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'CrontabPeriodicConfig',
  props: {
    'crontabPeriodicList': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      crontabPeriodicData: this.crontabPeriodicList
    }
  },
  watch: {
    crontabPeriodicList() {
      this.crontabPeriodicData = this.crontabPeriodicList
    }
  },
  methods: {
    // 编辑 Crontab 周期按钮
    crontabPeriodicEdit: function(row) {
      this.$emit('editCrontabPeriodicBtn', row)
    },
    // 删除 Crontab 周期按钮
    crontabPeriodicDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该 Crontab 周期吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteCrontabPeriodicBtn', row.id)
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
.crontab-periodic-list {
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
