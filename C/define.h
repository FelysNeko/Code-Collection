#define CALLOC(size, type) (type *)calloc(size, sizeof(type)); ++counter;
#define FREE(ptr) if (ptr!=NULL) {free(ptr); --counter;}
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

#define RED(msg) "\033[1;31m"msg"\033[0m\n"
#define GREEN(msg) "\033[1;32m"msg"\033[0m\n"
#define YELLOW(msg) "\033[1;33m"msg"\033[0m\n"
#define BLUE(msg) "\033[1;34m"msg"\033[0m\n"
#define MAGENTA(msg) "\033[1;35m"msg"\033[0m\n"
#define CYAN(msg) "\033[1;36m"msg"\033[0m\n"
#define WHITE(msg) "\033[1;37m"msg"\033[0m\n"


extern unsigned long counter;