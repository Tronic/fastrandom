import os
import sys
import time
from secrets import token_bytes
from threading import Thread

# Behold the insane namespacing of the cryptography module
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES, ChaCha20

BS = 1024 * 1024
run = None
count = None
error = None

def gencrypto(chacha=False):
    global count, error, run
    key, iv = token_bytes(32), token_bytes(16)
    be = default_backend()
    cipher = Cipher(ChaCha20(key, iv), None, be) if chacha else Cipher(AES(key), modes.CTR(iv), be)
    encryptor = cipher.encryptor()
    buf = bytearray(BS + 15)
    while run:
        l = encryptor.update_into(bytes(BS), buf)
        assert l == BS
        try:
            sys.stdout.buffer.write(buf[:l])
            count += 1
        except BrokenPipeError:
            break
        except OSError as e:
            error = e
            run = False
            break

def genzero():
    global count, error, run
    buf = bytes(BS)
    while run:
        try:
            sys.stdout.buffer.write(buf)
            count += 1
        except BrokenPipeError:
            break
        except OSError as e:
            error = e
            run = False
            break

def progress():
    t = None
    while run:
        if t is None:
            t = time.perf_counter()
            oldcount = count
        time.sleep(0.01)
        if time.perf_counter() - t >= 1.0:
            speed = BS * (count - oldcount) / 1.0
            sys.stderr.write(f"\r[fastrandom] {BS * count / 1024 / 1024:10,.0f} MiB {speed / 1e9:6.2f} GB/s  ")
            t = None
    sys.stderr.write("\r")

def main():
    global count, run
    if sys.stdout.isatty():
        sys.stderr.write(
            "Usage:  fastrandom > file.dat\n"
            "        fastrandom > /dev/yourdisk\n\n"
            "    -p  Display progress indication while working.\n"
            "    -q  Suppress all messages.\n"
            "    -z  Generate zeroes instead of random.\n\n"
            "Refusing to print random binary to your terminal.\n"
        )
        sys.exit(1)

    # The thread count is half the number of CPUs to avoid hyperthreading
    # and because using more is unlikely to give any benefit but will
    # disturb other processes more.
    threads = [
        Thread(target=genzero) if '-z' in sys.argv else
        Thread(target=gencrypto, kwargs=dict(chacha=i%2))
        for i in range(os.cpu_count() // 2)
    ]

    if '-p' in sys.argv and '-q' not in sys.argv:
        threads.append(Thread(target=progress))
    run = True
    count = 0
    start = time.perf_counter()

    for t in threads:
        t.start()

    for t in threads:
        try:
            t.join()
        except KeyboardInterrupt:
            run = False
            t.join()

    t = time.perf_counter() - start

    if not "-q" in sys.argv:
        sys.stderr.write(
            f"[fastrandom] {count*BS//1024//1024:10,.0f} MiB generated at {count*BS/1e9/t:.2f} GB/s\n"
        )
        if error:
            sys.stderr.write(f"{error}\n")

if __name__ == '__main__':
    main()
