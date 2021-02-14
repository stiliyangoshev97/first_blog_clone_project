from django import forms
from django.forms import ModelForm
from blog.models import Post, Comment

class PostForm(ModelForm):
	class Meta():
		model = Post
		fields = ('author', 'title', 'text')

		# Create widgets to then stylize them with CSS

		widgets = {
		    'title': forms.TextInput(attrs={'class':'textinputclass'}),
		    'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),

		    # textinputclass and postcontent are OUR OWN CLASSES
		    # editable and medium-editor-textarea are NOT OUR CLASSES
		}

class CommentForm(ModelForm):
	class Meta():
		model = Comment
		fields = ('author', 'text')

		widgets = {
		    'author': forms.TextInput(attrs={'class':'textinputclass'}),
		    'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
		}

