from rest_framework.response import Response
from rest_framework import status
from stories.models import Recipe, Story , Comment, CommentStory, Category, Subscriber, Tag
from stories.api.serializers import (
    RecipeSerializer, 
    RecipeCreateSerializer, 
    StorySerializer, 
    StoryCreateSerializer, 
    CommentSerializer, 
    CommentCreateSerializer,
    CommentStorySerializer,
    CommentStoryCreateSerializer,
    CategorySerializer,
    CategoryCreateSerializer,
    SubscriberSerializer,
    TagSerializer,
    )
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
import json
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView

# @api_view(('GET', 'POST'))
# def recipes(request):
#     if request.method == 'POST':
#         recipe_data = request.data
#         serializer = RecipeCreateSerializer(data=recipe_data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     recipes = Recipe.objects.filter(is_published=True)
#     serializer = RecipeSerializer(recipes, many=True, context={'request': request})

#     return Response(serializer.data)


class RecipesListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        recipes = Recipe.objects.filter(is_published=True)
        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecipeCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def recipe_detail(request, slug):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         recipe = Recipe.objects.get(slug=slug)
#     except Recipe.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = RecipeSerializer(recipe)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = RecipeSerializer(recipe, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = Recipe.objects.filter(pk=recipe_id).first()
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = Recipe.objects.filter(pk=recipe_id).first()
        serializer = RecipeCreateSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = Recipe.objects.filter(pk=recipe_id).first()
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        recipe = Recipe.objects.filter(pk=recipe_id).first()
        comment_data = request.data
        serializer = CommentCreateSerializer(data=comment_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(recipe = recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.filter(pk=comment_id).first()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.filter(pk=comment_id).first()
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.filter(pk=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(('GET', 'POST'))
# def stories(request):
#     if request.method == 'POST':
#         recipe_data = request.data
#         serializer = StoryCreateSerializer(data=recipe_data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     stories = Story.objects.filter(is_published=True)
#     serializer = StorySerializer(stories, many=True, context={'request': request})

#     return Response(serializer.data)


class StoriesListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        stories = Story.objects.filter(is_published=True)
        serializer = StorySerializer(stories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        story_data = request.data
        serializer = StoryCreateSerializer(data=story_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def story_detail(request, slug):
#     try:
#         story = Story.objects.get(slug=slug)
#     except Story.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = StorySerializer(story)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = StorySerializer(story, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         story.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class StoryDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_object(self, slug):
        try:
            return Story.objects.get(slug=slug)
        except Story.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        story = self.get_object(slug)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        story = self.get_object(slug)
        serializer = StoryCreateSerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        story = self.get_object(slug)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoryCommentsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        story_id = kwargs.get('pk')
        story = Story.objects.filter(pk=story_id).first()
        comment_data = request.data
        serializer = CommentStoryCreateSerializer(data=comment_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(story = story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryCommentDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_object(self, pk):
        try:
            return CommentStory.objects.get(pk=pk)
        except CommentStory.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = CommentStory.objects.filter(pk=comment_id).first()
        serializer = CommentStorySerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = CommentStory.objects.filter(pk=comment_id).first()
        serializer = CommentStoryCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = CommentStory.objects.filter(pk=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAdminUser,]
        return super().get_permissions()
    
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        category_data = request.data
        serializer = CategoryCreateSerializer(data=category_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAdminUser,]
        return super().get_permissions()

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = Category.objects.filter(pk=category_id).first()
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = Category.objects.filter(pk=category_id).first()
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = Category.objects.filter(pk=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeAPIView(CreateAPIView):
    queryset = Subscriber.objects.filter(is_active=True)
    serializer_class = SubscriberSerializer


class TagAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer