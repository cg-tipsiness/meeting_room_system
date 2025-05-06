
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Participant

class RoomListView(APIView):
    def get(self, request):
        try:
            # 获取所有会议室数据
            rooms = Room.objects.all()

            # 将 QuerySet 转换为字典列表
            data = [
                {
                    "id": room.id,
                    "name": room.name,
                    "area": room.area,
                    "floor": room.floor,
                    "status": room.status
                }
                for room in rooms  # 遍历 QuerySet 中的每个对象
            ]

            return Response({"success": True, "rooms": data},content_type='application/json')
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500,content_type='application/json')

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Participant,Room
from datetime import datetime
class ParticipantList(APIView):
    def get(self, request):
        try:
            participants = Participant.objects.all()
            data = [
                {
                    "id": participant.id,
                    "name": participant.name
                }
                for participant in participants
            ]
            return Response({"success": True, "participants": data},content_type='application/json')
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500,content_type='application/json')
            
# class MeetingCreate(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             meeting = .objects.create(
#                 title=data.get('title'),
#                 room_id=data.get('room'),
#                 purpose=data.get('purpose'),
#                 participants=data.get('participants'),
#                 date=data.get('date'),
#                 start_time=data.get('start_time'),
#                 end_time=data.get('end_time')
#             )
#             return Response({"success": True, "message": "会议预定成功"})
#         except Exception as e:
#             return Response({"success": False, "error": str(e)}, status=500)
class AreaFloorList(APIView):
    def get(self, request):
        try:
            # 获取所有区域和楼层信息（从Room表中唯一获取）
            areas = Room.objects.values('area').distinct()
            floors = Room.objects.values('floor').distinct()
            
            # 构建区域和楼层的返回数据
            area_data = [
                {
                    "id": area['area'],
                    "name": area['area']  # 假设区域是字符串
                }
                for area in areas
            ]
            floor_data = [
                {
                    "id": floor['floor'],
                    "name": floor['floor']  # 假设楼层是字符串
                }
                for floor in floors
            ]
            
            return Response({
                "success": True,
                "areas": area_data,
                "floors": floor_data
            })
        
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=500)

class RoomAvailability(APIView):
    def post(self, request):
        try:
            # 获取请求数据
            date = request.data.get("date")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            area_id = request.data.get("area")
            floor_id = request.data.get("floor")

            # 将字符串日期和时间转换为 datetime 对象
            meeting_date = datetime.strptime(date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()

            # 查询满足条件的会议室
            rooms = Room.objects.filter(area=area_id, floor=floor_id)

            available_rooms = []
            for room in rooms:
                # 检查会议室是否在指定的时间段内可用
                is_available = not room.is_room_busy(meeting_date, start_time_obj, end_time_obj)
                if is_available:
                    available_rooms.append({
                        "id": room.id,
                        "name": room.name,
                        "status": "available"
                    })
                else:
                    available_rooms.append({
                        "id": room.id,
                        "name": room.name,
                        "status": "busy"
                    })
            
            return Response({
                "success": True,
                "availableRooms": available_rooms
            }, content_type='application/json')
        
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=500, content_type='application/json')
