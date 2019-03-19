<template>
  <div class="user-container">
    <!-- 添加/搜索 -->
    <el-form :inline="true" class="user-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addUserButton">注册用户</el-button>
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.username" placeholder="用户名" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.phone" placeholder="手机号" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.group" placeholder="组名" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 用户列表 -->
    <user-list
      v-loading="listLoading"
      :users="userList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @changeAdminStatus="changeAdminStatus"
      @changeStatus="changeStatus"
      @changeUserInfoBtn="changeUserInfoBtn"
      @changeUserPasswdBtn="changeUserPasswdBtn"
      @deleteUserBtn="deleteUserBtn"
      @changeUserGroupsBtn="changeUserGroupsBtn"/>
    <!-- 分页 -->
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
    <!-- 添加弹窗 -->
    <el-dialog
      :visible.sync="userDialogVisible"
      width="50%"
      title="用户信息"
      center>
      <user-form
        ref="userFormIndex"
        :user-form="userForm"
        class="userDialogForm"
        @userObj="commitUserObj($event)"
        @cancel-user-obj="cancelUserObj"/>
    </el-dialog>
    <!-- 修改弹窗 -->
    <el-dialog
      :visible.sync="changeUserInfoDialogVisible"
      width="50%"
      title="修改用户信息"
      center>
      <user-info-form
        ref="userInfoFormIndex"
        :user-info="userInfoForm"
        class="userInfoDialogForm"
        @changeUserInfo="commitChangeUserObj($event)"
        @cancelChangeUserInfo="cancelChangeUserObj"/>
    </el-dialog>
    <!-- 修改密码弹窗 -->
    <el-dialog
      :visible.sync="changeUserPasswordDialogVisible"
      :title="'修改 '+user.username+' 的密码'"
      class="my-dialog-body"
      width="35%"
      center>
      <user-password-form
        ref="userPasswordFormIndex"
        :change-user-password-form="userPasswordForm"
        class="userPasswordDialogForm"
        @changeUserPassword="commitChangeUserObj($event)"
        @cancelChangeUserPassword="cancelChangeUserObj"/>
    </el-dialog>
    <!-- 修改用户组弹窗 -->
    <el-dialog
      :visible.sync="changeUserGroupsDialogVisible"
      :title="'修改 '+user.username+' 关联的用户组'"
      width="50%"
      center>
      <user-groups
        :user="user"
        :group-list="groupList"
        :get-user-group="getUserGroup"
        class="userGroupsDialogForm"
        @commitChangeUserGroups="commitChangeUserGroups"/>
    </el-dialog>
  </div>
</template>

<script>
import { getUserList, addUser, editUser, deleteUser } from '@/api/accounts/user'
import { getGroupList } from '@/api/accounts/group'
import MyPage from '@/components/Pagination'
import UserList from './user_list'
import UserForm from './user_form'
import UserPasswordForm from './user_password_form'
import UserInfoForm from './user_info_form'
import UserGroups from './user_groups'

export default {
  name: 'User',
  components: {
    MyPage,
    UserList,
    UserForm,
    UserPasswordForm,
    UserInfoForm,
    UserGroups
  },
  data: function() {
    return {
      userList: [],
      user: {},
      groupList: [],
      getUserGroup: [],
      listLoading: false,
      total: 0,
      userDialogVisible: false,
      changeUserInfoDialogVisible: false,
      changeUserGroupsDialogVisible: false,
      changeUserPasswordDialogVisible: false,
      userForm: {},
      userInfoForm: {},
      userPasswordForm: {},
      params: {
        page: 1,
        page_size: 10,
        username: '',
        phone: '',
        group: ''
      }
    }
  },
  created() {
    this.fetchData()
    this.fetchGroupData()
  },
  methods: {
    // 获取用户列表
    fetchData: function() {
      this.listLoading = true
      getUserList(this.params).then(res => {
        this.total = res.count
        this.userList = res.results
        this.listLoading = false
      })
    },
    // 获取用户组列表
    fetchGroupData: function() {
      this.listLoading = true
      getGroupList({ page_size: 'all' }).then(res => {
        this.groupList = res
        this.listLoading = false
      })
    },
    // 注册用户
    addUserButton: function() {
      this.userDialogVisible = true
    },
    // 修改用户是否为 admin 用户
    changeAdminStatus: function(row) {
      editUser(row.id, { is_superuser: row.is_superuser }).then(
        () => {
          this.$message({
            message: 'Good , 修改用户是否是管理员成功',
            type: 'success'
          })
          this.fetchData()
        }
      )
    },
    // 修改用户的状态
    changeStatus: function(row) {
      editUser(row.id, { is_active: row.is_active }).then(
        () => {
          this.$message({
            message: 'Good , 修改用户状态成功',
            type: 'success'
          })
          this.fetchData()
        }
      )
    },
    // 搜索提交
    searchSubmit: function() {
      this.fetchData()
    },
    // 注册用户表单提交
    commitUserObj: function(data) {
      addUser(data).then(
        () => {
          this.$message({
            message: 'Good , 用户注册成功',
            type: 'success'
          })
          this.userDialogVisible = false
          this.$refs['userFormIndex'].$refs['userInfoForm'].resetFields()
          this.userForm = {}
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 添加用户失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 注册用户表单取消
    cancelUserObj: function() {
      this.userForm = {}
      this.userDialogVisible = false
    },
    // 修改用户信息按钮
    changeUserInfoBtn: function(data) {
      const newval = data
      this.userInfoForm = newval
      this.changeUserInfoDialogVisible = true
    },
    // 修改密码按钮
    changeUserPasswdBtn: function(row) {
      this.userPasswordForm = { id: row.id }
      const newUserValue = row
      this.user = { ...newUserValue }
      this.changeUserPasswordDialogVisible = true
    },
    // 修改用户信息/密码表单提交
    commitChangeUserObj: function(form_data) {
      const { id, ...data } = form_data
      editUser(id, data).then(
        () => {
          this.$message({
            message: 'Good , 用户修改成功',
            type: 'success'
          })
          this.changeUserInfoDialogVisible = false
          this.changeUserPasswordDialogVisible = false
          // this.$refs['userInfoFormIndex'].$refs['userInfoForm'].resetFields()
          // this.$refs['userPasswordFormIndex'].$refs['changeUserPasswordForm'].resetFields()
          this.userInfoForm = {}
          this.userPasswordForm = {}
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          console.log('我的错误信息： ', errmsg)
          this.$message({
            message: 'Oh , 修改用户信息失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 修改用户信息/密码表单取消
    cancelChangeUserObj: function() {
      this.changeUserInfoDialogVisible = false
      this.changeUserPasswordDialogVisible = false
    },
    // 删除用户按钮
    deleteUserBtn: function(row) {
      deleteUser(row.id).then(
        () => {
          this.$message({
            message: `Good,用户 ${row.cn_name} 删除成功`,
            type: 'success'
          })
          this.fetchData()
        },
        () => {
          this.$message({
            message: `Oh,用户 ${row.cn_name} 删除失败,请查看 console 信息`,
            type: 'error'
          })
        }
      )
    },
    // 修改用户组按钮
    changeUserGroupsBtn: function(row) {
      var gid = []
      for (var g in row.groups) {
        gid.push(row.groups[g]['id'])
      }
      this.getUserGroup = gid
      const newUsersValue = row
      this.user = { ...newUsersValue }
      this.changeUserGroupsDialogVisible = true
    },
    // 修改用户组表单提交
    commitChangeUserGroups: function(groups) {
      const { id, ...data } = groups
      editUser(id, data).then(
        () => {
          this.$message({
            message: 'Good , 修改用户关联的用户组成功',
            type: 'success'
          })
          this.changeUserGroupsDialogVisible = false
          this.getUserGroup = []
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 修改用户关联的用户组信息失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 分页改变页码
    ChangeCurrentPage: function(val) {
      this.params.page = val
      this.fetchData()
    },
    // 分页改变展示的数据行数
    ChangePageSize: function(val) {
      this.params.page_size = val
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.user-container {
  margin: 30px 10px 10px;
  .user-form-inline {
    margin: 10px 10px 0px;
    text-align: right;
    .el-form-item:first-child {
      float: left;
    }
  }
  .userDialogForm, .userPasswordDialogForm, .userInfoDialogForm, .userGroupsDialogForm {
    width: 90%;
  }

  .my-dialog-body el-dialog__body{
    padding-bottom: 10px;
  }
}
</style>
