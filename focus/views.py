from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,Comment,NewUser
from .forms import LoginForm,CommentForm,RegisterForm,SetInfoForm,SearchForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#import hashlib
import markdown2,urllib

# Create your views here.
def index(request):
	latest_article_list = Article.objects.query_by_time()[:3]
	loginform = LoginForm()
	context = {'latest_article_list':latest_article_list,'loginform':loginform}
	return render(request,'index.html',context)

def register(request):
	if request.method == 'GET':
		form = RegisterForm()
		return render(request,'register.html',{'form':form})
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if request.POST.get('raw_username',None):
			try:
				user = NewUser.objects.get(username=request.POST.get('raw_username',''))
			except ObjectDoesNotExist:
				return render(request,'register.html',{'form':form,'error':'the username is valid'})
			else:
				return render(request,'register.html',{'form':form,'error':'the username is exist'})
		else:
			if form.is_valid():
				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				pwd1 = form.cleaned_data['password1']
				pwd2 = form.cleaned_data['password2']

				if pwd1 != pwd2:
					return render(request,'register.html',{'form':form,'error':'password is different'})

				else:
					#pwd = hashlib.sha1(pwd1.encode('utf8')).hexdigest()
					try:
						user = NewUser.objects.create_user(username=username,email=email,password=pwd1)
						#user.save()
					except IntegrityError:
						return render(request,'register.html',{'form':form,'error':'username is duplicated'})
					return redirect('/focus/login')
			else:
				return render(request,'register.html',{'form':form,'error':'is null'})

def login_in(request):
	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['uid']
			password = form.cleaned_data['pwd']	
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				url = request.POST.get('source_url','/focus') 
				return redirect(url)
			else:
				return render(request,'login.html', {'form':form, 'error': "password or username is not ture!"})
			
		else:
			return render(request, 'login.html', {'form': form})

@login_required
def login_out(request):
	url = request.POST.get('source_url', '/focus/')
	logout(request)
	return redirect(url)

def article(request,article_id):
	article = get_object_or_404(Article,id=article_id)
	content = markdown2.markdown(article.content, extras=["code-friendly", "fenced-code-blocks", "header-ids", "toc", "metadata"])
	commentForm = CommentForm()
	loginForm = LoginForm()
	comments = Comment.objects.all().filter(article_id=article_id)
	return render(request, 'article_page.html', {'article': article, 'loginform':loginForm,'commentform':commentForm,'content': content,'comments':comments})

@login_required
def comment(request, article_id):
	form = CommentForm(request.POST)
	url = urllib.parse.urljoin('/focus/',article_id)
	if form.is_valid():
		user = request.user
		article = Article.objects.get(id=article_id)
		new_comment = form.cleaned_data['comment']
		c = Comment(content=new_comment, article_id=article_id)
		c.user = user
		c.save()
		article.comment_num += 1
		article.save()
	return redirect(url)

@login_required
def get_keep(request,article_id):
	user = request.user
	#print(str(user))
	article = Article.objects.get(id=article_id)
	user_keeps = Article.objects.all().prefetch_related('user_keep').filter(id=article_id)[0]
	user_keeps_list = []

	for b in user_keeps.user_keep.all():
		user_keeps_list.append(b.username)

	#print(user_keeps_list)

	if str(user) not in user_keeps_list:
		article.user_keep.add(user)
		article.keep_num += 1
		article.save()

	url = urllib.parse.urljoin('/focus/',article_id)
	return redirect(url)

@login_required
def get_poll_article(request,article_id):
	user = request.user
	article = Article.objects.get(id=article_id)
	user_polls = Article.objects.all().prefetch_related('user_poll').filter(id=article_id)[0]
	user_polls_list=[]

	for b in user_polls.user_poll.all():
		user_polls_list.append(b.username)

	if str(user) not in user_polls_list:
		article.user_poll.add(user)
		article.poll_num += 1
		article.save()

	url = urllib.parse.urljoin('/focus/',article_id)
	return redirect(url)


