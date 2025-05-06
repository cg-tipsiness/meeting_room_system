<template>
  <div class="edit-meeting">
    <div class="left-section">
      <h1>编辑会议</h1>
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
              available: room.status === 'available',
              selected: room.id === meetingForm.roomId
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
          <el-button type="primary" @click="updateMeeting">保存修改</el-button>
          <el-button @click="cancelEdit">取消</el-button>
        </div>
      </div>
    </div>

    <CustomDialog
      v-model="showRoomDialog"
      title="选择会议室"
      @confirm="handleConfirmRoom"
      @cancel="showRoomDialog = false"
    >
      <p style="text-align: center">是否选择 {{ selectedRoom?.name }}？</p>
    </CustomDialog>

    <CustomDialog
      v-model="showSaveDialog"
      title="保存修改"
      :confirm-loading="confirmLoading"
      @confirm="handleConfirmSave"
      @cancel="showSaveDialog = false"
    >
      <p style="text-align: center">确认保存修改？</p>
    </CustomDialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import CustomDialog from '@/components/CustomDialog.vue'

const route = useRoute()
const router = useRouter()

// 模拟数据 - 实际应该从API获取
const meetingId = route.params.id
const selectedArea = ref('')
const selectedFloor = ref('')
const meetingDate = ref('')
const startTime = ref('')
const endTime = ref('')

const meetingForm = ref({
  title: '',
  room: '',
  roomId: null,
  purpose: '',
  participants: []
})

const participantOptions = [
  { value: '1', label: '张三' },
  { value: '2', label: '李四' },
  { value: '3', label: '王五' },
  { value: '4', label: '赵六' }
]

// 模拟会议室数据
const meetingRooms = ref([
  { id: 1, name: 'A区 101室', area: 'A', floor: '1', status: 'available' },
  { id: 2, name: 'A区 102室', area: 'A', floor: '1', status: 'busy' },
  { id: 3, name: 'B区 201室', area: 'B', floor: '2', status: 'available' },
  { id: 4, name: 'C区 301室', area: 'C', floor: '3', status: 'available' }
])

const filteredRooms = computed(() => {
  return meetingRooms.value.filter((room) => {
    return (
      (selectedArea.value ? room.area === selectedArea.value : true) &&
      (selectedFloor.value ? room.floor === selectedFloor.value : true)
    )
  })
})

// 模拟获取会议详情
const fetchMeetingDetail = () => {
  // TODO: 从API获取会议详情
  // 这里使用模拟数据
  const mockMeetingData = {
    id: meetingId,
    title: '项目进度会议',
    room: 'A区 101室',
    roomId: 1,
    date: '2024-03-20',
    startTime: '10:00',
    endTime: '11:00',
    purpose: '讨论项目进度和问题',
    participants: ['1', '2']
  }

  // 填充表单数据
  meetingForm.value = {
    title: mockMeetingData.title,
    room: mockMeetingData.room,
    roomId: mockMeetingData.roomId,
    purpose: mockMeetingData.purpose,
    participants: mockMeetingData.participants
  }

  meetingDate.value = new Date(mockMeetingData.date)
  startTime.value = mockMeetingData.startTime
  endTime.value = mockMeetingData.endTime

  // 根据会议室信息设置区域和楼层
  const room = meetingRooms.value.find((r) => r.id === mockMeetingData.roomId)
  if (room) {
    selectedArea.value = room.area
    selectedFloor.value = room.floor
  }
}

const checkRoomAvailability = () => {
  // TODO: 实际应该调用API检查会议室可用性
  console.log('检查会议室可用性')
}

// 弹窗相关
const showRoomDialog = ref(false)
const showSaveDialog = ref(false)
const confirmLoading = ref(false)
const selectedRoom = ref(null)

const confirmRoom = (room) => {
  selectedRoom.value = room
  showRoomDialog.value = true
}

const handleConfirmRoom = () => {
  meetingForm.value.room = selectedRoom.value.name
  meetingForm.value.roomId = selectedRoom.value.id
  showRoomDialog.value = false
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

const formatTime = (time) => {
  if (!time) return ''
  return time
}

const updateMeeting = () => {
  showSaveDialog.value = true
}

const handleConfirmSave = async () => {
  confirmLoading.value = true
  try {
    // TODO: 调用API更新会议信息
    console.log('保存修改:', {
      id: meetingId,
      ...meetingForm.value,
      date: meetingDate.value,
      startTime: startTime.value,
      endTime: endTime.value
    })
    // 模拟API调用延迟
    await new Promise((resolve) => setTimeout(resolve, 1000))
    // 模拟成功后返回列表
    router.push('/meetings')
  } catch (error) {
    console.error('保存修改失败:', error)
  } finally {
    confirmLoading.value = false
  }
}

const cancelEdit = () => {
  router.push('/meetings')
}

onMounted(() => {
  fetchMeetingDetail()
})
</script>

<style lang="scss" scoped>
@import '@/assets/mobile.scss';

.edit-meeting {
  display: flex;
  gap: 20px;
  height: 100vh;
  overflow: hidden;

  @include responsive(mobile) {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
  }

  .left-section {
    flex: 2;
    padding: 20px;
    overflow-y: auto;

    @include responsive(mobile) {
      flex: none;
      padding: 15px;
      overflow-y: visible;
    }

    h1 {
      margin-bottom: 20px;
      color: #333;

      @include responsive(mobile) {
        font-size: 20px;
        margin-bottom: 15px;
      }
    }

    .time-selection {
      margin-bottom: 20px;
      display: flex;
      gap: 20px;

      @include responsive(mobile) {
        flex-direction: column;
        gap: 10px;

        .el-date-picker,
        .el-time-picker {
          width: 100% !important;
          margin-bottom: 10px !important;
        }
      }
    }

    .filters {
      margin-bottom: 20px;

      @include responsive(mobile) {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .el-select {
          width: 100% !important;
          margin-right: 0 !important;
          margin-bottom: 10px;
        }
      }
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

        @include responsive(mobile) {
          gap: 10px;
          justify-content: space-between;
        }
      }

      .room-card {
        width: 150px;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
        cursor: pointer;

        @include responsive(mobile) {
          width: calc(50% - 5px);

          h3 {
            font-size: 14px;
          }

          p {
            font-size: 12px;
          }
        }

        &.busy {
          background-color: #ffcccc;
        }
        &.available {
          background-color: #ccffcc;
        }
        &.selected {
          border: 2px solid #409eff;
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

    @include responsive(mobile) {
      flex: none;
      height: auto;
      min-height: 300px;
    }

    .meeting-form {
      display: flex;
      flex-direction: column;
      height: 100%;

      .form-header {
        padding: 20px;
        background-color: #fff;
        border-bottom: 1px solid #eee;

        @include responsive(mobile) {
          padding: 15px;
        }

        h2 {
          margin: 0;
          color: #333;

          @include responsive(mobile) {
            font-size: 18px;
          }
        }
      }

      .form-content {
        flex: 1;
        padding: 20px;
        overflow-y: auto;

        @include responsive(mobile) {
          padding: 15px;
        }

        :deep(.el-form-item__label) {
          @include responsive(mobile) {
            float: none;
            display: block;
            text-align: left;
            padding: 0 0 8px;
          }
        }

        :deep(.el-form-item__content) {
          @include responsive(mobile) {
            margin-left: 0 !important;
          }
        }
      }

      .form-footer {
        padding: 20px;
        background-color: #fff;
        border-top: 1px solid #eee;
        text-align: center;

        @include responsive(mobile) {
          padding: 15px;
        }

        .el-button {
          margin: 0 10px;
        }
      }
    }
  }
}
</style>
