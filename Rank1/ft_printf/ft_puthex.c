/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 21:41:02 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/23 21:41:02 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex(unsigned long nr, char *base)
{
	size_t			len;
	unsigned long	num;

	num = nr;
	len = 0;
	if (num > 15)
		len += ft_puthex(num / 16, base);
	len += ft_putchar(base[num % 16]);
	return (len);
}
