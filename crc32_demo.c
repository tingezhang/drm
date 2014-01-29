/**
 * gcc crc32_demo.c -lz -o crc32_demo
 */
#include <zlib.h>
#include "stdio.h"
#include "stdlib.h"

void DumpHex(unsigned char* label, unsigned char* buf, int len)
{
    int idx = 0;
    printf("===========================================\n");
    printf("            dump :%s\n", label);

    for (idx = 0 ; idx < len ; idx++)
    {
        printf("%#.2x", buf[idx]);
        if (0 == (idx + 1) % 16)
            printf("\n");
        else
            printf(",");
    }
    printf("===========================================\n");
}

#define USAGE() \
    printf("%s,%d usage ========\n", __FUNCTION__, __LINE__); \
    printf("%s filecrc\n", argv[0]);


int main(int argc, char** argv)
{
    uLong crc;
    FILE *pInFile = NULL;
    unsigned char buf[1024];
    int len = 0;

    if(2 != argc)
    {
        USAGE();
        exit(1);
    }

    pInFile = fopen(argv[1],"rb");

    if (NULL == pInFile)
    {
        USAGE();
        exit(2);
    }

    crc = crc32(0L, Z_NULL, 0);

    while((len = fread(buf, 1, 1024, pInFile)) > 0)
    {
        if(0x0A == buf[len -1])
        {
            printf("end of 0x0A");
            len -= 1;
        }
        printf("%s,%d, buf len:%d\n", __FUNCTION__, __LINE__, len);
        crc = crc32(crc, buf, len);
    }
    DumpHex("crc", (unsigned char*)&crc, sizeof(uLong));
    if (NULL != pInFile)
    {
        fclose(pInFile);
        pInFile = NULL;
    }
}
