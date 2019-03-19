<template>
  <div class="itemRelateServersList">
    <!-- 表格内容 -->
    <el-table
      :data="itemsRelateServersList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="Item ID"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.itemid }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="服务器管理 IP "
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.server.manager_ip }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控周期(s)"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.item_delay }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控值单位"
        align="center"
        min-width="10%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.item_units }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控值存储表"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.history_model_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="监控值趋势存储表"
        align="center"
        min-width="20%">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.trends_model_name }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'MonitorItemRelateServers',
  props: {
    'itemsRelateServers': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      itemsRelateServersList: this.itemsRelateServers
    }
  },
  watch: {
    itemsRelateServers() {
      this.itemsRelateServersList = this.itemsRelateServers
    }
  },
  methods: {
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .itemRelateServersList {
    margin: 5px 30px 10px;
  }
</style>
