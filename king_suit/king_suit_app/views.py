from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from king_suit.king_suit_app.forms import UserCreateForm, ProductCreateForm, ProductEditForm, ProductDeleteForm, \
    DepartmentCreateForm, DepartmentEditForm, DepartmentDeleteForm, CommentCreateForm, CommentEditForm, \
    CommentDeleteForm
from king_suit.king_suit_app.models import Article, Product, Department, Employee, KingSuitUserFeedbackComment


UserModel = get_user_model()


def index(request):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True
    context = {
        'has_rights': has_rights,
    }
    return render(request, 'index.html', context)


def contacts(request):
    comments = KingSuitUserFeedbackComment.objects.all()
    context = {
        'comments': comments,
    }
    return render(request, 'contacts.html', context)


def about_us(request):
    return render(request, 'about_us.html')


class LogInView(LoginView):
    template_name = 'login.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response


class LogOutView(LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(DetailView):
    model = UserModel
    template_name = 'user_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object
        context['comments_count'] = KingSuitUserFeedbackComment.objects.filter(user_id=self.object.pk).count()
        context['comments'] = KingSuitUserFeedbackComment.objects.filter(user_id=self.object.id).all()

        return context


class UserEditView(UpdateView):
    model = UserModel
    template_name = 'user_edit.html'
    fields = ('first_name', 'last_name', 'gender', 'email', 'photo', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object

        return context

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={'pk': self.request.user.pk, })


class UserDeleteView(DeleteView):
    template_name = 'user_delete.html'
    model = UserModel
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object
        return context


class ArticleListView(ListView):
    context_object_name = 'articles' # rename 'object_list' to 'articles'
    model = Article
    template_name = 'list_articles.html'
    extra_context = {'title': 'List view'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context


class ArticleCreateView(CreateView):
    fields = '__all__'
    model = Article
    template_name = 'create_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        created_object = self.object
        return reverse_lazy('details article', kwargs={'pk': created_object.pk})


class ArticleDetailsView(DetailView):
    template_name = 'detail_article.html'
    context_object_name = 'article'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context


class ArticleEditView(UpdateView):
    fields = '__all__'
    model = Article
    context_object_name = 'article'
    template_name = 'edit_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        created_object = self.object
        return reverse_lazy('details article', kwargs={'pk': created_object.pk})


class ArticleDeleteView(DeleteView):
    fields = '__all__'
    model = Article
    template_name = 'delete_article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        return reverse_lazy('articles')


def create_product(request):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    if request.method == 'GET':
        form = ProductCreateForm()
    else:
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'has_rights': has_rights,
    }

    return render(request, 'create_product.html', context)


def details_product(request, pk):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    product = Product.objects.filter(pk=pk).get()

    context = {
        'product': product,
        'sizes': ', '.join(product.size.split()),
        'has_rights': has_rights,
    }

    return render(request, 'details_product.html', context)


def all_products(request):
    products = Product.objects.all()
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    context = {
        'products': products,
        'has_rights': has_rights,
    }

    return render(request, 'all_products.html', context)


def edit_product(request, pk):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    product = Product.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = ProductEditForm(instance=product)
    else:
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'pk': pk,
        'has_rights': has_rights,
    }

    return render(request, 'edit_product.html', context)


def delete_product(request, pk):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    product = Product.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = ProductDeleteForm(instance=product)
    else:
        form = ProductDeleteForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form,
        'pk': pk,
        'has_rights': has_rights,
    }

    return render(request, 'delete_product.html', context)


def create_department(request):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    if request.method == 'GET':
        form = DepartmentCreateForm()
    else:
        form = DepartmentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments')

    context = {
        'form': form,
        'has_rights': has_rights,
    }

    return render(request, 'create_department.html', context)


def all_departments(request):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    departments = Department.objects.all()
    context = {
        'departments': departments,
        'has_rights': has_rights,
    }
    return render(request, 'all_departments.html', context)


def edit_department(request, pk):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    department = Department.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = DepartmentEditForm(instance=department)
    else:
        form = DepartmentEditForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('departments')

    context = {
        'form': form,
        'pk': pk,
        'has_rights': has_rights,
    }

    return render(request, 'edit_department.html', context)


def delete_department(request, pk):
    has_rights = False
    if request.user.is_superuser or request.user.is_staff:
        has_rights = True

    department = Department.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = DepartmentDeleteForm(instance=department)
    else:
        form = DepartmentDeleteForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('departments')

    context = {
        'form': form,
        'pk': pk,
        'has_rights': has_rights,
    }

    return render(request, 'delete_department.html', context)


class EmployeeCreateView(CreateView):
    fields = '__all__'
    model = Employee
    template_name = 'create_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        created_object = self.object
        return reverse_lazy('details employee', kwargs={'pk': created_object.pk})


class EmployeesListView(ListView):
    context_object_name = 'employees' # rename 'object_list' to 'articles'
    model = Employee
    template_name = 'all_employees.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context


class EmployeeDetailsView(DetailView):
    template_name = 'details_employee.html'
    context_object_name = 'employee'
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context


class EmployeeEditView(UpdateView):
    fields = '__all__'
    model = Employee
    context_object_name = 'employee'
    template_name = 'edit_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        created_object = self.object
        return reverse_lazy('details employee', kwargs={'pk': created_object.pk})


class EmployeeDeleteView(DeleteView):
    fields = '__all__'
    model = Employee
    template_name = 'delete_employee.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['has_rights'] = True
        elif self.request.user.is_staff:
            context['has_rights'] = True
        else:
            context['has_rights'] = False

        return context

    def get_success_url(self):
        return reverse_lazy('employees')


def add_comment(request):
    if request.method == 'GET':
        form = CommentCreateForm()
    else:
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('details comment', pk=comment.pk)

    context = {
        'form': form,
    }
    return render(request, 'create_comment.html', context)


def details_comment(request, pk):
    comment = KingSuitUserFeedbackComment.objects.filter(pk=pk).get()

    context = {
        'comment': comment,
        'is_owner': comment.user == request.user,
    }
    return render(request, 'details_comment.html', context)


def edit_comment(request, pk):
    comment = KingSuitUserFeedbackComment.objects.filter(pk=pk,).get()

    is_owner = False
    if request.user == comment.user:
        is_owner = True

    if request.method == 'GET':
        form = CommentEditForm(instance=comment)
    else:
        form = CommentEditForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('details comment', pk=pk)

    context = {
        'form': form,
        'pk': pk,
        'is_owner': is_owner,
    }
    return render(request, 'edit_comment.html', context)


def delete_comment(request, pk):
    comment = KingSuitUserFeedbackComment.objects.filter(pk=pk, ).get()
    if request.method == 'GET':
        form = CommentDeleteForm(instance=comment)
    else:
        form = CommentDeleteForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
        'pk': pk,
        'is_owner': request.user == comment.user,
    }

    return render(request, 'delete_comment.html', context)


def handler404(request, *args, **kwargs):
    return render(request, '404.html')


def handler500(request, *args, **kwargs):
    return render(request, '404.html')
