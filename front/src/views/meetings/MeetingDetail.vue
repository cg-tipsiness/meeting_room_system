<template>
  <div class="meeting-detail">
    <div class="header">
      <h1>会议详情</h1>
      <div class="actions">
        <el-button type="primary" @click="editMeeting">编辑会议</el-button>
        <el-button type="danger" @click="cancelMeeting">取消会议</el-button>
      </div>
    </div>

    <div class="content">
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <h3>基本信息</h3>
            <el-tag :type="meetingStatus.type">{{ meetingStatus.text }}</el-tag>
          </div>
        </template>
        <div class="info-list">
          <div class="info-item">
            <span class="label">会议主题：</span>
            <span class="value">{{ meetingInfo.title }}</span>
          </div>
          <div class="info-item">
            <span class="label">会议室：</span>
            <span class="value">{{ meetingInfo.room }}</span>
          </div>
          <div class="info-item">
            <span class="label">会议日期：</span>
            <span class="value">{{ formatDate(meetingInfo.date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">会议时间：</span>
            <span class="value">
              {{ meetingInfo.startTime }} - {{ meetingInfo.endTime }}
            </span>
          </div>
          <div class="info-item">
            <span class="label">创建人：</span>
            <span class="value">{{ meetingInfo.creator }}</span>
          </div>
          <div class="info-item">
            <span class="label">创建时间：</span>
            <span class="value">
              {{ formatDateTime(meetingInfo.createTime) }}
            </span>
          </div>
        </div>
      </el-card>

      <el-card class="purpose-card">
        <template #header>
          <div class="card-header">
            <h3>会议用途</h3>
          </div>
        </template>
        <p class="purpose-content">{{ meetingInfo.purpose }}</p>
      </el-card>

      <el-card class="participants-card">
        <template #header>
          <div class="card-header">
            <h3>参会人员</h3>
            <span class="participant-count">
              共 {{ meetingInfo.participants.length }} 人
            </span>
          </div>
        </template>
        <div class="participants-list">
          <el-avatar
            v-for="participant in meetingInfo.participants"
            :key="participant.id"
            :size="40"
            :src="participant.avatar"
          >
            {{ participant.name.charAt(0) }}
          </el-avatar>
        </div>
        <div class="participants-table">
          <el-table :data="meetingInfo.participants" style="width: 100%">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="department" label="部门" />
            <el-table-column prop="position" label="职位" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="row.status === '已确认' ? 'success' : 'warning'">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>

    <CustomDialog
      v-model="showCancelDialog"
      title="取消会议"
      :confirm-loading="confirmLoading"
      @confirm="handleConfirmCancel"
      @cancel="showCancelDialog = false"
    >
      <p style="text-align: center">确定要取消该会议吗？</p>
    </CustomDialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import CustomDialog from '@/components/CustomDialog.vue'

const router = useRouter()

// 模拟会议详情数据
const meetingInfo = ref({
  id: '1',
  title: '项目进度评审会议',
  room: 'A区 101会议室',
  date: '2024-03-20',
  startTime: '10:00',
  endTime: '11:30',
  status: 'upcoming', // upcoming, ongoing, completed, cancelled
  creator: '张三',
  createTime: '2024-03-18 14:30:00',
  purpose:
    '1. 审查本月项目进度\n2. 讨论并解决当前遇到的技术难题\n3. 规划下一阶段的工作重点\n4. 分配新的任务和职责',
  participants: [
    {
      id: 1,
      name: '张三',
      department: '技术部',
      position: '技术经理',
      status: '已确认',
      avatar: ''
    },
    {
      id: 2,
      name: '李四',
      department: '产品部',
      position: '产品经理',
      status: '已确认',
      avatar: ''
    },
    {
      id: 3,
      name: '王五',
      department: '设计部',
      position: 'UI设计师',
      status: '待确认',
      avatar: ''
    },
    {
      id: 4,
      name: '赵六',
      department: '技术部',
      position: '前端开发',
      status: '已确认',
      avatar: ''
    }
  ]
})

// 计算会议状态
const meetingStatus = computed(() => {
  const statusMap = {
    upcoming: { type: 'primary', text: '即将开始' },
    ongoing: { type: 'success', text: '进行中' },
    completed: { type: 'info', text: '已结束' },
    cancelled: { type: 'danger', text: '已取消' }
  }
  return statusMap[meetingInfo.value.status] || statusMap.upcoming
})

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return ''
  return datetime
}

// 编辑会议
const editMeeting = () => {
  router.push(`/meetings/edit/${meetingInfo.value.id}`)
}

// 弹窗相关
const showCancelDialog = ref(false)
const confirmLoading = ref(false)

const cancelMeeting = () => {
  showCancelDialog.value = true
}

const handleConfirmCancel = async () => {
  confirmLoading.value = true
  try {
    // TODO: 调用取消会议API
    console.log('取消会议:', meetingInfo.value.id)
    // 模拟API调用延迟
    await new Promise((resolve) => setTimeout(resolve, 1000))
    meetingInfo.value.status = 'cancelled'
    showCancelDialog.value = false
  } catch (error) {
    console.error('取消会议失败:', error)
  } finally {
    confirmLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/mobile.scss';

.meeting-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;

  @include responsive(mobile) {
    padding: 15px;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    @include responsive(mobile) {
      flex-direction: column;
      align-items: flex-start;
      gap: 15px;
    }

    h1 {
      margin: 0;
      color: #333;

      @include responsive(mobile) {
        font-size: 20px;
      }
    }

    .actions {
      @include responsive(mobile) {
        width: 100%;
        display: flex;
        gap: 10px;

        .el-button {
          flex: 1;
        }
      }
    }
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .el-card {
      border-radius: 8px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        h3 {
          margin: 0;
          color: #333;
          font-size: 16px;
        }
      }
    }

    .info-card {
      .info-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;

        @include responsive(mobile) {
          grid-template-columns: 1fr;
          gap: 15px;
        }

        .info-item {
          .label {
            color: #666;
            margin-right: 8px;
          }

          .value {
            color: #333;
            font-weight: 500;
          }
        }
      }
    }

    .purpose-card {
      .purpose-content {
        margin: 0;
        white-space: pre-line;
        line-height: 1.6;
        color: #333;
      }
    }

    .participants-card {
      .participant-count {
        color: #666;
        font-size: 14px;
      }

      .participants-list {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;

        .el-avatar {
          background-color: #409eff;
          color: #fff;
        }
      }

      .participants-table {
        @include responsive(mobile) {
          margin: 0 -20px;

          :deep(.el-table) {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
