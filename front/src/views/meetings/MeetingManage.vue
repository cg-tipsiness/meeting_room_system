<template>
  <div class="meeting-manage">
    <div class="header">
      <h1>会议管理</h1>
      <el-button type="primary" @click="createMeeting">创建会议</el-button>
    </div>

    <div class="content">
      <el-card class="filter-card">
        <div class="filter-form">
          <el-form :model="filterForm" :class="{ 'is-mobile': isMobile }">
            <el-form-item label="会议室">
              <el-select v-model="filterForm.room" placeholder="选择会议室">
                <el-option label="全部" value=""></el-option>
                <el-option label="A区 101室" value="A101"></el-option>
                <el-option label="A区 102室" value="A102"></el-option>
                <el-option label="B区 201室" value="B201"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="filterForm.status" placeholder="选择状态">
                <el-option label="全部" value=""></el-option>
                <el-option label="即将开始" value="upcoming"></el-option>
                <el-option label="进行中" value="ongoing"></el-option>
                <el-option label="已结束" value="completed"></el-option>
                <el-option label="已取消" value="cancelled"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期">
              <el-date-picker
                v-model="filterForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                :style="{ width: '100%' }"
              />
            </el-form-item>
            <el-form-item class="form-buttons">
              <el-button type="primary" @click="handleFilter">查询</el-button>
              <el-button @click="resetFilter">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="table-card">
        <el-table :data="meetings" style="width: 100%">
          <el-table-column prop="title" label="会议主题" min-width="200">
            <template #default="{ row }">
              <td data-label="会议主题">
                <el-link type="primary" @click="viewMeetingDetail(row.id)">
                  {{ row.title }}
                </el-link>
              </td>
            </template>
          </el-table-column>
          <el-table-column prop="room" label="会议室" width="120">
            <template #default="{ row }">
              <td data-label="会议室">{{ row.room }}</td>
            </template>
          </el-table-column>
          <el-table-column label="会议时间" width="280">
            <template #default="{ row }">
              <td data-label="会议时间">
                {{ formatDate(row.date) }} {{ row.startTime }}-{{ row.endTime }}
              </td>
            </template>
          </el-table-column>
          <el-table-column prop="creator" label="创建人" width="120">
            <template #default="{ row }">
              <td data-label="创建人">{{ row.creator }}</td>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <td data-label="状态">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </td>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <td data-label="操作">
                <el-button-group>
                  <el-button size="small" @click="editMeeting(row.id)">
                    编辑
                  </el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="cancelMeeting(row.id)"
                    :disabled="!['upcoming', 'ongoing'].includes(row.status)"
                  >
                    取消
                  </el-button>
                </el-button-group>
              </td>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import CustomDialog from '@/components/CustomDialog.vue'

const router = useRouter()

// 移动端检测
const isMobile = ref(false)
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

// 监听窗口大小变化
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// 筛选表单
const filterForm = ref({
  room: '',
  status: '',
  dateRange: []
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 模拟会议数据
const meetings = ref([
  {
    id: 1,
    title: '项目进度评审会议',
    room: 'A区 101室',
    date: '2024-03-20',
    startTime: '10:00',
    endTime: '11:30',
    creator: '张三',
    status: 'upcoming'
  },
  {
    id: 2,
    title: '产品设计讨论会',
    room: 'B区 201室',
    date: '2024-03-20',
    startTime: '14:00',
    endTime: '15:30',
    creator: '李四',
    status: 'ongoing'
  },
  {
    id: 3,
    title: '团队周会',
    room: 'A区 102室',
    date: '2024-03-19',
    startTime: '09:00',
    endTime: '10:00',
    creator: '张三',
    status: 'completed'
  }
])

// 状态相关
const statusMap = {
  upcoming: { type: 'primary', text: '即将开始' },
  ongoing: { type: 'success', text: '进行中' },
  completed: { type: 'info', text: '已结束' },
  cancelled: { type: 'danger', text: '已取消' }
}

const getStatusType = (status) => statusMap[status]?.type || 'info'
const getStatusText = (status) => statusMap[status]?.text || '未知'

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 筛选相关
const handleFilter = () => {
  // TODO: 调用API进行筛选
  console.log('筛选条件：', filterForm.value)
}

const resetFilter = () => {
  filterForm.value = {
    room: '',
    status: '',
    dateRange: []
  }
  handleFilter()
}

// 分页相关
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchMeetings()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchMeetings()
}

// 获取会议列表
const fetchMeetings = () => {
  // TODO: 调用API获取会议列表
  console.log(
    '获取会议列表，页码：',
    currentPage.value,
    '每页数量：',
    pageSize.value
  )
}

// 页面操作
const createMeeting = () => {
  router.push('/meeting/create')
}

const editMeeting = (id) => {
  router.push(`/meeting/edit/${id}`)
}

const viewMeetingDetail = (id) => {
  router.push(`/meeting/detail/${id}`)
}

// 弹窗相关
const showCancelDialog = ref(false)
const currentMeetingId = ref(null)
const confirmLoading = ref(false)

const cancelMeeting = (id) => {
  currentMeetingId.value = id
  showCancelDialog.value = true
}

const handleConfirmCancel = async () => {
  confirmLoading.value = true
  try {
    // TODO: 调用取消会议API
    console.log('取消会议:', currentMeetingId.value)
    // 模拟API调用延迟
    await new Promise((resolve) => setTimeout(resolve, 1000))
    // 更新会议状态
    const meeting = meetings.value.find((m) => m.id === currentMeetingId.value)
    if (meeting) {
      meeting.status = 'cancelled'
    }
    showCancelDialog.value = false
  } catch (error) {
    console.error('取消会议失败:', error)
  } finally {
    confirmLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
@use '@/assets/mobile.scss' as mobile;

.meeting-manage {
  padding: 20px;

  @include mobile.responsive(mobile) {
    padding: 10px;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    @include mobile.responsive(mobile) {
      flex-direction: column;
      align-items: stretch;
      gap: 15px;

      h1 {
        margin: 0;
        font-size: 20px;
        text-align: center;
      }

      .el-button {
        width: 100%;
      }
    }
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .filter-card {
      .filter-form {
        .el-form {
          &.is-mobile {
            :deep(.el-form-item) {
              margin-bottom: 15px;

              .el-form-item__label {
                float: none;
                display: block;
                text-align: left;
                padding: 0 0 8px 0;
                height: auto;
                line-height: 1.5;
              }

              .el-form-item__content {
                margin-left: 0 !important;
              }

              .el-select {
                width: 100%;
              }

              .el-range-editor {
                width: 100% !important;
              }

              &.form-buttons {
                margin-bottom: 0;
                margin-top: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;

                .el-button {
                  flex: 1;
                  max-width: 120px;
                }
              }
            }
          }
        }

        @include mobile.responsive(mobile) {
          padding: 0;

          .el-form {
            .el-form-item {
              &:last-child {
                margin-bottom: 0;
              }
            }
          }
        }
      }
    }

    .table-card {
      @include mobile.responsive(mobile) {
        :deep(.el-table) {
          font-size: 13px;

          .el-table__header {
            display: none;
          }

          .el-table__body {
            tr {
              display: flex;
              flex-direction: column;
              padding: 10px;
              border-bottom: 1px solid #ebeef5;

              td {
                display: flex;
                padding: 5px 0;
                border: none;

                &::before {
                  content: attr(data-label);
                  font-weight: bold;
                  margin-right: 10px;
                  min-width: 80px;
                }

                &.el-table__cell {
                  display: flex;
                }
              }
            }
          }

          .el-button {
            padding: 6px 12px;
            font-size: 13px;
          }

          .el-button-group {
            display: flex;
            gap: 8px;

            .el-button {
              margin-left: 0 !important;
            }
          }
        }
      }

      .pagination {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;

        @include mobile.responsive(mobile) {
          justify-content: center;

          :deep(.el-pagination) {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 5px;

            .el-pagination__total,
            .el-pagination__sizes {
              margin-right: 0;
              margin-bottom: 10px;
            }

            .el-pagination__jump {
              margin-left: 0;
              margin-top: 10px;
            }
          }
        }
      }
    }
  }
}
</style>
