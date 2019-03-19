<template>
  <div class="user-list">
    <!-- 表格内容 -->
    <el-table
      :data="users"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="用户名"
        align="center"
        width="120px">
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
        label="角色"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ humanDisplayRole(scope.row.role) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="管理员"
        align="center">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_superuser"
            :disabled="scope.row.is_superuser"
            active-color="#13ce66"
            @change="adminStatusChangeBtn(scope.row)"/>
        </template>
      </el-table-column>
      <el-table-column
        label="手机号"
        align="center"
        width="110px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="邮箱"
        align="center"
        width="220px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            :disabled="scope.row.is_active"
            active-color="#13ce66"
            @change="statusChangeBtn(scope.row)"/>
        </template>
      </el-table-column>
      <el-table-column
        label="最近登录"
        align="center"
        width="160px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.last_update_time }}</span>
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
                <el-button type="text" size="mini" @click="editUserInfo(scope.row)">修改用户信息</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="editUserPassword(scope.row)">修改用户密码</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="editUserGroup(scope.row)">修改用户所属组</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="userDelete(scope.row)">删除用户</el-button>
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
  name: 'UserList',
  props: {
    'users': {
      type: Array,
      required: true
    }
  },
  methods: {
    // 用户觉得人性化显示
    humanDisplayRole: function(role) {
      if (role === '0') {
        return 'Head'
      } else if (role === '1') {
        return 'Controller'
      } else if (role === '2') {
        return 'Manager'
      } else {
        return 'Employee'
      }
    },
    // 修改用户为 admin
    adminStatusChangeBtn: function(row) {
      this.$emit('changeAdminStatus', row)
    },
    // 修改用户状态
    statusChangeBtn: function(row) {
      this.$emit('changeStatus', row)
    },
    // 修改用户信息
    editUserInfo: function(row) {
      this.$emit('changeUserInfoBtn', row)
    },
    // 修改用户密码
    editUserPassword: function(row) {
      this.$emit('changeUserPasswdBtn', row)
    },
    // 删除用户
    userDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该用户: \< ${row.cn_name} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteUserBtn', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 修改用户组
    editUserGroup: function(row) {
      this.$emit('changeUserGroupsBtn', row)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .user-list {
    margin: 0px 10px 10px;
  }
</style>
