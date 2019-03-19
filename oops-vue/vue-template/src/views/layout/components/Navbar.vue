<template>
  <el-menu class="navbar" mode="horizontal">
    <hamburger :toggle-click="toggleSideBar" :is-active="sidebar.opened" class="hamburger-container"/>
    <breadcrumb />
    <el-menu-item index="1" class="navbar-right">
      <ul>
        <li style="margin-right: 20px"><b>运维管理平台</b></li>
        <li style="margin-left: 10px">
          <icon name="sign-out-alt" />
          <!--<svg-icon icon-class="logout" />-->
          <span @click="logout">Log out</span>
        </li>
      </ul>
    </el-menu-item>
  </el-menu>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('ToggleSideBar')
    },
    logout() {
      this.$store.dispatch('LogOut').then(() => {
        location.reload() // 为了重新实例化vue-router对象 避免bug
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  height: 60px;
  line-height: 60px;
  border-radius: 0px !important;
  border-bottom: solid 4px #e6e6e6;
  .hamburger-container {
    line-height: 60px;
    height: 60px;
    float: left;
    padding: 0 10px;
    display: flex;
    align-items: center;
  }
  .screenfull {
    position: absolute;
    right: 90px;
    top: 16px;
    color: red;
  }
  .navbar-right {
    float: right;
  }
  .navbar-right ul {
    height: 60px;
    line-height: 60px;
    list-style-type:none;
  }
  .navbar-right ul li {
    height: 60px;
    line-height: 60px;
    display: block;
    float: left;
    font-size: 18px;
  }

  .fa-icon {
    width: auto;
    height: 1em;
    /*margin-right: 1px;*/
  }
}
</style>

