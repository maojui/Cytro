MORSE_CODE = {
# Alpha
'A': '.-',      'B': '-...',    'C': '-.-.',    'D': '-..',     'E': '.',    
'F': '..-.',    'G': '--.',     'H': '....',    'I': '..',      'J': '.---', 
'K': '-.-',     'L': '.-..',    'M': '--',      'N': '-.',      'O': '---',
'P': '.--.',    'Q': '--.-',    'R': '.-.',     'S': '...',     'T': '-',    
'U': '..-',     'V': '...-',    'W': '.--',     'X': '-..-',    'Y': '-.--', 
'Z': '--..',    
# Digit
'0': '-----',   '1': '.----',   '2': '..---',   '3': '...--',
'4': '....-',   '5': '.....',   '6': '-....',   '7': '--...',   '8': '---..',   
'9': '----.',   ' ': '/',
}


def morse_decode(message):
    """
    Input a string only contain 
    '/' for blank,
    '.' for dot and 
    '-' for dash, 
    split by blank: ' '
    """
    DECODE = dict((v,k) for k,v in MORSE_CODE.items())
    return  ''.join([DECODE[m] if m in DECODE else '?' for m in message.split()])

def morse_encode(message):
    "Input a string contain 'a-z, A-Z, 0-9, blank', will encode to morse code."
    try:
        return  ' '.join([MORSE_CODE[m] for m in message.upper()])
    except:
        raise ValueError('Only contain a-z, A-Z, 0-9 or blank')

