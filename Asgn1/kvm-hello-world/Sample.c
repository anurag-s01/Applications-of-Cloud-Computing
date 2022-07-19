#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <string.h>
#include <stdint.h>
#include <linux/kvm.h>

int main()
{
    int fd = open("foo.txt",  O_CREAT | O_RDWR, 0);
    // // printf("%d\n", O_CREAT);
    // char *c = (char *)malloc(sizeof(char) * 100);
    // read(fd, c, 10);
    // printf("%s\n", c);
    // close(fd);

    char c = 80;
    printf("%p\n", &c);
}