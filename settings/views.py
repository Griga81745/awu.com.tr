from django.shortcuts import render

def page_404(request, exception=Exception):
    return render(request, 'origin/404.html', status=404)