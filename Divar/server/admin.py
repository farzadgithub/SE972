from django.contrib import admin

# Register your models here.
from server.models import Userprofile, Post, RequestDetail, BlockedIP, Captcha, LoginAttempts

admin.site.register(Userprofile)
admin.site.register(Post)
admin.site.register(BlockedIP)
admin.site.register(Captcha)
admin.site.register(LoginAttempts)


class RequestDetailAdmin(admin.ModelAdmin):
    list_display = ('is_authenticated', 'time', 'username', 'browser', 'ip')
    list_filter = ('is_authenticated',)
    search_fields = ('is_authenticated',)


admin.site.register(RequestDetail, RequestDetailAdmin)
