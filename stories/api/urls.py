from django.urls import path
from stories.api.views import (
    RecipesListView, StoriesListView, 
    RecipeDetailView, StoryDetailView, 
    CommentsView, CommentDetailView,
    StoryCommentsView, StoryCommentDetailView,
    CategoryListView, CategoryDetailView,
    SubscribeAPIView, TagAPIView
)

app_name='api'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories_api'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='categories_detail_api'),
    path('recipes/', RecipesListView.as_view(), name='recipes_api'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipes_detail_api'),
    path('recipe-comments/<int:pk>/', CommentDetailView.as_view(), name='recipe_comments_detail_api'),
    path('recipes/<int:pk>/comments/', CommentsView.as_view(), name='recipe_comments_api' ),
    path('stories/', StoriesListView.as_view(), name='stories_api'),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='stories_detail_api'),
    path('story-comments/<int:pk>/', StoryCommentDetailView.as_view(), name='story_comments_detail_api'),
    path('stories/<int:pk>/comments/', StoryCommentsView.as_view(), name='story_comments_api' ),
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
    path('tags/',TagAPIView.as_view(), name='tags_api'),
]