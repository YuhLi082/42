/*Assignment name  : ft_range
Expected files   : ft_range.c
Allowed functions: malloc
--------------------------------------------------------------------------------

Write the following function:

int     *ft_range(int start, int end);

It must allocate (with malloc()) an array of integers, fill it with consecutive
values that begin at start and end at end (Including start and end !), then
return a pointer to the first value of the array.

Examples:

- With (1, 3) you will return an array containing 1, 2 and 3.
- With (-1, 2) you will return an array containing -1, 0, 1 and 2.
- With (0, 0) you will return an array containing 0.
- With (0, -3) you will return an array containing 0, -1, -2 and -3.*/




int     *ft_range(int start, int end)
{
    int *array;
    int i;
    int len;

    if(end >= start)
        len = start - end + 1;
    else
        len = end - start + 1;
    array = malloc(sizeof(int) * len);
    if(!array)
        return NULL;
    while(i < len)
    {
        if(start <= end)
            array[i] = start + i;
        else
            array[i] = start - i;
        i++;
    }
    return array;
}





























int     *ft_range(int start, int end)
{
    int i;
    int len;
    int *array;

    i = 0;
    if(start <= end)
        len = end - start + 1;
    else
        len = start - end + 1;
    array = malloc(sizeof(int) * len);
    if(!array)
        return NULL;
    while(i < len)
    {
        if(start <= end)
           array[i] = start + i;
        else
           array[i] = start - i;
        i++;
    }
    return array;
}



