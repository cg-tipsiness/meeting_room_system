import request from '@/utils/request'

// 获取会议室详情
export const GetMeetingRoomsService = async () => {
  try {
    const res = await request.get('/api/meeting-rooms') // 使用 Axios 实例调用 API
    return res.data // 返回响应数据
  } catch (error) {
    console.error('获取会议室数据失败:', error)
    throw error // 抛出错误以便调用者处理
  }
}
