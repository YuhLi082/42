# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/08 16:21:32 by yuhli             #+#    #+#              #
#    Updated: 2025/12/08 16:21:32 by yuhli            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


NAME = push_swap

SRCS = push_swap.c \
	   parse.c \
	   stack_init.c \
	   stack_utils.c \
	   stack_ops.c \
	   ft_split.c \
	   utils.c \
	   ft_utils.c \
	   ft_swap.c \
	   ft_push.c \
	   ft_rotate.c \
	   ft_reverse_rotate.c \
	   sort_utils.c \
	   sort_small.c \
	   sort_large.c \
	   

OBJS = $(SRCS:.c=.o)

CC = cc
CFLAGS = -Wall -Wextra -Werror

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re