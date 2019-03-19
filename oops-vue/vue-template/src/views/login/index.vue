<template>
  <div class="login-container">
    <div class="logo-img">
      <img src="@/../static/img/logo.jpg" style="border-radius:20px;">
    </div>
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" size="small" auto-complete="on" label-position="left">
      <h3 class="title">运维管理平台</h3>
      <el-form-item prop="username" style="line-height: 30px;">
        <span class="svg-container svg-container_login">
          <svg-icon icon-class="user" />
        </span>
        <el-input v-model="loginForm.username" name="username" type="text" auto-complete="on" placeholder="用户名" />
      </el-form-item>
      <el-form-item prop="password" style="line-height: 30px;">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :type="pwdType"
          v-model="loginForm.password"
          name="password"
          auto-complete="on"
          placeholder="密码"
          @keyup.enter.native="handleLogin" />
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye" />
        </span>
      </el-form-item>
      <el-form-item>
        <el-button :loading="loading" type="primary" style="width:100%;font-size: 20px" size="medium" @click.native.prevent="handleLogin">
          登陆
        </el-button>
      </el-form-item>
      <div class="tips">
        <a href="#" @click.prevent="forgetPasswd">忘记密码</a>
      </div>
      <div class="copy-right">
        <p><b>Copyright</b> Oops © 2017-2046</p>
      </div>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入正确的用户名'))
      } else {
        callback()
      }
    }
    const validatePass = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error('密码不能小于8位'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: 'admin',
        password: 'Abcd1234$#@!'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePass }]
      },
      loading: false,
      pwdType: 'password',
      forgetPasswdStr: '<div><p style="margin: 8px auto">低调而有内涵,默默背锅的</p>' +
                          '<p style="margin: 8px auto;font-size:20px; font-weight:bold;">运维工程师</p>' +
                          '<p style="margin: 8px auto">邮箱：ops@oops.com.cn</p></div>'
    }
  },
  methods: {
    showPwd() {
      if (this.pwdType === 'password') {
        this.pwdType = ''
      } else {
        this.pwdType = 'password'
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('Login', this.loginForm).then(() => {
            this.loading = false
            this.$router.push({ path: '/' })
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    forgetPasswd: function() {
      this.$swal('请你联系', this.forgetPasswdStr)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
$bg:#2d3a4b;
$light_gray:#eee;

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 40px;
    width: 80%;
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      /*padding: 12px 5px 12px 15px;*/
      color: #2f4050;
      font-size: 18px;
      &:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px #ffffff inset !important;
        -webkit-text-fill-color: #2d3a4b !important;
      }
    }
  }
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    /*background: rgba(0, 0, 0, 0.1);*/
    background-color: #ffffff;
    border-radius: 5px;
    color: #454545;
  }
}

</style>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#f3f3f4;
$dark_gray:#889aa4;
$light_gray:#eee;
.login-container {
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: $bg;
  .login-form {
    position: absolute;
    left: 0;
    right: 0;
    width: 400px;
    margin: 60px auto 30px;
  }
  .tips {
    font-size: 15px;
    color: $dark_gray;
    margin: 2px auto;
    padding-left: 170px;
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
    &_login {
      font-size: 20px;
    }
  }
  .title {
    font-size: 26px;
    color: #676a6c;
    text-align: center;
    font-weight: bold;
    margin: 10px auto 30px;
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .logo-img {
    width: 400px;
    height: 150px;
    margin: 40px auto 10px;
    text-align: center;
  }

  .logo-img img {
    width: 300px;
    height: 200px;
  }

  .copy-right {
    width: 400px;
    height: 50px;
    text-align: center;
    margin: 10px auto;
    color: #889aa4;
  }
}
</style>
