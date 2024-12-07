from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import Library
# Create your views here.
def sayHello(request):
    return HttpResponse('<h1 style="color:red">Hello, World!</h1>')
def list_library(request):
    context = {'book_list' : Library.objects.all().order_by("-date_added")}
    return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)
def get_book_list():
    return Library.objects.all().order_by("-date_added")
def insert_book_item(request):
    #instance of library model class
    library = Library(content = request.POST['content'], status = request.POST.get('status', 1))
    #django orm to add entries to db without sql
    library.save()
    return redirect("/list/") #maybe take out first dir
    #return render(request, 'HelloWorld_App/HelloWorld_App_list.html')
def delete_book_item(request, book_id):
    book_to_delete = Library.objects.get(id= book_id)
    book_to_delete.delete()
    return redirect("/list/")

def update_book_status(request, book_id):
    book_to_update = Library.objects.get(id= book_id)
    # Check for POST request to update status
    new_status = request.POST.get('status')
    print(new_status)
    book_to_update.status = int(new_status)
    book_to_update.save()
    return redirect("/list/")  # Redirect to the library list view after updating
def filter_books_by_status(request):
    new_status = request.POST.get('status')
    if new_status == 0:
        context = {'book_list': get_book_list()}
        return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)
    with connection.cursor() as cursor:
        # Use a parameterized query to prevent SQL injection (prepared statement)
        print(new_status)
        cursor.execute("SELECT * FROM \"HelloWorld_App_library\" WHERE status = %s", [new_status])
        # Fetch all results
        rows = cursor.fetchall()
        
    # Map the rows to dictionary keys for easy use in the template
    books = [
        {'id': row[0], 'content': row[1], 'status': row[2], 'date_added': row[3]} for row in rows
    ]
    status_total = len(rows)
    text_status = ""
    if new_status == '1':
        text_status = "To Be Read"
    elif new_status == '2':
        text_status = "Current"
    else:
        text_status = "Read"
    context = {'book_list': get_book_list(), 'books': books, 'text_status': text_status, 'status_total': status_total}
    return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)