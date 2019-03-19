<template>
  <div class="monitorItemRelateAppForm" style="text-align: center">
    <!-- 修改监控项关联应用 --->
    <el-transfer
      v-model="relateApps"
      :props="{
        key: 'id',
        label: 'name'
      }"
      :data="apps"
      :titles="['未关联的应用', '已关联的应用']"
      :button-texts="['取消关联', '关联应用']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
      filterable
      target-order="push"
      style="text-align: left; display: inline-block">
      <span slot-scope="{ option }">{{ option.id }} - {{ option.name }}</span>
      <div slot="right-footer" style="text-align: center;">
        <el-button class="transfer-footer" size="small" @click="commitChange">
          提交
        </el-button>
      </div>
    </el-transfer>
  </div>
</template>

<script>
function getAppList(apps) {
  var app_list = []
  if (apps) {
    for (const i of apps) {
      app_list.push(i['id'])
    }
    return app_list
  }
}
export default {
  name: 'MonitorItemRelateApps',
  props: {
    item: {
      required: true,
      type: Object,
      default: function() {
        return {
          app_name: []
        }
      }
    },
    apps: {
      required: true,
      type: Array
    }
  },
  data: function() {
    return {
      relateApps: getAppList(this.item.app_name)
    }
  },
  watch: {
    item() {
      this.relateApps = getAppList(this.item.app_name)
    }
  },
  methods: {
    commitChange: function() {
      const relate_apps_list = { 'id': this.item.id, 'item_name': this.item.item_name, 'app_name': this.relateApps }
      this.$emit('commitMonitorItemRelateAppsBtn', relate_apps_list)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .monitorItemRelateAppForm {
    margin: 0px auto;
    width: 100%;
    .el-transfer-panel__list {
      padding-bottom: 40px;
    }
  }
</style>
