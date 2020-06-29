from django.shortcuts import redirect,render,get_object_or_404,Http404
from django.contrib import messages
from urllib.parse import quote_plus
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.db.models import Q
# Create your views here.
'''
def posts_home(request):
    return render(request,'posts/home_page.html')

'''

def posts_list(request):
	# ordering the post with the latest first
	#display only post less than or equal to todays date
	#queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())
	today=timezone.now().date()
	queryset_list=Post.objects.active()#.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	# search bar
	query=request.GET.get('q')
	if query:
		queryset_list=queryset_list.filter( Q(title__icontains=query) | Q(content__icontains=query)|
			Q(slug__icontains=query)#Q(user_first_name__icontains=query)|
			#Q(user_last_name__icontains=query)|
			#Q(user__icontains=query)
		).distinct()# to prevent duplicate items

	paginator=Paginator(queryset_list,4)# show 4 post per page
	page=request.GET.get('page')
	try:
		queryset=paginator.get_page(page)
	except PageNotAnInteger:
		# IF PAGE NOT AN INTEGER DELIVER THE FIRST PAGE
		queryset = paginator.get_page(1)
	except EmptyPage:
		# if page out of range deliver the last page
		queryset = paginator.get_page(paginator.num_pages)


	context={'object_list':queryset,
			 'today':today,
	'title':'every'}
	return render(request,'posts/post_list.html',context)
	"""
    if request.user.is_authenticated():
        context={'title':'go'}
    else:
        context={'title':'bad'}

    return render(request,'posts/post_list.html',context)
   """


def posts_create(request):
	# prevent on staff from creating post
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method=='POST':
		form=PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			instance=form.save(commit=False)
			# it assume user is log in
			instance.user=request.user
			instance.save()
			# message should be in the redirected html file
			# YOU CAN WRITE SEVERAL MESSAGES
			messages.success(request,'new post successfully created')
			return redirect(instance.get_absolute_url())

	else:
		# if form is not successfully created
		#messages.error(request,'Post could not be created')
		form=PostForm()

	return render(request,'posts/post_form.html',{'form':form})
  

def posts_detail(request,id=None):
	instance=get_object_or_404(Post,id=id)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	#sharing the link to another site
	share_string=quote_plus(instance.content)
	context={'instance':instance,
			 'share_string':share_string}
	return render(request,'posts/post_detail.html',context)
  

def posts_update(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	# instance will load the form wiTH the populated data
	form=PostForm(request.POST or None,request.FILES or None, instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,'Post successfully updated')
		return redirect(instance.get_absolute_url()) # or return redirect('')
	context={'instance':instance,'form':form}
	return render(request,'posts/post_form.html',context)
    


def posts_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	# deleting the post
	instance.delete()
	messages.success(request,'Post successfully deleted')
	return redirect('home-list')
    