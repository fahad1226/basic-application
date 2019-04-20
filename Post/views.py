from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from .models import Post
from django.views.generic import ListView , DetailView, CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


Posts = [
    {
        'author':'Fahad Bin Munir',
        'title':'About Java',
        'content':'this is my first post about java programming language,hope u guys will like it',
        'date_posted':'January 28 2019'
    },

    {
        'author':'Sinthi Sen',
        'title':'About C Programming',
        'content':'this is my first post about C programming language,hope u guys will enjoy it',
        'date_posted':'January 28 2019'
    },

    {
        'author':'Rasik Hawk',
        'title':'About Meme',
        'content':'this is my first post about facebok meme,hope u guys will like it guyz',
        'date_posted':'January 28 2019'
    }

]
@login_required
def Home(request):
    context={
        'my_posts':Post.objects.all(),
        'title':'Facebook'
    }

    return render(request,'home.html',context)


class PostListView(LoginRequiredMixin ,ListView):

    model = Post
    template_name = 'home.html'
    context_object_name = 'my_posts'
    ordering = ['-date']
    paginate_by = 4


class UserPostListView(LoginRequiredMixin ,ListView):

    model = Post
    template_name = 'user_post.html'
    context_object_name = 'my_posts'
    paginate_by = 4

    def get_queryset(self):

        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):

    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):

    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def About(request):

    return render(request,'about.html',context={'title':'About-Facebook'})





    """def search(self):
        query_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            query_list = query_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author_first_name__icontains=query) |
            Q(author_last_name__icontains=query)
            ).distinct()"""
