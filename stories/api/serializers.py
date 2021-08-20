from rest_framework import serializers
from django.contrib.auth import  get_user_model
from stories.models import Recipe, Story, Tag, Comment, CommentStory, Category, Subscriber
from accounts.serializers import UserSerializer , UserLoginSerializer


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'title'
        ]


class RecipeSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title')
    author = UserSerializer()
    tag = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'image',
            'description',
            'created_at',
            'category',
            'author',
            'tag',
            'comments',
            'comment_count' 
            
        ]

    def get_comments(self, recipe):
        return CommentSerializer(recipe.comments.filter(parent_comment__isnull=True), many=True).data

    def get_comment_count(self, recipe):
        return recipe.comments.count()


class RecipeCreateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'image',
            'description',
            'created_at',
            'category',
            'author',
            'tag',
        ]
    
    def validate(self, data):
        request = self.context.get('request')
        data['author'] = request.user
        attrs = super().validate(data)
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField()
    author = UserSerializer()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'email',
            'author',
            'website',
            'message',
            'parent_comment',
            'created_at',
            'sub_comments',
        ]

    def get_sub_comments(self, parent_comment):
        sub_comments = parent_comment.sub_comments.all()
        return CommentSerializer(sub_comments, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'email',
            'author',
            'website',
            'message',
            'created_at',
        ]

    def validate(self, data):
        request = self.context.get('request')
        data['author'] = request.user
        attrs = super().validate(data)
        return attrs


class StorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title')
    author = UserSerializer()
    tag = TagSerializer(many=True)
    comments_story = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'slug',
            'image',
            'description',
            'created_at',
            'category',
            'author',
            'tag',
            'comments_story',
            'comment_count',
        ]

    def get_comments(self, story):
        return CommentStorySerializer(story.comments_story.filter(parent_comment__isnull=True), many=True).data

    def get_comment_count(self, story):
        return story.comments_story.count()


class StoryCreateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'slug',
            'image',
            'description',
            'created_at',
            'category',
            'author',
            'tag',
        ]

    def validate(self, data):
        request = self.context.get('request')
        data['author'] = request.user
        attrs = super().validate(data)
        return attrs


class CommentStorySerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField()
    author = UserSerializer()
    
    class Meta:
        model = CommentStory
        fields = [
            'id',
            'text',
            'email',
            'author',
            'website',
            'message',
            'sub_comments',
            'created_at',
        ]

    def get_sub_comments(self, parent_comment):
        return CommentStorySerializer(parent_comment.story_sub_comments.all(), many=True).data


class CommentStoryCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommentStory
        fields = [
            'id',
            'text',
            'email',
            'author',
            'website',
            'message',
            'created_at',
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'created_at',
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'created_at',
        ]


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriber
        fields = [
            'id',
            'email',
            'created_at',
            'updated_at',
        ]