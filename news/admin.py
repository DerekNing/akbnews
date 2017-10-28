from django.contrib import admin
from news.models import Link, Vote, Account

class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'hot', 'post_time']
    list_filter = ['post_time']
    search_fields = ['title']
    ordering = ['-hot']

admin.site.register(Link, LinkAdmin)
admin.site.register(Vote)
admin.site.register(Account)
