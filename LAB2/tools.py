from conf import MAX

def EbetE(value, init, end, MAX):
    if init > end:
        end = end + MAX - init
        init = 0
    if value == init or value == end:
        return True
    if value > init and value < end:
        return True
    else:
        return False

def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)

def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)