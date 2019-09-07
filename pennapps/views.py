from django.shortcuts import render

def present(request):
    my_template = "present.html"
    context = {}
    return render(request, my_template, context)