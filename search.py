import numpy
import scipy
#import pandas
import hashlib
import fileinput
import timeit #to calculate runtime

import sys

def PrintGrid(grid):
    i = 0
    while i < len(grid):
        print(grid[i])
        i += 1

def EmptyGrid():
    return [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

def CopyGrid(grid1):
    grid2 = EmptyGrid()
    i=0
    while( i < 4 ):
        j=0
        while( j < 4 ):
            grid2[i][j] = grid1[i][j]
            j += 1
        i += 1
    return grid2

def SameGrid(grid1, grid2):
    for row in range(0,4):
        for col in range(0,4):
            if (grid1[row][col] != grid2[row][col]):
                return False
    return True
    
def GridMax(grid):
    max_score = 0
    for row in range(0,4):
        for col in range(0,4):
            if (grid[row][col] > max_score ):
                max_score = grid[row][col]
    return max_score

def GridScore(grid):
    zero_value = 12
    grid_weight = 3
    total_score = 0
    for row in range(0,4):
        for col in range(0,4):
            if (grid[row][col] == 0):
                total_score += zero_value
            else:
                total_score += 2 * grid[row][col]
    
    total_score += GridMax(grid)
    return total_score





def MergeRow(index0, index1, index2, index3):
    i0 = index0
    i1 = index1
    i2 = index2
    i3 = index3
    largest_merge = 0
    row = [i0,i1,i2,i3]
    
    #the non-zero elements next to each other
    shifted_row = [0,0,0,0]
    #combine two adjacent, equL elements in the array
    merged_row = [0,0,0,0]

    #ith element of the original array
    i = 0
    #jth element that is not zero
    j = 0
    #kth element in the merged array
    k = 0
    while(i < 4):
        if row[i] != 0:
            shifted_row[j] = row[i]
            j = j+1
        i = i+1

    if(shifted_row[0] == shifted_row[1]) and (shifted_row[2] == shifted_row[3]):
        merged_row[0] = 2 * shifted_row[0]
        merged_row[1] = 2 * shifted_row[2]
    elif(shifted_row[0] == shifted_row[1]):
        merged_row[0] = 2 * shifted_row[0]
        merged_row[1] = shifted_row[2]
        merged_row[2] = shifted_row[3]
    elif(shifted_row[1] == shifted_row[2]):
        merged_row[0] = shifted_row[0]
        merged_row[1] = 2 * shifted_row[1]
        merged_row[2] = shifted_row[3]
    elif(shifted_row[2] == shifted_row[3]):
        merged_row[0] = shifted_row[0]
        merged_row[1] = shifted_row[1]
        merged_row[2] = 2 * shifted_row[2]
    else:
        merged_row[0] = shifted_row[0]
        merged_row[1] = shifted_row[1]
        merged_row[2] = shifted_row[2]
        merged_row[3] = shifted_row[3]

    return merged_row[0], merged_row[1], merged_row[2], merged_row[3]

def MergeCol(index0, index1, index2, index3):
    return MergeRow(index0, index1, index2, index3)





def MergeGrid(grid, direction):
    #0 = up
    #1 = down
    #2 = left
    #3 = right
    i = 0
    
    if(direction == 0):
        while i < 4:
            grid[0][i], grid[1][i], grid[2][i], grid[3][i] = MergeCol( grid[0][i], grid[1][i], grid[2][i], grid[3][i] )
            i += 1
            
    if(direction == 1):
        while i < 4:
            grid[3][i], grid[2][i], grid[1][i], grid[0][i] = MergeCol( grid[3][i], grid[2][i], grid[1][i], grid[0][i] )
            i += 1
            
    if(direction == 2):
        while i < 4:
            grid[i][0], grid[i][1], grid[i][2], grid[i][3] = MergeRow( grid[i][0], grid[i][1], grid[i][2], grid[i][3] )
            i += 1
            
    if(direction == 3):
        while i < 4:
            grid[i][3], grid[i][2], grid[i][1], grid[i][0] = MergeRow( grid[i][3], grid[i][2], grid[i][1], grid[i][0] )
            i += 1
        
    return grid





def Max_Move2(Grid) -> float:
    #matrices of each move
    move_up = CopyGrid(Grid)
    move_down = CopyGrid(Grid)
    move_left = CopyGrid(Grid)
    move_right = CopyGrid(Grid)
    
    up_score = 0.0
    down_score = 0.0
    left_score = 0.0
    right_score = 0.0

    #shift rows left for move_left
    move_up = MergeGrid(move_up, 0)
    move_down = MergeGrid(move_down, 1)
    move_left = MergeGrid(move_left, 2)
    move_right = MergeGrid(move_right, 3)
    
    nothing_score = GridScore(Grid)
    
    if SameGrid(Grid,move_up) is False:
        up_score = GridScore(move_up)
    else:
        up_score = nothing_score
        
    if SameGrid(Grid,move_down) is False:
        down_score = GridScore(move_down)
    else:
        down_score = nothing_score
        
    if SameGrid(Grid,move_left) is False:
        left_score = GridScore(move_left)
    else:
        left_score = nothing_score

    if SameGrid(Grid,move_right) is False:
        right_score = GridScore(move_right)
    else:
        right_score = nothing_score
    
    '''
    up_score = ExpectMax2(move_up)
    down_score = ExpectMax2(move_down)
    left_score = ExpectMax2(move_left)
    right_score = ExpectMax2(move_right)
    nothing_score = ExpectMax2(Grid)
    '''

    max_score = up_score
    if(down_score > max_score):
        max_score = down_score
    if(left_score > max_score):
        max_score = left_score
    if(right_score > max_score):
        max_score = right_score
    if(nothing_score > max_score):
        max_score = nothing_score

    return max_score





#expect the maximum for each move
#We'll only imagine each replacement being a 2 as a worst-case and the low
#probability of 4 occurring for a given space
def ExpectMax2(grid) -> float:
    #index in the grid(length)
    i = 0
    #index in the grid(height)
    j = 0
    #index in the list of grids
    k = 0
    grid_list = []
    weight_list = []
    score_list = []
    
    while( i < 4 ):
        j = 0
        while( j < 4 ):
            if( grid[i][j] == 0 ):
                new_grid_a = EmptyGrid()
                for row in range(0,4):
                    for col in range(0,4):
                        new_grid_a[row][col] = grid[row][col]
                new_grid_a[i][j] = 2
                grid_list.append(new_grid_a)
                weight_list.append(1)
                score_list.append( Max_Move2(new_grid_a) )
                k += 1
            j += 1
        i += 1
    
    '''
    print("===================================")
    '''
    l = 0
    total_score = 0
    while( l < k ):
        '''
        print("l=",l)
        PrintGrid( grid_list[l] )
        '''
        total_score += weight_list[l] * score_list[l]
        l += 1
    if( k > 0 ):
        return total_score/(k/2)
    return 0




    
#execute the best-scoring move for each option
def Max_Move(Grid) -> float:
    #matrices of each move
    move_up = CopyGrid(Grid)
    move_down = CopyGrid(Grid)
    move_left = CopyGrid(Grid)
    move_right = CopyGrid(Grid)
    
    up_score = 0.0
    down_score = 0.0
    left_score = 0.0
    right_score = 0.0

    #shift rows left for move_left
    move_up = MergeGrid(move_up, 0)
    move_down = MergeGrid(move_down, 1)
    move_left = MergeGrid(move_left, 2)
    move_right = MergeGrid(move_right, 3)
    
    '''
    nothing_score = ExpectMax2(Grid)
    
    if SameGrid(Grid,move_up) is False:
        up_score = ExpectMax2(move_up)
    else:
        up_score = nothing_score
        
    if SameGrid(Grid,move_down) is False:
        down_score = ExpectMax2(move_down)
    else:
        down_score = nothing_score
        
    if SameGrid(Grid,move_left) is False:
        left_score = ExpectMax2(move_left)
    else:
        left_score = nothing_score

    if SameGrid(Grid,move_right) is False:
        right_score = ExpectMax2(move_right)
    else:
        right_score = nothing_score
    '''
    nothing_score = ExpectMax2(Grid)
    
    if SameGrid(Grid,move_up) is False:
        up_score = ExpectMax2(move_up)
    else:
        up_score = nothing_score
        
    if SameGrid(Grid,move_down) is False:
        down_score = ExpectMax2(move_down)
    else:
        down_score = nothing_score
        
    if SameGrid(Grid,move_left) is False:
        left_score = ExpectMax2(move_left)
    else:
        left_score = nothing_score

    if SameGrid(Grid,move_right) is False:
        right_score = ExpectMax2(move_right)
    else:
        right_score = nothing_score
    
    '''
    up_score = ExpectMax2(move_up)
    down_score = ExpectMax2(move_down)
    left_score = ExpectMax2(move_left)
    right_score = ExpectMax2(move_right)
    nothing_score = ExpectMax2(Grid)
    '''

    max_score = up_score
    if(down_score > max_score):
        max_score = down_score
    if(left_score > max_score):
        max_score = left_score
    if(right_score > max_score):
        max_score = right_score
    if(nothing_score > max_score):
        max_score = nothing_score

    return max_score





#expect the maximum for each move
#We'll only imagine each replacement being a 2 as a worst-case and the low
#probability of 4 occurring for a given space
def ExpectMax(grid) -> float:
    #index in the grid(length)
    i = 0
    #index in the grid(height)
    j = 0
    #index in the list of grids
    k = 0
    grid_list = []
    weight_list = []
    score_list = []
    
    while( i < 4 ):
        j = 0
        while( j < 4 ):
            if( grid[i][j] == 0 ):
                new_grid_a = EmptyGrid()
                for row in range(0,4):
                    for col in range(0,4):
                        new_grid_a[row][col] = grid[row][col]
                new_grid_a[i][j] = 2
                grid_list.append(new_grid_a)
                weight_list.append(1)
                score_list.append( Max_Move(new_grid_a) )
                k += 1
            j += 1
        i += 1
    
    '''
    print("===================================")
    '''
    l = 0
    total_score = 0
    while( l < k ):
        '''
        print("l=",l)
        PrintGrid( grid_list[l] )
        '''
        total_score += weight_list[l] * score_list[l]
        l += 1
    if( k > 0 ):
        return total_score/(k/2)
    return 0





def NextMove(Grid, Step) -> int: 

    if(Step > 2150):
        return 4
    #matrices of each move
    move_up = CopyGrid(Grid)
    move_down = CopyGrid(Grid)
    move_left = CopyGrid(Grid)
    move_right = CopyGrid(Grid)
    
    '''
    PrintGrid(move_up)
    PrintGrid(move_down)
    PrintGrid(move_left)
    PrintGrid(move_right)
    '''
    '''    
    for row in range(0,4):
        for col in range(0,4):
            move_up[row][col] = Grid[row][col]
            move_down[row][col] = Grid[row][col]
            move_left[row][col] = Grid[row][col]
            move_right[row][col] = Grid[row][col]
    '''
    up_score = 0.0
    down_score = 0.0
    left_score = 0.0
    right_score = 0.0
    tmp_score = 0.0

    #shift rows left for move_left
    move_up = MergeGrid(move_up, 0)
    move_down = MergeGrid(move_down, 1)
    move_left = MergeGrid(move_left, 2)
    move_right = MergeGrid(move_right, 3)
    
    #no more possible moves
    #print( SameGrid(Grid,move_up), SameGrid(Grid,move_down), SameGrid(Grid,move_left), SameGrid(Grid,move_right) )
    
    if( (SameGrid(Grid,move_up) is True) and (SameGrid(Grid,move_down) is True) and (SameGrid(Grid,move_left) is True) and (SameGrid(Grid,move_right) is True)):
        return 4
    
    #Explore possible layouts for each movement
    #If layouts are the same as doing nothing, do not traverse branch
    nothing_score = ExpectMax(Grid)
    
    if SameGrid(Grid,move_up) is False:
        up_score = ExpectMax(move_up)
    else:
        up_score = nothing_score
        
    if SameGrid(Grid,move_down) is False:
        down_score = ExpectMax(move_down)
    else:
        down_score = nothing_score
        
    if SameGrid(Grid,move_left) is False:
        left_score = ExpectMax(move_left)
    else:
        left_score = nothing_score

    if SameGrid(Grid,move_right) is False:
        right_score = ExpectMax(move_right)
    else:
        right_score = nothing_score

    '''
    print("===========================================================")
    print("===========================================================")
    print("===========================================================")
    print("DEFAULT")
    PrintGrid(Grid)
    print("score: ")
    print("\nUP")
    PrintGrid(move_up)
    print("score: ", up_score)
    print("\nDOWN")
    PrintGrid(move_down)
    print("score: ", down_score)
    print("\nLEFT")
    PrintGrid(move_left)
    print("score: ", left_score)
    print("\nRIGHT")
    PrintGrid(move_right)
    print("score: ", right_score)
    '''
    
    if(up_score >= down_score) and (up_score >= left_score) and (up_score >= right_score) and (up_score >= nothing_score):
        return 0
    if(down_score >= up_score) and (down_score >= left_score) and (down_score >= right_score) and (down_score >= nothing_score):
        return 1
    if(left_score >= up_score) and (left_score >= down_score) and (left_score >= right_score) and (left_score >= nothing_score):
        return 2
    if(right_score >= up_score) and (right_score >= down_score) and (right_score >= left_score) and (right_score >= nothing_score):
        return 3
    if(nothing_score >= up_score) and (nothing_score >= down_score) and (nothing_score >= left_score) and (nothing_score >= right_score):
        return 5
    return 0





def main():
    #Start our Program
    start = timeit.default_timer()
    
    #initialize the grid
    Grid = EmptyGrid()

    ScoreList = []
    
    print("a")
    
    #generate the positions of the first 2 blocks
    for cfdsvv in range(0,25):
        first_seed = numpy.random.randint(0,16)
        second_seed = numpy.random.randint(0,15)
        if second_seed >= first_seed:
            second_seed += 1
        
        Grid[ (int)(first_seed/4) ][ first_seed % 4 ] = 2
        Grid[ (int)(second_seed/4) ][ second_seed % 4 ] = 2
        
        #new_grid = EmptyGrid()
        #PrintGrid(new_grid)
        #new_grid = CopyGrid(Grid)
        #PrintGrid(new_grid)
        
        #place these blocks on the board; both are worth 2pts
        move = 0
        index = 0
        while(index < 2150) and (move != 4):
            end = timeit.default_timer()
            move = NextMove(Grid, index)
            Grid = MergeGrid(Grid, move)
            if(move == 4):
                break
            index += 1
            #print(index,": t= ", end - start)
            adding_space = True
            adding_space_index = 0
            while(adding_space is True) and (adding_space_index < 30):
                first_seed = numpy.random.randint(0,16)
                if( Grid[ (int)(first_seed/4) ][ first_seed % 4 ] == 0 ):
                    second_seed = numpy.random.randint(0,10)
                    if(second_seed == 0):
                        Grid[ (int)(first_seed/4) ][ first_seed % 4 ] = 4
                    else:
                        Grid[ (int)(first_seed/4) ][ first_seed % 4 ] = 2
                    adding_space = False
                adding_space_index += 1
    
        if(move > 11):
            PrintGrid(Grid)
            print(index,": t= ", end - start)
            max_element = GridMax(Grid)
            #print("Highest-score block", max_element)
            ScoreList.append( max_element )
    
    total_score = 0
    j = 0
    for i in ScoreList:
        j += 1
        total_score += i
        print(i)
    
    print("Total score: ", total_score)
    print("Average score", total_score/j)

    

if __name__=="__main__":
    main()
