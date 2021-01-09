#k1 >> karp([(1,2),(3,5)], dur=[1,1/2,2/3], amp=[1,3/4,3/4])
def f():
    k1 >> karp([(1,2),(4,6)], dur=[1,1/2,2/3], amp=[1,3/4,3/4])
    b1 >> bass([0,2,3,4], dur=4)
    p1 >> pluck(dur=1/2).follow(b1) + (0,2,4) # This adds a triad to the bass notes
#d1 >> play("x-o-")
#p1 >> pluck([0, 2, 4], dur=[1, 1/2, 1/2], amp=0.75)
#p1 >> pluck([0, 1, 2, 3], dur=2) + [0, 0, 4]
#f()
k1 >> karp([(1,2, 4,6)], dur=[1,1/2,2/3], amp=[1,3/4,3/4]) + [0,0,4]
