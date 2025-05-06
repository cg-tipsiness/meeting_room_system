<template>
  <div class="user-profile">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人详情</h2>
          <el-button type="primary" @click="handleSave" :loading="loading">
            保存修改
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" disabled />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="部门" prop="department">
          <el-input v-model="form.department" placeholder="请输入所属部门" />
        </el-form-item>

        <el-form-item label="职位" prop="position">
          <el-input v-model="form.position" placeholder="请输入职位" />
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
  username: 'john_doe', // 这里应该从API获取
  name: '',
  email: '',
  phone: '',
  department: '',
  position: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  department: [{ required: true, message: '请输入所属部门', trigger: 'blur' }],
  position: [{ required: true, message: '请输入职位', trigger: 'blur' }]
}

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    // TODO: 调用获取用户信息API
    // const { data } = await getUserInfo()
    // form.value = { ...form.value, ...data }
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

// 保存用户信息
const handleSave = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 调用更新用户信息API
        // await updateUserInfo(form.value)
        ElMessage.success('保存成功')
      } catch (error) {
        ElMessage.error('保存失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 页面加载时获取用户信息
fetchUserInfo()
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.user-profile {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;

  @include mobile.responsive(mobile) {
    padding: 15px;
  }

  .profile-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      @include mobile.responsive(mobile) {
        flex-direction: column;
        gap: 15px;
        align-items: stretch;

        .el-button {
          width: 100%;
        }
      }

      h2 {
        margin: 0;
        font-size: 18px;
      }
    }

    .profile-form {
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
          }

          .el-input {
            width: 100%;
          }
        }
      }
    }
  }
}
</style>
