# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/22 00:00:11 by yuhli             #+#    #+#              #
#    Updated: 2025/10/22 00:00:11 by yuhli            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a

CC = gcc
CFLAGS = -Wall -Wextra -Werror
RM = rm -fr

SRCS =	ft_putchar.c		\
		ft_putstr.c			\
		ft_strlen.c 		\
		ft_putnbr.c			\
		ft_putunsigned.c	\
		ft_puthex.c			\
		ft_print_ptr.c		\
		ft_printf.c 		
		
		

OBJS = $(SRCS:.c=.o) 

$(NAME) : $(OBJS)
	@ar crs $(NAME) $(OBJS) 

all: 
	$(MAKE) $(NAME)

clean:
	@$(RM) $(OBJS)
fclean: clean
	@rm -f $(NAME)
re: fclean all
.PHONY: all re clean fclean