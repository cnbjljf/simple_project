from django import template
from django.utils.html import format_html
register = template.Library()

# 如果是filter ，那么后面的
@register.filter
def truncate_url(img_obj):
    '''
    这个方法用来处理图片路径的。去除uploads这个
    :param img_obj:
    :return:
    '''
    return img_obj.name.split('/',maxsplit=1)[-1]

@register.simple_tag
def filter_comment(article_obj):
    '''
    coment_set 是 article_obj 固有的属性
    这个方法用来统计一篇文章的点赞数和评论数的！
    :param article_obj: 文章这个对象，由views里面传给jinja模版渲染 的
    :return:
    '''
    query_set = article_obj.comment_set.select_related()
    comments = {
        'comment_count':query_set.filter(comment_type=1).count(),
        'thumb_count':query_set.filter(comment_type=2).count(),
    }
    return comments

