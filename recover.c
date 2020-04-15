#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if(f == NULL)
    {
        printf("Could not open\n");
        return 1;
    }
    unsigned char *block = malloc(512);
    int a=1;
    FILE *img;
    string filename = "";
    while(!feof(f))
    {
        fread(block, sizeof(unsigned char), 512, f);
        if(block[0]==0xff || block[1] == 0xd8 || block[2] == 0xff || (block[3] & 0xf0) == 0xe0)
        {
            sprintf(filename, "%03i.jpg", a);
            img = fopen(filename, "w");
            if(img == NULL)
            {
                printf("Could not create\n");
                return 1;
            }
            a++;
        }
        if(img!=NULL)
        {
            fwrite(block, sizeof(unsigned char), 512, img);
        }
    }
    return 0;
}
