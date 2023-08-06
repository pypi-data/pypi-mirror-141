def ranstr(lnum):
    import random
    try:
        if lnum == None:
            lnum = 10
        else:
            pass
        l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        ranmsg = ""
        for _ in range(lnum):
            ranmsg += random.choice(l)
        return ranmsg
        
    except TypeError:
        pass