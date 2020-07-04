from django.shortcuts import render
from stores.models import Visiting

# Create your views here.
def index(request):
    all_cnt = Visiting.objects.count()
    print("all_cnt::::", all_cnt)

    # 날짜 데이터 모아오기
    visitings = Visiting.objects.all()
    visiting_dates = [visiting.visiting_time.date() for visiting in visitings]
    visiting_dates = set(visiting_dates)
    visiting_dates = sorted(visiting_dates)

    visitings_date_cnt ={}
    for date in visiting_dates:
        visiting_list = [visiting for visiting in visitings if visiting.visiting_time.date() == date]
        cnt = len(visiting_list)
        visitings_date_cnt[date] = cnt

    context = {
        'all_cnt': all_cnt,
        'visitings_date_cnt': visitings_date_cnt,
    }
    return render(request, 'maps/index.html', context)


def map(request):
    return render(request, 'maps/map.html')