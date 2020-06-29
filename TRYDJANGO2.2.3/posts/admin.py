from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdimn(admin.ModelAdmin):
    list_display = ['user','title','slug','draft','publish','timestamp','updated']

    fieldsets=[
        ('user name ', {'fields': ['user']}),
    ('Title of your post with max_length(in characters) 150',{'fields':['title']}),
    ('Slug field ',{'fields':['slug']}),
    ('The body of your Post',{'fields':['content']}),
    ('Uploaded image',{'fields':['image']}),
    ('height of image uploaded ',{'fields':['height_field']}),
    ('width of image uploaded ',{'fields':['width_field']}),
        ('draft', {'fields': ['draft']}),
        ('published date', {'fields': ['publish']}),
]

    list_display_links = ['updated']
    list_editable = ['title']
    list_filter=['timestamp','updated']
    search_fields=['title','content']
   # fields = ['title','content']
   
admin.site.register(Post,PostAdimn)

#admin.site.register(Post)

