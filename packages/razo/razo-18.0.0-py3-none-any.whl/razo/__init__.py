import time
import sys
import datetime

rooting=False
sudoroot=False
nowsudo=False

def setting():
    a=input('Please set root password:')
    with open('settings.py','w') as c:
        c.write("rootpass='{}'\n".format('a'))
    a=input('What is your name?')
    with open('settings.py','a') as c:
        c.write("username='{}'\n".format(a))
    
def showinfo():
    listget={6:'Sun.',0:'Mon.',1:'Tue.',2:'Wed.',3:'Thu.',4:'Fri',5:'Sat.'}
    timer=datetime.datetime.now()
    weekday=listget[timer.weekday()]
    print(timer.strftime('%Y-%m-%d %H:%M:%S')+' {}'.format(weekday) )
    print('Razo 18.0.0(turtle_9).')
    print('Type help for help.')
    print('Still testing,please know.')


h=(
'''
help:Show help.
su:Ask for superuser license.
shutdown:Shutdown razo.
info:Show info.
setting:Run setting.
time:Get time.
sudo(add before commands):Let the command after sudo get temp root.
''')




try:
    import settings
    d=settings.rootpass
    username=settings.username
except ImportError as e:
    setting()
    
def sc():
    global sudoroot
    if not sudoroot:
        a=input('Please enter root password:')
        import settings
        if a==settings.rootpass:
            sudoroot=True
            return True
        else:
            print('Sorry.')
            return False
    else:
        return True
    
def wai(a):
    global rooting
    global sudoroot
    global nowsudo
    if a=='help':
        print(h)
    elif a=='su':
        a=input('Please enter root password:')
        import settings
        if a==settings.rootpass:
            rooting=True
        else:
            time.sleep(2)
            print('su:Sorry')
    elif a=='shutdown':
        if rooting:
            yes=input('Do you REALLY want to shutdown?[y/n]')
            if yes=='y':
                print('Shutting down.')
                time.sleep(5)
                sys.exit(0)
        else:
            print('Not able until root.')
    elif a=='info':
        showinfo()
    elif a=='setting':
        if rooting:
            setting()
            rooting=False
        else:
            print('Not able until root.')
    elif a=='time':
        listget={6:'Sun.',0:'Mon.',1:'Tue.',2:'Wed.',3:'Thu.',4:'Fri',5:'Sat.'}
        timer=datetime.datetime.now()
        weekday=listget[timer.weekday()]
        print(timer.strftime('%Y-%m-%d %H:%M:%S')+' {}'.format(weekday) )
        #The line between usually and sudo.
    elif a=='sudo help':
        if sc():
            nowsudo=True
        print(h)
        nowsudo=False
    elif a=='sudo su':
        if sc():
            nowsudo=True
        a=input('Please enter root password:')
        import settings
        if a==settings.rootpass:
            rooting=True
        else:
            time.sleep(2)
            print('su:Sorry')
        nowsudo=False
    elif a=='sudo shutdown':
        if sc():
            nowsudo=True
        if nowsudo:
            yes=input('Do you REALLY want to shutdown?[y/n]')
            if yes=='y':
                print('Shutting down.')
                time.sleep(5)
                sys.exit(0)
        else:
            print('Not able until root.')
    elif a=='sudo info':
        if sc():
            nowsudo=True
        showinfo()
        nowsudo=False
    elif a=='sudo setting':
        if sc():
            nowsudo=True
        if nowsudo:
            setting()
            rooting=False
            sudoroot=False
            nowsudo=False
        else:
            print('Not able until root.')
    elif a=='sudo time':
        if sc():
            nowsudo=True
        listget={6:'Sun.',0:'Mon.',1:'Tue.',2:'Wed.',3:'Thu.',4:'Fri',5:'Sat.'}
        timer=datetime.datetime.now()
        weekday=listget[timer.weekday()]
        print(timer.strftime('%Y-%m-%d %H:%M:%S')+' {}'.format(weekday) )
        nowsudo=False
    else:
        print('No this command.')
    

showinfo()
time.sleep(2)
import settings
print('Hello,{}.'.format(settings.username))

while True:
    if rooting:
        a=input('[root]>>>')
    else:
        a=input('[user]>>>')
    wai(a)
