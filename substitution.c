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
    if (argc != 2)
    {
        printf("Usage: ./substitution key");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.");
        return 1;
    }
    bool alpha[26], flag = true;
    int i;
    for (i = 0; i < 26 ;i++)
    {
        alpha[i] = false;
    }
    for (i = 0; i < 26 ;i++)
    {
        if (number(argv[1][i]) < 0 || number(argv[1][i]) > 25)
        {
            flag = false;
            break;
        }
        if (alpha[number(argv[1][i])])
        {
            flag = false;
            break;
        }
        alpha[number(argv[1][i])] = true;
    }
    if (flag)
    {
        string text = get_string("plaintext:  ");
        printf("ciphertext: ");
        for (i = 0; i < strlen(text); i++)
        {
            if (isalpha(text[i]))
            {
                if (islower(text[i]))
                {
                    printf("%c", tolower(argv[1][number(text[i])]));
                }
                else
                {
                    printf("%c", toupper(argv[1][number(text[i])]));
                }
            }
            else
            {
                printf("%c",text[i]);
            }
        }
    }
    else
    {
       printf("Usage: ./substitution key");
       return 1;
    }
    printf("\n");
    return 0;
}