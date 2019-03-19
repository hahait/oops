<template>
  <div class="myself-container clearfix">
    <div class="user_info">
      <div class="userinfo-img-container">
        <img alt="image" class="userinfo-img" src="@/../static/img/logo.jpg">
        <p class="userinfo-img-text">
          <strong style="color: #3c3a3a">{{ userInfo.username }} ({{ userInfo.cn_name }})</strong>
        </p>
        <el-row>
          <el-button type="primary" size="small" plain round @click="changeMyselfInfoBtn">修改信息</el-button>
          <el-button type="success" size="small" plain round @click="changeMyselfPasswdBtn">修改密码</el-button>
          <el-button type="info" size="small" plain round>更换头像</el-button>
        </el-row>
        <el-table
          :data="userInfoList"
          stripe
          center
          size="mini"
          style="width: 100%">
          <el-table-column
            prop="name"
            min-width="40%"/>
          <el-table-column
            prop="value"
            min-width="60%"/>
        </el-table>
      </div>
    </div>
    <div class="user_groups_apps">
      <div class="user_groups_apps_count clearfix">
        <div class="group_count clearfix">
          <div class="inner">
            <h3 style="margin: 5px">66</h3>
            <p>组数量</p>
          </div>
          <div class="group_icon">
            <svg class="svg-icon" aria-hidden="true">
              <use xlink:href="#icon-groups"/>
            </svg>
          </div>
        </div>
        <div class="app_count clearfix">
          <div class="inner">
            <h3 style="margin: 5px">66</h3>
            <p>应用数量</p>
          </div>
          <div class="app_icon">
            <svg class="svg-icon" aria-hidden="true">
              <use xlink:href="#icon-android"/>
            </svg>
          </div>
        </div>
      </div>
      <div class="user_groups_apps_info">
        <div class="group_info" style="text-align: center">
          <h4 style="margin-bottom: 10px">组信息</h4>
          <el-table
            :data="userGroups"
            stripe
            center
            size="mini"
            style="width: 100%">
            <el-table-column
              prop="id"
              label="ID"
              align="center"
              min-width="40%"/>
            <el-table-column
              prop="name"
              label="名称"
              align="center"
              min-width="60%"/>
          </el-table>
        </div>
        <div class="app_info" style="text-align: center">
          <h4 style="margin-bottom: 10px">应用信息</h4>
          <el-table
            :data="userGroups"
            stripe
            center
            size="mini"
            style="width: 100%">
            <el-table-column
              prop="id"
              label="ID"
              align="center"
              min-width="40%"/>
            <el-table-column
              prop="name"
              label="名称"
              align="center"
              min-width="60%"/>
          </el-table>
        </div>
      </div>
    </div>
    <div class="user_permissions">
      <div class="permission_count clearfix">
        <div class="inner">
          <h3 style="margin: 5px">66</h3>
          <p>权限数量</p>
        </div>
        <div class="permission_icon">
          <svg class="svg-icon" aria-hidden="true">
            <use xlink:href="#icon-permissions"/>
          </svg>
        </div>
      </div>
      <div class="user_permissions_info" style="text-align: center;">
        <h4 style="margin-bottom: 10px">API 接口权限信息</h4>
        <el-table
          :data="userPermissions"
          stripe
          center
          size="mini"
          style="width: 100%">
          <el-table-column
            prop="id"
            label="ID"
            align="center"
            min-width="40%"/>
          <el-table-column
            prop="name"
            label="名称"
            align="center"
            min-width="60%"/>
        </el-table>
      </div>
    </div>
    <!-- 修改个人信息弹窗 -->
    <el-dialog
      :visible.sync="changeMyselfInfoDialogVisible"
      width="50%"
      title="修改个人信息"
      center>
      <myself-change-form
        :myself-info="userInfo"
        class="userInfoChangeDialogForm"
        @commitChangeMyselfInfo="commitChangeMyselfInfo($event)"
        @cancelChangeMyselfInfo="cancelChangeMyselfInfo"/>
    </el-dialog>
    <!-- 修改密码弹窗 -->
    <el-dialog
      :visible.sync="changeMyselfPasswordDialogVisible"
      title="修改密码"
      class="my-dialog-body"
      width="35%"
      center>
      <user-password-form
        :change-user-password-form="{id: userInfo.id}"
        class="myselfPasswordDialogForm"
        @changeUserPassword="commitChangeMyselfPassword($event)"
        @cancelChangeUserPassword="cancelChangeMyselfPassword"/>
    </el-dialog>
  </div>
</template>

<script>
import { getUserInfo } from '@/api/accounts/user'
import MyselfChangeForm from './myself_change_form'
import UserPasswordForm from '../user/user_password_form'
import { editUser } from '@/api/accounts/user'

export default {
  name: 'MySelf',
  components: {
    MyselfChangeForm,
    UserPasswordForm
  },
  data: function() {
    return {
      userInfo: {},
      userInfoList: [],
      userGroups: [],
      userPermissions: [],
      changeMyselfInfoDialogVisible: false,
      changeMyselfPasswordDialogVisible: false
    }
  },
  created() {
    this.getMySelfData()
  },
  methods: {
    getMySelfData: function() {
      getUserInfo().then(
        (res) => {
          this.userInfo = res
          const { groups, user_permissions, ...userdata } = res
          this.userGroups = groups
          this.userPermissions = user_permissions
          const user = [
            { name: '角色', value: userdata.role },
            { name: '邮箱', value: userdata.email },
            { name: '手机', value: userdata.phone },
            { name: '管理员', value: userdata.is_superuser },
            { name: '状态', value: userdata.is_active },
            { name: '最近登录日期', value: userdata.last_login },
            { name: '最近修改日期', value: userdata.last_update_time }
          ]
          this.userInfoList = user
        }
      )
    },
    // 修改个人信息按钮
    changeMyselfInfoBtn: function() {
      this.changeMyselfInfoDialogVisible = true
    },
    // 修改密码按钮
    changeMyselfPasswdBtn: function() {
      this.changeMyselfPasswordDialogVisible = true
    },
    // 提交修改个人信息
    commitChangeMyselfInfo: function(form_data) {
      const { id, ...data } = form_data
      editUser(id, data).then(
        () => {
          this.$message({
            message: 'Good , 用户个人信息成功',
            type: 'success',
            duration: 2000
          })
          this.userInfo = {}
          this.changeMyselfInfoDialogVisible = false
          this.getMySelfData()
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 修改个人信息失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 取消修改按钮事件
    cancelChangeMyselfInfo: function() {
      this.changeMyselfInfoDialogVisible = false
    },
    // 提交修改密码
    commitChangeMyselfPassword: function(form_data) {
      const { id, ...data } = form_data
      editUser(id, data).then(
        () => {
          const ss = this.$store
          this.$message({
            message: 'Good , 修改密码成功,需重新登陆....',
            type: 'success',
            duration: 1000,
            onClose: function() {
              ss.dispatch('LogOut').then(() => {
                location.reload()
              })
            }
          })
          this.changeMyselfPasswordDialogVisible = false
        },
        (error) => {
          var errmsg = ''
          for (var v in error.response.data) {
            errmsg += error.response.data[v]
          }
          this.$message({
            message: 'Oh , 修改密码失败,错误信息: ' + errmsg,
            type: 'error'
          })
        }
      )
    },
    // 取消修改密码
    cancelChangeMyselfPassword: function() {
      this.changeMyselfPasswordDialogVisible = false
    }
  }
}
</script>

<style rel='stylesheet/scss' lang='scss' scoped>
.myself-container {
  width: 100%;
  margin: 20px auto;
  .user_info {
    width: 30%;
    height: 100%;
    margin: 10px;
    margin-left: 35px;
    float: left;
    .userinfo-img-container {
      text-align: center;
      background-color: #1625270d;
      border-radius: 10px;
      .userinfo-img {
        width: 100px;
        height: 100px;
        margin: 10px auto 10px;
        border-radius:50px;
      }
      .userinfo-img-text{
        color: #bfcbd9;
        margin: 10px auto 20px;
        font-size: 15px;
      }
      .el-row {
        margin-bottom: 5px;
      }
    }
  }
  .user_groups_apps {
    width: 30%;
    margin: 10px auto;
    float: left;
    background-color: #1625270d;
    border-radius: 10px;
    .group_count, .app_count {
      width: 40%;
      height: 15%;
      float: left;
      background-color: #00c0ef;
      border-radius: 10px;
      position: relative;
      display: block;
      margin: 15px;
      color: white;
      box-shadow: 0 1px 1px rgba(0,0,0,0.1);
      .inner {
        padding: 5px;
        width: 60%;
        float: left;
      }
      .group_icon, .app_icon {
        width: 30%;
        float: left;
        margin: 10px;
        position: absolute;
        right: 10px;
        top: 5px;
        .svg-icon {
          width: 3em;
          height: 3em;
          vertical-align: -0.15em;
          fill: currentColor;
          overflow: hidden;
        }
      }
    }
    .app_count {
      background-color: #00a65a;
    }
  }
  .user_permissions {
    width: 30%;
    margin: 10px;
    float: left;
    background-color: #1625270d;
    border-radius: 10px;
    .permission_count {
      width: 50%;
      height: 15%;
      background-color: #f39c12;
      border-radius: 10px;
      position: relative;
      display: block;
      margin: 15px auto;
      color: white;
      box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
      .inner {
        padding: 5px;
        width: 60%;
        float: left;
      }
      .permission_icon {
        width: 30%;
        float: left;
        margin: 10px;
        position: absolute;
        right: 10px;
        top: 5px;
        .svg-icon {
          width: 3em;
          height: 3em;
          vertical-align: -0.15em;
          fill: currentColor;
          overflow: hidden;
        }
      }
    }
  }
  .userInfoChangeDialogForm, .myselfPasswordDialogForm {
    width: 90%;
  }
}
</style>
