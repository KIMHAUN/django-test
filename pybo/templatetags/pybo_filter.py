from django import template
from django.utils.safestring import mark_safe

# 마크다운 ->html 태그로 변환
import markdown

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
#value는 마크다운 언어로 입력받을 값
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))