/*
Assignment name  : ft_itoa
Expected files   : ft_itoa.c
Allowed functions: malloc
--------------------------------------------------------------------------------

Write a function that takes an int and converts it to a null-terminated string.
The function returns the result in a char array that you must allocate.

Your function must be declared as follows:

char	*ft_itoa(int nbr);
*/





































int ft_len(int i)
{
    int len;
    len = 0;

    if(i <= 0)
       len++;
    while(i)
    {
        i /= 10;
        len++;
    }
    return len;
}

char    *ft_itoa(int nbr)
{
    long n;
    int len;
    char *str;

    n = nbr;
    len = ft_len(n);
    str = malloc(len + 1);
    if (!str)
        return (NULL);

    str[len] = '\0';
    if (n == 0)
        str[0] = '0';
    if (n < 0)
    {
        str[0] = '-';
        n = -n;
    }
    while (n > 0)
    {
        str[--len] = n % 10 + '0';
        n /= 10;
    }
    return (str);
}
