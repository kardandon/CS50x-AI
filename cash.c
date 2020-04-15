#include <cs50.h>
#include <stdio.h>

int main(void)
{
    float n;
    int num = 0;
    do
    {
        n = get_float("Change owed: ");
    }
    while (!(n > 0));
    n *= 100;
    while (n != 0)
    {
        if (n >= 25)
        {
            n -= 25;
            num++;
        }
        else if (n >= 10)
        {
            n -= 10;
            num++;
        }
        else if (n >= 5)
        {
            n -= 5;
            num++;
        }
        else if (n >= 1)
        {
            n -= 1;
            num++;
        }
    }
    printf("%d\n", num);
    return 0;
}
