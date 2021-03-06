#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>

/* Measure creating a large file and overwriting that file */

#define WSIZE (16 * 4096)
#define FILESIZE 50 * 1024 * 1024
#define NAMESIZE 100

static char name[NAMESIZE];
static char buf[WSIZE];
static char *prog;
static char *dir;

void printstats(int reset)
{
  int fd;
  int r;

  sprintf(name, "%s/stats", dir);
  if((fd = open(name, O_RDONLY)) < 0) {
    return;
  }

  bzero(buf, WSIZE);

  if ((r = read(fd, buf, WSIZE)) < 0) {
    perror("read");
    exit(1);
  }

  if (!reset) fprintf(stdout, "=== FS Stats ===\n%s========\n", buf);

  if ((r = close(fd)) < 0) {
    perror("close");
  }
}

int makefile()
{
  int i;
  int r;
  int fd;

  int n = FILESIZE/WSIZE;
  
  sprintf(name, "%s/d/f", dir);
  if((fd = open(name, O_RDWR | O_CREAT | O_TRUNC, S_IRWXU)) < 0) {
    printf("%s: create %s failed %s\n", prog, name, strerror(errno));
    exit(1);
  }

  sprintf(buf, "%s/stats", dir);
    
  for (i = 0; i < n; i++) {
    if (write(fd, buf, WSIZE) != WSIZE) {
      printf("%s: write %s failed %s\n", prog, name, strerror(errno));
      exit(1);
    }
  }
  if (fsync(fd) < 0) {
    printf("%s: fsync %s failed %s\n", prog, name, strerror(errno));
    exit(1);
  }

  lseek(fd, SEEK_SET, 0);
  write(fd, buf, WSIZE);
  close(fd);
  
  fd = open(".", O_DIRECTORY | O_RDONLY);
  if (fd < 0) {
    perror("open dir");
    exit(-1);
  }
  if (fsync(fd) < 0) {
    perror("fsync");
    exit(-1);
  }
}

int writefile()
{
  int i;
  int r;
  int fd;

  int n = FILESIZE/WSIZE;
  
  sprintf(name, "%s/d/f", dir);
  if((fd = open(name, O_RDWR, S_IRWXU)) < 0) {
    printf("%s: open %s failed %s\n", prog, name, strerror(errno));
    exit(1);
  }
  
  sprintf(buf, "%s/stats", dir);
  
  for (i = 0; i < n; i++) {
    if (write(fd, buf, WSIZE) != WSIZE) {
      printf("%s: write %s failed %s\n", prog, name, strerror(errno));
      exit(1);
    }
    if (((i + 1) * WSIZE) % (10 * 1024 * 1024) == 0) {
      if (fsync(fd) < 0) {
	  printf("%s: fsync %s failed %s\n", prog, name, strerror(errno));
	  exit(1);
	}
    }
  }
  if ((i * WSIZE) % (10 * 1024 * 1024) != 0 && fsync(fd) < 0) {
    printf("%s: fsync %s failed %s\n", prog, name, strerror(errno));
    exit(1);
  }
  close(fd);
}

int main(int argc, char *argv[])
{
  long time;
  struct timeval before;
  struct timeval after;
  float tput;

  if (argc != 2) {
    printf("Usage: %s basedir\n", argv[0]);
    exit(-1);
  }
  
  prog = argv[0];
  dir = argv[1];
  sprintf(name, "%s/d", dir);
  if (mkdir(name,  S_IRWXU) < 0) {
    printf("%s: create %s failed %s\n", prog, name, strerror(errno));
    exit(1);
  }

  printstats(1);
    
  gettimeofday ( &before, NULL );  
  makefile();
  gettimeofday ( &after, NULL );

  time = (after.tv_sec - before.tv_sec) * 1000000 +
	(after.tv_usec - before.tv_usec);
  tput = ((float) (FILESIZE/1024) /  (time / 1000000.0));
  float mf_tput = tput;
  //printf("makefile %d MB %ld usec throughput %5.1f KB/s\n", FILESIZE/(1024*1024), time, tput);

  printstats(0);
    
  gettimeofday ( &before, NULL );  
  writefile();
  gettimeofday ( &after, NULL );
  
  time = (after.tv_sec - before.tv_sec) * 1000000 +
	(after.tv_usec - before.tv_usec);
  tput = ((float) (FILESIZE/1024) /  (time / 1000000.0));
  float wf_tput = tput;
  //printf("writefile %d MB %ld usec throughput %5.1f KB/s\n", FILESIZE/(1024*1024), time, tput);
  printf("%5.1f, %5.1f\n", mf_tput, wf_tput);

  printstats(0);

}
