from django import forms
from .models import *
from django.forms import inlineformset_factory, widgets, ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Column
from .custom_layout_object import *
import re

# ФОРМА ФОТОГРАФИЙ
class PostImageForm(forms.ModelForm):

    class Meta:
        model = PostImage
        exclude = ()



PostImageFormSet = inlineformset_factory(
    Post, PostImage, form=PostImageForm,
    fields=['images', ], extra=1, can_delete=True
    )

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # exclude = ['author', "is_published"]
        fields = ["title", "content", "photo", 'price', "category"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control col-lg-3",'multiple': True}),
            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            # "category": forms.RadioSelect(
            #     attrs={
            #         "class": "form-check form-check-inline d-flex justify-content-between"
            #     }
            # ),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal '
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-2 '
        self.helper.layout = Layout(
            Row(Column('title', css_class='form-group col-md-6'),
                Column('photo', css_class='form-group col-md-6'),
                css_class='row g-3 mb-3'),
            'content',
            Row(Column('category', css_class='form-group col-md-6'),
                Column('price', css_class='form-group col-md-6'),
                css_class='row g-3 my-3'),
            Div(
                Fieldset('Галерея фотографий',
                    Formset('images')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Опубликовать')),
                )
            )


class AddPostImageForm(PostForm): #extending form
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ['images',]

    def save_for(self, post):
        for images in self.cleaned_data['images']:
            PostImage(images=images, post=post).save()



# КОММЕНТАРИИ
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
    

# ФОРМА ТЕХ ПОДДЕРЖКИ
class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        # fields = ('name', 'body')
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-4", 'placeholder':'Ваше имя'}),
            "body": forms.Textarea(attrs={"class": "form-control text", 'placeholder':'Текст ссобщения в тех. поддержку.'}),
            "phone": forms.NumberInput(attrs={"class": "form-control mb-4", 'placeholder':'Контактный телефон'}),

        }
