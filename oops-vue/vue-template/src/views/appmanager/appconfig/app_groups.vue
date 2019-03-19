<template>
  <div class="changeAppGroups" style="text-align: center">
    <!-- 修改管理组弹窗 --->
    <el-transfer
      v-model="appGroups"
      :props="{
        key: 'id',
        label: 'name'
      }"
      :data="groupList"
      :titles="['用户组列表', '应用管理组']"
      :button-texts="['取消关联', '关联该组']"
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
          操作
        </el-button>
      </div>
    </el-transfer>
  </div>
</template>

<script>
export default {
  name: 'AppGroups',
  props: {
    app: {
      required: true,
      type: Object
    },
    getAppGroup: {
      required: true,
      type: Array
    },
    groupList: {
      required: true,
      type: Array
    }
  },
  data: function() {
    return {
      appGroups: this.getAppGroup
    }
  },
  watch: {
    getAppGroup() {
      this.appGroups = this.getAppGroup
    }
  },
  methods: {
    commitChange: function() {
      const group_str = { 'id': this.app.id, 'manage_team': this.appGroups }
      this.$emit('commitChangeAppGroups', group_str)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .changeAppGroups {
    margin: 0px auto;
    width: 100%;
    .el-transfer-panel__list {
      padding-bottom: 40px;
    }
  }
</style>
