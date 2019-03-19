<template>
  <div class="group-permission">
    <!-- 修改组权限弹窗 -->
    <el-table
      :data="permissionList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column
        label="app 名称"
        align="center"
        width="100px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.content_type.app_label }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="模型名称"
        align="center"
        width="180px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.content_type.model }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="CodeName"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.codename }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="描述"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="80px">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            @change="commitChangeGroupPermissionBtn(scope.row)"/>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'GroupPermission',
  props: {
    'permissionList': {
      type: Array,
      required: true
    },
    'permissionRow': {
      type: Object,
      required: true
    },
    'permissionStatus': {
      type: Array,
      required: true,
      default: []
    }
  },
  watch: {
    permissionList() {
      console.log('this.permissionStatusTrue: ', this.permissionStatus)
      this.permissionList.forEach(perms => {
        if (this.permissionStatus.indexOf(perms.id) !== -1) {
          perms.status = true
        } else {
          perms.status = false
        }
      })
    }
  },
  methods: {
    commitChangeGroupPermissionBtn: function(row) {
      const changePermissionList = this.permissionStatus
      if (row.status) {
        changePermissionList.push(row.id)
      } else {
        changePermissionList.pop(row.id)
      }
      const data = { id: this.permissionRow.id, permissions: changePermissionList }
      this.$emit('commitChangeGroupPermission', data)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">

</style>
