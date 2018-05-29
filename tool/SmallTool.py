from datetime import datetime

def get_consume_time(func, args=()):
    begin = datetime.today()
    if len(args) == 0:
        func()
    else:
        func(args)
    end = datetime.today()
    consume = end - begin
    print(consume)
    return consume