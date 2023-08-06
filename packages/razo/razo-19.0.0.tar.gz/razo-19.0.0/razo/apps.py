def timer():
    import datetime
    e=0
    while True:
        try:
            a=int(input('Hour:'))
            b=int(input('Minute:'))
            c=int(input('Second:'))
        except ValueError as e:
            print('Not vaild number')
        finally:
            if not e:
                break
    e=datetime.datetime.now()
    f=datetime.timedelta(hours=a,minutes=b,seconds=c)
    e+=f
    ins=[]
    for i in range(0,100000):
        ins.append(datetime.timedelta(microseconds=i))
    while True:
        print(datetime.datetime.now())
        if datetime.datetime.now()+f in ins:
            print('Time up!')
            break

