from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from stories.models import *
from django.db.models import Count
from django.contrib import messages
from stories.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView, UpdateView
)


# Create your views here.

class HomeView(ListView):
    model = Story
    template_name = 'index.html'
    #queryset = Story.objects.filter(is_published=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.get('tags')
        queryset = queryset.filter(is_published=True)
        if tags:
            queryset = queryset.filter(tag__id=int(tags))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =  Category.objects.order_by('-created_at')[:3]
        context['recent_stories'] = Story.objects.order_by('-created_at')[:4]
        context['holiday_recipes'] = Recipe.objects.filter(tag__title="Holiday Recipes").order_by('-created_at')[:2]
        context['story_list'] = Story.objects.filter(is_published=True).order_by('-created_at')[:3]
        context['user'] = User.objects.filter(is_active=True).first()
        return context

# def home(request):
#     categories = Category.objects.order_by('-created_at')[:3]
#     recent_stories = Story.objects.order_by('-created_at')[:4]
#     holiday_recipes = Recipe.objects.filter(tag__title="Holiday Recipes").order_by('-created_at')[:2]
#     arr = ["Fruits", "Vegetables", "Protein", "Dairy"]
#     context = {
#         "arr": arr,
#         "recent_stories": recent_stories,
#         "holiday_recipes": holiday_recipes,
#         "categories": categories,
#     }
#     return render(request, "index.html", context)



class AboutView(TemplateView):
    template_name = 'about.html'

# def about(request):
#     arr = ["Fruits", "Vegetables", "Protein", "Dairy"]
#     context = {
#         "title": "Delicious Foods",
#         "description_texts": "Too easy to make",
#         "daily_visitors": "123",
#         "stories": "50",
#         "recipes": "450",
#         "users_count":"1000",
#         "arr": arr,
#     }
#     return render(request, "about.html", context)



# class StoryListView(TemplateView):
#     template_name = 'stories.html'

class StoryListView(ListView):
    model = Story
    template_name = 'stories.html'
    paginate_by = 3
    context_object_name = 'story_list'
    #queryset = Story.objects.filter(is_published=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.get('tags')
        queryset = queryset.filter(is_published=True)
        if tags:
            queryset = queryset.filter(tag__id=int(tags))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



# class StoryDetailView(TemplateView):
#     template_name = 'single1.html'

class StoryDetailView(DetailView):
    model = Story
    template_name = 'single1.html'
    context_object_name = 'story'
    queryset = Story.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.all()
        context['category'] = Category.objects.all()
        context['recent_blog'] = Story.objects.order_by('-created_at')[:5]
        return context



# class RecipeListView(TemplateView):
#     template_name = 'recipes.html'

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes.html'
    paginate_by = 3
    context_object_name = 'recipe_list'
    #queryset = Recipe.objects.filter(is_published=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.get('tags')
        queryset = queryset.filter(is_published=True)
        if tags:
            queryset = queryset.filter(tag__id=int(tags))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



# class RecipeDetailView(TemplateView):
#     template_name = 'single.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'single.html'
    context_object_name = 'recipe'
    queryset = Recipe.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.all()
        context['category'] = Category.objects.all()
        context['recent_blog'] = Story.objects.order_by('-created_at')[:3]
        return context



# class ContactView(TemplateView):
#     template_name = 'contact.html'

class ContactView(CreateView):
    form_class = ContactForm
    #fields = '__all__'
    #model = Contact
    template_name = 'contact.html'
    success_url = reverse_lazy('stories:index')

    def form_valid(self, form):
        result = super(ContactView, self).form_valid(form)
        messages.success(self.request, 'Sizin muracietiniz qebul edildi.')
        return result



class CreateRecipeView(TemplateView):
    template_name = 'add_recipe.html'

# class CreateRecipeView(LoginRequiredMixin, CreateView):
#     form_class = RecipeForm
#     template_name = 'add_recipe.html'

#     def form_valid(self, form):
#         result = super(CreateRecipeView, self).form_valid(form)
#         form.instance.author = self.request.user
#         messages.success(self.request, 'Sizin reseptiniz elave olundu.')
#         return result



class CreateStoryView(TemplateView):
    template_name = 'add_story.html'

# class CreateStoryView(LoginRequiredMixin, CreateView):
#     form_class = StoryForm
#     template_name = 'add_story.html'

#     def form_valid(self, form):
#         result = super(CreateStoryView, self).form_valid(form)
#         form.instance.author = self.request.user
#         messages.success(self.request, 'Sizin hekayeniz elave olundu.')
#         return result



class SubscribeView(TemplateView):
    template_name = 'base.html'

def subscribe(request):
    form = SubscriberForm()

    if request.method == 'POST':
        form = SubscriberForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Siz abune oldunuz.')
            return redirect(request.META.get("HTTP_REFERER"))
    context = {
        'form': form
    }
    return render(request,'base.html', context)


class EditRecipeView(DetailView):
    model = Recipe
    template_name = 'edit-recipe.html'
    context_object_name = 'recipe'
    # form_class = RecipeForm    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context