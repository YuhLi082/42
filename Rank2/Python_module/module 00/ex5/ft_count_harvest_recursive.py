def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count(i):
        if (i > days):
            print("Harvest time!")
            return
        print("Day", i)
        count(i + 1)
    count(1)
