from projects.imports import *

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.shortcuts import render


from django.shortcuts import render
from django.http import JsonResponse

def searchitems(request, customer_id):
    customer = None

    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(pk=customer_id)

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        items = Item.objects.filter(
            Q(itemtitle__icontains=search_query) |
            Q(seller__storename__icontains=search_query) |
            Q(category__categoryname__icontains=search_query)
        )

        context = {
            'items': items,
            'search_query': search_query,
            'customer': customer,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # This is an AJAX request, return the search results as HTML
            return render(request, 'customer/searchresult.html', context)

    # For non-AJAX requests, return the full HTML page
    return render(request, 'customer/search.html', context)

