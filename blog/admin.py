from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.contrib import admin
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('post', 'created_on', 'name', 'email', 'body')


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on', 'date_published')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]

    # readonly_fields = ('date_published',)

    def has_change_permission(self, request, obj=None):
        if obj and request.user.has_perm('blog.change_post'):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.has_perm('blog.delete_post'):
            return True
        return super().has_delete_permission(request, obj)

    actions = ['publish_publication', "send_publication_to_drafts"]

    def publish_publication(self, request, queryset):
        queryset.update(status=1)
        queryset.update(date_published = timezone.now())
        

    def send_publication_to_drafts(self, request, queryset):
        queryset.update(status=0)
        queryset.update(date_published = None)



admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class CustomActiveFilter(admin.SimpleListFilter):
        title = _('Active')
        parameter_name = 'active'

        def lookups(self, request, model_admin):
            return (
                (None, _('No')),
                ('yes', _('Yes')),
                ('all', _('All')),
            )

        def choices(self, cl):
            for lookup, title in self.lookup_choices:
                yield {
                    'selected': self.value() == lookup,
                    'query_string': cl.get_query_string({
                        self.parameter_name: lookup,
                    }, []),
                    'display': title,
                }

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.filter(active=True)
            elif self.value() is None:
                return queryset.filter(active=False)

    list_display = ('name', 'body', 'post',  'active')
    list_filter = ('active', 'created_on', 'post')
    search_fields = ('name', 'email', 'body', 'post')
    actions = ['approve_comments', 'disapprove_comments']
    fields = ('post', 'created_on', 'name', 'email',  'body',  'active')
    readonly_fields = ('post', 'created_on', 'name', 'email', 'body')

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)


class UserAdmin(BaseUserAdmin):
    actions = ["add_to_blog_managers"]

    def add_to_blog_managers(modeladmin, request, queryset):
        # Get the Blog Managers group
        try:
            blog_managers_group = Group.objects.get(name='Blog Managers')
        except Group.DoesNotExist:
            messages.error(request, 'Blog Managers group does not exist.')
            return

        # Update selected users
        for user in queryset:
            user.groups.add(blog_managers_group)
            user.is_staff = True
            user.save()

        # Notify the admin user about the update
        messages.success(
            request, 'Selected users have been added to the Blog Managers group and granted staff status.')

    add_to_blog_managers.short_description = "Make user a Blog Manager"

    #  Add a custom method to check if a user is in the Blog Managers group
    def is_blog_manager(self, obj):
        return obj.groups.filter(name='Blog Managers').exists()
    is_blog_manager.boolean = True  # Display as a boolean icon
    is_blog_manager.short_description = 'Blog Manager'  # Column name

    # Extend the list display to include the new method
    list_display = BaseUserAdmin.list_display + ('is_blog_manager',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
