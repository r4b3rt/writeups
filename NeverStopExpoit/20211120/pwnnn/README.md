# pwnnn

> author: b3ale

- environment: ubuntu 18.04 (Ubuntu GLIBC 2.27-3ubuntu1)
- vuls
  - use after free => leak libc (pwnnn.c:136)
  - index mismatch => tcache poisoning (pwnnn.c:137)
- forge `__free_hook` to `system`
- difficulties
  - reversing
  - bypass `get_xor` function

```bash
$ tree .
.
├── README.md
├── attachment
│   ├── libc.so.6_cd7c1a035d24122798d97a47a10f6e2b71d58710aecfd392375f1aa9bdde164d
│   └── pwnnn_ee7f3025cdbdc8ca19f4316c2a0b14dc32d908d4838029bd53ca8fb61c3b4529
├── exp.py
└── src
    ├── Makefile
    └── pwnnn.cc

2 directories, 6 files
```

