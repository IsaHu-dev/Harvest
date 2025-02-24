
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from client.forms import ArticleForm, UpdateUserForm
from .models import Article

@login_required(login_url='my-login')
def client_dashboard(request):
<<<<<<< HEAD
    user_articles = Article.objects.filter(user=request.user)
    return render(request, 'client/client-dashboard.html', {'articles': user_articles})
    return render(request, 'client/client-dashboard.html', context)
=======
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_creator):
        raise PermissionDenied("You do not have access to the creator dashboard.")

    user_articles = Article.objects.filter(user=request.user)
    return render(request, 'creator/creator-dashboard.html', {'articles': user_articles})

@login_required(login_url='my-login')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, 'Your article has been created successfully!')
            return redirect('published')
    else:
        form = ArticleForm()

    return render(request, 'creator/create-article.html', {'CreateArticleForm': form})
>>>>>>> 9db95efb8e3c3ad66f5385c45b0c93387a5959e2

@login_required(login_url='my-login')
def regular_articles(request):
    articles = Article.objects.all()
    return render(request, 'creator/regular-articles.html', {'AllArticles': articles})

@login_required(login_url='my-login')
def update_article(request, pk):
    article = get_object_or_404(Article, id=pk)

    if not (article.user == request.user or request.user.is_superuser or request.user.is_staff or request.user.is_creator):
        raise PermissionDenied("You do not have permission to update this article.")

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your article has been updated successfully!')
            return redirect('update-success')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'creator/update-article.html', {'UpdateArticleForm': form})

@login_required(login_url='my-login')
def delete_article(request, pk):
    article = get_object_or_404(Article, id=pk)

    if not (article.user == request.user or request.user.is_superuser or request.user.is_staff or request.user.is_creator):
        raise PermissionDenied("You do not have permission to delete this article.")

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'The article has been deleted successfully.')
        return redirect('delete-success')

    return render(request, 'creator/delete-article.html', {'article': article})

@login_required(login_url='my-login')
def manage_account(request):
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('creator-dashboard')

    return render(request, 'creator/manage-account.html', {'UpdateUserForm': form})

@login_required(login_url='my-login')
def delete_success(request):
    return render(request, 'creator/delete-success.html')

@login_required(login_url='my-login')
def update_success(request):
    return render(request, 'creator/update-success.html')
