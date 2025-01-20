# projectapp/views.py
from django.shortcuts import render
from .forms import SearchForm
from .models import Project
import os
import zipfile
from django.conf import settings
from django.http import HttpResponse
from projectapp.models import Project  # Replace this with your actual app name
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
# views.py/
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate

def index(request):

     return render(request, 'index.html')

def about(request):

     return render(request, 'about.html')

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('your-name')
        company = request.POST.get('company')
        email = request.POST.get('your-email')
        phone = request.POST.get('phone')
        message = request.POST.get('your-message')

        # Compose the email
        subject = f"New Contact Message from {name}"
        email_message = f"""
        Name: {name}
        Company: {company}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        # Send the email
        send_mail(
            subject,
            email_message,
            'your_email@gmail.com',  # Sender email
            ['default_receiver@gmail.com'],  # Recipient email(s)
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully!'})

    return render(request, 'contact.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ReviewForm

@login_required
def home(request):
    form = SearchForm(request.GET or None)
    projects = None

    if form.is_valid():
        search_type = form.cleaned_data['search_type']
        search_value = form.cleaned_data['search_value']

        # Filter based on the selected search type
        if search_type == 'year':
            projects = Project.objects.filter(year=search_value)
        elif search_type == 'document_link':
            projects = Project.objects.filter(document_link__icontains=search_value)
        elif search_type == 'project_id':
            projects = Project.objects.filter(project_id__icontains=search_value)
        elif search_type == 'project_details':
            projects = Project.objects.filter(project_details__icontains=search_value)
        
        if request.method == "POST":
            project_id = request.POST.get('project_id')
            project = get_object_or_404(Project, id=project_id)
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = project
                review.user = request.user
                form.save()
                return redirect('home')

    return render(request, 'home.html', {'form': form, 'projects': projects})



# Load the datasheet (assuming it's in your project)
DATA_PATH = "user_data.xlsx"  # Replace with your actual file path


def download_data(request):
    if request.method == 'POST':
        # Get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Load the Excel sheet and validate credentials
        data = pd.read_excel(DATA_PATH)
        user_row = data[(data['user_name'] == username) & (data['password'] == password)]

        if not user_row.empty:
            # Generate PDF with user data
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="user_data1.pdf"'

            # Create the PDF
            p = canvas.Canvas(response)
            p.drawString(100, 800, f"User Data for {username}")
            y = 750
            for index, row in user_row.iterrows():
                p.drawString(100, y, f"S.No: {row['s.no']}, Username: {row['user_name']}")
                y -= 20

            p.save()
            return response
        else:
            return render(request, 'home.html', {'error': 'Invalid credentials'})

    return render(request, 'home.html')



@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already exists!"})
        
        # Create the user
        User.objects.create_user(username=username, password=password)
        return JsonResponse({"success": True, "message": "User created successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request method"})




@csrf_exempt
@login_required
def validate_credentials(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            # Return the URL for downloading data if authenticated
            return JsonResponse({
                "success": True,
                "message": "Authentication successful!",
                "pdf_url": "/path/to/downloaded/data.pdf"
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password!"
            })
    return JsonResponse({"success": False, "message": "Invalid request method"})


@login_required
def download_files_as_zip(request, year):
    # Query projects for the selected year
    projects = Project.objects.filter(year=year)

    # Create a temporary ZIP file
    zip_filename = f"projects_{year}.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for project in projects:
            # Build the file path
            file_path = os.path.join(
                settings.MEDIA_ROOT, f"path/to/fake/documents/project_{project.sno}.pdf"
            )
            if os.path.exists(file_path):  # Ensure file exists
                # Add the file to the ZIP
                zip_file.write(file_path, os.path.basename(file_path))

    # Serve the ZIP file as a download
    with open(zip_path, "rb") as zip_file:
        response = HttpResponse(zip_file.read(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'

    # Optionally, clean up the ZIP file after serving it
    os.remove(zip_path)

    return response



def verify_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            project_id = data.get('project_id')

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Authentication successful, return a success response
                return JsonResponse({'success': True, 'message': 'User verified successfully.'})
            else:
                # Authentication failed
                return JsonResponse({'success': False, 'message': 'Invalid username or password.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the actual home page name
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render
from .forms import ContactForm

from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            success = True  # Set success flag
            form = ContactForm()  # Reset the form after saving
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form, 'success': success})



from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# def user_history(request):
#     context = {}
#     if request.method == "POST":
#         username = request.POST.get('username', '').strip()
        
#         # Load the Excel file (update the path as needed)
#         try:
#             df = pd.read_excel('/home/prasad/Downloads/hospital_data.xlsx')
            
#             # Filter the data by the username
#             filtered_data = df[df['Name'].str.contains(username, case=False, na=False)]
            
#             # Convert to a list of dictionaries
#             context['data'] = filtered_data.to_dict('records')
#             context['username'] = username
#         except Exception as e:
#             context['error'] = f"Error reading data: {str(e)}"
    
#     return render(request, 'user_history.html', context)

from django.shortcuts import render
from .models import UploadData  # Ensure this matches your model name

def user_history(request):
    context = {}

        # Filter the data based on the username (case insensitive)
    filtered_data = UploadData.objects.all().order_by('-created_at') 
        
        # Add the data and username to the context
    context = {
            'data': filtered_data,
        }
    
    return render(request, 'user_history.html', context)



# views.py
from django.shortcuts import render, redirect
from .forms import UploadDataForm
@login_required
def upload_data(request):
    if request.method == 'POST':
        form = UploadDataForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('upload_data')  # Redirect to a success page
    else:
        form = UploadDataForm()
    return render(request, 'upload_modal.html', {'form': form})
