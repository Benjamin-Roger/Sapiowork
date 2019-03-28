from django.db import models
from modelcluster.fields import ParentalKey,ForeignKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel,InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

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

# Models for top level domain page

class DomainPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def get_context(self, request):
        # Update context to include any children
        context = super().get_context(request)
        activities=ContentPage.objects.filter(
        live=True).descendant_of(self)
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

# Models for basic content page

class ContentPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    short_description = models.CharField(blank=True,max_length=500)
    class_code = models.CharField(blank=True,max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('short_description', classname="full"),
        FieldPanel('class_code', classname="full"),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images")
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image_url
        else:
            return None
            
    def get_context(self, request):
        # Update context to include translated links for the flags
        context = super().get_context(request)
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
    
class ContentPageGalleryImage(Orderable):
    page = ParentalKey(ContentPage, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.CharField(blank=True,max_length=400)
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image_url'),
        FieldPanel('caption'),
    ]

# Models for contact forms

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
    
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

# Models for web dev pages

class DevPage(ContentPage):
    text_techno = RichTextField(blank=True)
    text_responsive = RichTextField(blank=True)

    content_panels = ContentPage.content_panels + [
        FieldPanel('text_techno', classname="full"),
        FieldPanel('text_responsive', classname="full"),
        InlinePanel('dev_page_gallery_site', label="Gallery sites"),
        InlinePanel('dev_page_gallery_technologies', label="Gallery technologies")
    ]

class DevPageGallerySite(Orderable):
    page = ParentalKey(DevPage, on_delete=models.CASCADE, related_name='dev_page_gallery_site')
    image_url = models.CharField(blank=True,max_length=400)
    caption = RichTextField(blank=True, max_length=450)

    panels = [
        FieldPanel('image_url'),
        FieldPanel('caption'),
    ]



class DevPageGalleryTechnologies(Orderable):
    page = ParentalKey(DevPage, on_delete=models.CASCADE, related_name='dev_page_gallery_technologies')
    image_url = models.CharField(blank=True,max_length=400)
    panels = [
        FieldPanel('image_url'),
    ]

# Models for mobile dev page

class MobilePage(DevPage):
    pass


# Models for consulting page

class ConsultingPage(ContentPage):
    text_IT = RichTextField(blank=True)
    text_BPO = RichTextField(blank=True)
    text_consulting = RichTextField(blank=True)

    content_panels = ContentPage.content_panels + [
        FieldPanel('text_IT', classname="full"),
        FieldPanel('text_BPO', classname="full"),
        FieldPanel('text_consulting', classname="full")
        ]



# Models for business app page

class BizAppPage(ContentPage):

    quote_text = models.CharField(blank=True,max_length=400)
    sector_text = RichTextField(blank=True,max_length=400)
    principle = RichTextField(blank=True,max_length=400)
    text_techno = RichTextField(blank=True,max_length=400)

    
    content_panels = ContentPage.content_panels + [
        FieldPanel('quote_text',classname="full"),
        FieldPanel('sector_text',classname="full"),
        FieldPanel('principle',classname="full"),
        FieldPanel('text_techno', classname="full"),
        InlinePanel('ba_steps', label="Steps"),
        InlinePanel('ba_sectors', label="Sectors"),        
        InlinePanel('biz_page_gallery_technologies', label="Gallery technologies")
        ]


class BizAppStep(Orderable):
    page = ParentalKey(BizAppPage, on_delete=models.CASCADE, related_name='ba_steps')
    title = models.CharField(blank=True, max_length=250)
    text = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
    ]

class BizAppSector(Orderable):
    page = ParentalKey(BizAppPage, on_delete=models.CASCADE, related_name='ba_sectors')
    title = models.CharField(blank=True, max_length=250)
    text = models.CharField(blank=True, max_length=250)
    icon = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        FieldPanel('icon')
    ]


class BizPageGalleryTechnologies(Orderable):
    page = ParentalKey(BizAppPage, on_delete=models.CASCADE, related_name='biz_page_gallery_technologies')
    image_url = models.CharField(blank=True,max_length=400)
    panels = [
        FieldPanel('image_url'),
    ]
