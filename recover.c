#include <stdio.h>
#include <stdlib.h>



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
    unsigned char block[512];
    short a = 0;
    FILE *img = NULL;
    char filename[8] = "0000.jpg";
    while (fread(&block, 512, 1, f) == 1)
    {

        if(block[0]==0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
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
        if(img != NULL)
        {
            fwrite(&block, 512, 1, img);
        }
    }
    fclose(f);
    fclose(img);
    return 0;
}
