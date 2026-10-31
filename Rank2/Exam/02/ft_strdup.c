/*Assignment name  : ft_strdup
Expected files   : ft_strdup.c
Allowed functions: malloc
--------------------------------------------------------------------------------

Reproduce the behavior of the function strdup (man strdup).

Your function must be declared as follows:

char    *ft_strdup(char *src);*/




char    *ft_strdup(char *src)
{
	int len;
	int i;
	char *dst;

	i = 0;
	len = 0;
	while(src[len])
	    len++;
	dst = malloc(len + 1);
	if(!dst)
	    return NULL;
	while(src[i])
	{
		dst[i] = src[i];
		i++;
	}
    dst[i] = '\0';
    return dst;
}


