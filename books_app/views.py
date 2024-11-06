from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Book
from .forms import BookForm
from comments_app.forms import CommentForm

def view_books(request):
    books_list = Book.objects.filter(is_verified=True)
    paginator = Paginator(books_list, 12)
    
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    context = {
        "books": books
    }

    return render(request, "books/index.html", context=context)


def view_detail_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    genres = book.genre.all()
    comments = book.comments.filter(is_verified=True)
    form = CommentForm()
    
    context = {
        "book": book,
        "genres": genres,
        "comments": comments,
        "form": form
    }
    return render(request, "books/detail_book.html", context=context)


@login_required(login_url='users:login')
def add_book_view(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('books:index')
    else:
        form = BookForm()
        
    return render(request, 'books/add_book.html', context={'form': form})


@login_required(login_url='users:login')
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.seller != request.user:
        raise PermissionDenied(
            "У вас нет прав на редактирование."
        )
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = BookForm(instance=book)    
    return render(request, 'books/add_book.html', {'form': form})


@login_required(login_url='users:login')
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.seller != request.user:
        raise PermissionDenied(
            "У вас нет прав на удаление."
        )

    if request.method == "POST":
        book.delete()
        return redirect('books:index')
    return render(request, 'books/delete_book.html', {'book': book})


@require_POST
@user_passes_test(lambda user: user.is_superuser)
def change_book_status(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.is_verified = not book.is_verified
        book.save()
        return JsonResponse({"status": "success", "is_verified": book.is_verified})
    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Книга не найдена"})