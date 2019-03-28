from .models import HomePage,Testimonial
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register



@register(Testimonial)
class TestimonialTR(TranslationOptions):
	fields = ('text', 'name','position',)



@register(HomePage)
class HomePageTR(TranslationOptions):
	fields = ('testimonial_title','testimonial_text','highlight_title','highlight_text','cta1_title','cta1_text','cta2_title','cta2_text')

