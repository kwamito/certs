from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Trainee, File
from django.core.mail import send_mail
import csv


# Create your views here.
def register_admin(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_date.get('username')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'cate/register.html')


@login_required()
def home(request):
    # list of files uploaded
    files = File.objects.all()
    # getting number of trainees
    trainees = Trainee.objects.all().first()
    # number of trainees and files
    num_trainees = User.objects.filter(is_staff=False).count()
    num_files = File.objects.count()
    if request.method == 'POST' and request.FILES['file_button']:
        # get the value of the input
        file = request.FILES['file_button']
        print(file)

        # save the file to the database
        file_obj = File(file_n=file, uploaded=True)
        file_obj.save()

        file = str(file)

        # open the file from the location
        csv_file = open('./media/files/' + file)

        # read the file with the csv reader
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            # we use a try error to in case a user in the csv file has already been added
            # if not we add that user to the database
            try:
                obj = User.objects.get(email=row[3])
                print('User already exists')
            except User.DoesNotExist:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    # we create a random password for the user and save all info in
                    # the csv file to the database
                    generated_password = User.objects.make_random_password(length=14)
                    full_name = row[0] + row[1]

                    # First added users with the method below but found out users could'nt log in so i changed it obj
                    # = User(email=row[3], first_name=row[0], last_name=row[1], password=generated_password,
                    # username=full_name)

                    obj = User.objects.create_user(full_name, row[3], generated_password)
                    obj.first_name = row[0]
                    obj.last_name = row[1]
                    obj.save()

                    with open('passwords.txt', 'w') as text:
                        text.write(
                            '{} your password is {} username is {}'.format(row[3], generated_password, full_name))

                    # we send an email to the users email address
                    send_mail('Certificate',
                              '{row[0]} this is a link to see or download your certificate your password is {generated_password}',

                              'kuhneykwame@gmail.com', [row[3]], fail_silently=False)
                    # print(f'\t{row[0]} {row[1]} you have been given a certificate for completing our course this is
                    # a link to download it https://something.com, {row[2]} is your password {row[3]}')
                    line_count += 1

        print(f'Processed {line_count} lines')

    context = {
        'trainee': trainees,
        'num': num_trainees,
        'num_files': num_files,
        'files': files
    }
    return render(request, 'cate/home.html', context=context)


def UploadFile(CreateView):
    model = File
    template_name = 'cate/upload.html'
    fields = ['file']
