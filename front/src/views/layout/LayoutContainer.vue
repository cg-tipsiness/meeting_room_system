<template>
  <el-container class="layout-container">
    <!-- 移动端抽屉菜单 -->
    <el-drawer
      v-model="drawerVisible"
      direction="ltr"
      :with-header="false"
      :size="200"
      class="mobile-drawer"
    >
      <el-menu
        active-text-color="#ffd04b"
        background-color="#1E1E2F"
        :default-active="$route.path"
        text-color="#fff"
        router
        class="mobile-menu"
      >
        <div class="el-aside__logo"></div>
        <el-menu-item index="/meetinglist">
          <el-icon><Management /></el-icon>
          <span>会议列表</span>
        </el-menu-item>
        <el-menu-item index="/meeting/create">
          <el-icon><Promotion /></el-icon>
          <span>创建会议</span>
        </el-menu-item>
        <el-menu-item index="/meeting/manage">
          <el-icon><UserFilled /></el-icon>
          <span>管理会议</span>
        </el-menu-item>
        <el-menu-item index="/user/profile">
          <el-icon><User /></el-icon>
          <span>个人资料</span>
        </el-menu-item>
        <el-menu-item index="/user/avatar">
          <el-icon><Crop /></el-icon>
          <span>更换头像</span>
        </el-menu-item>
        <el-menu-item index="/user/password">
          <el-icon><EditPen /></el-icon>
          <span>重置密码</span>
        </el-menu-item>
      </el-menu>
    </el-drawer>

    <!-- 桌面版侧边栏 -->
    <el-aside width="200px" class="desktop-sidebar">
      <div class="el-aside__logo"></div>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#1E1E2F"
        :default-active="$route.path"
        text-color="#fff"
        router
      >
        <el-menu-item index="/meetinglist">
          <el-icon><Management /></el-icon>
          <span>会议列表</span>
        </el-menu-item>
        <el-menu-item index="/meeting/create">
          <el-icon><Promotion /></el-icon>
          <span>创建会议</span>
        </el-menu-item>
        <el-menu-item index="/meeting/manage">
          <el-icon><UserFilled /></el-icon>
          <span>管理会议</span>
        </el-menu-item>
        <el-menu-item index="/user/profile">
          <el-icon><User /></el-icon>
          <span>个人资料</span>
        </el-menu-item>
        <el-menu-item index="/user/avatar">
          <el-icon><Crop /></el-icon>
          <span>更换头像</span>
        </el-menu-item>
        <el-menu-item index="/user/password">
          <el-icon><EditPen /></el-icon>
          <span>重置密码</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <div class="header-content">
          <!-- 移动端菜单按钮 -->
          <div v-if="isMobileView" class="menu-button" @click="toggleDrawer">
            <el-icon size="24"><Menu /></el-icon>
          </div>

          <h1>智能会议系统</h1>
          <div class="avatar-container">
            <el-dropdown placement="bottom-end">
              <span class="el-dropdown__box">
                <el-avatar :src="avatar" />
                <el-icon v-if="!isMobileView"><CaretBottom /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile" :icon="User">
                    基本资料
                  </el-dropdown-item>
                  <el-dropdown-item command="avatar" :icon="Crop">
                    更换头像
                  </el-dropdown-item>
                  <el-dropdown-item command="password" :icon="EditPen">
                    重置密码
                  </el-dropdown-item>
                  <el-dropdown-item command="logout" :icon="SwitchButton">
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import {
  Management,
  Promotion,
  UserFilled,
  User,
  Crop,
  EditPen,
  SwitchButton,
  CaretBottom,
  Menu
} from '@element-plus/icons-vue'
import avatar from '@/assets/default.jpg'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useDeviceDetection } from '@/utils/device'

// 响应式布局状态
const drawerVisible = ref(false)
const screenWidth = ref(window.innerWidth)

// 计算当前是否为移动视图
const isMobileView = computed(() => {
  return screenWidth.value < 768
})

// 监听窗口大小变化
const handleResize = () => {
  screenWidth.value = window.innerWidth
  // 如果从移动视图切换到桌面视图，关闭抽屉
  if (!isMobileView.value) {
    drawerVisible.value = false
  }
}

// 切换抽屉菜单显示状态
const toggleDrawer = () => {
  drawerVisible.value = !drawerVisible.value
}

// 添加和清除窗口大小变化监听器
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.layout-container {
  height: 100vh;
  overflow: hidden;

  // 桌面版侧边栏
  .desktop-sidebar {
    display: block;
    background-color: #1e1e2f;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

    @include mobile.responsive(mobile) {
      display: none; // 在移动端隐藏桌面侧边栏
    }

    .el-aside__logo {
      height: 120px;
      background: url('@/assets/logo.png') no-repeat center / 80px auto;
    }

    .el-menu {
      border-right: none;
      .el-menu-item {
        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }
      }
    }
  }

  // 移动端抽屉菜单
  :deep(.mobile-drawer) {
    .el-drawer__body {
      padding: 0;
      background-color: #1e1e2f;
    }

    .mobile-menu {
      border-right: none;
      background-color: #1e1e2f;

      .el-menu-item {
        height: 50px;
        line-height: 50px;

        .el-icon {
          font-size: 18px;
        }
      }
    }

    .el-aside__logo {
      height: 80px;
      background: url('@/assets/logo.png') no-repeat center / 60px auto;
    }
  }

  .el-header {
    background-color: #1e1e2f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: relative;
    height: 60px;

    @include mobile.responsive(mobile) {
      padding: 0 15px;
      height: 50px !important;
    }

    .header-content {
      display: flex;
      align-items: center;
      width: 100%;
      justify-content: space-between;
      gap: 15px;

      .menu-button {
        color: #fff;
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background-color 0.3s;

        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .el-icon {
          font-size: 20px;
        }
      }

      h1 {
        margin: 0;
        color: #fff;
        font-size: 20px;
        flex: 1;

        @include mobile.responsive(mobile) {
          font-size: 16px;
          text-align: center;
        }
      }

      .avatar-container {
        display: flex;
        align-items: center;

        .el-dropdown__box {
          display: flex;
          align-items: center;
          cursor: pointer;
          padding: 2px;
          border-radius: 50%;
          transition: background-color 0.3s;

          &:hover {
            background-color: rgba(255, 255, 255, 0.1);
          }

          .el-avatar {
            width: 32px;
            height: 32px;

            @include mobile.responsive(mobile) {
              width: 28px;
              height: 28px;
            }
          }

          .el-icon {
            color: #fff;
            margin-left: 4px;
            font-size: 12px;
          }
        }

        :deep(.el-dropdown-menu) {
          .el-dropdown-menu__item {
            display: flex;
            align-items: center;
            padding: 8px 16px;

            .el-icon {
              margin-right: 8px;
              font-size: 16px;
            }
          }
        }
      }
    }
  }

  .el-main {
    background-color: #f5f7fa;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 20px;

    @include mobile.responsive(mobile) {
      padding: 15px;
    }
  }
}

// 自定义抽屉样式
:deep(.el-drawer) {
  background-color: #1e1e2f !important;

  .el-drawer__header {
    margin-bottom: 0;
    padding: 0;
    display: none;
  }

  .el-drawer__body {
    padding: 0;
  }
}

// 自定义下拉菜单样式
:deep(.el-dropdown-menu) {
  border-radius: 8px !important;
  padding: 4px !important;
  min-width: 120px !important;

  .el-dropdown-menu__item {
    border-radius: 4px !important;
    margin: 2px 0 !important;

    &:hover {
      background-color: #f5f7fa !important;
    }
  }
}
</style>
