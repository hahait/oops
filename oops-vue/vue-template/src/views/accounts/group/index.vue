<template>
  <div class="group-container">
    <!-- 添加/搜索 -->
    <el-form :inline="true" class="group-form-inline" size="small">
      <el-form-item>
        <el-button type="primary" size="small" @click="addGroupButton">添加用户组</el-button>
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.name" placeholder="组名" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="params.user" placeholder="用户名" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchSubmit">搜索</el-button>
      </el-form-item>
    </el-form>
    <!-- 用户组列表 -->
    <group-list
      v-loading="listLoading"
      :group-list="groupList"
      :user-list="userList"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#f3f7f3cc"
      @editGroup="editGroup"
      @deleteGroup="commitDeleteGroup"
      @changeGroupPermisssion="changeGroupPermisssion"
      @commitChangeGroupUser="commitChangeGroupUser"/>
    <!-- 用户组添加/修改 弹窗 -->
    <el-dialog
      :visible.sync="groupDialogVisible"
      width="40%"
      title="用户组信息"
      center>
      <group-form
        ref="groupFormIndex"
        :group-form="groupForm"
        class="groupDialogForm"
        @groupObj="commitGroupObj"
        @cancelGroupObj="cancelGroupObj"/>
    </el-dialog>
    <!-- 用户组修改权限弹窗 -->
    <el-dialog
      :visible.sync="changeGroupPermissionDialogVisible"
      :title="'修改组 ' + permissionRow.name +' 权限'"
      width="65%"
      center>
      <el-form :inline="true" size="small" style="float: right">
        <el-form-item>
          <el-input v-model="permsParams.label" placeholder="APP名称" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="permsParams.model" placeholder="模型名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchPermissionSubmit">搜索</el-button>
        </el-form-item>
      </el-form>
      <group-permission
        :permission-list="permissionList"
        :permission-row="permissionRow"
        :permission-status="permissionStatus"
        @commitChangeGroupPermission="commitChangeGroupPermission"
      />
      <my-page :total="permsTotal" :page_size="permsParams.page_size" :current_page="permsParams.page" @CurrentChange="ChangePermsCurrentPage" @SizeChange="ChangePermsPageSize"/>
    </el-dialog>
    <!-- 分页 -->
    <my-page :total="total" :page_size="params.page_size" :current_page="params.page" @CurrentChange="ChangeCurrentPage" @SizeChange="ChangePageSize"/>
  </div>
</template>

<script>
import { getGroupRelateList, editGroupRelate, deleteGroup, addGroup, editGroup } from '@/api/accounts/group'
import { getUserList } from '@/api/accounts/user'
import { getPermission } from '@/api/accounts/permission'
import MyPage from '@/components/Pagination'
import GroupList from './group_list'
import GroupForm from './group_form'
import GroupPermission from './group_permission'

export default {
  name: 'Group',
  components: {
    MyPage,
    GroupList,
    GroupForm,
    GroupPermission
  },
  data: function() {
    return {
      groupList: [],
      userList: [],
      permissionList: [],
      listLoading: true,
      total: 0,
      permsTotal: 0,
      groupForm: {},
      groupDialogVisible: false,
      changeGroupPermissionDialogVisible: false,
      permissionRow: {},
      permissionStatus: [],
      params: {
        page: 1,
        page_size: 10,
        name: '',
        user: ''
      },
      permsParams: {
        page: 1,
        page_size: 10,
        label: '',
        model: ''
      }
    }
  },
  created() {
    this.fetchData()
    this.fetchUserData()
  },
  methods: {
    // 获取用户组列表
    fetchData: function() {
      this.listLoading = true
      getGroupRelateList(this.params).then(res => {
        this.total = res.count
        this.groupList = res.results
        this.listLoading = false
      })
    },
    // 获取用户列表
    fetchUserData: function() {
      this.listLoading = true
      getUserList({ page_size: 'all' }).then(res => {
        this.userList = res
        this.listLoading = false
      })
    },
    // 获取权限列表
    fetchPermissionData: function() {
      this.listLoading = true
      getPermission(this.permsParams).then(res => {
        this.permsTotal = res.count
        this.permissionList = res.results
        this.listLoading = false
      })
    },
    // 添加用户组 按钮
    addGroupButton: function() {
      this.groupDialogVisible = true
    },
    // 修改用户组按钮
    editGroup: function(row) {
      const newGroupValue = row
      this.groupForm = { ...newGroupValue }
      this.groupDialogVisible = true
    },
    // 用户组信息表单提交(包括添加和修改)
    commitGroupObj: function(form_data) {
      if (form_data.id) {
        const { id, ...data } = form_data
        editGroup(id, data).then(
          () => {
            this.$message({
              message: 'Good , 修改用户组成功',
              type: 'success'
            })
            this.groupForm = {}
            this.groupDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh , 修改用户组失败,错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      } else {
        addGroup(form_data).then(
          () => {
            this.$message({
              message: 'Good , 添加用户组成功',
              type: 'success'
            })
            this.groupForm = {}
            this.groupDialogVisible = false
            this.fetchData()
          },
          (error) => {
            var errmsg = ''
            for (var v in error.response.data) {
              errmsg += error.response.data[v]
            }
            this.$message({
              message: 'Oh , 添加用户组失败,错误信息: ' + errmsg,
              type: 'error'
            })
          }
        )
      }
    },
    // 取消用户组表单信息提交
    cancelGroupObj: function() {
      this.groupForm = {}
      this.groupDialogVisible = false
    },
    // 修改用户组内用户提交
    commitChangeGroupUser: function(user_data) {
      const { id, ...data } = user_data
      editGroupRelate(id, data).then(
        () => {
          this.$message({
            message: 'Good , 用户组关联用户修改成功',
            type: 'success'
          })
          this.fetchData()
          this.fetchUserData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 修改用户组关联的用户失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 修改用户组权限按钮
    changeGroupPermisssion: function(row) {
      this.permsParams = { label: '', model: '', page: 1, page_size: 10 }
      const newPermissionRowValue = row
      this.permissionRow = { ...newPermissionRowValue }
      this.fetchPermissionData()
      this.permissionStatus = []
      row.permissions.forEach(perm => {
        this.permissionStatus.push(perm.id)
      })
      this.changeGroupPermissionDialogVisible = true
    },
    // 修改用户组权限提交
    commitChangeGroupPermission: function(row_str) {
      const { id, ...data } = row_str
      editGroupRelate(id, data).then(
        () => {
          this.$message({
            message: 'Good , 用户组的权限修改成功',
            type: 'success'
          })
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 修改用户组权限失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 删除用户组
    commitDeleteGroup: function(row) {
      deleteGroup(row.id).then(
        () => {
          this.$message({
            message: `Good , 删除用户组 ${row.name} 修改成功`,
            type: 'success'
          })
          this.fetchData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 删除用户组失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 搜索提交
    searchSubmit: function() {
      this.fetchData()
    },
    // 搜索权限提交
    searchPermissionSubmit: function() {
      this.permsParams.page = 1
      this.fetchPermissionData()
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
    },
    // 分页改变页码
    ChangePermsCurrentPage: function(val) {
      this.permsParams.page = val
      this.fetchPermissionData()
    },
    // 分页改变展示的数据行数
    ChangePermsPageSize: function(val) {
      this.permsParams.page_size = val
      this.fetchPermissionData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.group-container {
  margin: 30px 10px 10px;
  .group-form-inline {
    margin: 10px 10px 0px;
    text-align: right;
    .el-form-item:first-child {
      float: left;
    }
  }
  .groupDialogForm {
    width: 90%;
  }
}
</style>
