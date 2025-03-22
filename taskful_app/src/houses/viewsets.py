from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import House
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsHouseManagerOrNone]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["=name", "=description"]
    ordering_fields = [
        "points",
        "completed_tasks_count",
        "not_completed_tasks_count"
    ]
    filterset_fields = ["members"]

    @action(detail=True, methods=["GET"], name="Join Form")
    def join_form(self, request, pk=None):
        house = self.get_object()
        return render(request, 'houses/join_house.html', {'house': house})

    @action(detail=True, methods=["POST"], name="Join", permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if (user_profile.house is None):
                user_profile.house = house
                user_profile.save()

                return Response(status.HTTP_204_NO_CONTENT)
            elif (user_profile in house.members.all()):
                return Response(
                    {
                        "detail": "Already a member in this house."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {
                        "detail": "Already a member in another house."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["POST"], name="Leave", permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if (user_profile in house.members.all()):
                user_profile.house = None
                user_profile.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {
                        "detail": "User is not a member in the house."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["POST"], name="Remove")
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id', None)
            if (user_id is None):
                return Response(
                    {"user_id": "Not provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_profile = User.objects.get(pk=user_id).profile
            house_members = house.members
            if (user_profile in house_members.all()):
                house_members.remove(user_profile)
                house.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response(
                {"detail": "User is not a member of the house"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Provided user_id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
