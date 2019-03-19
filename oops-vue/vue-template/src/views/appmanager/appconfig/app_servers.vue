<template>
  <div class="changeAppServers" style="text-align: center">
    <!-- 修改管理组弹窗 --->
    <el-transfer
      v-model="appServers"
      :props="{
        key: 'id',
        label: 'manager_ip'
      }"
      :data="serverList"
      :titles="['服务器列表', '应用服务器']"
      :button-texts="['取消关联', '关联服务器']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
      filterable
      target-order="push"
      style="text-align: left; display: inline-block">
      <span slot-scope="{ option }">{{ option.id }} - {{ option.manager_ip }}</span>
      <div slot="right-footer" style="text-align: center;">
        <el-button class="transfer-footer" size="small" @click="commitChange">
          操作
        </el-button>
      </div>
    </el-transfer>
  </div>
</template>

<script>
export default {
  name: 'AppServers',
  props: {
    app: {
      required: true,
      type: Object
    },
    getAppServer: {
      required: true,
      type: Array
    },
    serverList: {
      required: true,
      type: Array
    }
  },
  data: function() {
    return {
      appServers: this.getAppServer
    }
  },
  watch: {
    getAppServer() {
      this.appServers = this.getAppServer
    }
  },
  methods: {
    commitChange: function() {
      const server_str = { 'id': this.app.id, 'server': this.appServers }
      this.$emit('commitChangeAppServers', server_str)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .changeAppServers {
    margin: 0px auto;
    width: 100%;
    .el-transfer-panel__list {
      padding-bottom: 40px;
    }
  }
</style>
