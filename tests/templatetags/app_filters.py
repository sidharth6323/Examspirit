from django import template
import textwrap
register = template.Library()

def inc(value):
    a=range(1,value+1)
    #./count=count+1
    return a

register.filter('inc', inc)

def wrap_me(value,integ):
	return textwrap.fill(value, int(integ))

register.filter('wrap_me', wrap_me)