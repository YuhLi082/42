/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/11 14:01:11 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/16 20:35:44 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	n;
	size_t	i;
	char	*s;

	if (!s1 && !s2)
		return (ft_strdup(""));
	s = malloc(ft_strlen(s1) + ft_strlen(s2) + 1);
	if (!s)
		return (NULL);
	i = 0;
	n = 0;
	while (s1 && s1[i])
	{
		s[n++] = s1[i++];
	}
	i = 0;
	while (s2 && s2[i])
	{
		s[n++] = s2[i++];
	}
	s[n] = '\0';
	return (s);
}
