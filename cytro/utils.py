

def sorted_array(array, inverse=None) :
    "Input array -> Return sorted [ (idx,value), ... ]"
    sd = {}
    idx = sorted(range(len(array)), key=lambda k: -array[k] if not inverse else array[k] )
    for i in idx :
        sd[i] = array[i]
    return list(sd.items())