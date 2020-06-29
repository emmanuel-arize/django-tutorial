from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class PostManager(models.Manager):
    def active(self, *args,**kwargs):
        # Post.objects.all=super(PostManager,self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

# this created a folder with the id of the post
def upload_location(instance,filename):
	return "%s/%s"%(instance.id,filename)
class Post(models.Model):
    # adding users to the model
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image= models.ImageField(null=True,blank=True,upload_to=upload_location,width_field='width_field',
                             height_field='height_field')
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    content=models.TextField()
    draft=models.BooleanField(default=False)
    publish=models.DateField(auto_now=False,auto_now_add=False)
    # auto_now_add Automatically set the field to now when the object is first created.
    # auto_now Automatically set the field to now every time the object is saved. Useful for
    # “last-modified” timestamps. Note that the current date is always used;
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp= models.DateTimeField(auto_now=False,auto_now_add=True)
    objects=PostManager()# initializing the postmanager
    def __str__(self):
        return self.title


    class Meta:
        # or this can be done in the view
        # ordering the post list with the recent post on toP using timestamp and updated
        ordering=['-timestamp','-updated']

    def get_absolute_url(self):
    	#return f"/{self.id}"
    	#better way of doing it
    	return reverse('post-detail',kwargs={'id':self.id})

#checking if slug exist
def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug)
	exists=qs.exists()
	if exists:
		new_slug="%s-%s" %(slug,qs.first.id)
		return create_slug(instance,new_slug)
	return slug



def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)


# or without creating create_slug but use this below

"""
def pre_save_post_receiver(sender,instance,*args,**kwargs):
	slug=slugify(instance.title)
	# if the slug exist take that slug
	exists=Post.objects.filter(slug=slug).exists()
	if exists:
		slug="%s-%s" %(slug,instance.id)

	instance.slug=slug
  """  

pre_save.connect(pre_save_post_receiver,sender=Post)