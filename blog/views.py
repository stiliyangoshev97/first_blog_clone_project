from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
import datetime

# Create your views here.


class AboutView(TemplateView):
	template_name = 'about.html'

class PostListView(ListView):
	model = Post
	context_object_name = 'post_list'

	def get_queryset(self):

		# Grab the published date (__lte means less then or equal to).
		# '-' means order them by the most recent and no dash means the opposite
		# SELECT + FROM Post WHERE pub_date <= timezone.now()
		return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(LoginRequiredMixin, DetailView):
	model = Post


class CreatePostView(CreateView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
	# Redirect if login isn't successful
	login_url = '/login/'
	# Redirect if login is successful
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	# Redirect after deleting successfully
	success_url = reverse_lazy('post_list')

# Draft is where the posts that haven't been published will appear
class DraftListView(LoginRequiredMixin, ListView):
	# Redirect if login isn't successful
	login_url = '/login/'
	# Redirect if login is successful
	redirect_field_name = 'blog/post_list.html'
	model = Post

	def get_queryset(self):
		# If the publication date is null then is a draft
		# because is not published
		return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#############################################################
############################################################

@login_required
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			# Save the form
			comment = form.save(commit = False)
			# Model Comment has an attribute 'post' which is a ForeignKey
			# To the actual Post. This means literally make comment.post
			# equal to Post
			comment.post = post
			# Save all the information
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		# Create the form and just open the comment_form.html section 
		# with the form to be filled up again
		form = CommentForm()
	return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	# We call comment.approve() from the models and change the state
	# from False to True with the line bellow
	comment.approve()
	# Comment is connected to a particular post, we are reaching
	# Comment class and the post attribute in it and its PK
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	# Create a post PK as on line 94
	# We save it as an extra var, because it will be deleted with line 102
	post_pk = comment.post.pk
	# delete() is a Django built-in function
	comment.delete()
	return redirect('post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# Publish is a method in the Post class in models
	post.publish()
	# PK is just a PK of the Post we made
	return redirect('post_detail', pk=pk)





