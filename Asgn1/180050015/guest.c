#include <stddef.h>
#include <stdint.h>
// #include <fcntl.h>

#define O_ACCMODE 0003
#define O_RDONLY 00
#define O_WRONLY 01
#define O_RDWR 02
#define O_CREAT 0100
#define O_EXCL 0200
#define O_NOCTTY 0400
#define O_TRUNC 01000
#define O_APPEND 02000
#define O_NONBLOCK 04000
#define O_SYNC 04010000
#define O_ASYNC 020000
#define SEEK_SET 0 /* Seek from beginning of file.  */
#define SEEK_CUR 1 /* Seek from current position.  */
#define SEEK_END 2 /* Seek from end of file.  */

typedef unsigned int mode_t;
typedef long off_t;

static void outb(uint16_t port, uint8_t value) {
	asm("outb %0,%1" : /* empty */ : "a" (value), "Nd" (port) : "memory");
}

static inline void outb2(uint16_t port, uint32_t value)
{
	asm("out %0,%1"
		: /* empty */
		: "a"(value), "Nd"(port)
		: "memory");
}

void printVal(uint32_t val)
{
	outb2(0xEA, val);
}

static inline uint32_t inb(uint16_t port)
{
	uint32_t ret;
	asm("in %1, %0"
		: "=a"(ret)
		: "Nd"(port)
		: "memory");
	return ret;
}

uint32_t getNumExits()
{
	return inb(0xEB);
}

void display(const char* str)
{
	outb2(0xEC, (uintptr_t)str);
}

//Filesystem hypercalls-----------------------

struct open_query
{
	int flags;
	int fd;
	int mode_present;
	mode_t mode;
	const char *pathname;
};

struct write_query
{
	int fd;
	size_t count;
	size_t ret_val;
	const void *buf;
};

struct close_query
{
	int fd;
	int ret_val;
};

struct read_query
{
	int fd;
	size_t count;
	size_t ret_val;
	void *buf;
};

struct seek_query
{
	int fd;
	off_t offset;
	int whence;
	off_t ret_val;
};

int open(const char* pathname, int flags)
{
	struct open_query q;
	q.flags = flags;
	q.pathname = pathname;
	q.mode_present = 0;
	q.mode = 0;
	outb2(0xED, (uintptr_t)&q);
	return q.fd;
}

int openc(const char *pathname, int flags, mode_t mode)
{
	struct open_query q;
	q.flags = flags;
	q.pathname = pathname;
	q.mode_present = 1;
	q.mode = mode;
	outb2(0xED, (uintptr_t)&q);
	return q.fd;
}


size_t write(int fd, const void* buf, size_t count)
{
	struct write_query q;
	q.fd = fd;
	q.count = count;
	q.buf = buf;
	outb2(0xEF, (uintptr_t)&q);
	return q.ret_val;
}

int close(int fd)
{
	struct close_query q;
	q.fd = fd;
	outb2(0xEE, (uintptr_t)&q);
	return q.ret_val;
}


size_t read(int fd, void *buf, size_t count)
{
	struct read_query q;
	q.fd = fd;
	q.count = count;
	q.buf = buf;
	outb2(0xF0, (uintptr_t)&q);
	return q.ret_val;
}

off_t lseek(int fd, off_t offset, int whence)
{
	struct seek_query q;
	q.fd = fd;
	q.offset = offset;
	q.whence = whence;
	outb2(0xF1, (uintptr_t)&q);
	return q.ret_val;
}

void
	__attribute__((noreturn))
	__attribute__((section(".start")))
	_start(void)
{

	const char *p;

	for (p = "Hello, world!\n"; *p; ++p)
		outb(0xE9, *p);

	// printVal(430);

	uint32_t numExits = getNumExits();
	printVal(numExits);

	display("Hello world!\n");

	numExits = getNumExits();
	printVal(numExits);

	int fd = openc("./foo.txt", O_RDWR | O_CREAT, 777);
	write(fd, "Hi there\n", 9);

	int fd2 = open("./foo.txt", O_RDONLY);
	lseek(fd2, 2, SEEK_SET);
	char c[100];
	read(fd2, c, 7);

	display(c);

	close(fd);

	* (long *)0x400 = 42;

	for (;;)
		asm("hlt" : /* empty */ : "a" (42) : "memory");
}
