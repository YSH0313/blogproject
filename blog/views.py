from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from .models import *


# Create your views here.

def index(request):
    context = {}
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 2)  # 每2份内容分页一次
    page_num = request.GET.get('page', 1)  # 获取url参数，127.0.0.1:8000/?page=<value>
    # 非法数值则返回1 数值为空也返回1 如 127.0.0.1:8000/?page=asdsa
    page_blogs = paginator.get_page(page_num)  # 获取当前(页码)所需要的文章列表 相当于一个容器
    page_list = [x for x in range(page_blogs.number - 2, page_blogs.number + 3) if x in paginator.page_range]
    # 添加省略号
    if page_list[0] - 1 >= 2:  # 判断当前第一个元素减1是否大于2
        page_list.insert(0, "...")  # 则插入该数组成为第一个元素 ...
    if paginator.num_pages - page_list[-1] >= 2:  # 判断最大页码数-最后一个元素相减是否大于2
        page_list.append("...")  # 则添加一个元素
    # 添加首尾页
    if page_list[0] == "...":
        page_list.insert(0, 1)  # 则插入该数组成为第一个元素(首页)
    if page_list[-1] != paginator.num_pages:  # 判断是否不等于最大页码
        page_list.append(paginator.num_pages)  # 不等于则插入到最后一个元素(尾页)
    context['blogs'] = page_blogs
    context['page_list'] = page_list
    context['post_list'] = page_blogs
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})

def login(request):
    return render(request, 'blog/login.html')