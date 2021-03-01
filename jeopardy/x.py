#!/usr/bin/env python
"""Exploit script template."""
import subprocess
import sys

from pwn import *

context.log_level = 'info'
#context.terminal = ['tmux', 'splitw', '-p', '75']
#context.aslr = False

BINARY = './binary'
LIB = './libc.so'
HOST = 'example.com'
PORT = 1337

GDB_COMMANDS = ['b main']


def read(p, addr):
    """Some helper function."""
    prog = log.progress(f'Start reading .. ({addr})')
    log.info('Doing progress')
    value = p.read()
    prog.success()
    return value


def exploit(p, mode, libc):
    """Exploit goes here."""
    p.interactive()


def main():
    """Does general setup and calls exploit."""
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <mode>')
        sys.exit(0)

    try:
        context.binary = ELF(BINARY)
    except IOError:
        print(f'Failed to load binary ({BINARY})')

    libc = None
    try:
        libc = ELF(LIB)
        env = os.environ.copy()
        env['LD_PRELOAD'] = LIB
    except IOError:
        print(f'Failed to load library ({LIB})')

    mode = sys.argv[1]

    #if mode == 'local':
    #    p = process(BINARY, env=env)
    #elif mode == 'debug':
    #    p = gdb.debug(args=BINARY, gdbscript='\n'.join(GDB_COMMANDS), env=env)

    if mode == 'local':
        p = remote('pwn.local', 2222)
    elif mode == 'debug':
        p = remote('pwn.local', 2223)
        gdb_cmd = [
            'tmux',
            'split-window',
            '-p',
            '75',
            'gdb',
            '-ex',
            'target remote pwn.local:2224',
        ]

        for cmd in GDB_COMMANDS:
            gdb_cmd.append('-ex')
            gdb_cmd.append(cmd)

        gdb_cmd.append(BINARY)

        subprocess.Popen(gdb_cmd)

    elif mode == 'remote':
        p = remote(HOST, PORT)
    elif mode == 'ssh':
        ssh_connection = ssh(host=HOST,
                             user='username',
                             port=1337,
                             password='password')
        p = ssh_connection.process('/path/to/binary', shell=True)
    else:
        print('Invalid mode')
        sys.exit(1)

    exploit(p, mode, libc)

if __name__ == '__main__':

    main()
