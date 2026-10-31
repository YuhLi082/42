/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/05 18:13:40 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/16 20:20:14 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dst, const void *src, size_t n)
{
	unsigned char	*i;
	unsigned char	*a;
	size_t			s;

	if (!dst && !src)
		return (NULL);
	i = (unsigned char *) dst;
	a = (unsigned char *) src;
	s = 0;
	while (s < n)
	{
		i[s] = a[s];
		s++;
	}
	return (dst);
}
