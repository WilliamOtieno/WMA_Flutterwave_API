from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserDetailSerializer, UserListSerializer
from .models import User


# Get All Users
class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


# Get details of each user made wrt id
class UserDetailAPIView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer

    def get(self, request, id):
        obj = User.objects.filter(id=id).last()
        if obj:
            return Response(self.serializer_class(obj).data)
        return Response(f"Oops, No User with id of {id}", status=status.HTTP_404_NOT_FOUND)
