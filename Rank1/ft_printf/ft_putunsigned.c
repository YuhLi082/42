/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunsigned.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 23:51:47 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/22 23:51:47 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunsigned(unsigned int n)
{
	size_t	len;

	len = 0;
	if (n > 9)
		len += ft_putunsigned(n / 10);
	len += ft_putchar(n % 10 + '0');
	return (len);
}
