<template>
  <div class="change-user-groups" style="text-align: center">
    <!-- 修改用户组弹窗 --->
    <el-transfer
      v-model="groups"
      :props="{
        key: 'id',
        label: 'name'
      }"
      :data="groupList"
      :titles="['用户组列表', '已加入的组']"
      :button-texts="['取消加入', '加入该组']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
      filterable
      target-order="push"
      style="text-align: left; display: inline-block"
      @change="handleChange">
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
  name: 'UserGroups',
  props: {
    user: {
      required: true,
      type: Object
    },
    getUserGroup: {
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
      groups: this.getUserGroup
    }
  },
  watch: {
    getUserGroup() {
      this.groups = this.getUserGroup
    }
  },
  methods: {
    handleChange: function(value, direction, movedKeys) {
      // value: 是 右边选择框的所有key,包含已经选择的默认key,等于 this.groups;
      // direction: 是本地移动的方向 right or left ;
      // movedKeys: 是本次点击移动的 key
      console.log(value, direction, movedKeys)
    },
    commitChange: function() {
      const group_str = { 'id': this.user.id, 'groups': this.groups }
      this.$emit('commitChangeUserGroups', group_str)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .change-user-groups {
    margin: 0px auto;
    width: 100%;
    .el-transfer-panel__list {
      padding-bottom: 40px;
    }
  }
</style>
