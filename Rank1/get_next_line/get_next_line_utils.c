/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/03 21:20:36 by yuhli             #+#    #+#             */
/*   Updated: 2025/11/03 21:20:36 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *s)
{
	const char	*p;

	if (!s)
		return (0);
	p = s;
	while (*p)
		p++;
	return (p - s);
}

char	*ft_strdup(char const*s)
{
	char	*p;
	size_t	n;

	if (!s)
		return (NULL);
	p = malloc(ft_strlen(s) + 1);
	if (!p)
		return (NULL);
	n = 0;
	while (s[n])
	{
		p[n] = s[n];
		n++;
	}
	p[n] = '\0';
	return (p);
}

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	i;
	size_t	t;
	char	*s;

	if (!s1 && !s2)
		return (ft_strdup(""));
	s = malloc(ft_strlen(s1) + ft_strlen(s2) + 1);
	if (!s)
		return (NULL);
	i = 0;
	t = 0;
	while (s1 && s1[t])
	{
		s[i++] = s1[t++];
	}
	t = 0;
	while (s2 && s2[t])
	{
		s[i++] = s2[t++];
	}
	s[i] = '\0';
	return (s);
}

char	*ft_strchr(const char *s, int c)
{
	size_t	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)&s[i]);
		i++;
	}
	if ((char)c == '\0')
		return ((char *)&s[i]);
	return (NULL);
}
