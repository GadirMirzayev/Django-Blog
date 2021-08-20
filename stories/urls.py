from django.urls import path, re_path

from stories.views import *

app_name = 'stories'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('stories/', StoryListView.as_view(), name="stories"),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='story_detail'),
    path('add-story/', CreateStoryView.as_view(), name='add-story'),
    path('recipes/', RecipeListView.as_view(), name="recipes"),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('add-recipe/', CreateRecipeView.as_view(), name='add-recipe'),
    path('contact/', ContactView.as_view(), name="contact"),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('edit-recipe/<int:pk>/', EditRecipeView.as_view(), name='edit_recipe'),
]