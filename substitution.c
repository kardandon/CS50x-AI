#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int number(char a){
    if (a >= 'A' && a <= 'Z')
    {
        a -= 'A';
    }
    else
    {
        a -= 'a';
    }
    return a;
}
int main(int argc, char* argv[])
{
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.");
    }
    else
    {
        string text = get_string("plaintext:  ");
        int i;
        printf("ciphertext: ");
        for (i = 0; i < strlen(text); i++)
        {
            if (isalpha(text[i]))
            {
                printf("%c", argv[1][number(text[i])]);
            }
            else
            {
                printf("%c",text[i]);
            }
        }
    }
    printf("\n");
    return 0;
}