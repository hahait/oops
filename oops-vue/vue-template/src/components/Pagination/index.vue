<template>
  <div class="MyPage block">
    <el-pagination
      :current-page="currentPage"
      :page-sizes="[5, 10, 50, 100]"
      :page-size="page_size"
      :total="total"
      background
      prev-text="上一页"
      next-text="下一页"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange" />
  </div>
</template>

<script>
export default {
  name: 'MyPage',
  props: {
    'page_size': {
      type: Number,
      required: true
    },
    'current_page': {
      type: Number,
      required: true,
      default: 1
    },
    total: {
      type: Number,
      required: true
    }
  },
  data: function() {
    return {
      currentPage: this.current_page
    }
  },
  watch: {
    current_page: function() {
      this.currentPage = this.current_page
    }
  },
  methods: {
    handleSizeChange(val) {
      this.$emit('SizeChange', val)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.$emit('CurrentChange', val)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.MyPage {
  margin: 30px;
  text-align: center;
}
</style>
