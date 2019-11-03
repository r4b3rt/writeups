from hashlib import sha1

def proof(t, prefix):
    i = 0
    while True:
        if sha1(str(t + str(i)).encode()).hexdigest().startswith(prefix):
            return str(i)
        i += 1

if __name__ == '__main__':
    from sys import argv
    print(proof(argv[1], argv[2]))
