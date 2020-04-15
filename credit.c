#include <cs50.h>
#include <stdio.h>

int digitsum(int n){
    int m=0;
    while (n!=0)
    {
        m += n % 10;
        n /= 10;
    }
    return m;
}
int poweroftwo(bool n){
    return n ? 2 : 1;
}
string what_is_it(long m){
    int count = 0;
    string result;
    while (m >= 100)
    {
        count++;
        m /=10;
    }
    count +=2;
    if (count == 15 && (m == 34 || m == 37))
    {
        result = "AMERICAN EXPRESS";
    }
    else if (count == 16 && (m == 51 || m == 52 || m == 53 || m == 54 || m == 55))
    {
        result = "MASTERCARD";
    }
    else if ((count == 13 || count == 16) && (m / 10) == 4){
        result = "VISA";
    }
    else 
    {
        result = "INVALID";
    }
    return result;
}
int main(void)
{
    long n;
    bool m=0;
    int z = 0;
    string result;
    do
    {
        n = get_long("Number: ");
    }
    while (!(n > 0));
    result = what_is_it(n);
    while (n > 0)
    {
        z += digitsum(n % 10 * poweroftwo(m));
        n /= 10;
        m = !m;
    }
    if (z % 10 == 0)
    {
        printf("%s\n" ,result);
    }
    else 
    {
        printf("INVALID\n");
    }
    return 0;
}
