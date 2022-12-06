from django.urls import path, include

from king_suit.king_suit_app.views import index, LogInView, RegisterView, LogOutView, contacts, about_us, \
    UserDetailsView, UserEditView, UserDeleteView, ArticleListView, ArticleCreateView, ArticleDetailsView, \
    ArticleEditView, ArticleDeleteView, create_product, details_product, all_products, edit_product, delete_product, \
    create_department, all_departments, edit_department, delete_department, EmployeeCreateView, EmployeesListView, \
    EmployeeDetailsView, EmployeeEditView, EmployeeDeleteView, add_comment, edit_comment, details_comment, \
    delete_comment

urlpatterns = (
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('aboutus/', about_us, name='about us'),
    path('login/', LogInView.as_view(), name='login user'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('logout/', LogOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='details user'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
    ])),
    path('article/', include([
        path('', ArticleListView.as_view(), name='articles'),
        path('create/', ArticleCreateView.as_view(), name='create article'),
        path('details/<int:pk>/', ArticleDetailsView.as_view(), name='details article'),
        path('edit/<int:pk>/', ArticleEditView.as_view(), name='edit article'),
        path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete article'),
    ])),
    path('product/', include([
        path('', all_products, name='products'),
        path('create/', create_product, name='create product',),
        path('details/<int:pk>/', details_product, name='details product'),
        path('edit/<int:pk>/', edit_product, name='edit product'),
        path('delete/<int:pk>/', delete_product, name='delete product'),
    ])),
    path('department/', include([
        path('', all_departments, name='departments'),
        path('create/', create_department, name='create department'),
        path('edit/<int:pk>/', edit_department, name='edit department'),
        path('delete/<int:pk>/', delete_department, name='delete department'),
    ])),
    path('employee/', include([
        path('', EmployeesListView.as_view(), name='employees'),
        path('create/', EmployeeCreateView.as_view(), name='create employee'),
        path('details/<int:pk>/', EmployeeDetailsView.as_view(), name='details employee'),
        path('edit/<int:pk>/', EmployeeEditView.as_view(), name='edit employee'),
        path('delete/<int:pk>/', EmployeeDeleteView.as_view(), name='delete employee'),
    ])),
    path('comment/', include([
        path('create/', add_comment, name='create comment'),
        path('edit/<int:pk>/', edit_comment, name='edit comment'),
        path('details/<int:pk>/', details_comment, name='details comment'),
        path('delete/<int:pk>/', delete_comment, name='delete comment'),
    ]))
)
