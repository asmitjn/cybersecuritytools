import hashlib

flag=0

print('-'*50)
print('This password cracker can crack MD5, SHA1, SHA256, SHA512 hashes......')
print('-'*50)

pass_hash=input("Input hash: ")

wordlist=input('File name: ')

try:
    pass_file=open(wordlist, 'r')
except:
    print('No file found')
    quit()

for word in pass_file:

    enc_word=word.encode('utf-8')
    digest=hashlib.md5(enc_word.strip()).hexdigest()
    digest2=hashlib.sha1(enc_word.strip()).hexdigest()
    digest3=hashlib.sha256(enc_word.strip()).hexdigest()
    digest4 = hashlib.sha512(enc_word.strip()).hexdigest()

    if digest==pass_hash :
        print('Hurray! Password found')
        print('Password is '+word)
        flag=1
        break

    elif digest2==pass_hash:
        print('Hurray! Password found')
        print('Password is '+word)
        flag=1
        break

    elif digest3 == pass_hash:
        print('Hurray! Password found')
        print('Password is ' + word)
        flag = 1
        break

    elif digest4 == pass_hash:
        print('Hurray! Password found')
        print('Password is ' + word)
        flag = 1
        break

if flag==0:
    print('Sorry, your password is not in the list')

