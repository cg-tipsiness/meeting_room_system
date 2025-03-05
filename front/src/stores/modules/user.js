import { defineStore } from 'pinia'
import { ref } from 'vue'

// 用户模块
export const useUserStore = defineStore(
  'meeting-user',
  () => {
    const token = ref('') // 定义 token
    const setToken = (newToken) => {
        token.value = newToken
      } // 设置 token

    return { token, setToken }
  },
  {
    persist: true // 持久化
  }
)
