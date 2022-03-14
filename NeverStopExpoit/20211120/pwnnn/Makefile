SOURCE  := $(wildcard *.c) $(wildcard *.cc)
OBJS    := $(patsubst %.c,%.o,$(patsubst %.cc,%.o,$(SOURCE)))

TARGET	:= pwnnn
CC		:= g++
LIBS	:=
LDFLAGS	:=
DEFINES	:=
INCLUDE	:= -I.
CFLAGS	:= -O3 -fno-stack-protector -z now -fpie -pie

.PHONY: everything objs clean veryclean rebuild

everything: $(TARGET)

all: $(TARGET)

rebuild: clean everything

clean:
	rm -rf *.so *.o $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS) $(LIBS)
	strip $@
