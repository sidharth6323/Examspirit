from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect,RequestContext
from models import test,e_user,paper,question,section,result,saved_paper
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
	ongoing=[]
	papers=paper.objects.all()
	today=datetime.datetime.now()
	for i in papers:
		if today.date()>=i.s_date and today.date()<=i.e_date:
			if today.date()==i.s_date:
				if today.time()<i.s_time:
					continue
			if today.date()==i.e_date:
				if today.time()>i.e_time:
					continue
			ongoing.append(i)
			print ongoing
	return render_to_response("index.html",{"tests":tests,"user":user_l,"ongoing":ongoing},context_instance=RequestContext(request))

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
	today=datetime.datetime.now()
	upcoming=[]
	previous=[]
	ongoing=[]
	saved = []
	t_given=[]
	if user_m.p_given:
		for i in user_m.p_given:
			try:
				paper_t = paper.objects.get(p_name=i)
				r_given= result.objects.get(user=user_l,paper=paper_t)
			except:
				r_given = ""
			if r_given:
				p_given=paper.objects.get(p_name=i)
				t_given.append(p_given)
			else:
				p_given=paper.objects.get(p_name=i)
				saved.append(p_given)
	new_p = [item for item in papers if item not in t_given]
	for i in new_p:
		if today.date()>=i.s_date and today.date()<=i.e_date:
			if today.date()==i.s_date:
				if  today.time()<i.s_time:
					upcoming.append(i)
					continue
			if today.date()==i.e_date:
				if today.time()>i.e_time:
					previous.append(i)
					continue
			try:
				p_saved = saved_paper.objects.get(paper=i,user=user_l)
			except:
				p_saved=""
			if p_saved:
				saved.append(i)
			else:
				ongoing.append(i)
		if today.date()>i.e_date:
			previous.append(i)
		if today.date()<i.s_date:
			upcoming.append(i)
	return render_to_response("dashboard.html",{"user":user_l,"tests":tests,"upcoming":upcoming,"previous":previous,"saved":saved,"ongoing":ongoing,"t_given":t_given,"user_m":user_m,"papers":papers})

@login_required	
def instruct_p(request,test,p_id):
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	paper_l=paper.objects.get(p_id=p_id)
	return render_to_response("instructions.html",{"user":user_l,"paper_l":paper_l,"user_m":user_m})

@login_required
def paper_p(request,test,p_id):
	paper_l=paper.objects.get(p_id=p_id)
	now=datetime.datetime.now()
	s_time=now.replace(hour=paper_l.s_time.hour,minute=paper_l.s_time.minute)
	e_time=now.replace(hour=paper_l.e_time.hour,minute=paper_l.e_time.minute)
	s_date=now.replace(day=paper_l.s_date.day,month=paper_l.s_date.month,year=paper_l.s_date.year)
	e_date=now.replace(day=paper_l.e_date.day,month=paper_l.e_date.month,year=paper_l.e_date.year)
	print "now: "+str(now.time())+" start: "+str(s_time.time())+" duration: "+str(paper_l.duration)+" e_time: "+str(e_time.time())
	if now.date()>e_date.date():
		print "invalid"
		return render_to_response("t_expired.html",{"user":request.user})
	if now.date()==e_date.date():
		if now.time()>e_time.time():
			return render_to_response("t_expired.html",{"user":request.user})
	print "valid"
	if s_time+paper_l.duration>e_time:
		print "exceeded"
		now=datetime.datetime.now()
		duration=e_time-now
		print duration
	else:
		duration=paper_l.duration
	iterator=itertools.count(1)
	iterator2=itertools.count(1)
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	if user_m.p_given:
		for i in user_m.p_given:
			if i==paper_l.p_name:
				return render_to_response("test_given.html",{"paper_l":paper_l})	
	try:
		paper_s = saved_paper.objects.get(user=user_l,paper=paper_l)
		saved_ans= dict([(str(k.encode("utf-8")), str(v.encode("utf-8"))) for k, v in paper_s.t_res.items()])
		answered = paper_s.ansered
		unanswered = paper_s.unanswered
		skipped = paper_s.skipped
	except:
		paper_s = ""
		saved_ans = ""
		answered = ""
		unanswered = ""
		skipped = ""
	question_l=question.objects.filter(paper=paper_l)
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
		count=1
		q_count=0
		q_5_count=1
		question_l=question.objects.filter(paper=paper_l)
		print "questions"+str(question_l)
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
		print "new_section"+str(new_section)
	nop=0
	section_p={}
	for i,j in new_section.iteritems():
		section_p[i]=len(j)
		nop=nop+len(j)
	print nop
	print section_p
	#return HttpResponse(json.dumps(new_section))
	return render_to_response("paper.html",{"user":user_l,"answered":answered,"unanswered":unanswered,"skipped":skipped,"saved_ans":saved_ans,"paper_s":paper_s,"section_p":section_p,"iterator":iterator,"iterator2":iterator2,"nop":range(1,nop+1),"duration":duration,"noq":range(1,len(question_l)+1),"final_q":new_section,"questions":question_l,"paper_l":paper_l,"user_m":user_m})

def generate_result(request):
	user_l=request.user
	user_m = e_user.objects.get(user=user_l)
	paper_l=paper.objects.get(p_id=json.loads(request.body)["p_id"])
	result_l=result.objects.create(user=user_l,paper=paper_l)
	p={}
	p_user=user_m.p_given
	if p_user:
		p_user.append(str(paper_l.p_name))
	else:
		p_user = [str(paper_l.p_name)]
	user_m.p_given=p_user
	user_m.save()
	for i,j in json.loads(request.body)["ans"].iteritems():
		ques=question.objects.get(q_id=i).q_id
		if j!="none":
			p[str(ques)]="c"+j[-1]
	result_l.res=p
	answered=0
	correct=0
	for i,j in p.iteritems():
		if j!="none":
			answered=answered+1
		ans=question.objects.get(q_id=i).correct
		if j==ans:
			correct=correct+1
	result_l.correct=correct
	result_l.answered=answered
	result_l.unanswered=(len(question.objects.filter(paper=paper_l))-answered)
	result_l.marks=(paper_l.p_marks*result_l.correct)+(paper_l.n_marks*(result_l.answered-result_l.correct))
	result_l.save()
	print "answered "+str(answered)
	print "correct "+str(correct)
	return HttpResponse(json.dumps(p))

@login_required
def finish_t(request,p_id): 
	user_l=request.user
	paper_l=paper.objects.get(p_id=p_id)
	return render_to_response("finish_t.html",{"user":user_l,"paper_l":paper_l})

def mission(request):
	tests=test.objects.all()
	user_l=request.user
	return render_to_response("mission.html",{"user":user_l,"tests":tests})

def contact(request):
	tests=test.objects.all()
	user_l=request.user
	return render_to_response("contact.html",{"user":user_l,"tests":tests})

@login_required
def result_r(request,p_id):
	user_l=request.user
	paper_l=paper.objects.get(p_id=p_id)
	try:
		result_l=result.objects.get(user=user_l,paper=paper_l)
	except:
		return render_to_response("result_not.html",{"user":user_l})
	return render_to_response("result.html",{"user":user_l,"paper":paper_l,"result":result_l})

@login_required
def rank(request,p_id):
	user_l=request.user
	paper_l=paper.objects.get(p_id=p_id)
	now=datetime.datetime.now()
	rank=1
	user_given=0
	if now.date()>=paper_l.e_date:
		if now.time()>paper_l.e_time:
			user_all=e_user.objects.all()
			for i in user_all:
				if paper_l.p_name in i.p_given:
					try:
						result_l=result.objects.get(paper=paper_l,user=user_l)
						result_m=result.objects.get(paper=paper_l,user=i.user)
						user_given=user_given+1
						if result_m.marks>result_l.marks:
							rank=rank+1
						print rank
					except:
						return render_to_response("rank.html",{"user":user_l})
			return render_to_response("rank.html",{"user":user_l,"rank":rank,"user_given":user_given})
	return render_to_response("rank.html",{"user":user_l})

@login_required
def profile(request):
	user_l=request.user
	user_m=e_user.objects.get(user=request.user)
	t_given=[]
	if user_m.p_given:
		for i in user_m.p_given:
				p_given=paper.objects.get(p_name=i)
				t_given.append(p_given)
	return render_to_response("profile.html",{"user":user_l,"e_user":user_m,"t_given":t_given},context_instance=RequestContext(request))

def parteners(request):
	user_l=request.user
	return render_to_response("parteners.html",{"user":user_l})

@login_required
def edit_basic(request):
	user_l=request.user
	user_m=e_user.objects.get(user=user_l)
	user_m.f_name=request.POST.get("name")
	user_m.email=request.POST.get("email")
	user_m.mobile=request.POST.get("mobile")
	user_m.dob=request.POST.get("dob")
	user_m.save()
	return HttpResponseRedirect("/profile/")

@login_required
def edit_sec(request):
	user_l=request.user
	username=request.POST.get("username")
	o_password=request.POST.get("o_password")
	n_password=request.POST.get("n_password")
	print user_l.password
	if user_l.check_password(o_password):
		user_l.username=username
		user_l.set_password(n_password)
		user_l.save()
	return HttpResponseRedirect("/dashboard/")

@login_required
def save_paper(request,p_id):
	user_l=request.user
	paper_l=paper.objects.get(p_id=p_id)
	try:
		paper_m = saved_paper.objects.get(user=user_l,paper=paper_l)
	except:
		paper_m= ""
	hours = int(json.loads(request.body)["t_left"].split(":")[0])
	minutes = int(json.loads(request.body)["t_left"].split(":")[1])
	seconds = int(json.loads(request.body)["t_left"].split(":")[2])
	time_left = datetime.timedelta(hours=hours,minutes=minutes,seconds=seconds)
	answered = json.loads(request.body)["answered"]
	unanswered = json.loads(request.body)["unanswered"];
	skipped = json.loads(request.body)["skipped"]
	print answered , unanswered , skipped
	if paper_m:
		paper_m.t_left=time_left
		paper_m.t_res = json.loads(request.body)["t_res"]
		paper_m.ansered = answered
		paper_m.skipped = skipped
		paper_m.unanswered = unanswered
		paper_m.save()
	else:
		saved_paper.objects.create(user=user_l,paper=paper_l,t_left=time_left,t_res=json.loads(request.body)["t_res"],ansered=answered,unanswered=unanswered,skipped=skipped)
	return HttpResponse(json.dumps({}))