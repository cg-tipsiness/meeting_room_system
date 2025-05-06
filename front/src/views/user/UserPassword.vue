<template>
  <div class="user-password">
    <el-card class="password-card">
      <template #header>
        <div class="card-header">
          <h2>密码修改</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="password-form"
      >
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input
            v-model="form.currentPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="form.newPassword"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            确认修改
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const formRef = ref(null)

// 表单数据
const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 验证新密码与确认密码是否一致
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== form.value.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const rules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' },
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,20}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 调用修改密码API
        // await changePassword({
        //   currentPassword: form.value.currentPassword,
        //   newPassword: form.value.newPassword
        // })
        ElMessage.success('密码修改成功')
        resetForm()
      } catch (error) {
        ElMessage.error('密码修改失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.user-password {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;

  @include mobile.responsive(mobile) {
    padding: 15px;
  }

  .password-card {
    .card-header {
      h2 {
        margin: 0;
        font-size: 18px;
      }
    }

    .password-form {
      margin-top: 20px;

      @include mobile.responsive(mobile) {
        :deep(.el-form-item) {
          margin-bottom: 20px;

          .el-form-item__label {
            padding: 0 0 10px;
            line-height: 1.5;
            text-align: left;
          }

          .el-form-item__content {
            margin-left: 0 !important;
            max-width: none;

            .el-button {
              margin-left: 0;
              margin-right: 12px;
            }
          }

          .el-input {
            width: 100%;
          }
        }
      }

      :deep(.el-form-item__content) {
        max-width: 300px;
      }
    }
  }
}
</style>
