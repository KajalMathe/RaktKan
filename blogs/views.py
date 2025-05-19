from django.shortcuts import render
from .models import Blog
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Blog
from django.core.paginator import Paginator

def blog_list(request):
    query = request.GET.get('q')
    blogs = Blog.objects.all().order_by('-published_date')
    
    if query:
        blogs = blogs.filter(title__icontains=query)

    # Pagination
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,  # Send page_obj instead of full blogs
        'query': query,
    }
    return render(request, 'blogs/blog_list.html', context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})


