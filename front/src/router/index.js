import { createRouter, createWebHistory } from 'vue-router'
import LayoutContainer from '../views/layout/LayoutContainer.vue'
import LoginPage from '../views/login/LoginPage.vue'
import MeetingList from '../views/meetings/MeetingList.vue'
import MeetingDetail from '../views/meetings/MeetingDetail.vue'
import CreateMeeting from '../views/meetings/CreateMeeting.vue'
import EditMeeting from '../views/meetings/EditMeeting.vue'
import UserProfile from '../views/user/UserProfile.vue'
import UserAvatar from '../views/user/UserAvatar.vue'
import UserPassword from '../views/user/UserPassword.vue'

const routes = [
  {
    path: '/',
    name: 'LayoutContainer',
    component: LayoutContainer,
    children: [
      {
        path: '',
        redirect: 'meetinglist' // 默认重定向到会议列表
      },
      {
        path: 'meetinglist',
        name: 'MeetingList',
        component: MeetingList
      },
      {
        path: 'meeting/detail/:id', // 会议详情应包含 ID
        name: 'MeetingDetail',
        component: MeetingDetail
      },
      {
        path: 'meeting/create',
        name: 'CreateMeeting',
        component: CreateMeeting
      },
      {
        path: 'meeting/edit/:id', // 编辑会议应包含 ID
        name: 'EditMeeting',
        component: EditMeeting
      },
      {
        path: 'user/profile',
        name: 'UserProfile',
        component: UserProfile
      },
      {
        path: 'user/avatar',
        name: 'UserAvatar',
        component: UserAvatar
      },
      {
        path: 'user/password',
        name: 'UserPassword',
        component: UserPassword
      }
    ]
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
