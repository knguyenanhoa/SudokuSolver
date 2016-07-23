#                   DECLARATIONS
# -- Imports
from Functions import BasicFunc;
from Functions import Check;
from Functions import Fill;
from copy import deepcopy;
from sys import exit;

# -- Globals
# grid = [[0, 2, 0,   0, 7, 0,    8, 0, 3],
#         [0, 9, 0,   1, 6, 0,    0, 5, 0],
#         [1, 3, 0,   0, 0, 5,    0, 6, 0],
#             
#         [0, 0, 0,   6, 0, 0,    0, 0, 0],
#         [3, 0, 0,   0, 8, 0,    0, 0, 0],
#         [0, 0, 7,   0, 0, 9,    0, 0, 0],
#             
#         [0, 0, 0,   0, 5, 0,    0, 2, 0],
#         [2, 0, 6,   3, 0, 0,    0, 0, 7],
#         [5, 0, 0,   7, 0, 0,    0, 9, 0]]; # Index [row][column]


grid = [[0, 9, 0,   0, 0, 7,    0, 3, 0],
        [0, 0, 4,   0, 0, 3,    0, 6, 8],
        [0, 0, 0,   0, 9, 0,    0, 0, 0],
             
        [0, 0, 0,   2, 0, 5,    7, 8, 0],
        [6, 0, 0,   0, 0, 0,    0, 0, 3],
        [0, 7, 2,   4, 0, 1,    0, 0, 0],
             
        [0, 0, 0,   0, 5, 0,    0, 0, 0],
        [5, 8, 0,   3, 0, 0,    6, 0, 0],
        [0, 2, 0,   9, 0, 0,    0, 1, 0]];
        
grid_result = deepcopy(grid);
tracker = [0 for i in range(0,9)]; # Grids to track number eligibility
initial_count = 0;
filled_count = 0;
test = 0;

# -- Functions
def FullGridCheck(subject) :
    dummy = Check();
    column_master = [];
    row_master = [];
    block_master = [];
    column_error = [];
    row_error = [];
    block_error = [];
    
    for i in range(0, 9) :
        column_error = dummy.ColumnCheck(subject, i);
        row_error = dummy.RowCheck(subject, i);
        block_error = dummy.BlockCheck(subject, i+1);
        if column_error != [] :
            column_master = column_master + [column_error];
        if row_error != [] :
            row_master = row_master + [row_error];
        if block_error != [] :
            block_master = block_master + [block_error];
           
    return([column_master, row_master, block_master]);

def BruteForce(subject, i_instance, j_instance, flag):
    '''
    Does what it says on the tin
    INCOMPLETE
    '''
    grid = subject;
    current_flag = flag;
    counter = 0;
    
    # Look for 0s and remember coordinates to feed back to next function call
    loop_break = 0;
    for i in range(0,9) :
        for j in range(0,9) :
            if grid[i][j] != 0 :
                counter = counter + 1;
            if grid[i][j] == 0 :
                current_i = i;
                current_j = j;
                grid[current_i][current_j] = 1;
                current_flag = BruteForce(grid, current_i, current_j, flag);
                loop_break = 1;
                break;
        else :
            continue;
           
        if loop_break == 1 :
            break;

    if counter == 81 :
        current_i = i_instance;
        current_j = j_instance;
    
    loop_break = 0;
    for test in range(1,10) :
        grid[current_i][current_j] = test;
        if current_flag == 1 :
            for i in range(0,9) :
                for j in range(0,9) :
                    if grid[i][j] == 0 :
                        next_i = i;
                        next_j = j;
                        current_flag = BruteForce(grid, next_i, next_j, 0);
                        loop_break = 1;
                        break;
                else :
                    continue;
            
                if loop_break == 1 :
                    break;
        
        valid_result = FullGridCheck(grid); # Check grid for stopping condition
        if valid_result == [[],[],[]] : # If valid
            current_flag = 0;
            break;
            
        if grid[current_i][current_j] == 9 :
            grid[current_i][current_j] = 0;
            current_flag = 1;
        
    return(current_flag);
                







#=================================================================================
#                   MAIN
# -- Input check and initial entry count
gridcheck = FullGridCheck(grid); # Expect [],[],[] for no error
if gridcheck != [[],[],[]] :
    print('Grid check --- fail');
    for i in range(0,3):
        print(gridcheck[i]);
    exit();
else :
    print('Grid check --- pass');

for i in range(0,9) :
    for j in range(0,9) :
        if grid[i][j] != 0 :
            initial_count = initial_count + 1;
 
# -- Preliminary tracker preparation
# Initialize trackers for numbers 1-9
for i in range(1,10) :
    tracker[i-1] = [[i for j in range(0,9)] for k in range(0,9)]

# Eliminate tracker entries for initial values
for i in range(0,9) :
    for j in range(0,9) :
        for k in range(0,9) :
            if grid[i][j] != 0 :
                tracker[k][i][j] = 0;

# -- Preliminary processing
iter_counter = 0;
flag = 0;
while flag == 0 :
    grid_result = Fill().BlockFill(grid, tracker); # out = [grid_result, tracker]
    grid_result = Fill().MissingNumberFill(grid_result[0], grid_result[1]); # out = [grid_result, tracker]
    grid_result = Fill().SequenceRowFill(grid_result[0], grid_result[1]); # out = [grid_result, tracker]
    grid_result = Fill().SequenceColumnFill(grid_result[0], grid_result[1]); # out = [grid_result, tracker]
     
    # Grid check after every iteration
    gridcheck = FullGridCheck(grid); # Expect [],[],[] for no error
    if gridcheck != [[],[],[]] :
        print('Grid check --- fail')
        for i in range(0,3) :
            print(gridcheck[i]);
        exit();  
        
    iter_counter = iter_counter + 1; # Counts number of iterations
     
    iter_result = Check().IterationCheck(grid, grid_result[0], flag); # out = [grid, grid_result, flag]
    grid = iter_result[0];
    grid_result = iter_result[1];
    flag = iter_result[2];

# -- Brute force
# BruteForce(grid, 0, 0, 0);

    






#===================================================================================
#                    CONTROL OUTPUTS
for i in range(0,9) :
    for j in range(0,9) :
        if grid[i][j] != 0 :
            filled_count = filled_count + 1;
print('Fill count : ', filled_count - initial_count);
print('% complete : ', (filled_count / 81) * 100);

print('');
print('====GRID====');
print('');

for i in range(0,9) :
    print(grid[i]);
