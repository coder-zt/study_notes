import Vue from 'vue'
import App from './App.vue'
import router from './router' // 引入上面创建路由文件
import './index.css'
import ElementUI  from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
// import VueRouter from 'vue-router'
// // import Vue from 'vue'

// Vue.use(VueRouter)



Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
