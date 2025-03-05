<template>
  <div class="meeting-list">
    <h1>会议列表</h1>
    <div class="stats-bar">
      <div class="stat-item ongoing">
        <el-icon><Edit /></el-icon>
        <span>进行中的会议数量: {{ ongoingCount }}</span>
      </div>
      <div class="stat-item ended">
        <el-icon><View /></el-icon>
        <span>已结束的会议数量: {{ endedCount }}</span>
      </div>
      <div class="stat-item upcoming">
        <el-icon><Edit /></el-icon>
        <span>即将开始的会议数量: {{ upcomingCount }}</span>
      </div>
    </div>
    <el-input
      placeholder="搜索会议"
      v-model="searchQuery"
      style="margin-bottom: 20px; width: 300px"
    />
    <el-table :data="filteredMeetings" style="width: 100%; margin: 0 auto">
      <el-table-column
        prop="title"
        label="会议标题"
        width="400"
      ></el-table-column>
      <el-table-column
        prop="date"
        label="会议时间"
        width="400"
      ></el-table-column>
      <el-table-column
        prop="participants"
        label="参与者"
        width="400"
      ></el-table-column>
      <el-table-column label="状态" width="120">
        <template #default="scope">
          <span :class="getStatusClass(scope.row.status)">
            {{ scope.row.status }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button @click="editMeeting(scope.row.id)" type="text">
            <el-icon style="font-size: 20px"><Edit /></el-icon>
          </el-button>
          <el-button @click="viewDetail(scope.row.id)" type="text">
            <el-icon style="font-size: 20px"><View /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Edit, View } from '@element-plus/icons-vue'

const meetings = ref([
  {
    id: 1,
    title: '项目启动会议',
    date: '2023-10-01 10:00',
    participants: '谢雨晴',
    status: '进行中'
  },
  {
    id: 2,
    title: '需求评审会议',
    date: '2023-10-05 14:00',
    participants: '才闯',
    status: '已结束'
  },
  {
    id: 3,
    title: '周例会',
    date: '2023-10-10 09:00',
    participants: '谢雨晴，才闯',
    status: '进行中'
  },
  {
    id: 4,
    title: '项目总结会议',
    date: '2023-10-15 15:00',
    participants: '才闯，谢雨晴',
    status: '即将开始'
  }
])

const searchQuery = ref('')

const filteredMeetings = computed(() => {
  return meetings.value.filter(
    (meeting) =>
      meeting.title.includes(searchQuery.value) ||
      meeting.participants.includes(searchQuery.value)
  )
})

const ongoingCount = computed(() => {
  return meetings.value.filter((meeting) => meeting.status === '进行中').length
})

const endedCount = computed(() => {
  return meetings.value.filter((meeting) => meeting.status === '已结束').length
})

const upcomingCount = computed(() => {
  return meetings.value.filter((meeting) => meeting.status === '即将开始')
    .length
})

const getStatusClass = (status) => {
  switch (status) {
    case '进行中':
      return 'status-ongoing'
    case '已结束':
      return 'status-ended'
    case '即将开始':
      return 'status-upcoming'
    default:
      return ''
  }
}

const editMeeting = (id) => {
  // 编辑会议的逻辑
  console.log(`编辑会议 ID: ${id}`)
}

const viewDetail = (id) => {
  // 查看会议详情的逻辑
  console.log(`查看会议详情 ID: ${id}`)
}
</script>

<style lang="scss" scoped>
.meeting-list {
  padding: 20px;
  h1 {
    margin-bottom: 20px;
    color: #333;
  }
  .stats-bar {
    display: flex;
    justify-content: space-between;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  .stat-item {
    display: flex;
    align-items: center;
    font-size: 16px;
    color: #555;
    transition:
      transform 0.2s,
      background-color 0.2s;
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .stat-item:hover {
    transform: scale(1.05);
    background-color: rgba(255, 255, 255, 0.1);
  }
  .stat-item.ongoing {
    color: #00796b; /* 深绿色 */
  }
  .stat-item.ended {
    color: #d32f2f; /* 深红色 */
  }
  .stat-item.upcoming {
    color: #f57c00; /* 橙色 */
  }
  .el-table {
    width: 100%;
    margin: 0 auto;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  .status-ongoing {
    color: green;
  }
  .status-ended {
    color: red;
  }
  .status-upcoming {
    color: orange;
  }
}
</style>
