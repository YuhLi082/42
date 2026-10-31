/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/11 12:32:25 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/16 20:43:51 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*substring;
	size_t	n;
	size_t	s_len;

	if (!s)
		return (NULL);
	s_len = ft_strlen(s);
	if (start >= s_len)
		return (ft_strdup (""));
	if (len > s_len - start)
		len = s_len - start;
	substring = malloc(len + 1);
	if (!substring)
		return (NULL);
	n = 0;
	while (n < len)
	{
		substring[n] = s[start + n];
		n++;
	}
	substring[n] = '\0';
	return (substring);
}
