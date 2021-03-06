from django.shortcuts import render, redirect
from django.contrib import auth
import random
import base64
from MockInterview.settings import BASE_DIR
import os, re, string
# from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf
from django.views.generic import TemplateView
from questions.models import *
from questions.forms import *
from users.models import *
from users.models import Member
from GTTS.forms import UploadAnswersForm
from nlp.views import predict
from nlp.views import sentiment
from Blink.tasks import *
from django.core.files import File
from Emotion.views import *
import sqlite3


conn=sqlite3.connect('db.sqlite3')
conn.execute("VACUUM")
conn.close()

class equipCheck(TemplateView): 
  template_name = 'equipCheck.html'

  def __init__(self, job_name=None):
    self.job_name = job_name

  def get(self, request):
    path = request.path
    print('current path: ', path)
    job_name = request.session['job_name']
    self.job_name = job_name
    print('You selected: '+ job_name)

    def create_ques(job):
      # EASY
      easy_QS = job.objects.filter(Difficulties='easy').values('Ques')
      easy_list = []
      for ques in easy_QS:
        ques = ques["Ques"]
        easy_list.append(ques)

      easy_length = len(easy_list)
      easy_rand = random.sample(easy_list, 3)
      # global r1
      # global r2
      global r1, r2, r3
      r1 = easy_rand[0]
      r2 = easy_rand[1]
      r3 = easy_rand[2]

      # MEDIUM
      medium_QS = job.objects.filter(Difficulties='medium').values('Ques')
      medium_list = []
      for ques in medium_QS:
        ques = ques["Ques"]
        medium_list.append(ques)

      medium_length = len(medium_list)
      medium_rand = random.sample(medium_list, 4)
      global r4, r5, r6, r7
      r4 = medium_rand[0]
      r5 = medium_rand[1]     
      r6 = medium_rand[2]
      r7 = medium_rand[3] 

      # HARD
      hard_QS = job.objects.filter(Difficulties='hard').values('Ques')
      hard_list = []
      for ques in hard_QS:
        ques = ques["Ques"]
        hard_list.append(ques)

      hard_length = len(hard_list)
      hard_rand = random.sample(hard_list, 3)
      global r8, r9 ,r10
      r8 = hard_rand[0]
      r9 = hard_rand[1]
      r10 = hard_rand[2]

      global final_list
      final_list = [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10]
      random.shuffle(final_list)

      # get difficulty of questions
      global diff_list
      diff_list = []
      for r in final_list:
        diff_QS = job.objects.filter(Ques=r).values('Difficulties')
        for diff in diff_QS:
          diff = diff['Difficulties']
          diff_list.append(diff)
    

    # throw questions according to selected job ==> ADD JOBS IN FUTURE!!
    if job_name == 'Software Engineer':
      create_ques(Software_Engineer)
    # for testing purposes only
    elif job_name == 'Cashier':
      create_ques(Test_Job_pls_dont_add_shit_into_this_model_thank)
    elif job_name == 'Sales Trading':
      create_ques(Sales_Trading)
    elif job_name == 'Hardware Engineer':
      create_ques(Hardware_Engineer)
    elif job_name == 'ML Engineer':
      create_ques(ML_Engineer)
    elif job_name == 'DBA':
      create_ques(DBA)
    elif job_name == 'Audit':
      create_ques(Audit)
    elif job_name == 'Quantitative':
      create_ques(Quantitative)
    elif job_name == 'Research':
      create_ques(Research)
    elif job_name == 'Investment Banking':
      create_ques(Investment_Banking)
    elif job_name == 'Data Scientist':
      create_ques(Data_Scientist)
    else:
      print('Job questions not created yet!!!')


    global q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
    q1 = final_list[0]
    q2 = final_list[1]
    q3 = final_list[2]
    q4 = final_list[3]
    q5 = final_list[4]
    q6 = final_list[5]
    q7 = final_list[6]
    q8 = final_list[7]
    q9 = final_list[8]
    q10 = final_list[9]

    # apply different time for different difficulty
    global prepare_time
    global answer_time
    prepare_time = []
    answer_time = []
    for i in range(0,10):
      if diff_list[i] == 'easy':
        prepare_time.append(15)
        answer_time.append(120)
      elif diff_list[i] == 'medium':
        prepare_time.append(15)
        answer_time.append(120)
      else:
        prepare_time.append(15)
        answer_time.append(120)

    print(diff_list)
    print(prepare_time)
    print(answer_time)

    global time_dict
    time_dict = {}
    for x in range(0,10):
      time_dict["prep_time{0}".format(x+1)] = prepare_time[x]
      time_dict["ans_time{0}".format(x+1)] = answer_time[x]
    
    return render(request, self.template_name)



class QuesView(TemplateView):
    template_name = 'speech_to_text.html'

    def __init__(self, job_name=None):
      self.job_name = job_name

    def get(self, request):
      job_name = request.session['job_name']
      self.job_name = job_name

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)
            # create answer & result table when getting website
            unit = Answer.objects.create(userID=account_instance, selected_job=job_name)
            uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')
            res = Result.objects.create(userID=account_instance, id=uid, selected_job=job_name)
            # create video table when getting website
            vid_unit = Video.objects.create(userID=account_instance, id=uid)
            vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')

      random_question = q1
      prep_time1 = time_dict['prep_time1']
      ans_time1 = time_dict['ans_time1']
      unit.q1 = q1
      unit.save()
      
      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a1 = request.POST['note-textarea']
        v1 = request.POST['video']
        t1 = request.POST['time']
        t1 = int(t1)

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.a1 = a1
        unit.v1 = v1
        unit.t1 = t1
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r1 = sentiment(1, account_name)
        res = Result.objects.get(id=uid)
        res.r1 = r1
        res.time1 = t1
        res.save()

        # decode base64 to mp4 file
        text = unit.v1
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid1.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        print('TIME =======> ', t1)
        path = request.path
        print('PATH =====> ', path)
        blink1(vid_path, account_name, t1, path)
        emotion1(vid_path, account_name, t1, path)

        return redirect('reply2/')
      
      return render(request, self.template_name,locals())   




class QuesView2(TemplateView):
    template_name = 'reply2.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q2
      prep_time2 = time_dict['prep_time2']
      ans_time2 = time_dict['ans_time2']
      total_time2 = prep_time2 + ans_time2 - 5

      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a2 = request.POST['note-textarea']
        v2 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t2 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q2 = q2
        unit.a2 = a2
        unit.v2 = v2
        unit.t2 = t2
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r2 = sentiment(2, account_name)
        res = Result.objects.get(id=uid)
        res.r2 = r2
        res.time2 = t2
        res.save()

        # decode base64 to mp4 file
        text = unit.v2
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid2.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid2
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink2(vid_path, account_name, t, path)
        emotion2(vid_path, account_name, t, path)

        return redirect('reply3/')

      return render(request, self.template_name, locals())   


class QuesView3(TemplateView):
    template_name = 'reply3.html'

    def get(self, request):

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q3
      prep_time3 = time_dict['prep_time3']
      ans_time3 = time_dict['ans_time3']
      total_time3 = prep_time3 + ans_time3
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a3 = request.POST['note-textarea']
        v3 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t3 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q3 = q3
        unit.a3 = a3
        unit.v3 = v3
        unit.t3 = t3
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r3 = sentiment(3, account_name)
        res = Result.objects.get(id=uid)
        res.r3 = r3
        res.time3 = t3
        res.save()

        # decode base64 to mp4 file
        text = unit.v3
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid3.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid3
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink3(vid_path, account_name, t, path)
        emotion3(vid_path, account_name, t, path)

        return redirect('reply4/')

      return render(request, self.template_name,locals())  


class QuesView4(TemplateView):
    template_name = 'reply4.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q4
      prep_time4 = time_dict['prep_time4']
      ans_time4 = time_dict['ans_time4']
      total_time4 = prep_time4 + ans_time4
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a4 = request.POST['note-textarea']
        v4 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t4 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q4 = q4
        unit.a4 = a4
        unit.v4 = v4
        unit.t4 = t4
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r4 = sentiment(4, account_name)
        res = Result.objects.get(id=uid)
        res.r4 = r4
        res.time4 = t4
        res.save()

        # decode base64 to mp4 file
        text = unit.v4
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid4.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid4
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink4(vid_path, account_name, t, path)
        emotion4(vid_path, account_name, t, path)
        return redirect('reply5/')

      return render(request, self.template_name,locals())  


class QuesView5(TemplateView):
    template_name = 'reply5.html'

    def get(self, request):
      #print(request.session.session_key)

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q5
      prep_time5 = time_dict['prep_time5']
      ans_time5 = time_dict['ans_time5']
      total_time5 = prep_time5 + ans_time5
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a5 = request.POST['note-textarea']
        v5 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t5 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q5 = q5
        unit.a5 = a5
        unit.v5 = v5
        unit.t5 = t5
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r5 = sentiment(5, account_name)
        res = Result.objects.get(id=uid)
        res.r5 = r5
        res.time5 = t5
        res.save()

        # decode base64 to mp4 file
        text = unit.v5
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid5.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid5
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink5(vid_path, account_name, t, path)
        emotion5(vid_path, account_name, t, path)
        return redirect('reply6/')

      return render(request, self.template_name,locals())   


class QuesView6(TemplateView):
    template_name = 'reply6.html'

    def get(self, request):
      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q6
      prep_time6 = time_dict['prep_time6']
      ans_time6 = time_dict['ans_time6']
      total_time6 = prep_time6 + ans_time6
      
      return render(request, self.template_name, locals())
    
    def post(self, request):   
      if request.method == "POST":
        # save answer to Answer models
        a6 = request.POST['note-textarea']
        v6 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t6 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q6 = q6
        unit.a6 = a6
        unit.v6 = v6
        unit.t6 = t6
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r6 = sentiment(6, account_name)
        res = Result.objects.get(id=uid)
        res.r6 = r6
        res.time6 = t6
        res.save()

        # decode base64 to mp4 file
        text = unit.v6
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid6.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid6
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink6(vid_path, account_name, t, path)
        emotion6(vid_path, account_name, t, path)

        return redirect('reply7/')

      return render(request, self.template_name,locals()) 

        
class QuesView7(TemplateView):
    template_name = 'reply7.html'

    def get(self, request):

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q7
      prep_time7 = time_dict['prep_time7']
      ans_time7 = time_dict['ans_time7']

      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a7 = request.POST['note-textarea']
        v7 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t7 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q7 = q7
        unit.a7 = a7
        unit.v7 = v7
        unit.t7 = t7
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r7 = sentiment(7, account_name)
        res = Result.objects.get(id=uid)
        res.r7 = r7
        res.time7 = t7
        res.save()

        # decode base64 to mp4 file
        text = unit.v7
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid7.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink7(vid_path, account_name, t, path)
        emotion7(vid_path, account_name, t, path)

        return redirect('reply8/')
      
      return render(request, self.template_name,locals())   


class QuesView8(TemplateView):
    template_name = 'reply8.html'

    def get(self, request):

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q8
      prep_time8 = time_dict['prep_time8']
      ans_time8 = time_dict['ans_time8']

      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a8 = request.POST['note-textarea']
        v8 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t8 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q8 = q8
        unit.a8 = a8
        unit.v8 = v8
        unit.t8 =t8
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r8 = sentiment(8, account_name)
        res = Result.objects.get(id=uid)
        res.r8 = r8
        res.time8 = t8
        res.save()

        # decode base64 to mp4 file
        text = unit.v8
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid8.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink8(vid_path, account_name, t, path)
        emotion8(vid_path, account_name, t, path)

        return redirect('reply9/')
      
      return render(request, self.template_name,locals())   


class QuesView9(TemplateView):
    template_name = 'reply9.html'

    def get(self, request):

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q9
      prep_time9 = time_dict['prep_time9']
      ans_time9 = time_dict['ans_time9']

      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a9 = request.POST['note-textarea']
        v9 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t9 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q9 = q9
        unit.a9 = a9
        unit.v9 = v9
        unit.t9 = t9
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r9 = sentiment(9, account_name)
        res = Result.objects.get(id=uid)
        res.r9 = r9
        res.time9 = t9
        res.save()

        # decode base64 to mp4 file
        text = unit.v9
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid9.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink9(vid_path, account_name, t, path)
        emotion9(vid_path, account_name, t, path)

        return redirect('reply10/')
      
      return render(request, self.template_name,locals())   

class QuesView10(TemplateView):
    template_name = 'reply10.html'

    def get(self, request):

      # retreive the current user name
      if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']

      random_question = q10
      prep_time10 = time_dict['prep_time10']
      ans_time10 = time_dict['ans_time10']

      return render(request, self.template_name, locals())
        
    def post(self, request):
      if request.method == "POST":
        # save answer to Answer models
        a10 = request.POST['note-textarea']
        v10 = request.POST['video']
        t = request.POST['time']
        t = int(t)
        t10 = request.POST['time']

        if 'is_login' in request.session and request.session['is_login']==True:
            account_name = request.session['account']
            account_instance = Member.objects.get(Account=account_name)        
        
        # retreive the user's id
        uid = Answer.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')   
        unit = Answer.objects.get(id=uid)
        unit.q10 = q10
        unit.a10 = a10
        unit.v10 = v10
        unit.t10 = t10
        unit.save()

        # retrieve video instance
        vid_unit = Video.objects.get(userID=account_instance, id=uid)
        vid_id = Video.objects.filter(userID=account_instance).order_by('-id')[:1].values('id')  
        

        # save result to Result models
        r10 = sentiment(10, account_name)
        res = Result.objects.get(id=uid)
        res.r10 = r10
        res.time10 = t10
        res.save()

        # decode base64 to mp4 file
        text = unit.v10
        text = text[23:]
        fh = open('interview_vid.mp4', 'wb')
        fh.write(base64.b64decode(text))
        fh.close()
        print('VIDEO DECODED!', '\n')

        # save to django video model
        f = open('interview_vid.mp4', 'rb')
        vid_unit.vid10.save('interview_vid.mp4', File(f), True)
        f.close()
        print('VIDEO SAVED TO MODEL!', '\n')

        # retrieve video file from django model
        vid_instance = Video.objects.get(id=uid).vid1
        print(vid_instance)
        vid_instance = str(vid_instance)
        vidname = str(vid_instance[7:])
        print(vidname)
        vid_path = os.path.join(BASE_DIR + '\\media\\videos\\' + vidname)
        
        # do blink detection and save to Result model
        path = request.path
        print('PATH =====> ', path)
        blink10(vid_path, account_name, t, path)
        emotion10(vid_path, account_name, t, path)

        return redirect('/')
      
      return render(request, self.template_name,locals())   


