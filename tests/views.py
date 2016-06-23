from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect,RequestContext
from models import test,e_user,paper,question,section,result
from django.contrib.auth.models import User
from django.contrib import auth
import json,datetime,itertools
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def base(request):
	return render_to_response("base.html",{})

def index(request):
	tests=test.objects.all()
	user_l=request.user
	return render_to_response("index.html",{"tests":tests,"user":user_l},context_instance=RequestContext(request))

def signup(request):
	tests=test.objects.all()
	if request.method=="POST":
		user_m=request.user
		if not user_m.is_authenticated:
			return HttpResponseRedirect("/")
		tests=test.objects.all()
		username=request.POST.get("username")
		password=request.POST.get("password")
		email=request.POST.get("email")
		try:
			user_l= User.objects.get(username=username)
		except:
			user_l=""
		if not user_l:
			user_new = User.objects.create_user(username, email, password)
			user_new.save()
		else:
			tests=test.objects.all()
			return HttpResponseRedirect("/")
		try:
			user_l= User.objects.get(username=username)
			f_name=request.POST.get("f_name")
			mobile=request.POST.get("mobile")
			dob=request.POST.get("dob")
			test_name=request.POST.get("test")
			test_l=test.objects.get(t_name=test_name)
			e_user.objects.create(user=user_l,f_name=f_name,mobile=mobile,dob=dob,test=test_l,email=email)
		except:
			a=User.objects.get(username=username)
			a.delete()
			return render_to_response("index.html",{"tests":tests,"error":"Fill all the fields appropriately!"},context_instance=RequestContext(request))
		user_logged = authenticate(username=username, password=password)
		if user_logged is not None:
			login(request,user_logged)
		return HttpResponseRedirect("/dashboard/")
	return HttpResponseRedirect("/")

def signin(request):
	auth.logout(request)
	if request.method=="POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		user_logged = authenticate(username=username, password=password)
		if user_logged is not None:
			login(request,user_logged)
		else:
			tests=test.objects.all()
			return render_to_response("index.html",{"tests":tests,"error":"Invalid Username or Password"},context_instance=RequestContext(request))
		return HttpResponseRedirect("/dashboard/")
	return HttpResponseRedirect("/dashboard/")

def logout(request):
	if request.user:
		auth.logout(request)
	return HttpResponseRedirect('/')

@login_required
def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/index/')
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	papers=paper.objects.all()
	tests=test.objects.all()
	today=datetime.datetime.now().date()
	upcoming=[]
	previous=[]
	ongoing=[]
	for i in papers:
		if i.date>today:
			upcoming.append(i)
		elif i.date<today:
			previous.append(i)
		else:
			ongoing.append(i)
	return render_to_response("dashboard.html",{"user":user_l,"tests":tests,"upcoming":upcoming,"previous":previous,"ongoing":ongoing,"user_m":user_m,"papers":papers})

@login_required	
def instruct_p(request,test,p_id):
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	paper_l=paper.objects.get(p_id=p_id)
	return render_to_response("instructions.html",{"user":user_l,"paper_l":paper_l,"user_m":user_m})

@login_required
def paper_p(request,test,p_id):
	iterator=itertools.count(1)
	iterator2=itertools.count(1)
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	paper_l=paper.objects.get(p_id=p_id)
	question_l=question.objects.filter(paper=paper_l)
	now=datetime.datetime.now()
	s_time=now.replace(hour=paper_l.s_time.hour,minute=paper_l.s_time.minute)
	e_time=now.replace(hour=paper_l.e_time.hour,minute=paper_l.e_time.minute)
	print "now: "+str(now.time())+" start: "+str(s_time.time())+" duration: "+str(paper_l.duration)+" e_time: "+str(e_time.time())
	if now > e_time or now < s_time:
		print "invalid"
		return render_to_response("t_expired.html",{})
	else:
		print "valid"
		if s_time+paper_l.duration>e_time:
			print "exceeded"
			duration=e_time-s_time
			print duration
		else:
			duration=paper_l.duration
		try:
			result.objects.get(user=user_l,paper=paper_l)
		except:
			result.objects.create(user=user_l,paper=paper_l,res="")
		section_l=paper_l.sections
		a=[]
		count=1
		q_count=0
		c=[]
		q_5_count=1
		final_q=[]
		new_section={}
		if section_l.all():
			for sec in section_l.all():
				a=[]
				c=[q_5_count]
				question_m=question.objects.filter(paper=paper_l,section=sec)
				print question_m
				for i in question_m:
					q_count=q_count+1
					b={}
					options=[i.c1,i.c2,i.c3,i.c4,count,str(i.q_id),str(sec)]
					count=count+1
					b[i.q_des]=options
					c.append(b)
					if q_count==5:
						a.append(c)
						q_count=0
						q_5_count=q_5_count+1
						c=[q_5_count]
					print count
				if len(c)>1:
					a.append(c)
				new_section[str(sec)]=a
				final_q.append(new_section)
		else:
			count=0
			for i in question_l:
					q_count=q_count+1
					b={}
					options=[i.c1,i.c2,i.c3,i.c4,count,str(i.q_id),"None"]
					count=count+1
					b[i.q_des]=options
					c.append(b)
					if q_count==5:
						a.append(c)
						q_count=0
						q_5_count=q_5_count+1
						c=[q_5_count]
					print count
			if len(c)>1:
					a.append(c)
			new_section["None"]=a
		nop=0
		section_p={}
		for i,j in new_section.iteritems():
			section_p[i]=len(j)
			nop=nop+len(j)
		print nop
		print section_p
		#return HttpResponse(json.dumps(new_section))
		return render_to_response("paper.html",{"user":user_l,"section_p":section_p,"iterator":iterator,"iterator2":iterator2,"nop":range(1,nop+1),"duration":duration,"noq":range(1,len(question_l)+1),"final_q":new_section,"questions":question_l,"paper_l":paper_l,"user_m":user_m})

def generate_result(request):
	user_l=request.user
	paper_l=paper.objects.get(p_id=json.loads(request.body)["p_id"])
	result_l=result.objects.get(user=user_l,paper=paper_l)
	p={}
	for i,j in json.loads(request.body)["ans"].iteritems():
		ques=question.objects.get(q_id=i).q_des
		p[ques]=j
	result_l.res=p
	result_l.save()
	return HttpResponse(json.dumps(p))

@login_required
def finish_t(request): 
	user_l=request.user
	return render_to_response("finish_t.html",{"user":user_l})

def mission(request):
	user_l=request.user
	return render_to_response("mission.html",{"user":user_l})

def contact(request):
	user_l=request.user
	return render_to_response("contact.html",{"user":user_l})