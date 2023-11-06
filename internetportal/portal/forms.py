from django import forms
from django.contrib.auth import password_validation

from .models import *


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Повторите тот же самый пароль еще раз')
    personal_data_agreement = forms.BooleanField(required=True)

    class Meta:
        model = AdvUser
        fields = ('fio', 'username', 'email', 'password1', 'password2', 'personal_data_agreement')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('name', 'description', 'category', 'photo')


class ApplicationUpdateStatusForm(forms.ModelForm):
    new_photo = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'bmp']),
                    validate_file_size], required=False)

    class Meta:
        model = Application
        fields = ('status', 'comment', 'new_photo')

    def clean(self):
        super().clean()
        status = self.cleaned_data.get('status')
        new_photo = self.cleaned_data.get('new_photo')
        comment = self.cleaned_data.get('comment')

        if status == 'd' and not new_photo:
            raise ValidationError('Меняя статус заявки на "Выполнено", прикрепите изображение созданного дизайна')
        elif status == 'd' and comment:
            raise ValidationError('Указывая статус "Выполнено", вы не должны указывать комментарий')

        if status == 'a' and not comment:
            raise ValidationError('Меняя статус заявки на "Принято в работу", укажите комментарий')
        elif status == 'a' and new_photo:
            raise ValidationError(
                'Меняя статус заявки на "Принято в работу, вы не имеете права прикреплять изображение созданного дизайна')

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_photo = self.cleaned_data.get('new_photo')
        if new_photo is not None:
            instance.photo = new_photo
        if commit:
            instance.save()
        return instance


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
