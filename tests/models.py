from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.auth.models import User
import uuid,datetime

# Create your models here.
choices=(
			('c1','c1'),
			('c2','c2'),
			('c3','c3'),
			('c4','c4'),
)

class test(models.Model):
	t_name=models.CharField(max_length=30)
	def __str__(self):
		return self.t_name

class section(models.Model):
	s_name=models.CharField(max_length=50)
	def __str__(self):
		return self.s_name

class e_user(models.Model):
	user= models.OneToOneField(User, unique=True)
	f_name=models.CharField(max_length=50)
	email=models.EmailField()
	mobile=models.IntegerField()
	dob=models.DateField()
	test=models.ForeignKey(test)
	all_papers=models.CharField(max_length=50,blank=True,null=True)
	rank=models.IntegerField(null=True,blank=True)
	def __str__(self):
		return self.user.username

class paper(models.Model):
	test=models.ForeignKey(test)
	p_id=models.UUIDField(default=uuid.uuid4)
	p_name=models.CharField(max_length=50)
	instructions=models.TextField(max_length=10000)
	sections=models.ManyToManyField(section,null=True,blank=True)
	duration=models.DurationField()
	s_time=models.TimeField()
	e_time=models.TimeField(default=datetime.datetime.now())
	date=models.DateField()
	def __str__(self):
		return str(self.test.t_name)+":"+str(self.p_name)+":"+str(self.p_id)

class question(models.Model):
	q_id=models.UUIDField(default=uuid.uuid4)
	paper=models.ForeignKey(paper)
	section=models.ForeignKey(section,null=True,blank=True)
	q_des=models.TextField(max_length=1000)
	c1=models.CharField(max_length=500)
	c2=models.CharField(max_length=500)
	c3=models.CharField(max_length=500)
	c4=models.CharField(max_length=500)
	correct=models.CharField(max_length=50,choices=choices)
	def __str__(self):
		return self.paper.test.t_name+":"+str(self.paper.p_id)+":"+self.q_des

class result(models.Model):
	user=models.ForeignKey(User)
	paper=models.ForeignKey(paper)
	res=models.TextField(max_length=100000)
