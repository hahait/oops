<template>
  <div class="cmdb-list">
    <!-- 表格内容 -->
    <el-table
      :data="cmdbs"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="ID">
              <span>{{ props.row.id }}</span>
            </el-form-item>
            <el-form-item label="UUID">
              <span>{{ props.row.uuid }}</span>
            </el-form-item>
            <el-form-item label="公网IP">
              <span>{{ props.row.public_ip }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.instance_id" label="实例ID">
              <span>{{ props.row.instance_id }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.instance_type" label="实例规格">
              <span>{{ props.row.instance_type }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.charge_type" label="付费类型">
              <span>{{ humanDisplayChargeType(props.row.charge_type) }}</span>
            </el-form-item>
            <el-form-item label="内存">
              <span>{{ props.row.mem }}</span>
            </el-form-item>
            <el-form-item label="SWAP">
              <span>{{ props.row.swap }}</span>
            </el-form-item>
            <el-form-item label="服务器品牌">
              <span>{{ props.row.server_brand.name }}</span>
            </el-form-item>
            <el-form-item label="服务器型号">
              <span>{{ props.row.server_model.name }}</span>
            </el-form-item>
            <el-form-item label="物理磁盘">
              <span v-html="props.row.disk"/>
            </el-form-item>
            <el-form-item label="磁盘挂载">
              <span v-html="props.row.disk_mount"/>
            </el-form-item>
            <el-form-item label="SN 码">
              <span>{{ props.row.sn_code }}</span>
            </el-form-item>
            <el-form-item label="远程管理卡IP">
              <span>{{ props.row.idrac_ip }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.idc" label="所属机房">
              <span>{{ props.row.idc.cn_name }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.cabinet" label="所在机柜">
              <span>{{ props.row.cabinet.label }}</span>
            </el-form-item>
            <el-form-item label="上线时间">
              <span>{{ props.row.online_time }}</span>
            </el-form-item>
            <el-form-item label="过期/保时间">
              <span>{{ props.row.expired_time }}</span>
            </el-form-item>
            <el-form-item v-if="props.row.offline_time" label="下线时间">
              <span>{{ props.row.offline_time }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="主机名"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.hostname }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="管理 IP"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.manager_ip }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="SSH 端口"
        align="center"
        width="80px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.ssh_port }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="类型"
        align="center"
        width="100px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ humanDisplayType(scope.row.type) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="配置"
        align="center">
        <template slot-scope="scope">
          <p style="margin: 0px auto">{{ scope.row.cpu_count }}</p>
          <p style="margin: 0px auto">{{ scope.row.mem }}</p>
          <p style="margin: 0px auto">{{ scope.row.os_version }}</p>
        </template>
      </el-table-column>
      <el-table-column
        label="状态"
        align="center"
        width="80px">
        <template slot-scope="scope">
          <el-tag :type="humanDisplayStatus(scope.row.status).type" size="small">{{ humanDisplayStatus(scope.row.status).value }}</el-tag>
          <!--<span style="color:#409EFF">{{ humanDisplayStatus(scope.row.status) }}</span>-->
        </template>
      </el-table-column>
      <el-table-column
        label="网卡信息"
        align="center"
        width="100px">
        <template slot-scope="scope">
          <el-button type="text" size="mini" plain @click="viewNetworkBtn(scope.row)">
            查看 ( {{ scope.row.network.length }} ) 个
          </el-button>
        </template>
      </el-table-column>
      <el-table-column
        label="最近更新时间"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px"> {{ scope.row.last_update_time }} </span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="120px">
        <template slot-scope="scope">
          <el-dropdown size="small" trigger="click" placement="bottom-start">
            <el-button type="primary" size="mini" plain>
              编辑<i class="el-icon-arrow-down el-icon--right"/>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="editCmdbBtn(scope.row)">修改 CMDB</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="editCmdbBtn(scope.row)">刷新 CMDB</el-button>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-button type="text" size="mini" @click="deleteCmdbBtn(scope.row)">删除 CMDB</el-button>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <!-- 网卡信息弹窗 -->
    <el-dialog
      :visible.sync="viewNetworkCardDialogVisible"
      :title="'服务器 ' + cmdbRow.hostname + ' 的网卡信息'"
      width="50%"
      center>
      <el-table
        :data="cmdbRow.network"
        stripe
        border
        size="mini"
        highlight-current-row
        style="min-width: 100%;">
        <el-table-column
          label="网卡名称"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="MAC 地址"
          align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.mac }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="IP 地址"
          align="center">
          <template slot-scope="scope">
            <p v-for="ip in scope.row.ips" :key="ip.id" style="margin: 0px auto">{{ ip.ip }}</p>
          </template>
        </el-table-column>
        <el-table-column
          label="状态"
          align="center">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.status"
              active-value="up"
              inactive-value="down"
              disabled/>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'CmdbList',
  props: {
    'cmdbs': {
      type: Array,
      required: true
    }
  },
  data: function() {
    return {
      cmdbRow: '',
      viewNetworkCardDialogVisible: false
    }
  },
  methods: {
    // 人性化展示 类型字段
    humanDisplayType: function(type) {
      if (type === 'physical') {
        return '物理机'
      } else if (type === 'cloud') {
        return '云主机'
      } else {
        return '虚拟机'
      }
    },
    // 人性化展示付费类型字段
    humanDisplayChargeType: function(charge_type) {
      if (charge_type === 'PrePaid') {
        return '包年包月'
      } else {
        return '按量付费'
      }
    },
    // 人性化展示状态字段
    humanDisplayStatus: function(status) {
      if (status === 'Running') {
        return { type: 'success', value: '运行中' }
      } else if (status === 'Starting') {
        return { type: 'info', value: '启动中' }
      } else if (status === 'Maintenance') {
        return { type: 'warning', value: '维护中' }
      } else if (status === 'Stopping') {
        return { type: 'warning', value: '停止中' }
      } else {
        return { type: 'danger', value: '已下线' }
      }
    },
    // 查看网卡按钮
    viewNetworkBtn: function(row) {
      this.cmdbRow = row
      this.viewNetworkCardDialogVisible = true
    },
    // 修改 CMDB 按钮
    editCmdbBtn(row) {
      this.$emit('editCmdbBtn', row)
    },
    // 删除 CMDB 按钮
    deleteCmdbBtn(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该cmdb: \<  ${row.hostname} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('deleteCmdbObj', row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .cmdb-list {
    margin: 5px 30px 10px;
    .demo-table-expand {
      font-size: 0;
    }
    .demo-table-expand label {
      width: 90px;
      color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
      margin-right: 0;
      margin-bottom: 0;
      width: 50%;
    }
  }
</style>
