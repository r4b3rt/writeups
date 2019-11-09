#include <windows.h> 
#include<stdio.h>
#include <winnt.h> 
#include <stdlib.h>
#include <tlhelp32.h>
////////////////////////////////////////////////////////////////////////////////
//使用tls 回调函数
//使用TLS 的宏
#pragma comment(linker, "/INCLUDE:__tls_used")
void lookupprocess()
{
	PROCESSENTRY32 pe32;
	pe32.dwSize = sizeof(pe32);
	HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0); // 在快照中包含系统中所有的进程
	BOOL bMore = Process32First(hProcessSnap, &pe32); // 获得第一个进程的句柄
	while (bMore)
	{
		_wcslwr_s(pe32.szExeFile, wcslen(pe32.szExeFile)+1);
		if (!wcscmp(pe32.szExeFile, L"ollyice.exe"))
		{
			printf("///////WARNING///////\n");
			exit(0);
		}
		if (!wcscmp(pe32.szExeFile, L"ollydbg.exe"))
		{
			printf("///////\nWARNING\n///////\n");
			exit(0);
		}
		if (!wcscmp(pe32.szExeFile, L"peid.exe"))
		{
			printf("///////\nWARNING\n///////\n");
			exit(0);
		}
		if (!wcscmp(pe32.szExeFile, L"ida.exe"))
		{
			printf("///////\nWARNING\n///////\n");
			exit(0);
		}
		if (!wcscmp(pe32.szExeFile, L"idaq.exe"))
		{
			printf("///////\nWARNING\n///////\n");
			exit(0);
		}
		bMore = Process32Next(hProcessSnap, &pe32); // 获取下一个进程的句柄
	}
	CloseHandle(hProcessSnap);
}
void Debugger(void) {
	int result = 0;
	__asm {
		mov eax, dword ptr fs:[30h]//TEB偏移30H处
		movzx eax, byte ptr ds:[eax + 2h]//取PEB中BeingDebug，若为1则被调试
		mov result, eax
	}
	if (result) {
		printf("///////\nWARNING\n///////\n");
		exit(0);
	}
}
void NTAPI tls_callback(PVOID h, DWORD reason, PVOID pv)
{
	lookupprocess();
	Debugger();
	//MessageBox(NULL, L"Not_Main_this_is_tls!", L"tls", MB_OK);
	return;
}
#pragma data_seg(".CRT$XLB")
PIMAGE_TLS_CALLBACK p_thread_callback[] = { tls_callback, 0 };
#pragma data_seg()
////////////////////////////////////////////////////////////////////////////////

char *table="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm";
char *secret="\x54\x4f\x69\x5a\x69\x5a\x74\x4f\x72\x59\x61\x54\x6f\x55\x77\x50\x6e\x54\x6f\x42\x73\x4f\x61\x4f\x61\x70\x73\x79\x53";

static int number=29;
HANDLE Mutex;
char flag[50];
char key[50];
void ck1()
{
	int i;
	for(i=0;i<29;i++)
	{
		if(flag[i]!=secret[i])
		{
			exit(0);
		}
	}
	printf("\nflag{%s}\n\n",key);
}
void ck2(char *enc,int i)
{	
	char k;
	k=enc[i];
	__asm{
		push eax
		xor eax,eax
		jz	betamao
		add esp,8
	   betamao:
		pop eax
	}
	if(k>='a'&&k<='z'||k>='A'&&k<='Z')
	{
		if(k>='a'&&k<='z')
		{
			enc[i]=table[enc[i]-'a'+1];
		}else
		{
			enc[i]=table[enc[i]-'A'+27];
		}
	}else
	{
		exit(0);
	}

}

DWORD WINAPI ThreadOne(LPVOID lpParameter)
{
    while(1)
    {
        //等待互斥对象有多有权才返回 
        WaitForSingleObject(Mutex,INFINITE);  
        if(number>-1)
        {
            ck2(flag,number);
            number--;
            Sleep(100);        
        }
        //释放互斥对象所有权 
        ReleaseMutex(Mutex);    
    }
    return 0;
}
DWORD WINAPI ThreadTwo(LPVOID lpParameter)
{
    while(1)
    {
        WaitForSingleObject(Mutex,INFINITE);
        if(number>-1)
        {
            Sleep(100);
            number--;
        }
        ReleaseMutex(Mutex);
    }
    return 0;
}
void print0()
{
	    printf(
		"1111111111111111111111111111111111111111111111111111111111111111111111111111111\n"
		"*******************************************************************************\n"
		"**************             ****************************************************\n"
		"**************   ********   *********************                 *************\n"
		"**************   *********  *********************   ***************************\n"
		"**************   *********  *********************   ***************************\n"
		"**************   *********  *********************   ***************************\n"
		"**************   *******   **********************   ***************************\n"
		"**************   ****   *************************   ***************************\n"
		"**************   *    ***************************                **************\n"
		"**************   ***    *************************   ***************************\n"
		"**************   ******   ***********************   ***************************\n"
		"**************   ********   *********************   ***************************\n"
		"**************   **********   *******************   ***************************\n"
		"**************   ***********    *****************                 *************\n"
		"*******************************************************************************\n"
		"1111111111111111111111111111111111111111111111111111111111111111111111111111111\n"
		);
	printf("input flag:\n");
	scanf("%36s",flag);
}

int main()
{

	//flag{ThisisthreadofwindowshahaIsESE}
	print0();

    HANDLE HOne,HTwo;
    Mutex=CreateMutex(NULL,FALSE,NULL);
	strcpy(key,flag);
    HOne=CreateThread(NULL,0,ThreadOne,NULL,0,NULL);
    HTwo=CreateThread(NULL,0,ThreadTwo,NULL,0,NULL);
    CloseHandle(HOne);
    CloseHandle(HTwo);
    while(TRUE)
    {
        if(number==-1)
        {
            ck1();
            CloseHandle(Mutex);
            return 0;
        }
        else
        {
            continue;
        }    
    }

//  	MessageBox(NULL,L"Congratulation!!!!",L"wking",MB_OK); 
	return 0; 
}