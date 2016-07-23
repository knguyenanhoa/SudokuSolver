class BasicFunc :
    def __init__(self) :
        '''
        Initializes class. This class contains basic functions.
        '''
    
    def BlockCoord(self, block_id):
        '''
        Function for block coordinate retrieval.
        '''
        self.block_coord = {1:[0,0], 2:[0,3], 3:[0,6],
                            4:[3,0], 5:[3,3], 6:[3,6],
                            7:[6,0], 8:[6,3], 9:[6,6]
                            }; # Coord format [start_row][start_column]
        
        self.i_start = self.block_coord[block_id][0];
        self.j_start = self.block_coord[block_id][1];
        self.result = [self.i_start, self.j_start];
        
        return(self.result);
            
    
    def Comparator(self, subject, i, j, m, n):
        '''
        Basic comparison function. Returns coordinates of duplicate cells.
        '''
        self.result = [];
        
        if ((subject[i][j] == subject[m][n]) and (subject[i][j] != 0)) :
            if (i != m) or (j != n) :
                self.result = [[i,j],[m,n]];
        # Returns coordinates of duplicate if found [1st, 2nd];
    
        return(self.result);

    
    def Eliminator(self, number, pos_i, pos_j, tracker):
        '''
        Eliminates number possibilities in tracker for any grid cell.
        pos_i and pos_j denote coords of cell being considered.
        '''
        # -- Row and Column Elimination
        # Select tracker according to number in cell. number - 1 to convert to coord.
        self.result = tracker[number - 1];
        
        for self.j in range(0,9) : # Eliminate row
            self.result[pos_i][self.j] = 0;
        for self.i in range(0,9) : # Eliminate column
            self.result[self.i][pos_j] = 0;
        
        # -- Block elimination
        # Range finder (selects approriate block coordinates)
        for self.i in range(0,9,3) :
            self.i_range = pos_i - self.i;
            if self.i_range < 3 :
                self.i_lim = self.i;
                break;
        for self.j in range(0,9,3) :
            self.j_range = pos_j - self.j;
            if self.j_range < 3 :
                self.j_lim = self.j;
                break;
        # Elimination routine (all entries of block in tracker set to 0)
        for self.i in range(self.i_lim, self.i_lim+3) :
            for self.j in range(self.j_lim, self.j_lim+3) :
                self.result[self.i][self.j] = 0;
                
        return(self.result)

class Check :
    def __init__(self):
        '''
        Initializes class. This class contains grid check functions.
        '''     
        
    def ColumnCheck(self, subject, column) :
        '''
        Checks specified column for error (duplicate number)
        '''
        self.result = [];
        self.dummy = BasicFunc();
        
        for self.i in range(0, 8) :
            for self.j in range(self.i+1, 9) :
                self.error = self.dummy.Comparator(subject, 
                                                    self.i, 
                                                    column, 
                                                    self.j, 
                                                    column);
                if self.error != [] :
                    self.result = self.result + [self.error];
            
        return(self.result);
    
    def RowCheck(self, subject, row) :
        '''
        Checks specified row for error (duplicate number)
        '''
        self.result = [];
        self.dummy = BasicFunc();
        
        for self.i in range(0, 8) :
            for self.j in range(self.i+1, 9) :
                self.error = self.dummy.Comparator(subject, 
                                                    row, 
                                                    self.i, 
                                                    row, 
                                                    self.j);
                if self.error != [] :
                    self.result = self.result + [self.error];
            
        return(self.result);
      
     
    def BlockCheck(self, subject, block_id) :
        '''
        Check current block for duplicates
        '''
        self.result = [];
        self.dummy = BasicFunc();
        
        self.coord = self.dummy.BlockCoord(block_id);
         
        for self.i in range(self.coord[0], self.coord[0]+3) :
            for self.j in range(self.coord[1], self.coord[1]+3) :
                for self.m in range(self.coord[0], self.coord[0]+3) :
                    for self.n in range(self.coord[1], self.coord[1]+3) :
                        self.error = self.dummy.Comparator(subject,
                                                           self.i,
                                                           self.j,
                                                           self.m,
                                                           self.n);
                        if self.error != [] :
                            self.result = self.result + [self.error];
                    
        return(self.result);
    
    def IterationCheck(self, subject_1, subject_2, flag) :
        '''
        Check subjects to see if identical. If identical, then break loop 
        to advance to next method
        '''
        from copy import deepcopy;
        
        self.counter = 0;
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if subject_2[self.i][self.j] != subject_1[self.i][self.j] :
                    self.counter = self.counter + 1;
        
        if self.counter == 0 : # Subjects identical
            flag = 1; # Pass iteration check
        
        subject_1 = deepcopy(subject_2); # Updates old grid with new grid for next iteration
    
        return([subject_1, subject_2, flag]);

class Fill :
    def __init__(self) :
        '''
        Initializes class. Class contains grid filling routines
        '''
        
    def BlockFill(self, grid, tracker) :
        '''
        Fill blocks using tracker. Entry is filled with number corresponding
        to tracker that only has 1 non-zero entry in block.
        '''
        from copy import deepcopy;
        
        self.grid_result = deepcopy(grid);
        
        #Eliminate row, column and block entries for tracker
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if grid[self.i][self.j] != 0 :
                    BasicFunc().Eliminator(grid[self.i][self.j], self.i, self.j, tracker);
    
        # Block fill
        for self.i in range(0,9) : # Cycle tracker
            for self.j in range(1,10) : # Cycle block ID
                self.coord = BasicFunc().BlockCoord(self.j); # Returns coord according to block ID
                self.counter = 0; # Count number instance - must be 1 at the end to fill
                # Cycle through block coords
                for self.m in range(self.coord[0], self.coord[0]+3) :
                    for self.n in range(self.coord[1], self.coord[1]+3) :
                        if tracker[self.i][self.m][self.n] != 0 :
                            self.counter = self.counter + 1;
                            self.m_holder = self.m; # Stores m and n coordinates.
                            self.n_holder = self.n;
                if self.counter == 1 : # Only 1 instance in block detected
                    self.grid_result[self.m_holder][self.n_holder] = self.i+1; # Converts coords to number
                    for self.k in range(0,9) : # Updates all trackers with 0 for new entry
                        tracker[self.k][self.m_holder][self.n_holder] = 0;
                        
        return([self.grid_result, tracker]);
    
    def MissingNumberFill(self, grid, tracker) :
        '''
        Fill entries in grid by looking at each entry separately and evaluating corresponding
        tracker entries for all trackers. Grid entry only filled if only 1 tracker holds 
        non-zero entry at corresponding location.
        '''
        from copy import deepcopy
        
        self.grid_result = deepcopy(grid);
        
        #Eliminate row, column and block entries for tracker
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if grid[self.i][self.j] != 0 :
                    BasicFunc().Eliminator(grid[self.i][self.j], self.i, self.j, tracker);
                    
        # Missing number fill
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if grid[self.i][self.j] == 0 : # Evaluate entries separately
                    self.counter = 0; # Count number of trackers with non-zero entry at i,j
                    # Container to keep track of tracker that meets criteria
                    sequence = [1 for self.p in range(0,9)];
                    for self.k in range(0,9) :
                        if tracker[self.k][self.i][self.j] == 0 :
                            sequence[self.k] = 0;
                            self.counter = self.counter + 1;
                    if self.counter == 8 :
                        for self.k in range(0,9) :
                            if sequence[self.k] != 0 :
                                # Convert coord to no.
                                self.grid_result[self.i][self.j] = self.k + 1;
                        # Update all trackers with new entry
                        for self.m in range(0,9) :
                            tracker[self.m][self.i][self.j] = 0;
                            
        return([self.grid_result, tracker]);
    
    def SequenceRowFill(self, grid, tracker) :
        '''
        Looks at sequence in row and fills in blanks according to missing
        numbers in sequence. 
        '''
        from copy import deepcopy
        
        self.grid_result = deepcopy(grid);
        
        #Eliminate row, column and block entries for tracker
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if grid[self.i][self.j] != 0 :
                    BasicFunc().Eliminator(grid[self.i][self.j], self.i, self.j, tracker);
                    
        # Consider rows
        for self.i in range(0,9) : # Cycle row
            for self.k in range(0,9) : # Cycle numbers
                # Counter to count instances of a number in sequence. If only 1 instance 
                # detected then fill.
                self.counter = 0;
                for self.j in range(0,9) : # Cycle column entry
                    if ((grid[self.i][self.j] == 0) and 
                        (tracker[self.k][self.i][self.j] != 0)) :
                        self.counter = self.counter + 1;
                        # Store possible fill location
                        self.i_holder = self.i; 
                        self.j_holder = self.j;
                if self.counter == 1 :
                    # Convert coord to number and fill grid_result
                    self.grid_result[self.i_holder][self.j_holder] = self.k + 1;
                    # Updates all tracker with new entry
                    for self.m in range(0,9) :
                        tracker[self.m][self.i_holder][self.j_holder] = 0;
        
        return([self.grid_result, tracker]);
    
    def SequenceColumnFill(self, grid, tracker) :
        '''
        Looks at sequence in column and fills in blanks according to missing
        numbers in sequence. 
        '''
        from copy import deepcopy
        
        self.grid_result = deepcopy(grid);
        
        #Eliminate row, column and block entries for tracker
        for self.i in range(0,9) :
            for self.j in range(0,9) :
                if grid[self.i][self.j] != 0 :
                    BasicFunc().Eliminator(grid[self.i][self.j], self.i, self.j, tracker);
                    
        # Consider columns
        for self.j in range(0,9) : # Cycle column
            for self.k in range(0,9) : # Cycle numbers
                # Counter to count instances of a number in sequence. If only 1 instance 
                # detected then fill.
                self.counter = 0;
                for self.i in range(0,9) : # Cycle row entry
                    if ((grid[self.i][self.j] == 0) and 
                        (tracker[self.k][self.i][self.j] != 0)) :
                        self.counter = self.counter + 1;
                        self.i_holder = self.i;
                        self.j_holder = self.j;
                if self.counter == 1 :
                    # Convert coord to number and fill grid_result
                    self.grid_result[self.i_holder][self.j_holder] = self.k + 1;
                    # Update all tracker with new entry
                    for self.m in range(0,9) :
                        tracker[self.m][self.i_holder][self.j_holder] = 0;
        
        return([self.grid_result, tracker]);