from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from slugify import slugify
import datetime
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.

class Tag(models.Model):
    # information's
    title = models.CharField('Title', max_length=50)


    # moderation's
    order = models.PositiveIntegerField('Order', default=1)
    is_published = models.BooleanField('Is Published', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('order', '-created_at')

    def __str__(self):
        return self.title


class Category(models.Model):
    # information's
    title = models.CharField('Title', max_length=127)
    image = models.ImageField('Image', upload_to='categories_images',)


    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Story(models.Model):
    # information's
    title = models.CharField('Title', max_length=127)
    image = models.ImageField('Image', upload_to='stories_images',)
    description = RichTextUploadingField('Description')
    slug = models.SlugField('Slug', default='slug')
    is_published = models.BooleanField('Is Published', default=True)
    category = models.ForeignKey(Category, verbose_name='Category',
                                 on_delete=models.CASCADE, db_index=True, related_name='stories')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, db_index=True,
                               related_name='stories')
    tag = models.ManyToManyField(Tag, verbose_name='Tag', db_index=True, blank=True, )
    

    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}-{datetime.datetime.now()}')
        return super(Story, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('stories:story_detail', kwargs={'slug': self.slug})


class Recipe(models.Model):
    # information's
    title = models.CharField('Title', max_length=127)
    short_description = models.CharField('Short Description', max_length=255)
    image = models.ImageField('Image', upload_to='recipes_images',)
    description = RichTextUploadingField('Description', )
    slug = models.SlugField('Slug', default='slug')
    is_published = models.BooleanField('Is Published', default=True)
    category = models.ForeignKey(Category, verbose_name='Category',
                                 on_delete=models.CASCADE, db_index=True, related_name='recipes')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, db_index=True,
                               related_name='recipes')
    tag = models.ManyToManyField(Tag, verbose_name='Tag', db_index=True, blank=True, related_name='recipes')


    # moderation's
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}-{datetime.datetime.now()}')
        return super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('stories:recipe_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    # information's
    text = models.TextField('Text',)
    email = models.EmailField('E-mail', max_length=63)
    website = models.TextField('Website',)
    message = models.TextField('Message',)
    recipe = models.ForeignKey(Recipe, verbose_name='Recipe',
                                on_delete=models.CASCADE, db_index=True, related_name='comments')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, db_index=True,
                                related_name='comments')
    parent_comment = models.ForeignKey('self', verbose_name='Parent Comment', on_delete=models.CASCADE, db_index=True,
                                related_name='sub_comments', blank=True, null=True)


    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recipe Comment'
        verbose_name_plural = 'Recipe Comments'
        ordering = ('-created_at',)

    def __str__(self):
        return self.text


class CommentStory(models.Model):
    # information's
    text = models.TextField('Text',)
    email = models.EmailField('E-mail', max_length=63)
    website = models.TextField('Website',)
    message = models.TextField('Message',)
    story = models.ForeignKey(Story, verbose_name='Story',
                                on_delete=models.CASCADE, db_index=True, related_name='comments_story', blank=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, db_index=True,
                                related_name='comments_story')
    parent_comment = models.ForeignKey('self', verbose_name='Parent Comment', on_delete=models.CASCADE, db_index=True,
                                related_name='story_sub_comments', blank=True, null=True)


    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Story Comment'
        verbose_name_plural = 'Story Comments'
        ordering = ('-created_at',)

    def __str__(self):
        return self.text


class Contact(models.Model):
    # information's
    full_name = models.CharField('Full Name', max_length=127)
    email = models.EmailField('E-mail', max_length=63)
    subject = models.CharField('Subject', max_length=255)
    message = models.TextField('Message', help_text='Write your message here.')


    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ('-created_at',)

    def __str__(self):
        return self.full_name


class Subscriber(models.Model):
    # information's
    email = models.EmailField('E-mail', max_length=63)


    # moderation's
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


    