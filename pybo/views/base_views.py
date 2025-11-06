from django.shortcuts import render, get_object_or_404
from ..models import Question
#Paginator 불러오기
from django.core.paginator import Paginator
from django.db.models import Q, Count

# Create your views here.
def index(request):
    #question_list = Question.objects.order_by('-create_date')

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') #검색어
    so = request.GET.get('so', 'recent') #정렬기준

    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    if so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  #제목 검색
            Q(content__icontains=kw) |  #내용 검색
            Q(answer__content__icontains=kw) | #답변 내용 검색
            Q(author__username__icontains=kw) #질문 글쓴이 검색
        ).distinct() #답변 중복 방지.(질문의 답변, )

        """
        SELECT DISTINCT Q.*  FROM PYBO_QUESTION Q
        LEFT JOIN PYBO_ANSWER A ON A.QUESTION_ID = Q.ID
        RIGHT JOIN CUSTOMER C ON C.ID = A.AUTHOR
        WHERE Q.SUBJECT LIKE '%KW%'
            OR Q.CONTENT LIKE '%KW%'
        """

    #쿼리셋으로 조회됨.
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기

    #get_page 메서드는 유효하지 않은 번호도 자동 처리.(999->마지막 페이지로 처리.)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {'question_list': page_obj,
               'page_range':page_range,
               'kw':kw,
               'so':so
               }
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
