FLAGS = -Wextra -Wall -Wconversion -std=c11 -Werror -D_XOPEN_SOURCE=700
DBG_FLAGS = -g -DDEBUG

.PHONY: all

all: libreuse.so

.PHONY: clean

clean:
	rm -f *.o *.so

%.o: %.c
	gcc -c $(FLAGS) $? -o $@

libreuse.o: libreuse.c
	gcc -fPIC -c $(FLAGS) $? -o $@

libreuse.so: libreuse.o
	gcc -shared $(FLAGS) -o $@ $? -ldl
