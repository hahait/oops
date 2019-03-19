<template>
  <div class="group-list">
    <!-- 用户组列表 -->
    <el-table
      :data="groupList"
      stripe
      border
      size="mini"
      highlight-current-row
      style="min-width: 100%;">
      <el-table-column
        label="组名"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="用户管理"
        align="center">
        <template slot-scope="scope">
          <el-button type="text" size="mini" plain @click="viewGroupUser(scope.row)">
            查看 ( {{ scope.row.user.length }} ) 人
          </el-button>
          <el-button type="text" size="mini" plain @click="changeGroupUser(scope.row)">
            修改 成员
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        label="API 权限管理"
        align="center">
        <template slot-scope="scope">
          <el-button type="text" size="mini" plain @click="viewGroupPermisssion(scope.row)">
            查看 ( {{ scope.row.permissions.length }} ) 个
          </el-button>
          <el-button type="text" size="mini" plain @click="changeGroupPermisssionBtn(scope.row)">
            修改 权限
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            plain
            @click="groupEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            plain
            @click="groupDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 查看组内用户弹窗 -->
    <el-dialog
      :visible.sync="viewGroupsUsersDialogVisible"
      :title="'查看组 ' + row.name + ' 关联的用户'"
      width="50%"
      center>
      <el-table
        :data="row.user"
        stripe
        border
        size="mini"
        highlight-current-row
        style="min-width: 100%;">
        <el-table-column
          label="用户名"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.username }}</span>
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
          label="状态"
          align="center">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.is_active"
              disabled/>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <!-- 修改组内用户弹窗 -->
    <el-dialog
      :visible.sync="changeGroupsUsersDialogVisible"
      :title="'修改组 '+ row.name +' 关联的用户'"
      width="50%"
      center>
      <div style="text-align:center">
        <el-transfer
          v-model="users"
          :props="{
            key: 'id',
            label: 'username'
          }"
          :data="userList"
          :titles="['用户列表', '已加入的用户']"
          :button-texts="['取消加入', '加入该组']"
          :format="{
            noChecked: '${total}',
            hasChecked: '${checked}/${total}'
          }"
          filterable
          filter-placeholder="在当前页搜索用户名"
          target-order="push"
          style="text-align: left; display: inline-block">
          <span slot-scope="{ option }">{{ option.id }} - {{ option.username }}</span>
          <div slot="right-footer" style="text-align: center;">
            <el-button class="transfer-footer" size="small" @click="commitChange">
              操作
            </el-button>
          </div>
        </el-transfer>
      </div>
    </el-dialog>
    <!-- 查看组的权限弹窗 -->
    <el-dialog
      :visible.sync="viewGroupsPermissionsDialogVisible"
      :title="'查看组 ' + row.name + ' 的权限'"
      width="50%"
      center>
      <el-table
        :data="row.permissions"
        stripe
        border
        size="mini"
        highlight-current-row
        style="min-width: 100%;">
        <el-table-column
          label="CodeName"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.codename }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="名称"
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
  name: 'GroupList',
  props: {
    'userList': {
      type: Array,
      required: true
    },
    'groupList': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      row: {},
      users: [],
      viewGroupsUsersDialogVisible: false,
      changeGroupsUsersDialogVisible: false,
      viewGroupsPermissionsDialogVisible: false
    }
  },
  methods: {
    // 查看组内成员
    viewGroupUser: function(row) {
      this.viewGroupsUsersDialogVisible = true
      this.row = row
    },
    // 修改组内成员按钮
    changeGroupUser: function(row) {
      const group_user_list = row.user
      var uid_list = []
      for (var u in group_user_list) {
        uid_list.push(group_user_list[u]['id'])
      }
      this.row = row
      this.users = uid_list
      this.changeGroupsUsersDialogVisible = true
    },
    // 修改组内成员提交
    commitChange: function() {
      const data = { id: this.row.id, user: this.users }
      this.$emit('commitChangeGroupUser', data)
    },
    // 查看组内权限
    viewGroupPermisssion: function(row) {
      this.row = row
      this.viewGroupsPermissionsDialogVisible = true
    },
    // 修改组内权限
    changeGroupPermisssionBtn: function(row) {
      this.$emit('changeGroupPermisssion', row)
    },
    // 编辑用户组
    groupEdit: function(row) {
      this.$emit('editGroup', row)
    },
    // 删除用户组
    groupDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该用户组: \< ${row.name} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteGroup', row)
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
  .group-list {
    margin: 0px 10px 10px;
    .el-table__body-wrapper .el-table__body {
      min-width: 100%;
    }
    .el-table__header-wrapper .el-table__header {
      min-width: 100%;
    }
    .el-transfer-panel__list {
      padding-bottom: 40px;
    }
    .el-transfer-panel__footer {
      line-height: 40px;
    }
  }
</style>
