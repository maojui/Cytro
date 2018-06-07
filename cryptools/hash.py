#! coding:utf-8
import os
from .strings import *
from hashlib import sha1
from PIL import Image

def sha1_collision(image1,image2) :
    '''
    Usage: input two image, open in bytes or just a string path
    
    A reimplementation of sonickun sha1-collider
    https://github.com/sonickun/sha1-collider/blob/master/collider.py
    '''
    if type(image1) == str :
        img1 = open(image1, "rb").read()
    elif type(image1) == bytes :
        img1 = image1
        images1 = 'temp1'
    else :
        assert False, "Unknown type"
    
    if type(image2) == str :
        img2 = open(image2, "rb").read()
    elif type(image2) == bytes :
        img2 = image2
        images2 = 'temp2'
    else :
        assert False, "Unknown type"
        
    # Check JPEG format
    if s2n(img1[:2]) != 0xffd8 or s2n(img2[:2]) != 0xffd8:
        print("Image is not JPEG format.")
        sys.exit(1)

    size1 = Image.open(image1).size
    size2 = Image.open(image2).size
    print("Image size:", size1)

    # Resize the image if different sizes
    if size1 != size2 : 
        new = Image.open(image2).resize(size1) 
        new.save('temp.jpg')
        img2 = open('temp.jpg', "rb").read()
        os.remove('temp.jpg')
        print("Resized:", image2)

    pdf_header = n2s(0x255044462D312E330A25E2E3CFD30A0A0A312030206F626A0A3C3C2F57696474682032203020522F4865696768742033203020522F547970652034203020522F537562747970652035203020522F46696C7465722036203020522F436F6C6F7253706163652037203020522F4C656E6774682038203020522F42697473506572436F6D706F6E656E7420383E3E0A73747265616D0A)
    jpg_header = n2s(0xFFD8FFFE00245348412D3120697320646561642121212121852FEC092339759C39B1A1C63C4C97E1FFFE01)

    # Collision blocks (This is the only part of the files which is different)
    collision_block1 = n2s(0x7F46DC93A6B67E013B029AAA1DB2560B45CA67D688C7F84B8C4C791FE02B3DF614F86DB1690901C56B45C1530AFEDFB76038E972722FE7AD728F0E4904E046C230570FE9D41398ABE12EF5BC942BE33542A4802D98B5D70F2A332EC37FAC3514E74DDC0F2CC1A874CD0C78305A21566461309789606BD0BF3F98CDA8044629A1)
    collision_block2 = n2s(0x7346DC9166B67E118F029AB621B2560FF9CA67CCA8C7F85BA84C79030C2B3DE218F86DB3A90901D5DF45C14F26FEDFB3DC38E96AC22FE7BD728F0E45BCE046D23C570FEB141398BB552EF5A0A82BE331FEA48037B8B5D71F0E332EDF93AC3500EB4DDC0DECC1A864790C782C76215660DD309791D06BD0AF3F98CDA4BC4629B1)

    prefix1 = pdf_header + jpg_header + collision_block1
    prefix2 = pdf_header + jpg_header + collision_block2

    data = b''
    data += b'\x00' * 242

    # JPEG comment
    n = (8 + len(img1))
    data += b'\xff\xfe' + n2s(n>>8) + n2s(n & 0xff)

    data += b'\x00' * 8
    data += img1[2:]
    data += img2[2:]
    data += b'endstream\nendobj\n\n'

    # Cross-reference Table
    xref = b'xref\n'
    xref += b'0 13 \n'
    xref += b'0000000000 65535 f \n'
    xref += b'0000000017 00000 n \n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)

    # width
    data += b'2 0 obj\n%010d\nendobj\n\n' % size1[0]
    xref += b'%010d 00000 n \n' % len(prefix1+data)

    # height
    data += b'3 0 obj\n%010d\nendobj\n\n' % size1[1]
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'4 0 obj\n/XObject\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'5 0 obj\n/Image\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'6 0 obj\n/DCTDecode\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'7 0 obj\n/DeviceRGB\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)

    # JPEG size
    data += b'8 0 obj\n%010d\nendobj\n\n' % len(img1+img2)
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'9 0 obj\n<<\n  /Type /Catalog\n  /Pages 10 0 R\n>>\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'10 0 obj\n<<\n  /Type /Pages\n  /Count 1\n  /Kids [11 0 R]\n>>\nendobj\n\n'
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'11 0 obj\n<<\n  /Type /Page\n  /Parent 10 0 R\n  /MediaBox [0 0 %010d %010d]\n  /CropBox [0 0 %010d %010d]\n  /Contents 12 0 R\n  /Resources\n  <<\n    /XObject <</Im0 1 0 R>>\n  >>\n>>\nendobj\n\n' % (size1[0], size1[1], size1[0], size1[1])
    xref += b'%010d 00000 n \n' % len(prefix1+data)
    data += b'12 0 obj\n<</Length 49>>\nstream\nq\n  %010d 0 0 %010d 0 0 cm\n  /Im0 Do\nQ\nendstream\nendobj\n\n' % (size1[0], size1[1])

    xref_pos = len(prefix1 + data)
    data += xref
    trailer = b'\ntrailer << /Root 9 0 R /Size 13>>\n\nstartxref\n%010d\n%%%%EOF\n' % xref_pos

    data += trailer

    outfile1 = prefix1 + data
    outfile2 = prefix2 + data
    
    # Check SHA-1 collision
    digest1 = sha1(outfile1).hexdigest()
    digest2 = sha1(outfile2).hexdigest()

    assert digest1 == digest2, "SHA1 Collision Failed."
    print(digest1,image1+"-collision.pdf")
    print(digest2,image2+"-collision.pdf")

    open(image1 + "-collision.pdf", "wb").write(outfile1)
    open(image2 + "-collision.pdf", "wb").write(outfile2)

    print("Successfully Generated Collision PDF !!!")
    print("SHA1 for collisions pdf : %s" % digest1)
    
    return True
