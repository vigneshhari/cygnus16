from django.shortcuts import render
from accounts.models import User_Account 
import datetime
from models import Quiz_history,Quiz,Quiz_data
from django.http import HttpResponseRedirect
# Create your views here.


def dash(request):
	try:
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	quiz = Quiz_history.objects.all().filter(user_id = _id)
	quiz_info = Quiz.objects.all() 
	for h in acc:
		name = h.name
		check = h.vericode
		score = h.score
	if(check != vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	done = 0
	avail = 0
	done_quiz = []
	for k in quiz:
		done = done + 1
		done_quiz.append(k.quiz_id)
	for i in quiz_info:
		if(i.quiz_id not in done_quiz):avail = avail + 1
	return render(request,'dash.html',{'name' : name , 'score' : score,'done':done , 'avail' : avail})

def attempted(request):
	try:
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	data = Quiz_history.objects.all().filter(user_id = _id)
	return render(request,'quizold.html',{'name' : name , 'data' : data })

def avaliable(request):
	try:
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	quiz = Quiz_history.objects.all().filter(user_id = _id)
	quiz_info = Quiz.objects.all() 
	done_quiz = []
	lis = []
	done = 0
	for k in quiz:
		done = done + 1
		done_quiz.append(k.quiz_id)
	for i in quiz_info:
		if(i.quiz_id not in done_quiz):
			lis.append({ 'quizid' : i.quiz_id , 'quizname' :i.quizname })
	return render(request,'newquiz.html',{'name' : name , 'data' : lis ,'link':"/quiz/attempt?id="})

def attempt(request):
	try:
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	quizid =request.GET.get('id')
	quiz_history = Quiz_history.objects.all().filter(user_id = _id ,quiz_id = quizid)
	for i in quiz_history:
		return HttpResponseRedirect('/quiz/dash')
	quizdata = Quiz_data.objects.all().filter(quiz_id = quizid)
	request.session['quizid'] = quizid
	temp = 1
	data = []
	for e in quizdata:
		print temp
		data.append({'qid' : temp , 'question' : e.question , 'question_type' : e.question_type , 'Option1' : e.Option1 ,'Option2' : e.Option2 ,'Option3' : e.Option3 ,'Option4' : e.Option4})
		temp = temp + 1
	return render(request,'quiz.html',{'name' : name , 'data' : data})

def validate(request):
	try:
		quizid = request.session['quizid']
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	quiz_history = Quiz_history.objects.all().filter(user_id = _id ,quiz_id = quizid)
	for i in quiz_history:
		return HttpResponseRedirect('/quiz/dash')
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		oldscore = h.score
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'})
	quizdata = Quiz_data.objects.all().filter(quiz_id = quizid)
	temp = 1
	score = 0
	for i in quizdata:
		val = request.GET.get(str(temp),'')
		if(i.answer.lower() == val.lower()):
			score += 10
		temp = temp + 1
	print score
	hist = Quiz_history(quiz_id = quizid , user_id = _id , score = score , Date = datetime.datetime.now())
	hist.save()
	score = score + oldscore
	User_Account.objects.all().filter(user_id = _id).update(score = score)
	return HttpResponseRedirect('/quiz/dash')

def rank(request):
	try:
		_id = request.session['logid']
		vericode = request.session['vericode']
	except Exception, e:
		return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	acc = User_Account.objects.all().filter(user_id = _id)
	for h in acc:
		name = h.name
		if(vericode != h.vericode):return render(request,'login.html',{'message' : 'Please Login Again to Continue'  })
	Userdata = User_Account.objects.all().order_by('-score')
	temp = []
	pos = 1
	for e in Userdata:
		temp.append({'pos' : pos , 'name':e.name , 'score':e.score})
		pos = pos + 1
	return render(request,'rank.html',{'name' : name , 'data' : temp})
