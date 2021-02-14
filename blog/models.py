from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

# Create your models here.

class Post(models.Model):
	# Since we expect only one person to come in and have power over this blog
	# We create the models like this above. This means when somebody creates a post
	# The superuser 'auth.User' will have to approve that post.

	author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	text = models.TextField()
	create_date = models.DateTimeField(default = timezone.now())
	# or ->  create_date = models.DateTimeField(default = timezone.now())
	# Blank because we maybe don't want to published it yet or
	# null because we maybe have no publication date
	published_date = models.DateTimeField(blank = True, null = True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def approve_comments(self):
		# Bellow we can see that approved_comment is created in the Comment
		# model and is a boolean field
		return self.comments.filter(approved_comment = True)

	# After someone creates a Post or a Comment - where should the website take them?
	def get_absolute_url(self):
	 	return reverse('post_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.title

class Comment(models.Model):
	# Connect each comment to an actual post
	post = models.ForeignKey('blog.Post', related_name = 'comments', on_delete = models.CASCADE)
	author = models.CharField(max_length = 200)
	text = models.TextField()
	create_date = models.DateTimeField(default = datetime.datetime.now())
	approved_comment = models.BooleanField(default = False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def get_absolute_url(self):
		return reverse('post_list')


	def __str__(self):
		return self.text



