<template>
  <div class="meeting-list">
    <h1>会议列表</h1>

    <!-- 桌面端统计栏 -->
    <div class="stats-bar desktop-stats">
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

    <!-- 移动端统计卡片 -->
    <div class="stats-cards mobile-stats">
      <div class="stat-card ongoing">
        <div class="stat-title">进行中</div>
        <div class="stat-value">{{ ongoingCount }}</div>
      </div>
      <div class="stat-card ended">
        <div class="stat-title">已结束</div>
        <div class="stat-value">{{ endedCount }}</div>
      </div>
      <div class="stat-card upcoming">
        <div class="stat-title">即将开始</div>
        <div class="stat-value">{{ upcomingCount }}</div>
      </div>
    </div>

    <el-input
      placeholder="搜索会议"
      v-model="searchQuery"
      class="search-input"
    />

    <!-- 桌面版表格 -->
    <el-table
      :data="filteredMeetings"
      style="width: 100%; margin: 0 auto"
      class="desktop-table"
    >
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

    <!-- 移动端卡片列表 -->
    <div class="mobile-meeting-cards">
      <div
        v-for="meeting in filteredMeetings"
        :key="meeting.id"
        class="meeting-card"
      >
        <div class="meeting-card-header">
          <div class="meeting-title">{{ meeting.title }}</div>
          <div :class="['meeting-status', getStatusClass(meeting.status)]">
            {{ meeting.status }}
          </div>
        </div>
        <div class="meeting-info">
          <div class="info-item">
            <el-icon><Clock /></el-icon>
            <span>{{ meeting.date }}</span>
          </div>
          <div class="info-item">
            <el-icon><Avatar /></el-icon>
            <span>{{ meeting.participants }}</span>
          </div>
        </div>
        <div class="meeting-actions">
          <el-button
            @click="viewDetail(meeting.id)"
            type="primary"
            size="small"
          >
            详情
          </el-button>
          <el-button @click="editMeeting(meeting.id)" type="info" size="small">
            编辑
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Edit, View, Clock, Avatar } from '@element-plus/icons-vue'

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
@import '@/assets/mobile.scss';

.meeting-list {
  padding: 20px;

  @include responsive(mobile) {
    padding: 15px;
  }

  h1 {
    margin-bottom: 20px;
    color: #333;

    @include responsive(mobile) {
      font-size: 20px;
      margin-bottom: 15px;
    }
  }

  // 桌面端统计栏
  .stats-bar {
    display: flex;
    justify-content: space-between;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

    @include responsive(mobile) {
      display: none;
    }
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

  // 移动端统计卡片
  .stats-cards {
    display: none;

    @include responsive(mobile) {
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
    }

    .stat-card {
      flex: 1;
      text-align: center;
      padding: 10px;
      border-radius: 8px;
      margin: 0 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

      &.ongoing {
        background-color: rgba(0, 200, 83, 0.1);
        color: #00796b;
      }

      &.ended {
        background-color: rgba(244, 67, 54, 0.1);
        color: #d32f2f;
      }

      &.upcoming {
        background-color: rgba(255, 152, 0, 0.1);
        color: #f57c00;
      }

      .stat-title {
        font-size: 12px;
        margin-bottom: 5px;
      }

      .stat-value {
        font-size: 18px;
        font-weight: bold;
      }
    }
  }

  .search-input {
    margin-bottom: 20px;
    width: 300px;

    @include responsive(mobile) {
      width: 100%;
      margin-bottom: 15px;
    }
  }

  // 桌面端表格
  .desktop-table {
    width: 100%;
    margin: 0 auto;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    @include responsive(mobile) {
      display: none;
    }
  }

  // 移动端卡片列表
  .mobile-meeting-cards {
    display: none;

    @include responsive(mobile) {
      display: block;
    }

    .meeting-card {
      background-color: #fff;
      border-radius: 8px;
      padding: 15px;
      margin-bottom: 15px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

      .meeting-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;

        .meeting-title {
          font-weight: bold;
          font-size: 16px;
        }

        .meeting-status {
          font-size: 12px;
          padding: 2px 8px;
          border-radius: 10px;

          &.status-ongoing {
            background-color: rgba(0, 200, 83, 0.1);
            color: #00796b;
          }

          &.status-ended {
            background-color: rgba(244, 67, 54, 0.1);
            color: #d32f2f;
          }

          &.status-upcoming {
            background-color: rgba(255, 152, 0, 0.1);
            color: #f57c00;
          }
        }
      }

      .meeting-info {
        margin-bottom: 10px;

        .info-item {
          display: flex;
          align-items: center;
          margin-bottom: 5px;
          color: #666;
          font-size: 14px;

          .el-icon {
            margin-right: 5px;
          }
        }
      }

      .meeting-actions {
        display: flex;
        justify-content: flex-end;

        .el-button {
          margin-left: 10px;
        }
      }
    }
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
