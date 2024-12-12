from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from collections import Counter
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
    library = Library(content = request.POST['content'],
                      author = request.POST['author'],
                      genre = request.POST['genre'],
                      status = request.POST.get('status', 1),
                      rating = request.POST.get(None),
                      review_id = request.POST.get(None)
                    )
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
    #new_rating = request.POST.get('rating')
    #print(new_status, new_rating)
    if new_status:
        book_to_update.status = int(new_status)
    #if new_rating:
    #    book_to_update.rating = float(new_rating)
    book_to_update.save()
    return redirect("/list/")  # Redirect to the library list view after updating
'''
def rate_book(request, book_id):
    book_to_rate = Library.objects.get(id=book_id)
    new_rating = request.POST.get('rating')
    if new_rating:
        book_to_rate.rating = float(new_rating)
        book_to_rate.save()
    return redirect("/list/")
'''
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
def filter_books_by_date(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if not start_date or not end_date:
        context = {'book_list': get_book_list()}
        return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)
    with connection.cursor() as cursor:
        # Use a parameterized query to prevent SQL injection (prepared statement)
        print(start_date, end_date)
        cursor.execute("SELECT * FROM \"HelloWorld_App_library\" WHERE date_added >= %s AND date_added <= %s", [start_date, end_date])
        # Fetch all results
        rows = cursor.fetchall()
    status_total = len(rows)
    context = {'book_list': get_book_list(), 'books': rows, 'status_total': status_total}
    return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)
def filter_books(request):
    new_status = request.POST.get('status')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    for_all_time = request.POST.get('for_all_time')
    book_genre = request.POST.get('book_genre')
    book_title = request.POST.get('book_title')
    book_author = request.POST.get('book_author')

    query = "SELECT * FROM \"HelloWorld_App_library\" WHERE 1=1"
    query_params = []
    if new_status and new_status != '0':
        query += " AND status = %s"
        query_params.append(new_status)
    if not for_all_time and start_date and end_date:
        query += " AND date_added >= %s AND date_added <= %s"
        query_params.extend([start_date, end_date])
    if book_genre:
        query += " AND genre ILIKE %s"  # Use ILIKE for case-insensitive search
        query_params.append(f"%{book_genre}%")  # Allow partial matching
    if book_title:
        query += " AND content ILIKE %s"  # Use ILIKE for case-insensitive search
        query_params.append(f"%{book_title}%")  # Allow partial matching
    if book_author:
        query += " AND author ILIKE %s"  # Use ILIKE for case-insensitive search
        query_params.append(f"%{book_author}%")  # Allow partial matching
    with connection.cursor() as cursor:
        # Use a parameterized query to prevent SQL injection (prepared statement)
        print(new_status, start_date, end_date, book_title, book_genre, book_author)
        print(query, query_params)
        cursor.execute(query, query_params)
        # Fetch all results
        rows = cursor.fetchall()
    status_total = len(rows)
    books = [
        {'id': row[0], 'content': row[1], 'status': row[2], 'date_added': row[3], 'author': row[4], 'genre': row[5]} for row in rows
    ]
    '''
    status_counts = Counter(row[2] for row in rows)  # Count book statuses
    if status_counts:
        predominant_status, count = status_counts.most_common(1)[0]
        proportion = count / status_total
    else:
        predominant_status = "None"
        proportion = 0

    genre_counts = Counter(row[5] for row in rows if row[5])  # Count non-empty genres

    if genre_counts:
        predominant_genre, count = genre_counts.most_common(1)[0]
        proportion = count / (status_total - len([row for row in rows if not row[5]]))  # Exclude books with no genre
    else:
        predominant_genre = "None"
        proportion = 0
    '''

    status_counts = Counter(row[2] for row in rows)
    most_common_status, most_common_count = status_counts.most_common(1)[0]

    # Check for ties
    if any(count == most_common_count for status, count in status_counts.items() if status != most_common_status):
        predominant_status = "None"
    else:
        predominant_status = most_common_status

    genre_counts = Counter(row[5] for row in rows if row[5])
    most_common_genre, most_common_count = genre_counts.most_common(1)[0]

    # Check for ties in genres
    if any(count == most_common_count for genre, count in genre_counts.items() if genre != most_common_genre):
        predominant_genre = "None"
    else:
        predominant_genre = most_common_genre
    text_status = ""
    if new_status == '1':
        text_status = "To Be Read"
    elif new_status == '2':
        text_status = "Current"
    elif new_status == '3':
        text_status = "Read"

    predom_status = ""
    print(predominant_status)
    if predominant_status == 1:
        predom_status = "To Be Read"
    elif predominant_status == 2:
        predom_status = "Current"
    elif predominant_status == 3:
        predom_status = "Read"
    elif predominant_status == "None":
        predom_status = "None"
    context = {'book_list': get_book_list(), 'books': books, 'text_status': text_status or "All Statuses", 'status_total': status_total, 'predom_status': predom_status,
            'predominant_genre': predominant_genre,}
    return render(request, 'HelloWorld_App/HelloWorld_App_list.html', context)