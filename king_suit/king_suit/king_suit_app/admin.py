from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from king_suit.king_suit_app.forms import UserEditForm, UserCreateForm
from king_suit.king_suit_app.models import KingSuitUserFeedbackComment, Product, Article, Department, Employee

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class KingSuitUserAdmin(auth_admin.UserAdmin):
    form = UserEditForm
    add_form = UserCreateForm

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            }),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'gender'
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)


@admin.register(KingSuitUserFeedbackComment)
class KingSuitUserFeedbackCommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'user', ]
    list_filter = ['title', 'user', ]
    search_fields = ['title', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price', ]
    list_filter = ['name', 'price', 'size', ]
    search_fields = ['name', 'price', ]
    fields = [('name', 'price'), ('size', 'photo'), 'description', ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', ]
    list_filter = ['title', ]
    search_fields = ['title', 'content', ]
    fields = [('title', 'photo'), 'content', ]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', ]
    list_filter = ['name', ]
    search_fields = ['name', ]
    fields = ['name', ]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['position', 'first_name', 'last_name', 'department', ]
    list_filter = ['position', 'department', 'first_name', 'last_name', 'age', ]
    search_fields = ['position', 'department', ]
    fieldsets = (
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'age', 'hobby', 'photo')}),
        ('Corporate info',
         {'fields': ('position', 'department')}),
    )

