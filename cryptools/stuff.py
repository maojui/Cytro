
import subprocess
def sageworks():
    # Check if sage is installed and working
    try:
        sageversion = subprocess.check_output(['sage', '-v'])
    except OSError:
        print("[-] Check if sage is installed and working")
        return False
    if 'SageMath version' in sageversion.decode('utf-8'):
        return True
    else:
        print("[-] Check if sage is installed and working")
        return False

