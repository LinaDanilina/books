
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book,Opinion
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.utils.html import escape

def index(request):
    latest_book_list = Book.objects.order_by('-pub_date')[:100]
    context = {'latest_book_list': latest_book_list}
    return render(request, 'bks/index.html', context)

def results(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bks/results.html', {'book': book})

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bks/book.html', {'book': book})

def vote(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        selected_opinion = book.opinion_set.get(pk=request.POST['opinion'])
    except (KeyError, Opinion.DoesNotExist):
        return render(request, 'bks/book.html', {
        'book': book,
        'error_message': "You didn't select a choice.",
})
    else:
        selected_opinion.votes += 1
        selected_opinion.save()
    return HttpResponseRedirect(reverse('bks:results', args=(book.id,)))

def render_book(request, book_id, additional_context={}):
    book = get_object_or_404(Book, id=book_id)
    opinions = book.opinion_set\
    .order_by('-created_at')
    context = {'book': book,
    'opinions': opinions,
    **additional_context}
    return render(request, 'bks/book.html', context)

def create_opinion(request, book_id):
    text = request.POST['text']

    error_message = None
    if not text or text.isspace():
        error_message = 'Пожалуйста, введите текст!'
    if error_message:
        context = {'error': error_message,
        'text': escape(text)}
        return render_book(request, book_id, context)
    else:
        Opinion(book_id=book_id, opinion_text=text).save()
        redirect_url = reverse('bks:book_by_id', kwargs={'book_id': book_id})
        return HttpResponseRedirect(redirect_url)

def book(request, book_id):
    if request.method == 'POST':
        return create_opinion(request, book_id)
    else:
        return render_book(request, book_id)