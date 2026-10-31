# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/18 01:05:00 by yuhli             #+#    #+#              #
#    Updated: 2025/10/18 01:05:00 by yuhli            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libft.a
CC = cc
CFLAGS = -Wall -Wextra -Werror

AR = ar rcs
RM = rm -f

# -------------------------
# List all your 44 .c files
# -------------------------
SRC = 			\
ft_isalpha.c	\
ft_isalnum.c	\
ft_isascii.c	\
ft_isprint.c	\
ft_toupper.c	\
ft_tolower.c	\
ft_strlcpy.c	\
ft_strlen.c		\
ft_strlcat.c	\
ft_strrchr.c	\
ft_strncmp.c	\
ft_strdup.c		\
ft_substr.c		\
ft_strjoin.c	\
ft_strtrim.c	\
ft_strmapi.c	\
ft_split.c		\
ft_striteri.c	\
ft_memset.c		\
ft_bzero.c		\
ft_memcpy.c		\
ft_memmove.c	\
ft_memchr.c		\
ft_memcmp.c		\
ft_calloc.c		\
ft_putchar_fd.c	\
ft_putstr_fd.c	\
ft_putendl_fd.c	\
ft_putnbr_fd.c	\
ft_atoi.c		\
ft_isdigit.c	\
ft_strchr.c	 	\
ft_strnstr.c	\
ft_itoa.c		

SRCS_BONUS = 		\
ft_lstnew.c			\
ft_lstadd_front.c	\
ft_lstsize.c		\
ft_lstlast.c		\
ft_lstadd_back.c	\
ft_lstdelone.c		\
ft_lstclear.c		\
ft_lstiter.c		\
ft_lstmap.c			\

# -------------------------
# Objects
# -------------------------

OBJS = $(SRC:.c=.o)
OBJS_BONUS = $(SRCS_BONUS:.c=.o)

# -------------------------
# Phony targets
# -------------------------
.PHONY: all clean fclean re test bonus

# -------------------------
# Default target
# -------------------------
all: $(NAME)

# -------------------------
# Build libft.a
# -------------------------
$(NAME): $(OBJS)
	$(AR) $@ $^

# -------------------------
# Compile .c -> .o
# -------------------------
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

bonus: $(OBJS) $(OBJS_BONUS)
	$(AR) $(NAME) $^
# -------------------------
# Clean object files
# -------------------------
clean:
	$(RM) $(OBJS) $(OBJS_BONUS)

# -------------------------
# Clean object files + library
# -------------------------
fclean: clean
	$(RM) $(NAME)

# -------------------------
# Rebuild everything
# -------------------------
re: fclean all

test: $(NAME) main.o
	$(CC) $(CFLAGS) main.o -L. -lft -o test

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o
