from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event
from api.serializers import EventsSerializer


class EventListAPI(APIView):
    '''For getting all events created by the requester'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Uses get request to fetch all events created by the user'''
        user = request.user
        events = Event.objects.filter(created_by=user).order_by("-id")
        serializer = EventsSerializer(events, many=True)
        return Response({
            "events": serializer.data,
        }, status=status.HTTP_200_OK)


class CUDEventAPI(APIView):
    '''For Create, Update, Delete of events'''
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        '''Uses the post request to create a new event'''
        user = request.user
        name = request.data.get("name")
        date = request.data.get("date")
        event = Event.objects.create(
            name=name,
            date=date,
            created_by=user
        )
        serializer = EventsSerializer(event, many=False)
        return Response({
            "event": serializer.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        '''Uses the put request to update existing event'''
        user = request.user
        event_id = request.data.get("event_id")
        event = Event.objects.filter(id=event_id, created_by=user).first()  # noqa
        name = request.data.get("name")
        date = request.data.get("date")
        if event is not None:
            event.name = name
            event.date = date
            event.save()
            serializer = EventsSerializer(event, many=False)
            return Response({
                "event": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Event Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        '''Uses the delete request to delete an event'''
        user = request.user
        event_id = request.data.get("event_id")
        event = Event.objects.filter(id=event_id, created_by=user).first()  # noqa
        if event is not None:
            event.delete()
            return Response({
                "message": "Event Deleted Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Event Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
