import subprocess
import hashlib


def run_cmd(user_input):
    subprocess.call(user_input, shell=True)


def weak_hash(data):
    return hashlib.md5(data.encode()).hexdigest()
