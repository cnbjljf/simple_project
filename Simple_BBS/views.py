from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from Simple_BBS import models
from Simple_BBS import forms
from Simple_BBS import comment_hander
from django.core.paginator import  EmptyPage,PageNotAnInteger,Paginator
import datetime

# Create your views here.



category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')

def index(request):
    """
    处理首页的方法
    :param request:
    :return:
    """
    return render(request,'BBS/index.html',{'category_list':category_list})


def paginate(request,show_data):
    '''
    处理分页功能的方法，
    :param request:
    :param show_data: 需要做分页的数据
    :return:
    '''
    # show 10 number every page!
    paginator = Paginator(show_data,3)
    page = request.GET.get('page')
    try:
        content_list = paginator.page(page)
    except PageNotAnInteger:
        # if page number is not Integer, then we deliver first page !
        content_list = paginator.page(1)
    except EmptyPage:
        # if page is out of page range, then deliver last page !
        content_list = paginator.page(paginator.num_pages)
    return content_list


def category(request,category_id=4):
    '''
    展示页面顶部模块的名字.
    :param request:
    :param category_id:
    :return:
    '''
    category_obj = models.Category.objects.get(id=category_id)
    if category_obj.position_index == 1: # 1 表示是首页
        article_list = models.Article.objects.filter(status='published')
    else:
        article_list = models.Article.objects.filter(category_id=category_obj.id,status='published')

    article_list = paginate(request,article_list)   # 分页方法处理下，使其返回前台是分页的！
    return render(request,'bbs/index.html',{'category_list':category_list,
                                            'category_obj':category_obj,
                                            'article_list':article_list})


def acc_login(request):
    '''
    处理用户账户登陆的方法
    :param request:
    :return:
    '''
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            #pass authentication
            login(request,user)
            return HttpResponseRedirect(request.GET.get('next') or '/bbs')
        else:
            login_err = "Wrong username or password!"
            return render(request,'login.html',{'login_err':login_err})
    return render(request,'login.html')

def acc_logout(request):
    '''
    处理退出登陆的方法
    :param request:
    :return:
    '''
    logout(request)
    return HttpResponseRedirect('/bbs')

def article_detail(request,article_id):
    '''
    展示文章详情的
    :param request:
    :param article_id:
    :return:
    '''
    article_obj = models.Article.objects.get(id=article_id)
    comment_obj = models.Comment.objects.filter(article=article_obj.id)
    return render(request,'BBS/article_detail.html',{'article_obj':article_obj,
                                                     'category_list':category_list,
                                                     'comment_list':comment_obj,})

def person_zone(request,user_name,belong_author=None):
    '''
    用来处理用户操作的事情。
    :param request:
    :param user_name: it's user's  id
    :return:
    '''
    #user_name = models.UserProfile.objects.get(id=user_id)

    article_total = models.Article.objects.filter(author_id=user_name).count()
    article_published = models.Article.objects.filter(status='published',author_id=user_name).count()
    article_draft = models.Article.objects.filter(status='draft',author_id=user_name).count()
    article_hidden = models.Article.objects.filter(status='hidden',author_id=user_name).count()
    #belong_author = models.Article.objects.filter(author=user_name).
    if not belong_author:
        print('---->',belong_author)
        belong_author = models.Article.objects.filter(author_id=user_name)
    return render(request,'BBS/person_zone.html',{'article_list':belong_author,
                                                  'article_total':article_total,
                                                  'already_published':article_published,
                                                  'in_draft':article_draft,
                                                  'in_hide':article_hidden,
                                                  'category_list':category_list})
    #return  HttpResponse('belong_author %s'%(belong_author))

def article_modify(request,article_id):
    '''
    更改文章/博客内容的方法
    :param request:
    :param article_id: 文章ID
    :return: 网页
    '''
    article_id_obj = models.Article.objects.get(id=article_id)
    form = forms.get_form(models.Article,instance=article_id_obj)
    if request.method == 'POST':
        form = forms.get_form(models.Article,request.POST,instance=article_id_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/person_zone/%s'%(request.user.userprofile.id))
    return render(request,'BBS/add_article.html',{'category_list':category_list,
                                                  'title_of_page':u'修改文章信息',
                                                  'article':form,})

def search_article(request):
    '''
    处理搜索书籍的功能
    :param request:
    :return:
    '''
    username = request.POST.get('login_username')
    if request.method == 'POST':
        if request.POST.get('article_status') == 'all':
            articles = models.Article.objects.filter(title=request.POST.get('title'))
        else:
            articles = models.Article.objects.filter(title=request.POST.get('title'),
                                                     status=request.POST.get('article_status'))
    if articles:
        return person_zone(request,user_name=username,belong_author=articles)
    else:
        return  render(request,'BBS/404.html')

@login_required()
def add_article(request):
    '''
    除了添加文章的方法
    :param request:
    :return:
    '''
    import datetime
    errors = None
    article_list = forms.get_form(models.Article)
    if request.method == 'POST':
        article_form = forms.get_form(models.Article,request.POST,request.FILES)
        if article_form.is_valid():
            data =  article_form.cleaned_data
            data['author_id'] = request.user.userprofile.id
            if data['status'] == "published":
                data['pub_date'] == datetime.datetime.now()

            article_obj = models.Article(**data)
            article_obj.save()
            return HttpResponseRedirect('/bbs/')

        else:
             errors = '输入的信息不完整或者错误，不符合格式。'

    return render(request,'BBS/add_article.html',{'article':article_list,
                                                  'category_list':category_list,
                                                  'errors':errors,
                                                  'title_of_page':u'写一篇新文章'})

def handler_comemnt(request):
    '''
    处理评论功能的
    :param request:
    :return:
    '''
    if request.method == 'POST':
        # article_id = request.POST.get('article')
        # comment_type = request.POST.get('comment_type')
        # user = request.POST.get('user')
        # parent_ment = request.POST.get('parent_comment')
        # comment = request.POST.get('comment')
        # models.Comment.objects.create(article=article_id,comment_type=comment_type,
        #                               parent_comment=parent_ment,comment=comment,
        #                               user=user)
        if int(request.POST.get('comment_type')) == 2:
            article_id = request.POST.get('article')
            user = request.POST.get('user')
            praise_num =  models.Comment.objects.filter(comment_type=2,article_id=article_id,user_id=user).count()
            if praise_num >=1:
                return HttpResponse('limit')


        form = forms.get_form(models.Comment,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("post-comment-success")
        else:
            return HttpResponse('error!!')
    print(request.GET)
    article_id = request.GET['id']
    comment_type = request.GET['choice']
    # 获取这个点赞的文章，需要注意的是，praise_obj 这是一个列表，列表不具备comment_set属性，列表元素才有
    praise_obj = models.Article.objects.filter(id=article_id)
    for pb in praise_obj:
        # 通过反向查询，来获取comment表里面的内容，表后面必须紧接着 _set ！
        pb_obj = pb.comment_set.select_related()
        # get the praise's number,and count that!
        praise = pb_obj.filter(comment_type=comment_type).count()
    return HttpResponse(praise)



def get_comments(request,article_id):
    '''
    处理获取评论的方法
    :param request:
    :param article_id:
    :return:
    '''
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_hander.build_tree(article_obj.comment_set.select_related().order_by('date'))
    tree_html = comment_hander.render_comment_tree(comment_tree)
    return HttpResponse(tree_html)
