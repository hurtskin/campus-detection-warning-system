import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import ECharts from 'vue-echarts'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.component('ECharts', ECharts)
Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(ElementUI)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
