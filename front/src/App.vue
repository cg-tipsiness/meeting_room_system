<script setup>
import { onMounted } from 'vue'

// 添加移动端meta viewport设置
onMounted(() => {
  const viewportMeta = document.createElement('meta')
  viewportMeta.name = 'viewport'
  viewportMeta.content =
    'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
  document.head.appendChild(viewportMeta)
})
</script>

<template>
  <div class="app-container">
    <router-view></router-view>
  </div>
</template>

<style>
/* 全局基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  height: 100vh;
  width: 100%;
}

/* 移动端用户体验优化 */
@media (max-width: 768px) {
  input,
  select,
  textarea {
    font-size: 16px !important; /* 防止iOS缩放 */
  }

  .app-container {
    -webkit-tap-highlight-color: transparent; /* 移除移动端点击高亮 */
    touch-action: manipulation; /* 优化触摸体验 */
  }
}
</style>
