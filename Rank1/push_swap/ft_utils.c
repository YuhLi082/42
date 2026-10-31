/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_utils.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 16:20:07 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 16:25:57 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	ft_strlen(const char *s)
{
	const char	*p = s;

	while (*p)
		p++;
	return (p - s);
}

char	*ft_strdup(const char *s1)
{
	char	*copy;
	size_t	n;

	copy = malloc (ft_strlen(s1) + 1);
	if (copy == NULL)
		return (NULL);
	n = 0;
	while (s1[n])
	{
		copy[n] = s1[n];
		n++;
	}
	copy[n] = '\0';
	return (copy);
}
