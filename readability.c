#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    int L = 0, S = 0, W = 0, i;
    string text;
    text = get_string("Text: ");
    for (i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            L++;
        }
        else if (isspace(text[i]))
        {
            W++;
            while (isspace(text[i]))
            {
                i++;
            }
            i--;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            S++;
        }
    }
    W++;
    int z = round(0.0588 * L / W * 100 - 0.296 * S / W * 100 - 15.8) > 16 ? 17 : round(0.0588 * L / W * 100 - 0.296 * S / W * 100 -
            15.8);
    if (z == 17)
    {
        printf("Grade 16+\n");
    }
    else if (z >= 1)
    {
        printf("Grade %d\n", z);
    }
    else
    {
        printf("Before Grade 1\n");
    }
    return 0;
}

