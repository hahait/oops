<template>
  <div class="cabinet-list">
    <h4 style="text-align: center">{{ idcCabinets.cn_name }} 的机柜信息</h4>
    <!-- 表格内容 -->
    <el-table
      :data="idcCabinets.cabinets"
      stripe
      border
      size="mini"
      highlight-current-row
      style="width: 100%;">
      <el-table-column
        label="标签"
        align="center"
        width="200px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.label }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="描述信息"
        align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.description }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="电源"
        align="center"
        width="200px">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.power }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="200px">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            plain
            @click="cabinetEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            plain
            @click="cabinetDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'CabinetList',
  props: {
    'idcCabinets': {
      type: Object,
      required: true,
      default: function() {
        return {
          cn_name: '',
          cabinets: [
            {
              label: '',
              description: '',
              power: ''
            }
          ]
        }
      }
    }
  },
  methods: {
    // 编辑 机柜
    cabinetEdit: function(row) {
      this.$emit('cabinetEdit', row)
    },
    // 删除 机柜
    cabinetDelete: function(row) {
      this.$confirm(`<p style="margin:20px">你确定将永久<b style="color:red;">删除该机柜: \< ${row.label} \> </b> 吗?<p>`, '嘿，知道自己在干嘛吗', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true,
        dangerouslyUseHTMLString: true
      }).then(() => {
        this.$emit('cabinetDelete', row.id)
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
  .cabinet-list {
    margin: 5px 30px 10px;
  }
</style>
