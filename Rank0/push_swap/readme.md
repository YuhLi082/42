*This project has been created as part of the 42 curriculum by yuhli*
<h1>PUSH_SWAP</h1>
<h2>Introduction</h2>
<p>Push_swap is a 42 School project that challenges you to sort data on a stack using a limited set of instructions, with the goal of achieving the lowest possible number of operations. The project requires implementing an efficient sorting algorithm that can handle various input sizes while adhering to strict constraints.</p>
<br>
<h2>Operations Implemented</h2>
| Instruction | Description | Example |
|-------------|-------------|---------|
| **sa** | Swap first two elements of stack A | `1 2 3` → `2 1 3` |
| **sb** | Swap first two elements of stack B | |
| **ss** | sa and sb simultaneously | |
| **pa** | Push top element from B to A | `A: 1 2, B: 3` → `A: 3 1 2, B: (empty)` |
| **pb** | Push top element from A to B | `A: 1 2 3, B: (empty)` → `A: 2 3, B: 1` |
| **ra** | Rotate stack A upward | `1 2 3` → `2 3 1` |
| **rb** | Rotate stack B upward | |
| **rr** | ra and rb simultaneously | |
| **rra** | Reverse rotate stack A | `1 2 3` → `3 1 2` |
| **rrb** | Reverse rotate stack B | |
| **rrr** | rra and rrb simultaneously | |
<br>
<h1> Project Structure</h1>
push_swap/
├── Makefile                    # Build configuration
├── push_swap.h                 # Header file
├── push_swap.c                 # Main program
├── parse.c                     # Input validation
├── utils.c                     # Utility functions
├── stack_init.c                # Stack initialization
├── stack_ops.c                 # Core stack operations
├── ft_swap.c                   # sa, sb, ss
├── ft_push.c                   # pa, pb
├── ft_rotate.c                 # ra, rb, rr
├── ft_reverse_rotate.c         # rra, rrb, rrr
├── sort_small.c                # Small stack sorting
├── sort_large.c                # Large stack sorting
└── sort_utils.c                # Sorting utilities
<br>
<h1>Basic Test</h1>
# Test with random 100 numbers
ARG=$(shuf -i 1-100 -n 100 | tr '\n' ' ')
./push_swap $ARG | ./checker_linux $ARG
# Test with random 500 numbers
ARG=$(shuf -i 1-500 -n 500 | tr '\n' ' ')
./push_swap $ARG | ./checker_linux $ARG

# Count operations
./push_swap $ARG | wc -l
<br>
<h1>AI USE</h1>
<p>During the development of this project, AI tools were utilized as supplementary learning and optimization aids in the following areas:<p>
<br>
<h3>Algorithm Concept Understanding and Ideation</h3>
<h5>Conceptual Support:</h5> 
<p>Assisted in clarifying core sorting algorithm concepts and implementation approaches</p>
<h5>Idea Validation:</h5> 
<p>Provided theoretical references and validation for algorithm selection, particularly for large-scale input processing</p>
<h5>Concept Clarification:</h5>
<p>Helped understand complex algorithmic concepts such as chunk-based sorting and index optimization</p>
<br>
<h3>Efficiency Analysis and Strategy Optimization</h3>
<h5>Performance Evaluation:</h5> 
<p>Conducted efficiency analysis of selected sorting strategies, especially for large-scale data processing</p>
<h5>Optimization Discussion:</h5> 
<p>Assisted in exploring optimization possibilities for key parameters including the index system and chunk sizes</p>
<h5>Strategy Comparison:</h5>
<p> Supported understanding of complexity characteristics and application scenarios of different sorting approaches</p>
