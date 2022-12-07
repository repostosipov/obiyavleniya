from email.mime import image
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Post, Category, Comment, PostImage
from users.models import Profile
from .forms import *
from django.contrib import messages
# ДЕКОРАТОР, ЧТОБ ТОЛЬКО ЗАРЕГАННЫЙ ПОЛЬЗОВАТЕЛЬ ВИДЕЛ СТРАНИЦУ   PostImageForm,
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# ПОИСК ПО САЙТУ
from django.db.models import Q 
# МИКСИН, ЧТОБ ТОЛЬКО ЗАРЕГАННЫЙ ПОЛЬЗОВАТЕЛЬ ВИДЕЛ СТРАНИЦУ
from django.contrib.auth.mixins import LoginRequiredMixin
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db import transaction
from django.core.mail import EmailMessage
from .filters import PostFilter


# Ошибка при отправке email
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


class ProfileCity:
    '''Города продавцов'''
    def get_city(self):
        return Profile.objects.all().values_list('city')


# ПАГИНАЦИЯ
PAGINATION_COUNT = 2

class HomeViews(ListView, ProfileCity):
    model = Post
    template_name = "post/index.html"
    context_object_name = "post"
    paginate_by = 6
    categories = Category.objects.filter(parent_category=None)
    
    # ФИЛЬТРЫ
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["filter"] = PostFilter(self.request.GET, queryset=self.get_queryset())
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Все объявления"
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related("category")



class PostByCategory(ListView):
    model = Post
    template_name = "post/index.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):

        return Post.objects.filter(
            category_id=self.kwargs["category_id"], is_published=True
        ).select_related("category")



class ViewPost(DetailView):
    model = Post
    context_object_name = "post_item"
    template_name = "post/post_detail.html"
    form_class = CommentForm
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        photos = PostImage.objects.filter(post=post)
        context['photos'] = photos
        form = CommentForm()
        comments = post.comments.filter(active=True)
        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context
    
    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comments.filter(active=True)
        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():           
            name = form.cleaned_data['name']
            body = form.cleaned_data['body']
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))      
            comments = Comment.objects.create(
                name=name, body=body, post=post,
            )
            form = CommentForm()
      
            #  parent_id=form.parent_id,
  
            context['form'] = form
            
        return self.render_to_response(context=context)

    def delete_comment( request, comment_id):
        users_comment = get_object_or_404(Comment, pk=comment_id)
        users_comment.delete()
     
        return redirect(reverse('home'))
     

# СОЗДАТЬ ПОСТ
@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
    model = Post
    template_name = "post/add.html"
    success_url = None
    form_class = PostForm

    def get_context_data(self, **kwargs):
        data = super(CreatePost, self).get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            data['images'] = PostImageFormSet()
        return data
   
    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        email = EmailMessage(f'{self.request.user} добавил пост '+ form.instance.title+ self.request.user.email, f'Все круто, пост от {self.request.user} добавлен!', to=[self.request.user.email])
        # {self.request.user.email}
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            email.send()
            if images.is_valid():
                images.instance = self.object
                images.save()
               
        return super(CreatePost, self).form_valid(form)
  
    def get_success_url(self):
        messages.success(
            self.request, 'Объявление успешно добавлено.')
        return reverse_lazy('views_post', kwargs={'pk': self.object.pk})


#РЕДАКТИРОВАТЬ ПОСТ С ГАЛЕРЕЕЙ
@method_decorator(login_required, name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    template_name = "post/add.html"
    pk_url_kwarg = "pk"
    success_url = None
    form_class = PostForm

    def get_context_data(self, **kwargs):
        data = super(UpdatePost, self).get_context_data(**kwargs)
        update = True
        data['update'] = update
        if self.request.POST:
            data['images'] = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['images'] = PostImageFormSet(instance=self.object)
        return data
   
    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
          
            if images.is_valid():
                images.instance = self.object
                images.save()
               
        return super(UpdatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('views_post', kwargs={'pk': self.object.pk})


    

# УДАЛИТЬ ПОСТ
@method_decorator(login_required, name='dispatch')
class PostDeleteView( DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Объявление удалено.')
        return reverse_lazy("user_posts")

    def get_queryset(self):
        return self.model.objects.all()


# ПОИСК ПО САЙТУ
class SearchResultsView(ListView):
    model = Post
    template_name = 'post/search.html'

    def get_queryset(self): # Поиск или заголовок или тело. Учитывает регистр
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list

def signup(request):
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'updated_ad')
        user = self.request.user
        
        return Post.objects.filter(author=user).order_by(order_by) 


def help(request):

    # если метод GET, вернем форму
    if request.method == 'GET':
        form = HelpForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = HelpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            body = form.cleaned_data['body']
            phone = form.cleaned_data['phone']
            email = EmailMessage(
                'Обращение в техподдержку',
                'Обращение в техподдержку от '+name ,
                to=['repostwebsite@gmail.com'])
            try:
                email.send()
                Help.objects.create(name=name, body=body, phone=phone)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('help')
    else:
        return HttpResponse('Неверный запрос.')

    # form = HelpForm()
    # if form.is_valid():
    #     # phone = form.cleaned_data.get('phone') 
    #     name = form.cleaned_data.get('name')

    #     email = EmailMessage(
    #             'Обращение в техподдержку',
    #             'Обращение в техподдержку от '+name ,
    #             to=['repostwebsite@gmail.com'])
                
    #     email.send()
    #     form.save()
    return render(request, 'help/help.html', {'form': form})

# def success_view(request):
#     return HttpResponse('Приняли! Спасибо за вашу заявку.')

def confidence(request):
    return render(request, 'help/confidence.html')

def doc(request):
    return render(request, 'help/doc.html')

def rules(request):
    return render(request, 'help/rules.html')