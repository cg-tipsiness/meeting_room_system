import { createApp } from 'vue'
import pinia from '@/stores/index'
import App from './App.vue'
import router from './router'
import '@/assets/main.scss'
import '@/assets/mobile.scss'
import { optimizeMobile } from '@/utils/mobileOptimization'

// 移动端优化
optimizeMobile()

const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')
