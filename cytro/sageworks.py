import subprocess as sp
import os, sys, tempfile, socket, json

_sage_script = '''
import socket, base64, json
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect({})
sock_file = sock.makefile('rwb')
    
while True:
    code = eval(sock_file.readline())
    result = None
    try:
        exec(code)
    except Exception as e:
        print(e.args)
        result = None
        break
    result = json.dumps(result)
    sock_file.write(result + '\\n')
    sock_file.flush()
'''

class Sage:

    def __init__(self):
        if sagework():
            self.sock_path = tempfile.mktemp()
            self.sage_proc = sp.Popen(['sage', '-c', _sage_script.format(repr(self.sock_path).strip())])
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.server.bind(self.sock_path)
            self.server.listen(1)
            self.client, _ = self.server.accept()
            self.client_file = self.client.makefile('rwb')
        else :
            raise Exception("Executing sage error.")
    
    def load(self, filepath):
        if filepath.endswith('.sage') :
            filepath += '.py'
            print(f'Searching {filepath}')
        elif filepath.endswith('.py'):
            # Compile .sage to .py
            if os.path.exists( filepath ) :
                pass
            elif os.path.exists( filepath[:-3] ) :
                sp.Popen([ 'sage', filepath[:-3] ]).communicate()
            else :
                raise IOError('File not found.')
        else :
            raise ValueError('Input file must be .sage or .py')
        # Load file to Sage()
        with open(filepath,'r') as script :
            self.run(script.read())
            print(f'{filepath} Loaded.')


    def run(self, code):
        code_bytes = (repr(code) + '\n').encode()
        self.client_file.write(code_bytes)
        self.client_file.flush()
        result = self.client_file.readline().rstrip()
        result = json.loads(result)
        return result

    def close(self):
        self.server.close()
        self.sage_proc.kill()
        self.sage_proc.communicate()
        os.unlink(self.sock_path)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

def sagework():
    '''Check if sage is installed and working'''
    try:
        sageversion = sp.check_output(['sage', '-v'])
        if 'SageMath version' in sageversion.decode('utf-8'):
            return True
        raise RuntimeError
    except OSError:
        print("[-] Check if sage is installed and working")
        return False

if __name__ == "__main__":
    with Sage() as sage :
        sage.load('/Users/Neptune/Desktop/github/cytro/cytro/sage/boneh_durfee.sage.py')
        a = sage.run('result = boneh_durfee(1234,12341234)\n')