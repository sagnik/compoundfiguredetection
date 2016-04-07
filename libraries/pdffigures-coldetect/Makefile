CC=g++ -std=c++11

UNAME := $(shell uname)
ifeq ($(UNAME),Linux)
# The older version of lepontica that is in the Debian package does not have 
# pkg-config setup so we need to add it in manually, this setting will work 
# if leptonica was installed with apt-get
## pkg-config --cflags lept works for leptonica on my Ubuntu 15.10. Try the command `pkg-config --cflags lept`
## on your machine. If you don't see something like -I/usr/include/leptonica or /usr/leptonica
## you might need to change the command `pkg-config --cflags lept` to -I/usr/include/leptonica or
## wherever you have the leptonica header files.

	LIBS=`pkg-config --libs poppler` -llept
	CFLAGS=-c -Wall `pkg-config --cflags poppler` `pkg-config --cflags lept`
        #LIBS= -lpoppler -llept
        #CFLAGS=-c -Wall -I/usr/include/poppler/ -I/usr/local/include/leptonica/
else
	LIBS=`pkg-config --libs poppler lept`
	CFLAGS=-c -Wall `pkg-config --cflags poppler lept`
endif

DEBUG_FLAGS=-g
RELEASE_FLAGS=-g -O3

DEBUG =? 0
ifeq (0, $(DEBUG))
	CFLAGS += $(RELEASE_FLAGS)
else
	CFLAGS += $(DEBUG_FLAGS)
endif

OBJECTS=PDFUtils.o TextUtils.o ExtractCaptions.o BuildCaptions.o ExtractRegions.o ExtractFigures.o pdffigures.o

pdffigures: $(OBJECTS)
	$(CC) -o pdffigures $(OBJECTS) $(LIBS)

.cpp.o:
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *o pdffigures
