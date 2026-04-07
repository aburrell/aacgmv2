#
# $Id: Makefile,v 1.6 2007/02/26 19:49:42 burrell Exp $
#
# Makefile for building the AACGMV2 test function.

CC        = $(COMPILERS)/bin/gcc
AAGCM_DIR = $(GITDIR)/aacgmv2/c_aacgmv2

INCDIRS  = -I./ -I$(AAGCM_DIR)/include
CFLAGS   = -g
LDFLAGS  = -lm

AACGM_SRC =	aacgmlib_v2.c \
		astalglib.c \
		igrflib.c \
		mlt_v2.c \
		rtime.c

AACGM_OBJ = $(AACGM_SRC:.c=.o)

all: test_aacgm

test_aacgm: test_aacgm.o $(AACGM_OBJ)
	$(CC) $(CFLAGS) -o test_aacgm test_aacgm.o $(AACGM_OBJ) $(LDFLAGS)

clean:
	rm -f test_aacgm.o $(AACGM_OBJ) test_aacgm 
	rm -rf test_aacgm.dSYM

install_test: 
	chmod 755 test_aacgm
	mv test_aacgm ../
	rm -f test_aacgm.o $(AACGM_OBJ)

#
# rules for compilation
#

.f.a:
	$(F77) $(FFLAGS) -c `pwd`/$<
.f.o:
	$(F77) $(FFLAGS) -c `pwd`/$<

.c.a:
	$(CC) $(CFLAGS) $(INCDIRS) -c `pwd`/$<
.c.o:
	$(CC) $(CFLAGS) $(INCDIRS) -c `pwd`/$<




