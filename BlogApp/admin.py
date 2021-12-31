from django.contrib import admin
from BlogApp.models import ContactUs,Post,BlogComment

# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['serialno','name','phone','email','content']

class PostAdmin(admin.ModelAdmin):
    list_display = ['serialno','title','content','author',]

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['serialno','comment','user','post','parent','timestamp']


admin.site.register(ContactUs,ContactUsAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(BlogComment,BlogCommentAdmin)
