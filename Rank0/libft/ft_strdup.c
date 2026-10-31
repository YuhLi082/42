/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/11 11:22:41 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/16 20:33:18 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

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
