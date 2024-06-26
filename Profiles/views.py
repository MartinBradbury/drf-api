from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from django.http import Http404
from drf_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        post_count = Count('owner__post', distinct=True),
        follower_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True),

    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile', # get all profiles that are followed by a profile, given its id
    ]
    
    ordering_fields = [
        'post_count',
        'follower_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes =[IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        post_count = Count('owner__post', distinct=True),
        follower_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True),

    ).order_by('-created_at')






"""
Below is the Profiles view not using generics
"""
# from django.http import Http404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly


# class ProfileList(APIView):
#     """
#     List all profiles
#     No Create view (post method), as profile creation handled by django signals
#     """
#     def get(self, request):
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(
#             profiles, many=True, context={'request': request}
#         )
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     """
#     Retrieve a profile or edit it if you own it
#     """
#     serializer_class = ProfileSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, context={'request': request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)