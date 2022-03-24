from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Question,Learner
import random
import pymc as pm
import time


# Create your views here.

def index(request):
    return render(request,"index.html")#("<h1>MYLEARNING</h1>")      


@csrf_exempt
def question(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        q = Question.objects.all()
        l = Learner.objects.get(id=data['user_id'])
        answered = l.getList(l.answered)
        responses = l.getList(l.responses)
        if data['last_response']==-1:
            if not answered:
                infoList = list()
                qList = list()
                for ques in q:
                    infoList.append(ques.evalIIF(l.ability))
                    qList.append(ques)
                maxInfo = max(infoList)
                recoQList = [ques for ques in qList if ques.evalIIF(l.ability) == maxInfo]
                index = random.randint(0,len(recoQList)-1)
                s = recoQList[index]
                content = {'id':s.id, 'question':s.question, 'choices':s.choices, 'difficulty':s.difficulty, 'answer':s.answer, 'ability':l.ability, 'time':time.time()}
                return JsonResponse(content,status=status.HTTP_200_OK)
            else:
                infoList = list()
                qList = list()
                for ques in q:
                    if ques.id not in answered:
                        infoList.append(ques.evalIIF(l.ability))
                        qList.append(ques)
                if(len(qList)==0):
                    return JsonResponse({'data': 'No More Questions'},status=status.HTTP_404_NOT_FOUND)
                maxInfo = max(infoList)
                recoQList = [ques for ques in qList if ques.evalIIF(l.ability) == maxInfo]
                index = random.randint(0,len(recoQList)-1)
                s = recoQList[index]
                content = {'id':s.id, 'question':s.question, 'choices':s.choices, 'difficulty':s.difficulty, 'answer':s.answer, 'ability':l.ability, 'time':time.time()}
                return JsonResponse(content,status=status.HTTP_200_OK)
        else:
            if not answered:
                answered = list()
                responses = list()
                responses.append(data['last_response'])
                answered.append(data['last_qid'])
                r = Question.objects.get(id=data['last_qid'])
                theta = pm.Beta('theta',1,1)
                l.updateAbility(r,responses,theta)
                l.answered = l.setList(answered)
                l.responses = l.setList(responses)
                l.save()
                infoList = list()
                qList = list()
                for ques in q:
                    if ques.id not in answered:
                        infoList.append(ques.evalIIF(l.ability))
                        qList.append(ques)
                maxInfo = max(infoList)
                recoQList = [ques for ques in qList if ques.evalIIF(l.ability) == maxInfo]
                index = random.randint(0,len(recoQList)-1)
                s = recoQList[index]
                content = {'id':s.id, 'question':s.question, 'choices':s.choices, 'difficulty':s.difficulty, 'answer':s.answer, 'ability':l.ability, 'time':time.time()}
                return JsonResponse(content,status=status.HTTP_200_OK)
            else:
                theta = pm.Beta('theta',1,1)
                count = 0
                for ques in answered:
                    r = Question.objects.get(id=ques)
                    l.update(r,responses[count],theta)
                    count += 1
                responses.append(data['last_response'])
                answered.append(data['last_qid'])
                r = Question.objects.get(id=data['last_qid'])
                l.updateAbility(r,responses,theta)
                l.answered = l.setList(answered)
                l.responses = l.setList(responses)
                l.save()
                infoList = list()
                qList = list()
                for ques in q:
                    if ques.id not in answered:
                        infoList.append(ques.evalIIF(l.ability))
                        qList.append(ques)
                if(len(qList)==0):
                    return JsonResponse({'data': 'No More Questions','ability': l.ability},status=status.HTTP_404_NOT_FOUND)
                maxInfo = max(infoList)
                recoQList = [ques for ques in qList if ques.evalIIF(l.ability) == maxInfo]
                index = random.randint(0,len(recoQList)-1)
                s = recoQList[index]
                content = {'id':s.id, 'question':s.question, 'choices':s.choices, 'difficulty':s.difficulty, 'answer':s.answer, 'ability': l.ability, 'time':time.time()}
                return JsonResponse(content,status=status.HTTP_200_OK)
    return JsonResponse({"data":"Erroneous Navigation"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
