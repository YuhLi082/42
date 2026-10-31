/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/07 20:53:38 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/07 20:53:38 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	size_t	i;
	size_t	t;

	if (!s)
		return (NULL);
	t = ft_strlen(s);
	i = t + 1;
	while (i > 0)
	{
		i--;
		if (s[i] == (char) c)
			return ((char *)&s[i]);
	}
	return (NULL);
}
