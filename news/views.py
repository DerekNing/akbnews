# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import *
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.core.mail import send_mail


from django.contrib.auth import views

from news.models import Link, Account, Vote
from news.forms import UserForm, AccountForm, LinkForm, EmailForm
from news import hot

import pytz
from datetime import datetime


#set the number of items in each page
PAGE_ITEMS = 2

#all_links: all the links to show; page: the page index; return links in that page
def get_page_links(all_links, page):
    paginator = Paginator(all_links, PAGE_ITEMS)
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)
    return links

# receive order_value as order, return context contain links and voted_links
def get_feed_context(request, order_value):
    # get the voted links if user is loged in else set voted_links to be None
    if request.user.is_authenticated():
        account = Account.objects.get(user=request.user)
        votes = Vote.objects.filter(account=account)
        voted_links = [vote.link for vote in votes]
    else:
        voted_links = None

    if order_value == 'hot':
        link_list = Link.objects.order_by('-hot')
    elif order_value == 'post_time':
        link_list = Link.objects.order_by('-post_time')
    else:
        link_list = Link.objects.all()
    page = request.GET.get('page')
    links = get_page_links(link_list, page)

    context = {'links': links, 'voted_links': voted_links}
    return context

def feed(request):
    context = get_feed_context(request, 'hot')
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit_time = request.session.get('last_visit_time')
    if last_visit_time:
        if (datetime.now() - datetime.strptime(last_visit_time, "%Y-%m-%d %H:%M:%S")).seconds > 10:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['visits'] = visits

    context['visits'] = visits
    response = render(request, 'news/index.html', context)

    return response

def latest_news(request):

    context = get_feed_context(request, 'post_time')
    response = render(request, 'news/index.html', context)

    return response

#@login_required(login_url='/news/login/')
def up_link(request):
    if not request.user.is_authenticated():
        return HttpResponse('/news/login/')

    link_id = None
    if request.method == 'GET':
        #print request.GET
        link_id = int(request.GET['linkid'])

    if link_id:
        try:
            link = Link.objects.get(id=link_id)
        except ObjectDoesNotExist:
            link = None
        if link:
            account = Account.objects.get(user=request.user)
            (vote, created) = Vote.objects.get_or_create(link=link, account=account, defaults={'up': 1},)
            if created:
                #print 'befor: ', link.score, link.hot
                link.score += 1
                link.hot = hot.hot(link.score, link.post_time)
                #print 'after: ', link.score, link.hot
                link.save()
                print 'uped!'
    return HttpResponse(link.score)


def about(request):
    last_visit_time = request.session.get('last_visit_time')
    if not last_visit_time:
        last_visit_time = ''

    return render(request, 'news/about.html', {'last_visit_time': last_visit_time})


def test(request):
    return JsonResponse({'test': 'just for test'})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # hash the password and then save it
            user.set_password(user.password)
            user.save()

            # This delays saving the model until we're ready to avoid integrity problems?
            account = Account(user=user)
            account.save()

            registered = True
            #print 'success'
    else:
        user_form = UserForm()

    content = {'user_form': user_form, 'registered':registered}
    return render(request, 'news/register.html', content)

# use user_login as name because login is a imported fuction name
def user_login(request):
    error = u''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/news/')

        else:
            error = '非法的用户名和输入密码: {0}, {1}'.format(username, password)


    return render(request, 'news/login.html', {'error':error})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/news/')

@login_required(login_url='/news/login/')
def account(request):
    try:
        account = Account.objects.get(user=request.user)
    except ObjectDoesNotExist:
        logout(request)
        return  HttpResponseRedirect('/news/login/')

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = request.user
            old_email = user.email
            user.email = form.cleaned_data.get('email')
            user.save()

            send_mail(
                '邮箱变更通知',
                '您在akbnews的注册邮箱已经变更，如果不是您本人的操作，请回复邮件通知我们',
                '353268509@derekning.club',
                [old_email],
                fail_silently=False,
            )

            return HttpResponseRedirect('/news/account/')
    else:
        form = EmailForm()

    context = {'account':account, 'form':form}
    return render(request, 'news/account.html', context)



@login_required(login_url='/news/login/')
def add_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            account = Account.objects.get(user=request.user)
            link.creator = account
            link.post_time = timezone.now()
            link.score = 0
            link.hot = hot.hot(link.score, link.post_time)
            link.save()

            return HttpResponseRedirect('/news/')
    else:
        form = LinkForm()

    return render(request, 'news/add_link.html', {'form': form})

def track_url(request):
    url = '/news/'
    if request.method == 'GET':
        link_id = request.GET.get('link_id')
        #print 'link_id', link_id
        if link_id:
            try:
                link = Link.objects.get(id=link_id)
                link.view += 1
                link.save()
                url = link.url
            except:
                pass

    return redirect(url)
