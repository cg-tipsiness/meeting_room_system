<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>会议室管理系统</h1>
        <p>欢迎登录</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <div class="form-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary">忘记密码？</el-link>
        </div>

        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const rememberMe = ref(false)
const formRef = ref(null)

const form = ref({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 调用登录API
        // const { data } = await login(form.value)
        // 存储token等信息
        // localStorage.setItem('token', data.token)

        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        ElMessage.error('登录失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;

  .login-container {
    width: 100%;
    max-width: 400px;
    background: white;
    border-radius: 12px;
    padding: 40px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);

    @include mobile.responsive(mobile) {
      padding: 30px 20px;
    }

    .login-header {
      text-align: center;
      margin-bottom: 40px;

      @include mobile.responsive(mobile) {
        margin-bottom: 30px;
      }

      h1 {
        font-size: 24px;
        color: #303133;
        margin: 0 0 10px;

        @include mobile.responsive(mobile) {
          font-size: 20px;
        }
      }

      p {
        font-size: 16px;
        color: #606266;
        margin: 0;

        @include mobile.responsive(mobile) {
          font-size: 14px;
        }
      }
    }

    .login-form {
      .form-options {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;

        @include mobile.responsive(mobile) {
          flex-direction: column;
          gap: 10px;
          align-items: flex-start;
        }
      }

      :deep(.el-input) {
        .el-input__wrapper {
          padding: 1px 15px;
          height: 42px;

          @include mobile.responsive(mobile) {
            height: 38px;
          }
        }
      }

      .login-button {
        width: 100%;
        height: 42px;
        font-size: 16px;

        @include mobile.responsive(mobile) {
          height: 38px;
          font-size: 14px;
        }
      }
    }
  }
}
</style>
