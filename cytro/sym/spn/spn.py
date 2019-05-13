import types

def rev_sbox(sbox):
    """
    Reverse Sbox
    """
    rev_sbox = [None]*len(sbox)
    for i in range(len(sbox)) :
        rev_sbox[sbox[i]] = i

def get_masks(sbox,bias=0,dumb=True):
    """
    Given @sbox with hope minimum @bias (default for 50)  
    [@dumb = True for nothing print out]  
    return the a,b which presents input mask & output mask with it's bias
    """
    pairs = []
    threshold = bias or 50
    for insum in range(1,len(sbox)):
        for outsum in range(1,len(sbox)):
            if not insum*outsum:
                continue
            bias = sum((bin(x&insum).count('1') - bin(sbox[x]&outsum).count('1')) % 2 for x in range(256)) - 128
            if abs(bias) > 50:
                pairs.append((insum,outsum,bias))
                print('+'.join(['x{i}'.format(i) for i in range(8) if insum&(2**i)]) + ' -> ' + '+'.join(['y{i}'.format(i) for i in range(8) if outsum&(2**i)]),bias) if not dumb else None
    return pairs

# compute the linear approximation for a given "input = output" equation
def LAT(sbox, input_size, output_size, dumb=True):
    """ 
        Generate Linear Approximation Table (DDT)  
        @sbox is for square(n x n) sbox. 
    """
    if type(sbox) == types.FunctionType :
        _sbox = sbox
    else :
        def _sbox(i):
            return sbox[i]
    # Initialize linear approximation table.
    Atable = [[0 for _ in range(output_size)] for _ in range(input_size)]
    
    # Loop over all input bytes
    for inp in range(input_size) :
        print(inp)
        for outp in range(output_size) :
            total = 0
            
            # calculate Bias
            for bs in range(input_size):
                input_masked = bs & inp
                output_masked = _sbox(bs) & outp
                if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
                    total += 1 
            Atable[inp][outp] = total - (input_size//2)
    
    if not dumb :
        print("   |" + ''.join([hex(i)[2:].rjust(3) + ' ' for i in range(input_size)]))
        print(" " + "-" * ((input_size) * 4 + 4))
        for idx in range(output_size):
            print("{}|".format(hex(idx)[2:].rjust(3,' ')),end='')
            print(' '.join([str(abs(i)).rjust(3) for i in Atable[idx]]))
            
    return Atable
    
def DDT(sbox, dumb=True):
    """ 
    Differential Distribution Table (DDT)  
    @sbox is for square(n x n) sbox. 
    """
    SIZE = [2**i for i in range(9)]
    assert len(sbox) in SIZE, 'length of sbox must be 2**n, n<=8'
    input_size = output_size = SIZE.index(len(sbox))
    Dtable = [[0 for _ in range(1<<output_size)] for _ in range(1<<input_size)]
    for i in range(1<<input_size) :
        for j in range(1<<output_size) :
            Din = i ^ j
            Dout = sbox[i] ^ sbox[j]
            Dtable[Din][Dout] += 1
    
    # Print out the result
    if not dumb :
        print("   |" + ''.join([hex(i)[2:].rjust(3) + ' ' for i in range(1<<input_size)]))
        print(" " + "-" * ((1<<input_size) * 4 + 4))
        for idx in range(1<<output_size):
            print("{}|".format(hex(idx)[2:].rjust(3,' ')),end='')
            print(' '.join([hex(i)[2:].rjust(3) for i in Dtable[idx]]))

    return Dtable


