#include <iostream>
#include <string>
#include <unistd.h>
#include <string.h>

using namespace std;

string menu = "\
+-------------+\n\
|  1. add     |\n\
|  2. remove  |\n\
|  3. show    |\n\
|  4. flip    |\n\
|  5. exit    |\n\
+-------------+\
";

struct chunk {
    unsigned int magic_1;
    unsigned int magic_2;
    char * buf;
};

struct buffer {
    int idx_1;
    int idx_2;
    int counter;
    bool flipper;
    struct chunk * data;
};

struct buffer * object;

bool is_delete[0x80];

int read_int() {
    char buf[0x10];
    read(0, buf, 0x10);
    return atoi(buf);
}

int read_str(char * buf, int len) {
    return read(0, buf, len);
}

int cal_idx(char * buf, int len) {
    int r = 0;
    for (int i = 0; i < len; i++) {
        r += (buf[i] & 0xff);
    }
    return abs(r) % 0x80;
}

int get_idx() {
    if (object->flipper) {
        return object->idx_1;
    } else {
        return object->idx_2;
    }
}

unsigned int get_xor(char * buf, int type) {
    unsigned int r = 0;
    //cout << buf << endl;
    for (int i = 0; i < 4; i++) {
        if (type == 1) {
            r += (buf[i] & 0xff) << (8 * i);
            //printf("0x%x => 0x%x\n", buf[i] & 0xff, r);
        } else {
            r += (buf[i + 4] & 0xff) << (8 * i);
            //printf("0x%x => 0x%x\n", buf[i + 4] & 0xff, r);
        }
    }
    if (type == 1) {
        return r ^ 0xcafebabe;
    } else {
        return r ^ 0xdeadbeef;
    }
}

void init_object() {
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    object = (struct buffer *) malloc(sizeof(struct buffer));
    object->idx_1 = 0;
    object->idx_2 = 0;
    object->counter = 0;
    object->flipper = true;
    object->data = (struct chunk *) malloc(0x7e8);
    memset(is_delete, true, sizeof(is_delete));
}

bool is_overflow() {
    if (object->counter < 0 && object->counter >= 0x7f) {
        return true;
    } else {
        return false;
    }
}

void add() {
    char buf[0x100];
    int idx, len;
    char * temp_buf;
    if (is_overflow()) {
        cout << "index overflow" << endl;
        exit(-1);
    }
    len = read_str(buf, 0x100);
    if (object->flipper) {
        object->idx_1 = cal_idx(buf, len);
        idx = object->idx_1;
    } else {
        object->idx_2 = cal_idx(buf, len);
        idx = object->idx_2;
    }
    // idx can be change
    //cout << "idx = " << idx << endl;
    //cout << "is_delete = " << is_delete[idx] << endl;
    if (!object->data[idx].buf || is_delete[idx]) {
        temp_buf = (char *) malloc(0x100);
        memcpy(temp_buf, buf, len);
        object->data[idx].magic_1 = get_xor(temp_buf, 1);
        object->data[idx].magic_2 = get_xor(temp_buf, 2);
        object->data[idx].buf = temp_buf;
        object->counter++;
        is_delete[idx] = false;
    }
}

void remove() {
    int idx = get_idx();
    if (object->flipper) {
        while (object->data[idx].buf && idx >= 0 && idx < 0x80) {
            free(object->data[idx].buf); // uaf
            is_delete[--idx] = true; // idx mismatch
        }
    } else {
        while (object->data[idx].buf && idx >= 0 && idx < 0x80) {
            free(object->data[idx].buf);
            is_delete[++idx] = true;
        }
    }
    object->counter--;
}

void show() {
    int idx = get_idx();
    puts(object->data[idx].buf);
}

void flip() {
    if (object->flipper) {
        object->flipper = false;
    } else {
        object->flipper = true;
    }
}

int main() {
    int c;
    init_object();
    while(1) {
        cout << menu << endl;
        cout << ">> ";
        c = read_int();
        switch(c) {
            case 1:
                add();
                break;
            case 2:
                remove();
                break;
            case 3:
                show();
                break;
            case 4:
                flip();
                break;
            case 5:
                exit(0);
            default:
                cerr << "[!] invalid input" << endl;
                exit(-1);
        }
    }
}
