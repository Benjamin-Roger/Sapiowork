from django import forms
from django.db import models


from modelcluster.fields import ParentalKey,ParentalManyToManyField, ForeignKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.utils import translation


class TranslatedField(object):

    def __init__(self, en_field, fr_field):
        self.fr_field = en_field
        self.en_field = fr_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'en':
            return getattr(instance, self.en_field)
        else:
            return getattr(instance, self.fr_field)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon_url = models.CharField(blank=True,max_length=300)
    panels = [
        FieldPanel('name'),
        FieldPanel('icon_url'),
    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'blog categories'


class BlogPage(Page):
    date = models.DateField("Post date")
    author = models.CharField(default="Author",max_length=200)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    body_stream = StreamField([
        ('heading', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('html_raw', blocks.RawHTMLBlock()),
        ('picture', ImageChooserBlock()),
    ], blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('author'),
        index.SearchField('body_stream'),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories',widget = forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('author'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('body_stream'),
        InlinePanel('gallery_images', label="Gallery images")
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.url_image
        else:
            return None

    def get_context(self, request):
        # Update context to include translated links for the flags
        context = super().get_context(request)
        parenting = Page.objects.filter(
        live=True).parent_of(self)

        path_en_array = ['/en']
        path_fr_array = ['/fr']


        for page in parenting :
            if (page.slug != 'home') and (page.slug != 'root') :
                path_en_array.append(page.slug_en) 
                path_fr_array.append(page.slug_fr)

        if (page.slug != 'home') and (page.slug != 'root') :
            path_en_array.append(self.slug_en)
            path_fr_array.append(self.slug_fr)

        context['path_en'] = '/'.join(path_en_array)
        context['path_fr'] = '/'.join(path_fr_array)

        return context

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    url_image = models.CharField(blank=True,max_length=400)
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('url_image'),
        FieldPanel('caption'),
    ]

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        
        # Update context to include translated links for the flags
        parenting = Page.objects.filter(live=True).parent_of(self)

        path_en_array = ['/en']
        path_fr_array = ['/fr']


        for page in parenting :
            if (page.slug != 'home') and (page.slug != 'root') :
                path_en_array.append(page.slug_en) 
                path_fr_array.append(page.slug_fr)

        if (page.slug != 'home') and (page.slug != 'root') :
            path_en_array.append(self.slug_en)
            path_fr_array.append(self.slug_fr)

        context['path_en'] = '/'.join(path_en_array)
        context['path_fr'] = '/'.join(path_fr_array)

        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]
    
    
    

class BlogTagIndexPage(Page):
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag) 

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        
        
        # Update context to include translated links for the flags
        context = super().get_context(request)
        parenting = Page.objects.filter(
        live=True).parent_of(self)

        path_en_array = ['/en']
        path_fr_array = ['/fr']


        for page in parenting :
            if (page.slug != 'home') and (page.slug != 'root') :
                path_en_array.append(page.slug_en) 
                path_fr_array.append(page.slug_fr)

        if (page.slug != 'home') and (page.slug != 'root') :
            path_en_array.append(self.slug_en)
            path_fr_array.append(self.slug_fr)

        context['path_en'] = '/'.join(path_en_array)
        context['path_fr'] = '/'.join(path_fr_array)

        return context
