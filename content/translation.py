from .models import DomainPage,ContentPage,ContentPageGalleryImage,FormField,FormPage, DevPage, MobilePage, DevPageGallerySite, DevPageGalleryTechnologies, ConsultingPage, BizAppPage, BizAppStep, BizAppSector, BizPageGalleryTechnologies
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(DomainPage)
class DomainPageTR(TranslationOptions):
	fields=('intro',)

@register(ContentPage)
class ContentPageTR(TranslationOptions):
	fields=('intro','body','short_description',)

@register(ContentPageGalleryImage)
class ContentPageGalleryImageTR(TranslationOptions):
	fields = ('caption',)

@register(FormField)
class FormFieldTR(TranslationOptions):
	pass

@register(FormPage)
class FormPageTR(TranslationOptions):
	fields=('intro','thank_you_text','subject',)

@register(DevPage)
class DevPageRT(TranslationOptions):
	fields=('text_techno','text_responsive',)

@register(MobilePage)
class MobilePageRT(TranslationOptions):
	pass

@register(DevPageGallerySite)
class DevPageGallerySiteRT(TranslationOptions):
	fields=('caption',)

@register(DevPageGalleryTechnologies)
class DevPageGalleryTechnologiesRT(TranslationOptions):
	pass

@register(ConsultingPage)
class ConsultingPageRT(TranslationOptions):
	fields=('text_IT','text_BPO','text_consulting',)

@register(BizAppPage)
class BizAppPageRT(TranslationOptions):
	fields=('quote_text','sector_text','principle','text_techno',)

@register(BizAppStep)
class BizAppStepRT(TranslationOptions):
	fields=('text','title',)

@register(BizAppSector)
class BizAppSectorRT(TranslationOptions):
	fields=('text','title',)


@register(BizPageGalleryTechnologies)
class DevPageGalleryTechnologiesRT(TranslationOptions):
	pass

