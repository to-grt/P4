import numpy as np
HEIGHT = 6
cdef int WIDTH = 7
cdef int DIFFICULTY = 11

def update_bitmap(long mymask,long mypos1,long mypos2, int col):
    cdef long p2,m
    p2 = mypos2
    m = mymask             
    p2 = m ^ mypos1
    m = m | (m + bottommask(col))
    return np.array([m,p2])
    # self.p1pos, self.p2pos, self.mask updated tout seul

    # self.p1pos, self.p2pos, self.mask updated tout seul    
cdef int coupsPossibles2(long mymask): 
    #cdef int[:] coups  = np.full(WIDTH+1,-1,dtype=np.int32)  
    #cdef int[:] cases  = np.array([3,4,2,5,1,6,0],dtype=np.int32)
    cdef int coups = 0
    cdef int i
    for i in range(6):
        if(can_play(i,mymask)):    coups |= (1 << i)
    return coups



cdef bint can_play(int col,long mymask):
    return mymask & topmask(col) == 0
cdef long topmask(int col):
    return 1 << col*(HEIGHT+1) << (HEIGHT-1)
cdef long bottommask(int col):
    return 1 << col*(HEIGHT+1)

cdef bint alignements2(long bitmap):
        cdef long m
        cdef long local_HEIGHT
        local_HEIGHT = HEIGHT

        m = bitmap & bitmap>> local_HEIGHT+1
        if( m & m>> 14 != 0): return True
        m = bitmap & bitmap>> local_HEIGHT
        if( m & m>> 12 != 0): return True
        m = bitmap & bitmap>> local_HEIGHT+2
        if( m & m>> 16 != 0): return True
        m = bitmap & bitmap>> 1
        if( m & m>>  2):      return True
        return False

def minMax(int alpha,int beta,int depth,long mymask,long mypos1,long mypos2):           
    if alignements2(mypos2):        return (-50 + depth), None
    if depth >= DIFFICULTY:         return 0, None
    cdef int coups = coupsPossibles2(mymask)
    if coups == 0:             return 0, None  
    cdef int score = - 999
    cdef int meilleurCoup = 0
    cdef int i,coup,cur,compteur
    cdef long[:] u
    i = 3
    compteur = 0
    while(i-compteur != -1) :
        coup = coups & (1 << i+compteur)

        if(coup != 0):
            u   =    update_bitmap(mymask,mypos1,mypos2,i+compteur)
            cur =  - minMax(-beta,-alpha,depth+1,u[0],u[1],mypos1)[0]
            if(cur   >  score):  
                score = cur
                meilleurCoup = i+compteur
            if(score >  alpha):  alpha = score     
            if(alpha >= beta ):  return alpha,i+compteur

        coup = coups & (1 << i-compteur)

        if(coup != 0):
            u   =    update_bitmap(mymask,mypos1,mypos2,i-compteur)
            cur =  - minMax(-beta,-alpha,depth+1,u[0],u[1],mypos1)[0]
            if(cur   >  score):  
                score = cur
                meilleurCoup = i-compteur
            if(score >  alpha):  alpha = score     
            if(alpha >= beta ):  return alpha,i-compteur
        
        compteur += 1
    return score, meilleurCoup
