#include <cs50.h>
#include <stdio.h>

int main(void)
{
    float m;
    int num = 0;
    do
    {
        m = get_float("Change owed: ");
    }
    while (!(m > 0));
    int n = round(m * 100);
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
