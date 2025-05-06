<template>
  <div class="create-meeting">
    <div class="left-section">
      <h1>创建会议</h1>
      <div class="time-selection">
        <el-date-picker
          v-model="meetingDate"
          type="date"
          placeholder="选择日期"
          style="margin-bottom: 20px; width: 200px"
          @change="checkRoomAvailability"
        />
        <el-time-picker
          v-model="startTime"
          placeholder="开始时间"
          style="margin-bottom: 20px; width: 150px"
          format="HH:mm"
          @change="checkRoomAvailability"
        />
        <el-time-picker
          v-model="endTime"
          placeholder="结束时间"
          style="margin-bottom: 20px; width: 150px"
          format="HH:mm"
          @change="checkRoomAvailability"
        />
      </div>
      <div class="filters">
        <el-select
          v-model="selectedArea"
          placeholder="选择区域"
          style="width: 200px; margin-right: 20px"
        >
          <el-option label="A区" value="A"></el-option>
          <el-option label="B区" value="B"></el-option>
          <el-option label="C区" value="C"></el-option>
          <el-option label="D区" value="D"></el-option>
        </el-select>
        <el-select
          v-model="selectedFloor"
          placeholder="选择楼层"
          style="width: 200px"
        >
          <el-option label="一层" value="1"></el-option>
          <el-option label="二层" value="2"></el-option>
          <el-option label="三层" value="3"></el-option>
          <el-option label="四层" value="4"></el-option>
        </el-select>
      </div>
      <div class="meeting-rooms">
        <h2>会议室</h2>
        <div class="room-cards">
          <div
            v-for="room in filteredRooms"
            :key="room.id"
            class="room-card"
            :class="{
              busy: room.status === 'busy',
              available: room.status === 'available'
            }"
            @click="room.status === 'available' ? confirmRoom(room) : null"
          >
            <h3>{{ room.name }}</h3>
            <p>状态: {{ room.status === 'busy' ? '忙碌' : '空闲' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="right-section">
      <div class="meeting-form">
        <div class="form-header">
          <h2>会议信息</h2>
        </div>
        <div class="form-content">
          <el-form :model="meetingForm" label-width="100px">
            <el-form-item label="会议主题">
              <el-input
                v-model="meetingForm.title"
                placeholder="请输入会议主题"
              />
            </el-form-item>
            <el-form-item label="会议室">
              <el-input v-model="meetingForm.room" disabled />
            </el-form-item>
            <el-form-item label="会议日期">
              <el-input :value="formatDate(meetingDate)" disabled />
            </el-form-item>
            <el-form-item label="会议时间">
              <el-input
                :value="formatTime(startTime) + ' - ' + formatTime(endTime)"
                disabled
              />
            </el-form-item>
            <el-form-item label="会议用途">
              <el-input
                type="textarea"
                v-model="meetingForm.purpose"
                placeholder="请输入会议用途"
                :rows="4"
              />
            </el-form-item>
            <el-form-item label="参会人员">
              <el-select
                v-model="meetingForm.participants"
                multiple
                filterable
                placeholder="请选择参会人员"
              >
                <el-option
                  v-for="item in participantOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
        <div class="form-footer">
          <el-button type="primary" @click="createMeeting">创建会议</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import { GetMeetingRoomsService } from '@/api/meeting' // 引入服务方法

const selectedArea = ref('')
const selectedFloor = ref('')
const meetingDate = ref('')
const startTime = ref('')
const endTime = ref('')

const meetingForm = ref({
  title: '',
  room: '',
  purpose: '',
  participants: []
})

const participantOptions = [
  { value: '1', label: '张三' },
  { value: '2', label: '李四' },
  { value: '3', label: '王五' },
  { value: '4', label: '赵六' }
]

const meetingRooms = ref([])

const filteredRooms = computed(() => {
  return meetingRooms.value.filter((room) => {
    return (
      (selectedArea.value ? room.area === selectedArea.value : true) &&
      (selectedFloor.value ? room.floor === selectedFloor.value : true) &&
      (room.status === 'available' || room.status === 'busy')
    )
  })
})

const checkRoomAvailability = () => {
  meetingRooms.value.forEach((room) => {
    if (
      meetingDate.value &&
      startTime.value &&
      endTime.value &&
      room.name === 'A区 102室'
    ) {
      room.status = 'busy'
    } else {
      room.status = 'available'
    }
  })
}

const confirmRoom = (room) => {
  ElMessageBox.confirm(`是否选择 ${room.name}？`, '确认选择', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info',
    customClass: 'custom-confirm-dialog',
    distinguishCancelAndClose: true,
    confirmButtonClass: 'confirm-button',
    cancelButtonClass: 'cancel-button',
    closeOnClickModal: false,
    showClose: false
  })
    .then(() => {
      meetingForm.value.room = room.name
    })
    .catch(() => {
      // 用户取消选择
    })
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

const formatTime = (time) => {
  if (!time) return ''
  return time
}

const createMeeting = () => {
  console.log('创建会议:', {
    ...meetingForm.value,
    date: meetingDate.value,
    startTime: startTime.value,
    endTime: endTime.value
  })
}

const getmeetingRooms = async () => {
  try {
    const data = await GetMeetingRoomsService() // 调用服务方法
    console.log(data)
    if (data.success) {
      meetingRooms.value = data.rooms // 存储会议室数据
    } else {
      ElMessageBox.alert('获取会议室数据失败，请稍后重试。', '错误', {
        confirmButtonText: '确定'
      })
    }
  } catch (_) {
    // 使用下划线表示不使用的参数
    ElMessageBox.alert('获取会议室数据失败，请稍后重试。', '错误', {
      confirmButtonText: '确定'
    })
  }
}

onMounted(() => {
  getmeetingRooms()
})
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.create-meeting {
  display: flex;
  min-height: calc(100vh - 60px);
  padding: 20px;
  gap: 20px;

  @include mobile.responsive(mobile) {
    flex-direction: column;
    padding: 15px;
    gap: 15px;
  }

  .left-section {
    flex: 1;
    min-width: 300px;
    max-width: 600px;

    @include mobile.responsive(mobile) {
      max-width: none;
    }

    h1 {
      margin: 0 0 20px;
      font-size: 24px;

      @include mobile.responsive(mobile) {
        font-size: 20px;
        margin-bottom: 15px;
      }
    }

    .time-selection {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;

      @include mobile.responsive(mobile) {
        gap: 10px;

        :deep(.el-date-picker),
        :deep(.el-time-picker) {
          width: 100% !important;
          margin-bottom: 10px !important;
        }
      }
    }

    .filters {
      margin: 20px 0;
      display: flex;
      gap: 20px;

      @include mobile.responsive(mobile) {
        flex-direction: column;
        gap: 10px;

        .el-select {
          width: 100% !important;
          margin-right: 0 !important;
        }
      }
    }

    .meeting-rooms {
      h2 {
        margin: 0 0 20px;
        font-size: 18px;

        @include mobile.responsive(mobile) {
          font-size: 16px;
          margin-bottom: 15px;
        }
      }

      .room-cards {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;

        @include mobile.responsive(mobile) {
          grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
          gap: 15px;
        }

        .room-card {
          padding: 15px;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;

          &.available {
            background-color: #f0f9eb;
            border: 1px solid #e1f3d8;

            &:hover {
              transform: translateY(-2px);
              box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            }
          }

          &.busy {
            background-color: #fef0f0;
            border: 1px solid #fde2e2;
            cursor: not-allowed;
          }

          h3 {
            margin: 0 0 10px;
            font-size: 16px;
            color: #303133;
          }

          p {
            margin: 0;
            font-size: 14px;
            color: #606266;
          }
        }
      }
    }
  }

  .right-section {
    flex: 1;
    min-width: 300px;
    max-width: 600px;

    @include mobile.responsive(mobile) {
      max-width: none;
    }

    .meeting-form {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

      .form-header {
        padding: 20px;
        border-bottom: 1px solid #eee;

        @include mobile.responsive(mobile) {
          padding: 15px;
        }

        h2 {
          margin: 0;
          font-size: 18px;

          @include mobile.responsive(mobile) {
            font-size: 16px;
          }
        }
      }

      .form-content {
        padding: 20px;

        @include mobile.responsive(mobile) {
          padding: 15px;
        }

        :deep(.el-form-item) {
          margin-bottom: 20px;

          @include mobile.responsive(mobile) {
            margin-bottom: 15px;

            .el-form-item__label {
              float: none;
              display: block;
              text-align: left;
              padding: 0 0 8px;
            }

            .el-form-item__content {
              margin-left: 0 !important;
            }
          }
        }

        :deep(.el-select) {
          width: 100%;
        }
      }

      .form-footer {
        padding: 20px;
        border-top: 1px solid #eee;
        text-align: center;

        @include mobile.responsive(mobile) {
          padding: 15px;

          .el-button {
            width: 100%;
          }
        }
      }
    }
  }
}

// 自定义确认弹框样式
:global(.custom-confirm-dialog) {
  border-radius: 12px !important;
  padding: 0 !important;
  background: #ffffff !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
  border: none !important;
  width: 400px !important;
  min-height: 200px !important;
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;

  @include mobile.responsive(mobile) {
    width: 90% !important;
    max-width: 300px !important;
  }

  // 标题区域样式
  .el-message-box__header {
    flex-shrink: 0 !important;
    padding: 20px 24px !important;
    background-color: #409eff !important;
    border-top-left-radius: 12px !important;
    border-top-right-radius: 12px !important;
    text-align: center !important;

    @include mobile.responsive(mobile) {
      padding: 15px !important;
    }
  }

  // 标题样式
  .el-message-box__title {
    font-size: 18px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.4 !important;

    @include mobile.responsive(mobile) {
      font-size: 16px !important;
    }
  }

  // 内容样式
  .el-message-box__content {
    flex: 1 !important;
    padding: 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background-color: #ffffff !important;

    @include mobile.responsive(mobile) {
      padding: 20px 15px !important;
    }

    .el-message-box__message {
      margin: 0 !important;
      padding: 0 !important;
      font-size: 16px !important;
      color: #5e6d82 !important;
      line-height: 1.6 !important;
      text-align: center !important;

      @include mobile.responsive(mobile) {
        font-size: 14px !important;
      }

      p {
        margin: 0 !important;
      }
    }
  }

  // 按钮容器样式
  .el-message-box__btns {
    flex-shrink: 0 !important;
    padding: 16px 24px !important;
    background-color: #ffffff !important;
    border-top: 1px solid #ebeef5 !important;
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
    display: flex !important;
    justify-content: center !important;
    gap: 12px !important;

    @include mobile.responsive(mobile) {
      padding: 12px 15px !important;
    }
  }

  // 确认按钮样式
  .confirm-button {
    flex: 1 !important;
    max-width: 120px !important;
    height: 36px !important;
    background-color: #409eff !important;
    border-color: #409eff !important;
    color: white !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
    margin: 0 !important;

    @include mobile.responsive(mobile) {
      max-width: 100px !important;
      height: 32px !important;
      font-size: 13px !important;
    }

    &:hover {
      background-color: #66b1ff !important;
      border-color: #66b1ff !important;
      transform: translateY(-1px) !important;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3) !important;
    }
  }

  // 取消按钮样式
  .cancel-button {
    flex: 1 !important;
    max-width: 120px !important;
    height: 36px !important;
    border: 1px solid #dcdfe6 !important;
    color: #606266 !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    background-color: white !important;
    transition: all 0.3s ease !important;
    margin: 0 !important;

    @include mobile.responsive(mobile) {
      max-width: 100px !important;
      height: 32px !important;
      font-size: 13px !important;
    }

    &:hover {
      color: #409eff !important;
      border-color: #c6e2ff !important;
      background-color: #ecf5ff !important;
    }
  }
}

// 添加遮罩层样式
:global(.v-modal) {
  background-color: rgba(0, 0, 0, 0.5) !important;
  backdrop-filter: blur(3px) !important;
  opacity: 1 !important;
}
</style>
