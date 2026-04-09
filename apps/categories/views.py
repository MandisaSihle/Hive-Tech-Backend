# from rest_framework import generics

# from apps.categories.models import Category
# from apps.categories.serializers import CategorySerializer


# class CategoryList(generics.ListAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     pagination_class = None

from rest_framework import generics
from rest_framework.permissions import AllowAny 

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer

class CategoryList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = None