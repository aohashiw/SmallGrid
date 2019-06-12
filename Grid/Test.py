import numpy as np
'''
Aciton:
    0:up
    1:down
    2:left
    3:right
'''

def update_value(Value,Policy,wide,high):
    new_value = np.zeros([wide,high])
    for i in range(wide):
        for j in range(high):
            if (i == 0 and j == 0) or (i == wide-1 and j == high-1):
                continue
            v_up = (Value[i][j-1] if(j!=0) else Value[i][j])
            v_down = (Value[i][j+1] if(j!=high-1) else Value[i][j])
            v_left = (Value[i-1][j] if (i!= 0) else Value[i][j])
            v_right = (Value[i+1][j] if (i!= wide-1) else Value[i][j]) # 撞墙就停止
            # x = [v_up,v_down,v_left,v_right]
            # print(x)
            new_v = -1 + Policy[i][j][0]*v_up+ Policy[i][j][1] * v_down+ Policy[i][j][2] * v_left+ Policy[i][j][3]*v_right
            new_value[i][j]=new_v

    new_value = np.around(new_value,decimals=2)
    #print(new_value)
    return new_value

def update_policy(Value,wide,high):
    new_policy = np.zeros([wide,high, 4])
    for i in range(wide):
        for j in range(high):
            if (i==0 and j==0) or(i==wide-1 and j==4):
                continue
            v_up = (Value[i][j-1] if (j != 0) else Value[i][j])
            v_down = (Value[i][j+1] if (j != high-1) else Value[i][j])
            v_left = (Value[i-1][j] if (i != 0) else Value[i][j])
            v_right = (Value[i+1][j] if (i != wide-1) else Value[i][j])
            list = [v_up,v_down,v_left,v_right]
            size = 0
            #print(i,j," max =  ",max(list))
            for x in list:
                # print(x)
                if x == max(list):
                    size = size+1
            p = 1/size
            for k in range(4):
                if list[k] == max(list):
                    new_policy[i][j][k] = p

    return new_policy








