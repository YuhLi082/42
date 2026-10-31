/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 22:53:10 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/26 22:53:10 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	put_format(char t, va_list args)
{
	if (t == 'c')
		return (ft_putchar(va_arg(args, int)));
	else if (t == 's')
		return (ft_putstr(va_arg(args, char *)));
	else if (t == 'd' || t == 'i')
		return (ft_putnbr(va_arg(args, int)));
	else if (t == 'u')
		return (ft_putunsigned(va_arg(args, unsigned int)));
	else if (t == 'x')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789abcdef"));
	else if (t == 'X')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789ABCDEF"));
	else if (t == 'p')
		return (ft_print_ptr(va_arg(args, void *)));
	else if (t == '%')
		return (ft_putchar('%'));
	else
		return (write(1, &t, 1));
}

int	ft_printf(const char	*format, ...)
{
	va_list	args;
	int		len;
	int		n;

	n = 0;
	len = 0;
	va_start(args, format);
	while (format[n])
	{
		if (format[n] == '%' && format[n + 1] != '\0')
		{
			n++;
			len += put_format(format[n], args);
		}
		else if (format[n] == '%' && format[n + 1] == '\0')
		{
			break ;
		}
		else
			len += write(1, &format[n], 1);
		n++;
	}
	va_end(args);
	return (len);
}
