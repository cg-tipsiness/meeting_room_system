<template>
  <el-container class="layout-container">
    <el-aside width="200px">
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
          <h1>智能会议系统</h1>
          <div class="avatar-container">
            <el-dropdown placement="bottom-end">
              <span class="el-dropdown__box">
                <el-avatar :src="avatar" />
                <el-icon><CaretBottom /></el-icon>
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
  CaretBottom
} from '@element-plus/icons-vue'
import avatar from '@/assets/default.jpg'
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  .el-aside {
    background-color: #1e1e2f;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    &__logo {
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
  .el-header {
    background-color: #1e1e2f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: relative;
    .header-content {
      display: flex;
      align-items: center;
      h1 {
        margin: 0;
        color: #fff;
        font-size: 24px;
      }
      .avatar-container {
        position: absolute;
        right: 20px;
        display: flex;
        align-items: center;
      }
    }
    .el-dropdown__box {
      display: flex;
      align-items: center;
      .el-icon {
        color: #fff;
        margin-left: 10px;
      }
      &:active,
      &:focus {
        outline: none;
      }
    }
  }
}
</style>
