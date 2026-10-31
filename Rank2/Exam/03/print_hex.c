/*Assignment name  : print_hex
Expected files   : print_hex.c
Allowed functions: write
--------------------------------------------------------------------------------

Write a program that takes a positive (or zero) number expressed in base 10,
and displays it in base 16 (lowercase letters) followed by a newline.

If the number of parameters is not 1, the program displays a newline.

Examples:

$> ./print_hex "10" | cat -e
a$
$> ./print_hex "255" | cat -e
ff$
$> ./print_hex "5156454" | cat -e
4eae66$
$> ./print_hex | cat -e
$
*/
































void print_hex(unsigned long n)
{
    char *base;
	char c;
	base = "0123456789abcdef";
	if(n > 15)
	    print_hex(n / 16);
	c = base[n % 16];
	write(1, &c, 1);
}


int main(int argc, char**argv)
{
	unsigned long n;
	int i;
	if(argc == 2)
	{
		n = 0;
		i = 0;
		while(argv[1][i] >= '0' && argv[1][i] <= '9')
		{
			n = n * 10 + (argv[1][i] - '0');
			i++;
		}
		print_hex(n);
	}
	write(1, "\n", 1);
	return 0;
}

