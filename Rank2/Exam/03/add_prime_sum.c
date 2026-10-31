/*Assignment name  : add_prime_sum
Expected files   : add_prime_sum.c
Allowed functions: write, exit
--------------------------------------------------------------------------------

Write a program that takes a positive integer as argument and displays the sum
of all prime numbers inferior or equal to it followed by a newline.

If the number of arguments is not 1, or the argument is not a positive number,
just display 0 followed by a newline.

Yes, the examples are right.

Examples:

$>./add_prime_sum 5
10
$>./add_prime_sum 7 | cat -e
17$
$>./add_prime_sum | cat -e
0$
$>*/





































int ft_atoi(char *str)
{
    int i;
    int result;
    int sign;
    i = 0;
    sign = 1;
    result = 0;
    while(str[i] == ' ' || (str[i] >= 9 && str[i] <= 13))
       i++;
    if(str[i] == '+' || str[i] == '-')
    {
        if(str[i] == '-')
            sign = -1;
        i++;
    }
    while(str[i] >= '0' && str[i] <= '9')
    {
        result = result * 10 + (str[i] - '0');
        i++;
    }
    return (sign *result);
}

void ft_num(int c)
{
    char i;

    if(c > 9)
       ft_num(c / 10);
    i = c % 10 + '0';
    write(1, &i, 1);
}

int is_prime(int c)
{
    int i;
    i = 2;
    if(c < 2)
        return 0;
    while(i < c)
    {
        if(c % i == 0)
            return 0;
        i++;
    }
    return 1;
}

int main(int argc, char**argv)
{
    int n;
    int sum;
    int i;

    if(argc != 2)
    {
        write(1, "0\n", 2);
        return 0;
    }
    n = ft_atoi(argv[1]);
    sum = 0;
    i = 2;
    while(i <= n)
    {
        if(is_prime(i))
            sum += i;
        i++;
    }
    ft_num(sum);
    write(1, "\n", 1);
	return (0);
}
