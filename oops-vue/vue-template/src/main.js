import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import router from './router'
import store from './store'

// 引入 sweetalert 插件
import VueSweetAlert from 'vue-sweetalert'

// 引入 awesome 图标插件
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

// 引入 vue-echarts
import 'echarts/lib/theme/light'// 注册echart主题
import ECharts from 'vue-echarts'

import '@/icons' // icon
import '@/permission' // permission control

// Vue.use(ElementUI, { locale })
Vue.use(ElementUI)
Vue.use(VueSweetAlert)
Vue.component('icon', Icon)
Vue.component('mychart', ECharts)

Vue.config.productionTip = false

new Vue({
  // 控制 index.html 中的 #app 标签
  el: '#app',
  router,
  store,
  render: h => h(App)
})
