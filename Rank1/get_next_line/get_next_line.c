/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/09 21:00:38 by yuhli             #+#    #+#             */
/*   Updated: 2025/11/22 11:07:38 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*join_and_free(char *left, char *buffer)
{
	char	*temp;

	if (!left)
		return (ft_strdup(buffer));
	temp = left;
	left = ft_strjoin(temp, buffer);
	free (temp);
	return (left);
}

static char	*read_and_fill(int fd, char *left_c, char *buffer)
{
	ssize_t	bytes_read;

	bytes_read = 1;
	while (bytes_read > 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read == -1)
			return (free(left_c), NULL);
		if (bytes_read == 0)
			break ;
		buffer[bytes_read] = 0;
		left_c = join_and_free(left_c, buffer);
		if (!left_c)
			return (NULL);
		if (ft_strchr(left_c, '\n'))
			break ;
	}
	return (left_c);
}

static char	*extract_line(char *left_c)
{
	int		len;
	int		j;
	char	*line;

	len = 0;
	if (!left_c || !left_c[0])
		return (NULL);
	while (left_c[len] != '\n' && left_c[len] != '\0')
		len++;
	if (left_c[len] == '\n')
		len++;
	//line = malloc(len + 1);
	line = NULL;
	if (!line)
		return (NULL);
	j = 0;
	while (j < len)
	{
		line[j] = left_c[j];
		j++;
	}
	line[j] = '\0';
	return (line);
}

static char	*clean_left_c(char *left_c)
{
	int		i;
	int		j;
	char	*new_left;

	if (!left_c)
		return (NULL);
	i = 0;
	while (left_c[i] && left_c[i] != '\n')
		i++;
	if (!left_c[i])
		return (free(left_c), NULL);
	i++;
	if (!left_c[i])
		return (free(left_c), NULL);
	new_left = malloc(ft_strlen(left_c) - i + 1);
	if (!new_left)
		return (free(left_c), NULL);
	j = 0;
	while (left_c[i])
	{
		new_left[j++] = left_c[i++];
	}
	new_left[j] = '\0';
	free(left_c);
	return (new_left);
}

char	*get_next_line(int fd)
{
	static char	*left_c;
	char		*buffer;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
	{
		free(left_c);
		left_c = NULL;
		return (NULL);
	}
	buffer = malloc(BUFFER_SIZE + 1);
	if (!buffer)
		return (NULL);
	left_c = read_and_fill(fd, left_c, buffer);
	free(buffer);
	if (!left_c)
		return (NULL);
	line = extract_line(left_c);
	// if (!line)
	// 	return (free(left_c), NULL);
	left_c = clean_left_c(left_c);
	return (line);
}

