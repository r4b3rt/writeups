FROM ubuntu:jammy
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update && apt-get install -y xinetd 
RUN useradd -m ctf
COPY ./pwn /pwn/pwn
COPY ./flag /pwn/flag
COPY ./ctf.xinetd /etc/xinetd.d/ctf
RUN chown root:ctf /pwn/pwn && chmod 750 /pwn/pwn
RUN echo 'ctf - nproc 1500' >>/etc/security/limits.conf

CMD exec /bin/bash -c "/etc/init.d/xinetd start; trap : TERM INT; sleep infinity & wait"

EXPOSE 9999
