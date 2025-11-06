from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

#답변 페이징과 정렬 기능
# 페이징
from django.core.paginator import Paginator
from django.db.models import Q, Count


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)

            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm()

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') #검색어
    so = request.GET.get('so', 'recent') #정렬기준

    #정렬
    if so == 'recommend':
        answer_list = Question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    if so == 'popular':
        answer_list = Question.answer_set.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        answer_list = Question.answer_set.order_by('-create_date')

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |  #내용 검색
            Q(author__username__icontains=kw)   #내용 검색          
        ).distinct() #답변 중복 방지.(질문의 답변, )

    paginator = Paginator(answer_list, 5) #페이지당 10개씩 보여줌
    page_obj = paginator.get_page(page)
    context = {'question': question, 'form': form}

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        'question' : question,
        'form' : form,
        
        'page_range' : page_range,
        'kw' : kw,
        'so' : so
    }


    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)