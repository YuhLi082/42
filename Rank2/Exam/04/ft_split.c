/*Assignment name  : ft_split
Expected files   : ft_split.c
Allowed functions: malloc
--------------------------------------------------------------------------------

Write a function that takes a string, splits it into words, and returns them as
a NULL-terminated array of strings.

A "word" is defined as a part of a string delimited either by spaces/tabs/new
lines, or by the start/end of the string.

Your function must be declared as follows:

char    **ft_split(char *str); */


int is_space(char c)
{
    return(c == ' ' || c == '\n' || c == '\t');
}

int word_count(char *str)
{
    int i;
    int count;

    i = 0;
    count = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        if(str[i])
            count++;
        while(str[i] && !is_space(str[i]))
            i++;
    }
    return count;
}

char *word_dup(char *str, int start, int end)
{
    char *dst;
    int i;

    i = 0;
    dst = malloc(end - start + 1);
    if(!dst)
        return NULL;
    while(start < end)
        dst[i++] = str[start++];
    dst[i] = '\0';
    return dst;
}

char    **ft_split(char *str)
{
    char **result;
    int j;
    int start;
    int i;

    result = malloc(sizeof(char *) * (word_count(str) + 1));
    if(!result)
        return NULL;
    i = 0;
    j = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        start = i;
        while(str[i] && !is_space(str[i]))
            i++;
        if(start < i)
            result[j++] = word_dup(str, start, i);
    }
    result[j] = NULL;
    return result;
}


























int is_space(char c)
{
    return(c == ' ' || c == '\t' || c == '\n');
}

int count_word(char *str)
{
    int i;
    int count;

    i = 0;
    count = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        if(str[i])
            count++;
        while(str[i] && !is_space(str[i]))
            i++;
    }
    return count;
}


char *word_dup(char *str, int start, int end)
{
    char *result;
    int i;

    i = 0;
    result = malloc(end - start + 1);
    if(!result)
        return NULL;
    while(start < end)
        result[i++] = str[start++];
    result[i] = '\0';
    return result;
}


char    **ft_split(char *str)
{
    char **result;
    int i;
    int j;
    int start;

    result = malloc(sizeof(char *) * (count_word(str) + 1));
    if(!result)
        return NULL;
    i = 0;
    j = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        start = i;
        while(str[i] && !is_space(str[i]))
            i++;
        if(i > start)
            result[j++] = word_dup(str, start, i);
    }
    result[j] = NULL;
    return result;
}






















int is_space(char c)
{
    return(c == ' ' || c == '\t' || c == '\n');
}

int word_count(char *str)
{
    int i;
    int count;

    i = 0;
    count = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        if(str[i])
            count++;
        while(str[i] && !is_space(str[i]))
            i++;
    }
    return(count);
}

char *word_dup(char *str, int start, int end)
{
    char *word;
    int i;

    word = malloc(end - start +1);
    if(!word)
        return NULL;
    i = 0;
    while(start < end)
        word[i++] = str[start++];
    word[i] = '\0';
    return(word);
}


char    **ft_split(char *str)
{
    char **result;
    int i;
    int j;
    int start;

    result = malloc(sizeof(char *) * (word_count(str) + 1));
    if(!result)
        return NULL;
    i = 0;
    j = 0;
    while(str[i])
    {
        while(str[i] && is_space(str[i]))
            i++;
        start = i;
        while(str[i] && !is_space(str[i]))
            i++;
        if(i > start)
            result[j++] = word_dup(str, start, i);
    }
    result[j] = NULL;
    return result;
}
