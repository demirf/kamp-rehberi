from django.shortcuts import render, redirect, get_object_or_404, reverse   
from django.contrib import messages
from .forms import ArticleForm
from .models import Article, Comment 
from django.contrib.auth.decorators import login_required # Oturum Kontrol Etme
# Create your views here.

def index(request):
    keyword = request.GET.get('keyword')

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, 'index.html', {'articles': articles})

    articles = Article.objects.all() # Tüm Yazıları Seç
    
    return render(request, 'index.html', {'articles': articles})

@login_required(login_url = 'User:login') # Oturum Kontrol Etme
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        'articles': articles
    }    
    return render(request, 'dashboard.html', context)

@login_required(login_url = 'User:login') # Oturum Kontrol Etme
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit = False)

        article.author = request.user
        article.save()

        messages.success(request, 'Yazınız Başarıyla Oluşturuldu')
        return redirect('index')


    return render(request, 'addArticle.html', {'form': form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id) # id'si bulunmayan yazıyı da göstermemek için

    comments = article.comments.all() #Yorumları saklayacak liste
    
    return render(request, 'detail.html', {'article': article, 'comments': comments})

@login_required(login_url = 'User:login') # Oturum Kontrol Etme
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id, author = request.user)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)

    if form.is_valid():
        article = form.save(commit = False)

        article.author = request.user
        article.save()

        messages.success(request, 'Yazınız Başarıyla Güncellendi')
        return redirect('index')

    return render(request, 'update.html', {'form': form})

@login_required(login_url = 'User:login') # Oturum Kontrol Etmee
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)

    article.delete()

    messages.success(request, 'Yazınız Başarıyla Yok Edildi.')

    return redirect('index')

def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    
    if request.method == 'POST':
        comment_author = request.POST.get('comment_author')   #Form'un içindeki bilgileri alıyoruz.
        comment_content = request.POST.get('comment_content')

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)

        newComment.article = article

        newComment.save()

    return redirect(reverse('Blog:detail', kwargs = {'id': id})) #Redirect 'Dinamik URL' Olayı