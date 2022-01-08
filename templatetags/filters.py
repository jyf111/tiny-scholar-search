from django.template import Library

register = Library()

@register.filter
def work(num):
    res = ""
    while num>1000:
        res = ',' + str(int(num%1000)) + res;
        num //= 1000;
    res = str(num) + res;
    return res;