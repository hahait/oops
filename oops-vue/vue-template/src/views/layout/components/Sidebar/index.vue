<template>
  <el-scrollbar wrap-class="scrollbar-wrapper">
    <el-menu
      :show-timeout="200"
      :default-active="$route.path"
      :collapse="isCollapse"
      mode="vertical"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <div class="head-img-container">
        <img alt="image" class="head-img" src="@/../static/img/logo.jpg">
        <p class="head-img-text">
          <a href="#">
            <strong>{{ username }}</strong> | {{ cn_name }}
          </a>
        </p>
      </div>
      <sidebar-item v-for="route in routes" :key="route.name" :item="route" :base-path="route.path"/>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'
import { getUserInfo } from '@/api/accounts/user'

export default {
  components: { SidebarItem },
  data: function() {
    return {
      username: '',
      cn_name: ''
    }
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    routes() {
      return this.$router.options.routes
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  },
  created() {
    this.fetchUserInfo()
  },
  methods: {
    fetchUserInfo: function() {
      getUserInfo().then(
        (res) => {
          this.username = res.username
          this.cn_name = res.cn_name
        }
      )
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .head-img-container {
    text-align: center;
    .head-img {
      width: 80px;
      height: 80px;
      margin: 30px auto 10px;
      border-radius:50px;
    }
    .head-img-text{
      color: #bfcbd9;
      margin: 10px auto 20px;
      font-size: 15px;
    }
  }
</style>
