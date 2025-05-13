import VueRouter from 'vue-router'
import Vue from 'vue'

import Common from "./components/Common.vue"
import XiaoMi from "./components/XiaoMi.vue"

Vue.use(VueRouter)


const Hauwei = { template: '<div>Hauwei</div>' }
const Oppo = { template: '<div>Oppo</div>' }
const Vivo = { template: '<div>Vivo</div>' }

const routes = [
  { path: '/', component: Common },
  { path: '/huawei', component: Hauwei },
  { path: '/xiaomi', component: XiaoMi },
  { path: '/oppo', component: Oppo },
  { path: '/vivo', component: Vivo }
]

const router = new VueRouter({
  routes // (缩写) 相当于 routes: routes
})

export default router