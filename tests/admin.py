from django.contrib import admin
from models import paper,result,question,test,e_user,section,saved_paper
from django import template
# Register your models here.


@admin.register(paper)
class paperAdmin(admin.ModelAdmin):
	pass

@admin.register(question)
class questionAdmin(admin.ModelAdmin):
	pass

@admin.register(saved_paper)
class saved_paperAdmin(admin.ModelAdmin):
	pass

@admin.register(test)
class testAdmin(admin.ModelAdmin):
	pass

@admin.register(e_user)
class e_userAdmin(admin.ModelAdmin):
	pass

@admin.register(section)
class sectionAdmin(admin.ModelAdmin):
	pass

@admin.register(result)
class resultAdmin(admin.ModelAdmin):
	pass
