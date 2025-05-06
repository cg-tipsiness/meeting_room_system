<template>
  <div class="user-avatar">
    <el-card class="avatar-card">
      <template #header>
        <div class="card-header">
          <h2>用户头像</h2>
        </div>
      </template>

      <div class="avatar-content">
        <div class="current-avatar">
          <h3>当前头像</h3>
          <el-avatar :size="100" :src="currentAvatar" :icon="UserFilled" />
        </div>

        <div class="upload-section">
          <h3>上传新头像</h3>
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-success="handleAvatarSuccess"
            :on-error="handleAvatarError"
            :headers="uploadHeaders"
            name="avatar"
            action="/api/user/avatar"
          >
            <img v-if="imageUrl" :src="imageUrl" class="avatar-preview" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">
            <p>支持 jpg、png 格式，文件大小不超过 2MB</p>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, UserFilled } from '@element-plus/icons-vue'

const currentAvatar = ref('') // 当前头像URL
const imageUrl = ref('') // 预览图URL

// 上传请求头
const uploadHeaders = {
  Authorization: localStorage.getItem('token') || '' // 如果需要token认证
}

// 上传前验证
const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }

  // 创建本地预览
  imageUrl.value = URL.createObjectURL(file)
  return true
}

// 上传成功回调
const handleAvatarSuccess = (response) => {
  if (response.code === 0) {
    currentAvatar.value = response.data.url
    ElMessage.success('头像上传成功')
  } else {
    ElMessage.error(response.message || '头像上传失败')
    imageUrl.value = '' // 清除预览
  }
}

// 上传失败回调
const handleAvatarError = (err) => {
  console.error('Avatar upload error:', err)
  ElMessage.error('头像上传失败')
  imageUrl.value = '' // 清除预览
}

// 获取当前用户头像
const fetchCurrentAvatar = async () => {
  try {
    // TODO: 调用获取用户头像API
    // const { data } = await getUserAvatar()
    // currentAvatar.value = data.avatarUrl
  } catch {
    ElMessage.error('获取头像信息失败')
  }
}

// 页面加载时获取当前头像
fetchCurrentAvatar()

// 组件销毁时清理
onUnmounted(() => {
  if (imageUrl.value && imageUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(imageUrl.value)
  }
})
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.user-avatar {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;

  @include mobile.responsive(mobile) {
    padding: 15px;
  }

  .avatar-card {
    .card-header {
      h2 {
        margin: 0;
        font-size: 18px;
      }
    }

    .avatar-content {
      display: flex;
      flex-direction: column;
      gap: 30px;
      align-items: center;
      padding: 20px 0;

      @include mobile.responsive(mobile) {
        padding: 15px 0;
        gap: 25px;
      }

      .current-avatar,
      .upload-section {
        text-align: center;
        width: 100%;

        h3 {
          margin-bottom: 20px;
          font-size: 16px;
          color: #606266;

          @include mobile.responsive(mobile) {
            margin-bottom: 15px;
          }
        }
      }

      .avatar-uploader {
        :deep(.el-upload) {
          border: 1px dashed var(--el-border-color);
          border-radius: 6px;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          transition: var(--el-transition-duration);

          &:hover {
            border-color: var(--el-color-primary);
          }
        }

        .avatar-uploader-icon {
          font-size: 28px;
          color: #8c939d;
          width: 100px;
          height: 100px;
          text-align: center;
          line-height: 100px;
        }

        .avatar-preview {
          width: 100px;
          height: 100px;
          display: block;
          object-fit: cover;
        }
      }

      .upload-tip {
        margin-top: 10px;
        color: #909399;
        font-size: 12px;

        @include mobile.responsive(mobile) {
          margin-top: 8px;
        }
      }
    }
  }
}
</style>
