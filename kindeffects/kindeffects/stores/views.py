from django.shortcuts import render, redirect, get_object_or_404
from .models import Store, Visiting
from .forms import StoreForm
from django.contrib.auth.decorators import login_required

import qrcode
import qrcode.image.svg
# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        'stores' : stores,
    }
    return render(request, 'stores/index.html', context)


def store_new(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stores:index')
    else:
        form = StoreForm()

    context = {
        'form': form,
    }
    return render(request, 'stores/store_new.html', context)

@login_required
def update(request):
    print(request.user.store_id)
    store = Store.objects.get(pk=request.user.store_id)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
    return redirect('accounts:update')




def detail(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    context = {
        'store': store,
    }
    return render(request, 'stores/store_detail.html', context)

# qr이 인식되면 visit_time이 저장됨.
def visiting(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    visiting = Visiting.objects.create()
    visiting.store = store
    visiting.save()
    return redirect('stores:detail', store_pk)

# 로그인 조건이 추가되었음
@login_required
def mypage(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)

    # 수퍼유저로 로그인 했을 때 또는
    # 로그인한 사용자의 업체일 때만 --- 접근가능
    if request.user.is_superuser or request.user.store == store:
        domain = "http://www.dreamtree.site"
        store_url = f"{domain}/stores/visiting/{store_pk}/" 
        visitings = Visiting.objects.filter(store_id=store_pk)
        visiting_dates = [visiting.visiting_time.date() for visiting in visitings]
        visiting_dates = set(visiting_dates)
        visiting_dates = sorted(visiting_dates)
        
        # 방문횟수 DB를 dictionary로 만들어 context로 전달
        visitings_date_cnt ={}
        for date in visiting_dates:
            visiting_list = [visiting for visiting in visitings if visiting.visiting_time.date() == date]
            cnt = len(visiting_list)
            visitings_date_cnt[date] = cnt            
    
        context = {
            'store': store,
            'store_url': store_url,
            # 'total_visiting_date_cnt': total_visiting_date_cnt,
            'visitings_date_cnt': visitings_date_cnt,
        }
        return render(request, 'stores/store_mypage.html', context)

    # 로그인을 했으나, 다른 업체일 때 -- 본인 업체 Mypage로 이동
    return redirect('maps:index')

# 서포트 현황 report 페이지 보기
def report(request):
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

    return render(request, 'stores/report.html', context)