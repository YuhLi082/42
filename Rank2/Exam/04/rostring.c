/*Assignment name  : rostring
Expected files   : rostring.c
Allowed functions: write, malloc, free
--------------------------------------------------------------------------------

Write a program that takes a string and displays this string after rotating it
one word to the left.

Thus, the first word becomes the last, and others stay in the same order.

A "word" is defined as a part of a string delimited either by spaces/tabs, or
by the start/end of the string.

Words will be separated by only one space in the output.

If there's less than one argument, the program displays \n.

Example:

$>./rostring "abc   " | cat -e
abc$
$>
$>./rostring "Que la      lumiere soit et la lumiere fut"
la lumiere soit et la lumiere fut Que
$>
$>./rostring "     AkjhZ zLKIJz , 23y"
zLKIJz , 23y AkjhZ
$>
$>./rostring "first" "2" "11000000"
first
$>
$>./rostring | cat -e
$
$>*/


int is_space(char c)
{
    return(c == ' ' || c== '\t');
}

void print_test(char *str, int i)







#include <unistd.h>

int is_sep(char c)
{
    return (c == ' ' || c == '\t');
}

int main(int argc, char **argv)
{
    int i;
    int start;
    int end;

    if (argc == 2)
    {
        i = 0;
        while (is_sep(argv[1][i]))
            i++;
        start = i;
        while (argv[1][i] && !is_sep(argv[1][i]))
            i++;
        end = i;
        while (argv[1][i])
        {
            while (is_sep(argv[1][i]))
                i++;
            if (argv[1][i])
            {
                while (argv[1][i] && !is_sep(argv[1][i]))
                    write(1, &argv[1][i++], 1);
                write(1, " ", 1);
            }
        }
        while (start < end)
            write(1, &argv[1][start++], 1);
    }
    write(1, "\n", 1);
    return 0;
}

