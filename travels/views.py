from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from travels.forms import ProfileForm, BlogPostForm
from django.core.exceptions import ObjectDoesNotExist

from travels.models import Profile, BlogPost, Comment


# Create your views here.
class LandingPage(View):
    def get(self, request):
        all_posts = BlogPost.objects.all()
        return render(request, 'index.html', {'all_posts': all_posts})


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')


class EditProfileView(View, LoginRequiredMixin):
    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, "edit_profile.html", {'form': form})

    def post(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "profile.html", {'alert': alert})
        return render(request, "edit_profile.html", {'form': form})

class BlogViews(View):
    def get(self, request):
        # posts_all = BlogPost.objects.all()
        posts = BlogPost.objects.filter().order_by('-dateTime')
        users_posts = BlogPost.objects.filter(author=request.user)
        return render(request, "blog.html", {'posts': posts, 'users_posts': users_posts})


class AddBlogsView(View, LoginRequiredMixin):
    def get(self, request):
        form = BlogPostForm()
        return render(request, "add_blogs.html", {'form': form})

    def post(self, request):
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return redirect('blogs')
        else:
            return render(request, "add_blogs.html", {'form': form})


class BlogDetailView(View):
    def get(self, request, id):
        blog_details = get_object_or_404(BlogPost, id=id)
        return render(request, 'blog_post_detail.html', {'blog_details': blog_details})


class BlogCommentsView(View):
    def get(self, request, slug):
        post = BlogPost.objects.filter(slug=slug).first()
        comments = Comment.objects.filter(blog=post)
        return render(request, "blog_comments.html", {'post':post, 'comments':comments})

    def post(self, request, slug):
        if slug:
            post = BlogPost.objects.filter(slug=slug).first()
            if post:
                user = request.user
                content = request.POST.get('content', '')
                comment = Comment(user=user, content=content, blog=post)
                comment.save()
                # return redirect('blog_comments', slug=slug)
                return HttpResponseRedirect(reverse('blogs'))
        # Obsługa przypadku gdy slug nie został podany lub post nie istnieje
        return HttpResponseNotFound("Not Found")

