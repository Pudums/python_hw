from multiprocessing import *
import sys
import time
import codecs


def process_A(conn, q):
    while True:
        s = q.get()
        conn.send(s.lower())
        time.sleep(5)


def process_B(conn_input, conn_output):
    while True:
        val = conn_input.recv()
        conn_output.send(codecs.encode(val, 'rot_13'))


time_start = time.time()
q = Queue()
conn_B_input, conn_A_output = Pipe(duplex=False)
conn_main_input, conn_B_output = Pipe(duplex=False)
a = Process(target=process_A, args=(conn_A_output, q,), daemon=True)
b = Process(target=process_B, args=(conn_B_input, conn_B_output,), daemon=True)
a.start()
b.start()
fout = open("artifacts/hard.txt", "w")
try:
    while True:
        s = sys.stdin.readline()
        print(f"time: {time.time() - time_start}, input: {s}",
              file=fout, end="")
        q.put(s)
        if not conn_main_input.poll(timeout=0):
            res = conn_main_input.recv()
            print(res, end="")
            print(
                f"time: {time.time() - time_start}, output: {res}", file=fout, end="")
except KeyboardInterrupt:
    fout.close()
