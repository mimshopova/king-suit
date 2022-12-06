from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django import forms

from king_suit.king_suit_app.models import Product, Department, KingSuitUserFeedbackComment

UserModel = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', )
        field_classes = {'username': UsernameField}


class UserEditForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'gender', 'email', 'photo',)
        field_classes = {'username': UsernameField}


class ProductBaseForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateForm(ProductBaseForm):
    pass


class ProductEditForm(ProductBaseForm):
    pass


class ProductDeleteForm(ProductBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


class DepartmentBaseForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentCreateForm(DepartmentBaseForm):
    pass


class DepartmentEditForm(DepartmentBaseForm):
    pass


class DepartmentDeleteForm(DepartmentBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


class CommentBaseForm(forms.ModelForm):
    class Meta:
        model = KingSuitUserFeedbackComment
        fields = ('title', 'content', 'photo')


class CommentCreateForm(CommentBaseForm):
    pass


class CommentEditForm(CommentBaseForm):
    pass


class CommentDeleteForm(CommentBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


