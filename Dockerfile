# docker build -t pwn .
# docker run --rm --publish=2222-2224:2222-2224 -v $PWD:/root/pwd --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -d --name pwn -i pwn
# docker exec -it pwn /bin/bash

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential curl dnsutils gcc gcc-multilib gdb gdb-multiarch git jq libc6-dev libdb-dev libffi-dev libncurses5:i386 libpcre3-dev libssl-dev libstdc++6:i386 libxaw7-dev libxt-dev ltrace make net-tools netcat procps python python3 python3-dev python3-pip rubygems socat strace tmux tree vim wget wget zsh

RUN pip3 install capstone capstone keystone-engine pwntools pwntools r2pipe requests ropper unicorn

RUN mkdir /root/tools
WORKDIR /root/tools

RUN git clone https://github.com/JonathanSalwan/ROPgadget
#RUN git clone https://github.com/radare/radare2 && cd radare2 && sys/install.sh
#RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && git checkout stable && ./setup.sh
RUN git clone https://github.com/niklasb/libc-database && cd libc-database && ./get ubuntu debian

RUN gem install one_gadget

ADD jeopardy/run.py run.py

WORKDIR /root
