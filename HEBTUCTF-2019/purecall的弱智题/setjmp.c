#include <stdio.h>
#include <signal.h>
#include <setjmp.h>
#include <unistd.h>
#include <sys/time.h>
sigjmp_buf jmp_env;

static void connect_alarm(int time)
{
    siglongjmp(jmp_env, 1);
}

int main()
{
    // 当超时时间sec_timeout大于等于运行时间run_time时会跳过printf("running...\n");
    int sec_timeout = 3;
    int run_time = 2;

    printf("timeout = %d, run time = %d\n", sec_timeout, run_time);
    if (sec_timeout)
    {
        // 超过用alarm函数设置的时间时产生此信号，调用connect_alarm函数
        signal(SIGALRM, connect_alarm);
        alarm(sec_timeout);
        printf("set timeout\n");
        if (sigsetjmp(jmp_env, 1))
        {
            printf("timeout\n");
            goto out;
        }
    }

    sleep(run_time);
    printf("running...\n");

out:
    if (sec_timeout)
    {
        // 取消先前设置的闹钟
        alarm(0);
        printf("cancel timeout\n");
    }

    return 0;
}
