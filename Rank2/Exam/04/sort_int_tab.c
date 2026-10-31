/*Assignment name  : sort_int_tab
Expected files   : sort_int_tab.c
Allowed functions:
--------------------------------------------------------------------------------

Write the following function:

void sort_int_tab(int *tab, unsigned int size);

It must sort (in-place) the 'tab' int array, that contains exactly 'size'
members, in ascending order.

Doubles must be preserved.

Input is always coherent.*/


























void sort_int_tab(int *tab, unsigned int size)
{
    unsigned int i;
    unsigned int j;
    int temp;

    if(!tab || size <= 1)
        return ;
    i = 0;
    while(i < size - 1)
    {
        j = 0;
        while(j < size - 1 - i)
        {
            if(tab[j] > tab[j + 1])
            {
                temp = tab[j];
                tab[j] = tab[j + 1];
                tab[j + 1] = temp;
            }
            j++;
        }
        i++;
    }
}














