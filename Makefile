# Makefile
UNAME_S := $(shell uname -s)

CC = gcc
CFLAGS = -fPIC -O2

# Detect OS and set correct shared library extension
ifeq ($(UNAME_S), Linux)
	LIB_EXT = so
endif
ifeq ($(UNAME_S), Darwin)
	LIB_EXT = dylib
endif
# For Windows (MinGW), you'd set it to dll

TARGET = pytinyfiledialogs/libtinyfiledialogs.$(LIB_EXT)

all:
	@echo "Compiling for $(UNAME_S)..."
	$(CC) -shared $(CFLAGS) src/tinyfiledialogs.c -o $(TARGET)
	@echo "Done! Binary created at $(TARGET)"

clean:
	rm -f pytinyfiledialogs/libtinyfiledialogs.*
