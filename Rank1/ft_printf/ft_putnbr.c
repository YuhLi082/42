/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 22:17:25 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/22 22:17:25 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(int n)
{
	long	num;
	int		len;

	num = n;
	len = 0;
	if (num < 0)
	{
		write(1, "-", 1);
		len++;
		num = -num;
	}
	if (num > 9)
		len += ft_putnbr(num / 10);
	len += ft_putchar(num % 10 + '0');
	return (len);
}
