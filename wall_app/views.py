from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from bcrypt import checkpw

def index(request):
  return render(request, 'index.html')



def register(request):
  print('\n------------ REGISTER METHOD ---------')
  if request.method == "POST":
    print(request.POST)
    
    errors = User.objects.validate_user_registration(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value, extra_tags="danger")
      return redirect('/')
    else:
      print('\n-------------- register success no errors!')
      # create User
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      birthday = request.POST['birthday']
      password = request.POST['password']
      hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
      
      created_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, birthday=birthday, password=hashed_pw) 
      request.session['user_id'] = created_user.id
      request.session['user_first_name'] = created_user.first_name
      
      messages.success(request, "Welcome from Registration")
      return redirect('/wall_page')
  return redirect('/')





def login(request):
  print('\n------------ LOGIN METHOD ---------')
  if request.method == "POST":
    print(request.POST)
    
    errors = User.objects.validate_user_login(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value, extra_tags="danger")
      return redirect('/')
    else :
      user = User.objects.get(email=request.POST['email'])
      request.session['user_id'] = User.objects.get(email=request.POST['email']).id
      request.session['user_first_name'] = User.objects.get(email=request.POST['email']).first_name
      messages.success(request, f'Welcome {user.first_name} from login', extra_tags="success")
      return redirect('/wall_page')
  return redirect('/')





def wall_page(request):
  print('\n------------ THE WALL PAGE ---------')
  if 'user_id' not in request.session:
    messages.error(request, "please log in", extra_tags="warning")
    return redirect('/')
  context = {
  'all_messages' : Message.objects.all(),
  'all_comments' : Comment.objects.all()
  }
  return render(request, 'wall_page.html', context)





def post_message(request):
  print('\n-------- post  <main>  M E S S A G E   METHOD -----')
  if request.method == "POST":
    print(request.POST)
    message = request.POST['message']
    user = User.objects.get(id=request.session['user_id'])
    Message.objects.create(message=message, user=user)
    messages.success(request, "you made a post!", extra_tags="success")
  return redirect('/wall_page')




def delete_message(request):
  pass




def post_comment(request):
  print('\n-------- commenting on a message!   METHOD -----')
  if request.method == "POST":
    print(request.POST)

    message = Message.objects.get(id=request.POST['message_id'])
    user = User.objects.get(id=request.session['user_id'])
    comment = request.POST['comment']

    Comment.objects.create(comment=comment, user=user, message=message)
    messages.success(request, "thanks for commenting! 😎", extra_tags="success")
    
  return redirect('/wall_page')




def logout(request):
  print('\n --------- LOGOUT ⛔ -------')
  if 'user_id' in request.session:
    request.session.pop('user_id')
    request.session.clear()
    messages.warning(request, "session cleared - user logged out!")
    return redirect('/')
  else:
    messages.warning(request, "nothing to clear", extra_tags="warning")
    return redirect('/')
