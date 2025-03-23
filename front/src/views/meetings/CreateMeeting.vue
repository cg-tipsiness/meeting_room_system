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
import { ref, computed } from 'vue'
import { ElMessageBox } from 'element-plus'

const selectedArea = ref('')
const selectedFloor = ref('')
const meetingDate = ref('')
const startTime = ref('')
const endTime = ref('')
const meetingTitle = ref('')
const meetingDescription = ref('')
const meetingParticipants = ref('')
const isDialogVisible = ref(false)
const selectedRoom = ref(null)

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

const meetingRooms = ref([
  { id: 1, name: 'A区 101室', area: 'A', floor: '1', status: 'available' },
  { id: 2, name: 'A区 102室', area: 'A', floor: '1', status: 'busy' },
  { id: 3, name: 'A区 201室', area: 'A', floor: '2', status: 'available' },
  { id: 4, name: 'B区 101室', area: 'B', floor: '1', status: 'busy' },
  { id: 5, name: 'B区 102室', area: 'B', floor: '1', status: 'available' },
  { id: 6, name: 'C区 301室', area: 'C', floor: '3', status: 'busy' },
  { id: 7, name: 'D区 401室', area: 'D', floor: '4', status: 'available' }
])

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
</script>

<style lang="scss" scoped>
.create-meeting {
  display: flex;
  gap: 20px;
  height: 100vh; // 设置为视口高度
  overflow: hidden; // 防止滚动

  .left-section {
    flex: 2;
    padding: 20px;
    overflow-y: auto; // 允许内容滚动

    h1 {
      margin-bottom: 20px;
      color: #333;
    }

    .time-selection {
      margin-bottom: 20px;
      display: flex;
      gap: 20px;
    }

    .filters {
      margin-bottom: 20px;
    }

    .meeting-rooms {
      h2 {
        margin-bottom: 10px;
        color: #333;
      }
      .room-cards {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
      }
      .room-card {
        width: 150px;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
        cursor: pointer;
        &.busy {
          background-color: #ffcccc;
        }
        &.available {
          background-color: #ccffcc;
        }
        &:hover {
          transform: scale(1.05);
        }
      }
    }
  }

  .right-section {
    flex: 1;
    background-color: #f5f7fa;
    height: 100%;
    position: relative;

    .meeting-form {
      display: flex;
      flex-direction: column;
      height: 100%;

      .form-header {
        padding: 20px;
        background-color: #fff;
        border-bottom: 1px solid #eee;
        h2 {
          margin: 0;
          color: #333;
        }
      }

      .form-content {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
      }

      .form-footer {
        padding: 20px;
        background-color: #fff;
        border-top: 1px solid #eee;
        text-align: center;
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
  min-height: 200px !important; // 添加最小高度
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important; // 防止内容溢出

  // 标题区域样式
  .el-message-box__header {
    flex-shrink: 0 !important; // 防止标题区域被压缩
    padding: 20px 24px !important;
    background-color: #409eff !important; // 使用主题蓝色
    border-top-left-radius: 12px !important;
    border-top-right-radius: 12px !important;
    text-align: center !important;
  }

  // 标题样式
  .el-message-box__title {
    font-size: 18px !important;
    color: #ffffff !important; // 白色文字
    font-weight: 600 !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.4 !important;
  }

  // 内容样式
  .el-message-box__content {
    flex: 1 !important;
    padding: 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background-color: #ffffff !important;

    .el-message-box__message {
      margin: 0 !important;
      padding: 0 !important;
      font-size: 16px !important;
      color: #5e6d82 !important;
      line-height: 1.6 !important;
      text-align: center !important;

      p {
        margin: 0 !important;
      }
    }
  }

  // 按钮容器样式
  .el-message-box__btns {
    flex-shrink: 0 !important; // 防止按钮区域被压缩
    padding: 16px 24px !important;
    background-color: #ffffff !important;
    border-top: 1px solid #ebeef5 !important;
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
    display: flex !important;
    justify-content: center !important;
    gap: 12px !important;
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
