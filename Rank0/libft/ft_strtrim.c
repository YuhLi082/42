/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/11 16:31:04 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/16 20:43:04 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_in_set(char c, char const *set)
{
	size_t	i;

	i = 0;
	if (!set)
		return (0);
	while (set[i])
	{
		if (set[i] == c)
			return (1);
		i++;
	}
	return (0);
}

static char	*new_str(const char *s1, size_t start, size_t len)
{
	char	*i;
	size_t	t;

	if (len == 0 || start >= ft_strlen(s1))
		return (ft_strdup(""));
	i = malloc(len + 1);
	if (!i)
		return (NULL);
	t = 0;
	while (t < len)
	{
		i[t] = s1[start + t];
		t++;
	}
	i[t] = '\0';
	return (i);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	start;
	size_t	end;

	if (!s1 || !set)
		return (NULL);
	if (ft_strlen(s1) == 0)
		return (ft_strdup(""));
	start = 0;
	end = ft_strlen(s1) - 1;
	while (s1[start] && ft_in_set(s1[start], set))
		start++;
	while ((end > start) && ft_in_set(s1[end], set))
		end--;
	return (new_str (s1, start, end - start + 1));
}
