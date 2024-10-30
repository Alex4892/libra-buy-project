from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


from .models import Comment
from .forms import CommentForm
from books_app.models import Book


def add_comment_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book_id = book_id
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('books:detail_book', book_id=book.id)
    else:
        form = CommentForm()

    return redirect('books:detail_book', book_id=book.id)

@login_required(login_url='users:login')
def delete_comment_view(request, comment_id, book_id):
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    if comment.author != request.user:
        raise PermissionDenied(
            "У вас нет прав на удаление"
        )
    comment.delete()
    return redirect('books:detail_book', book_id=book_id)

@login_required(login_url='users:login')
def edit_comment_view(request, comment_id, book_id):
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    book = get_object_or_404(Book, id=book_id)
    if comment.author != request.user:
        raise PermissionDenied(
            "У вас нет прав на редактирование"
        )

    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('books:detail_book', book_id=book_id)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'book': book,
        'comment': comment
    }
    
    return render(request, 'comments/edit_comment.html', context)
