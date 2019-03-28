import django

from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel

from modelcluster.fields import ParentalKey,ForeignKey
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from blog.models import BlogPage
from content.models import ContentPage

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

class HomePage(Page):
    highlight_title = models.CharField(blank=True,max_length=200)
    highlight_text = RichTextField(blank=True)

    testimonial_title = models.CharField(blank=True,max_length=200)
    testimonial_text = RichTextField(blank=True)

    cta1_title = models.CharField(blank=True,max_length=200)
    cta1_text = RichTextField(blank=True)

    cta2_title = models.CharField(blank=True,max_length=200)
    cta2_text = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('highlight_title'),
        FieldPanel('highlight_text'),
        FieldPanel('testimonial_title'),
        FieldPanel('testimonial_text'),
        InlinePanel('list_testimonials', label = "Témoignages"),
        FieldPanel('cta1_title'),
        FieldPanel('cta1_text'),
        FieldPanel('cta2_title'),
        FieldPanel('cta2_text'),
    ]


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['menuitems'] = self.get_children().filter(
        live=True, show_in_menus=True)
        context['blogarticles']=BlogPage.objects.filter(live=True)[:3]
        activity_domain = self.get_children().filter(
        live=True, show_in_menus=True)[0]
        activities=ContentPage.objects.filter(
        live=True).descendant_of(activity_domain)
        for i in range(0,len(activities)):
            link = 'acti_url_' + str(i)
            job = 'acti_job_' + str(i)
            title = 'acti_title_' + str(i)
            code = 'class_code_' + str(i)
            context[link]=activities[i].url
            context[job]=activities[i].short_description
            context[title]=activities[i].title
            context[code]=activities[i].class_code

        # Update context to include translated links for the flags
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



class Testimonial(Orderable):
    page = ParentalKey(HomePage,on_delete=models.CASCADE, related_name='list_testimonials')
    name = models.CharField(max_length=75)
    text = models.CharField(blank=True,max_length=400)
    position = models.CharField(blank=True,max_length=50)
    picture_url = models.CharField(blank=True,max_length=400)
    panels = [
        FieldPanel('picture_url'),
        FieldPanel('text'),
        FieldPanel('name'),
        FieldPanel('position'),
    ]


