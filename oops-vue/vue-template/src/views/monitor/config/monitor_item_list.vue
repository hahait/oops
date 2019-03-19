<template>
  <div class="items-list">
    <!-- 表格内容 -->
    <el-table
      :data="items"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="监控项名称"
        align="center"
        min-width="15%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.item }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控项别名"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.item_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控项 key"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.item_key }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="关联信息"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <el-button type="text" size="mini" plain @click="bindAppsInfo(scope.row)">
            应用 ( {{ scope.row.app_name.length }} ) 个
          </el-button>
          <el-button type="text" size="mini" plain @click="bindServersInfo(scope.row)">
            服务器 ( {{ scope.row.server_count }} ) 台
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        min-width="25%">
        <template slot-scope="scope">
          <el-button type="primary" plain size="mini" @click="changeMonitorItemBtn(scope.row)">编辑</el-button>
          <el-button type="success" plain size="mini" @click="bindAppBtn(scope.row)">关联应用</el-button>
          <el-button type="danger" plain size="mini" @click="deleteMonitorItemBtn(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 查看监控项关联的应用 -->
    <el-dialog
      :visible.sync="viewMonitorItemRelateAppsDialogVisible"
      :title="'查看监控项 <' + row.item_name + '> 关联的应用'"
      width="50%"
      center>
      <el-table
        :data="row.app_name"
        stripe
        border
        size="mini"
        highlight-current-row
        style="min-width: 100%;">
        <el-table-column
          label="ID"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="应用名"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'MonitorItemList',
  props: {
    'items': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      row: {},
      viewMonitorItemRelateAppsDialogVisible: false
    }
  },
  methods: {
    changeMonitorItemBtn: function(row) {
      this.$emit('changeMonitorItem', row)
    },
    bindAppBtn: function(row) {
      this.$emit('bindApp', row)
    },
    deleteMonitorItemBtn: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该监控项: \< ${row.item_name} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteMonitorItem', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    bindAppsInfo: function(row) {
      this.row = row
      this.viewMonitorItemRelateAppsDialogVisible = true
    },
    bindServersInfo: function(row) {
      this.$emit('bindServersInfo', row.item_key)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.items-list {
  margin: 5px 30px 10px;
}
</style>
