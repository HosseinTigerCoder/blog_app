import re
import html

from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def plain_text(value):
    if not value:
        return ""

    # حذف تگ‌های HTML
    text = strip_tags(str(value))

    # تبدیل کدهای HTML به کاراکترهای معمولی
    text = html.unescape(text)

    # یکسان‌سازی فاصله‌ها و حذف فاصله‌های اضافی
    text = re.sub(r'\s+',' ',text).strip()

    return text

