#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>

#include <time.h>
#include <unistd.h>

int main() {
	pid_t pid;
	time_t t;

	if ((pid = fork()) < 0) {
		perror("fork");
		exit(-1);
	} else if (pid > 0) {
		exit(0);
	}	
	
	if (setsid() < 0) {
		perror("setsid");
		exit(0);
	}

	chdir("/");

	if (umask(0) < 0) {
		perror("unmask");
		exit(0);
	}		

  while(1) {
    time_t now = time(NULL);
    struct tm tm_now;
    localtime_r(&now, &tm_now);
    char buff[100];
    strftime(buff, sizeof(buff), "%H:%M", &tm_now);
    if (!strcmp(buff, "02:25")) {
      if ((pid = fork()) < 0) {
        perror("fork");
        exit(-1);
      } else if (pid > 0) {
        sleep(100);
      } else {
        worker();
      }
    }
    sleep(10);
  }

	return 0;
}

void worker() {
	if (execl("/bin/sh", "sh", "/root/magazines_spider/run.sh",  NULL) < 0) {
		printf("execl error!\n");	
	}
	return ;
}	
