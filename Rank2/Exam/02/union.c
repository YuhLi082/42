/*Assignment name  : union
Expected files   : union.c
Allowed functions: write
--------------------------------------------------------------------------------

Write a program that takes two strings and displays, without doubles, the
characters that appear in either one of the strings.

The display will be in the order characters appear in the command line, and
will be followed by a \n.

If the number of arguments is not 2, the program displays \n.

Example:

$>./union zpadinton "paqefwtdjetyiytjneytjoeyjnejeyj" | cat -e
zpadintoqefwjy$
$>./union ddf6vewg64f gtwthgdwthdwfteewhrtag6h4ffdhsd | cat -e
df6vewg4thras$
$>./union "rien" "cette phrase ne cache rien" | cat -e
rienct phas$
$>./union | cat -e
$
$>
$>./union "rien" | cat -e
$
*/







































int is_in_s1(char *str, int c)
{
	int i;
	i = 0;
	while(str[i])
	{
		if(str[i] == c)
		    return 1;
		i++;
	}
	return 0;
}

int already_print(char *str, int c, int pos)
{
	int i;
	i = 0;
	while(i < pos)
	{
        if(str[i] == c)
		    return 1;
		i++;
	}
	return 0;
}

int main(int argc, char **argv)
{
	int i;
	if(argc == 3)
	{
        i = 0;
		while(argv[1][i])
		{
			if(!already_print(argv[1], argv[1][i], i))
			    write(1, &argv[1][i], 1);
            i++;	
		}
		i = 0;
		while(argv[2][i])
		{
			if(!is_in_s1(argv[1], argv[2][i]) && !already_print(argv[2], argv[2][i], i))
			    write(1, &argv[2][i], 1);
			i++;
		}
	}
	write(1, "\n", 1);
	return 0;
}














int is_in_s2(char *str, int c)
{
	int i;
	i = 0;
	while(str[i])
	{
		if(str[i] == c)
		   return 1;
		i++;
	}
	return 0;
}
int seen(char *str, int c, int pos)
{
	int i = 0;
	while(i < pos)
	{
		if(str[i] == c)
		   return 1;
		i++;
	}
	return 0;
}

int main(int argc, char **argv)
{
	int i;

	if(argc == 3)
	{
		i = 0;
		while(argv[1][i])
		{
			if(!seen(argv[1], argv[1][i], i))
			    write(1, &argv[1][i], 1);
			i++;
		}
		i = 0;
		while(argv[2][i])
		{
			if(!is_in_s2(argv[1], argv[2][i]) && !seen(argv[2], argv[2][i], i))
               write(1, &argv[2][i], 1);
			i++;
		}
	}
	write(1, "\n", 1);
	return 0;
}