import socket, sys
import time, queue
import threading
import requests

usage='python3 fast_port_scanner.py TARGET START_PORT END_PORT THREADS'

print('*'*50)
print('Python Fast Port Scanner')
print('*'*50)

target=sys.argv[1]
start_port=int(sys.argv[2])
end_port=int(sys.argv[3])
thread_no=int(sys.argv[4])

result='PORT\tSTATE\tSERVICE\n'

try:
    target = socket.gethostbyname(target)
except:
    print('[-] Host resolution failed')
    exit()

print('[+] Scanning target {}'.format(target))

if not target or not str(start_port) or not end_port or not thread_no:
    print(usage)
    exit()

def get_banner(port,s):
    if (port==80):
        response=requests.get('http://'+ target)
        return response.headers['Server']
    try:
        return s.recv(1024).decode()
    except:
        return 'Not Found'



def scan_port(t_no):
   global result
   while not q.empty():
        port=q.get()
        # print('[+] Scanning port {}....'.format(port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            conn = s.connect_ex((target, port))
            if not conn:
                banner=get_banner(port,s)
                banner=''.join(banner.splitlines()) # Used to remove the extra spacing between the two lines
                result+=f'{port}\tOPEN\t{banner}\n'
            s.close()
        except socket.gaierror as e:
            pass
        # except TypeError:
        #     pass
        # except ZeroDivisionError:
        #     print('Cannot be divided by 0')
        #     pass
        # except KeyboardInterrupt:
        #     print('Pressed ctrl+c, quitting the program')
        #     exit()
        q.task_done()


q=queue.Queue() # It is used to store the ports in a queue

start_time=time.time()

for j in range(start_port, end_port+1):
    q.put(j)

for i in range(thread_no):
    t=threading.Thread(target=scan_port,args=(i,))
    # Everytime it is run, 'scan_port' function is called which scans each port
    t.start()


q.join() # It is used to specify that the code below it runs only after the code above it is executed completely

end_time=time.time()
print(result)
print('Time taken {}'.format(end_time-start_time))

with open('ports.txt', 'w') as file:
    file.write(f'Port scan results for target: {target}\n')
    file.write(result)

print('Written to file ports.txt')