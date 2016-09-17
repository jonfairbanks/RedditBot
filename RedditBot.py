import getpass
import praw
import string
import random
import sys
import os
import time

def id_generator(size = 16, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
userAgent = id_generator()
print ("\033[1;33;40mUser Agent: " + str(userAgent) + '\033[1;37;40m \n')
usr = praw.Reddit(user_agent = userAgent)

def Login():
   global userName
   userName = input('Username: ')
   userPassword = getpass.getpass()
   try:
       usr.login(username=userName, password=userPassword, disable_warning=True)
       return 0
   except Exception:
       print ("\033[1;31;40m[ERROR] Login Failed \033[1;37;40m \n")
       Login()

def Downvote(targetUser): 
   counter = 0
   usr2 = usr.get_redditor(targetUser)
   limit = int(input('How many comments? '))
   print ('\n' * 100)
   time.sleep(1)
   print('\033[1;34;40mStarting... \033[1;37;40m \n')
   time.sleep(1)
   list = usr2.get_comments(sort='new', time='all', limit=limit)
   for comment in list:
       counter += 1
       print('\033[1;34;40m[Downvoting ' + str(targetUser) + ' (' + str(counter) + ' of ' + str(limit) + ')]\n\"' + str(comment) + '\" \033[1;37;40m \n')
       comment.downvote()
   time.sleep(3)
   print ('\033[1;32;40m[SUCCESS] Downvoted ' + str(limit) + ' of ' + str(targetUser) + '\'s comments. \033[1;37;40m \n')

print('----Reddit Login----')
while Login():
   break

print ('\n' * 100)
targetUser = input('Who do you want to downvote? ')
Downvote(targetUser)