# onlyone

> author: b3ale

- environment: ubuntu 16.04 (Ubuntu GLIBC 2.23-0ubuntu11.3)
- vuls
    - use after free => leak libc
    - unsorted bin attack => overwrite `global_max_fast`
- exploit
    - forge `__free_hook` to `setcontext+0x35` (orw)
- difficulties
    - reversing (junk code in `main`, cannot `f5` directly)
    - bypass the magic number
    - find the fake chunk (0x200) at `&__free_hook-0x59` (set by `_IO_list_all_stamp`)

```bash
$ tree .
.
├── Makefile
├── README.md
├── attachment
│   ├── libc.so.6_926ee3653de7b71c8567061f3a4dfbc2ea91b6df2b49a05f11351fe1addf20cf
│   └── onlyone_c5115116e610082059c405814bc7ea8732cfee4dbf180604fedb770b729a824a
├── deploy
│   ├── Dockerfile
│   ├── bin
│   │   ├── flag
│   │   ├── libc.so.6
│   │   └── pwn
│   ├── ctf.xinetd
│   ├── deploy.sh
│   ├── ld-linux-x86-64.so.2
│   └── start.sh
├── exp.py
└── onlyone.c

3 directories, 14 files
```

