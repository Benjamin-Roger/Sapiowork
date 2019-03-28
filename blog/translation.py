from .models import BlogPageTag,BlogCategory,BlogPage,BlogPageGalleryImage,BlogIndexPage,BlogTagIndexPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(BlogPageTag)
class BlogPageTagTR(TranslationOptions):
	pass

@register(BlogCategory)
class BlogCategoryTR(TranslationOptions):
	fields = ('name',)

@register(BlogPage)
class BlogPageTR(TranslationOptions):
	fields = ('intro','body','body_stream',)

@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
	fields=('intro',)

@register(BlogTagIndexPage)
class BlogTagIndexPageTR(TranslationOptions):
	pass


@register(BlogPageGalleryImage)
class BlogPageGalleryImageTR(TranslationOptions):
	fields = ('caption',)
