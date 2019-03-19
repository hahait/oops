<template>
  <div class="idc-list">
    <!-- 表格内容 -->
    <el-table
      :data="idcs"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="名称"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="中文名"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.cn_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="联系人"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.contact_user }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="电话"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="地址"
        align="center"
        width="220px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.address }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="邮箱"
        align="center"
        width="200px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="120px">
        <template slot-scope="scope">
          <el-dropdown size="small" trigger="click" placement="bottom-start">
            <el-button type="primary" size="mini" plain>
              编辑<i class="el-icon-arrow-down el-icon--right"/>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="handleIdcEdit(scope.row)">修改 IDC 信息</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini">
                  <router-link :to="{ name: 'cabinet',params: { idc_id: scope.row.id } }">机柜管理</router-link>
                </el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="handleIdcDelete(scope.row)">删除 IDC</el-button>
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
  name: 'IdcList',
  props: {
    'idcs': {
      type: Array,
      required: true
    }
  },
  methods: {
    handleIdcEdit(row) {
      this.$emit('idcEdit', row)
    },
    handleIdcDelete(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该IDC: \< ${row.name} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('idcDelete', row.id)
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

<style rel="stylesheet/scss" lang="scss" scoped>
.idc-list {
  margin: 5px 30px 10px;
}
</style>
