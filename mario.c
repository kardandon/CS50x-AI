#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n, i, j;
    do
    {
        n = get_int("Height: ");
    }
    while (!(n > 0 && n < 9));
    for (i = 0; i < n; i++)
    {
        for (j = n - i - 1; j > 0; j--)
        {
            printf(" ");
        }
        for (j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }

    return 0;
}
