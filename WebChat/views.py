from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import  login_required
from WebChat import forms,models
from django.core.cache import cache
import queue,json,time,os.path,os


# Create your views here.

GLOBAL_MSG_QUEUES = {

}



@login_required()
def index(request):
    return render(request,'WeChat/ChatRoom.html',)

@login_required()
def send_msg(request):
    '''
    发送消息的方法,发送消息的时候会去创建队列，并且入库存档
    :param request:
    :return:
    '''
    print(request.POST)
    print(request.POST.get('msg'))
    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            if not GLOBAL_MSG_QUEUES.get(int(msg_data.get('to'))):
                GLOBAL_MSG_QUEUES[int(msg_data['to'])] = queue.Queue()
                print('already create queue')
            GLOBAL_MSG_QUEUES[int(msg_data['to'])].put(msg_data)
            models.ChatRecord.objects.create(myself_id=int(msg_data.get('from')),peer_self_id=int(msg_data.get('to')),
                                            chat_type=msg_data.get('type'),TimeStamp=str(msg_data.get('timestamp')),
                                             Content=msg_data.get('msg'))
        else:  # this is group
            group_obj = models.WebGroup.objects.get(id=int(msg_data['to']))
            for member in group_obj.members.select_related():
                if not GLOBAL_MSG_QUEUES.get(int(member.id)):
                    GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
                if member.id != request.user.userprofile.id:
                    GLOBAL_MSG_QUEUES[int(member.id)].put(msg_data)
                    models.ChatRecord.objects.create(myself_id=int(msg_data.get('to')),peer_self_id=int(msg_data.get('from')),
                                            chat_type=msg_data.get('type'),TimeStamp=str(msg_data.get('timestamp')),
                                             Content=msg_data.get('msg'))

    print('\033[33m global_msg_queues \033[0m',GLOBAL_MSG_QUEUES)
    return HttpResponse('---msg received----')


def get_msg(request):
    '''
    获取消息的方法
    :param request:
    :return:
    '''

    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print('no queue for this user %s'% request.user.userprofile.name)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()
    msg_count = GLOBAL_MSG_QUEUES[request.user.userprofile.id].qsize()
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_list = []
    print('p'*50,msg_count)
    if msg_count > 0:
        for msg in range(msg_count):
            msg_data = q_obj.get()
            msg_list.append(msg_data)
        print('\033[32m new msg --------> \033[0m', msg_list)

    else: # 没有消息，要挂起
        try:
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:
            print("\033[41;1m no msg for [%s][%s] ,timeout\033[0m" %(request.user.userprofile.id,request.user))

    print('------> begin send msg to peer !!!---')
    print('\033[32m new msg --------> \033[0m', msg_list)
    # for i in range(0,len(msg_list)):
    #     models.ChatRecord.objects.create(myself_id=int(msg_list[i].get('from')),peer_self_id=int(msg_list[i].get('to')),
    #                                         chat_type=msg_list[i].get('type'),TimeStamp=str(msg_list[i].get('timestamp')),
    #                                          Content=msg_list[i].get('msg'))
    return HttpResponse(json.dumps(msg_list))



def Get_History_Record(request):
    '''
    从数据库里面获取聊天记录,通过json格式返回
    :param request:
    :return:
    '''
    myself_id = request.user.userprofile.id
    print('peer_id --->',request.GET['peer_id'])
    peer_self_id = request.GET['peer_id']
    print(myself_id,peer_self_id)
    chat_record_one = models.ChatRecord.objects.filter(myself=myself_id,peer_self=peer_self_id).order_by('TimeStamp')
    chat_record_two = models.ChatRecord.objects.filter(myself=peer_self_id,peer_self=myself_id).order_by('TimeStamp')
    chat_record_json = []
    for i in chat_record_one.values():
        chat_record_json.append(i)
    for i in chat_record_two.values():
        chat_record_json.append(i)
    msg_list = sorted(chat_record_json,key=lambda x:x['TimeStamp'])
    return HttpResponse(json.dumps(msg_list))



def file_upload(request):
    '''
    处理上传文件的方法
    :param request:
    :return:
    '''
    print(request.FILES)
    file_obj = request.FILES.get('file')
    print('file--obj',file_obj)
    user_home_dir = "upload/%s" %(request.user.userprofile.id)
    if not os.path.isdir(user_home_dir):
        os.mkdir(user_home_dir)
    upload_file = "%s/%s" %(user_home_dir,file_obj.name)
    print('upload_file ==>',upload_file)
    recv_size = 0
    with open(upload_file,'wb') as new_file:
        for chunk in file_obj.chunks():
            new_file.write(chunk)
            recv_size+=len(chunk)
            cache.set(file_obj.name,recv_size)
    return HttpResponse('upload_ok')


def file_upload_progress(request):
    '''
    获取已经上传文件大小的值
    :param request:
    :return:
    '''
    filename = request.GET.get('filename')
    progress = cache.get(filename)
    print('-------------->file %s uploading process %s'%(filename,progress))
    return HttpResponse(json.dumps({'recv_size':progress}))


def delete_cache_key(request):
    cache_key = request.GET.get('cache_key')
    cache.delete(cache_key)
    return HttpResponse('cache_key_was_deleted',cache_key)


def remove_admin_on_numbers(**kwargs):
    '''
     把管理员从组成员里面删除掉
    :param kwargs:  传入一个字典，这个字典是返回给js使用的的数据，展现组成员信息的
    :return:
    '''
    group_numbers = kwargs['group_members']
    group_admins = kwargs['group_admins']
    for admin in group_admins:
        if admin in group_numbers:
            group_numbers.remove(admin)
    kwargs['group_members']=group_numbers
    print(kwargs)
    return kwargs


def get_group_numbers(request):
    '''
    获取组成员信息，群主，管理员信息等，获取后调用其他的处理后返回给js
    :param request:
    :return:
    '''
    groupd_id = request.GET['group_id']
    select_result = models.WebGroup.objects.filter(id=groupd_id)[0]
    info_dic = {}
    info_dic['group_members'] = []
    for member in select_result.members.select_related().values():
        info_dic['group_members'].append(member)
    info_dic[str(select_result.owner.id)] = select_result.owner.name
    info_dic['group_admins'] = []
    for admin in select_result.admins.select_related().values():
         info_dic['group_admins'].append(admin)
    info_dic=remove_admin_on_numbers(**info_dic)
    return HttpResponse(json.dumps(info_dic))