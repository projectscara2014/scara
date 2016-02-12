import var
import this_to_that

def run(n) :

    spacing = var.SPACING
    block_dim = var.BLOCK_DIM
    #Total_number_of_blocks--> L
    #number_of_blocks_to_place-->L
    #Total_area--> T
    #Area_ required_to_place_the_blocks-->t
    #first_position_of_block-->b
    L=var.MAXIMUM_NUMBER_OF_BLOCKS
    l=n
    T= L*block_dim + (L-1)* spacing
    C=T/2.0
    t= l*block_dim + (l-1)* spacing
    c=t/2
    x=C-c
    Z=T-c
    B=block_dim/2.0
    # #print x
    x_array = []
    y_array = []
    #Block_cordinates-->X,Y
    for i in range (0,l) :
        X = 0
        if(l%2 !=0):
              X= x + B-40.5
              #print 'x=', X , 'y=' ,Y
              x=x+spacing+block_dim
        else:
            X= x+ B-41
            #print 'x=', X , 'y=' ,Y
            x=x+spacing+block_dim
        x_array.append(X)
        y_array.append(this_to_that.beta_to_y(var.beta))
    # print(x_array)
    # print(y_array)

    return_array = []
    for (x,y) in zip(x_array,y_array) :
        return_array.append(this_to_that.coordinates_to_list(x,y))
    
    # #print(return_array)

    for block in return_array : 
        block[0] += var.offset
        block[2] += var.offset

    def angle_to_scars(angle) :
        return int(angle*4096.0/360)

    r = []
    for block in return_array :
        m = []
        for i in range(4) :
            m.append(angle_to_scars(block[i]))
        for i in range(4,7) :
            m.append(block[i])
        r.append(m)

    return r

    #return return_array


print(run(1))
# ##print(run(3))
# for i in range (1,var.MAXIMUM_NUMBER_OF_BLOCKS):
#     print i
#     print run(i)
#     print '-------------------------------------------------------------'


    
