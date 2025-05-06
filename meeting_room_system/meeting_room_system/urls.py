"""
URL configuration for meeting_room_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path,include
# from meeting import views
# from rest_framework.authtoken import views as auth_views
# from meeting.views import reservation_list
# urlpatterns = [
#     # path("admin/", admin.site.urls),
#     # path('api-auth/',include('rest_framework.urls')),
#     # path('api/rooms/', RoomListView.as_view(), name='room-list'),
#     # path('api/token/', auth_views.obtain_auth_token),  # Token认证
#     # path('meetinglist/',views.meetinglist),
#      path('api/reservations/', reservation_list, name='reservation-list'),
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from meeting import views
# from django.urls import path
# from meeting.views import RoomListView, ParticipantListView

# router = DefaultRouter()
# router.register(r'rooms', views.RoomAPI, basename='room')
# # router.register(r'reservations', views.ReservationAPI, basename='reservation')

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/auth/', include('rest_framework.urls')),
#     path('api/rooms/', RoomListView.as_view(), name='room-list'),  # 获取所有会议室
#     path('api/participants/', ParticipantListView.as_view(), name='participant-list'),  # 获取所有参会人员
# ]
# urls.py
from django.urls import path
from meeting.views import RoomListView, ParticipantList,AreaFloorList

urlpatterns = [
    path('api/meeting-rooms/', RoomListView.as_view(), name='room-list'),  # 获取所有会议室
    path('api/participants/', ParticipantList.as_view(), name='participant-list'),  # 获取所有参会人员
    path('api/areas/', AreaFloorList.as_view(), name='AreaFloorList'), 
]
