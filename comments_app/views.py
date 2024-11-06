from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
            "У вас нет прав на удаление."
        )

    comment.delete()
    return redirect('books:detail_book', book_id=book_id)


@login_required(login_url='users:login')
def edit_comment_view(request, comment_id, book_id):
    comment = get_object_or_404(Comment, id=comment_id, book_id=book_id)
    book = get_object_or_404(Book, id=book_id)
    
    if comment.author != request.user:
        raise PermissionDenied(
            "У вас нет прав на редактирование."
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


@require_POST
@user_passes_test(lambda user: user.is_superuser)
def change_comment_status(request, book_id):
    try:
        comment = Comment.objects.get(id=book_id)
        comment.is_verified = not comment.is_verified
        comment.save()
        return JsonResponse({"status": "success", "is_verified": comment.is_verified})
    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Комментарий не найден"})
