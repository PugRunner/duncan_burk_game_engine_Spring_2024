import time

# keeps loop going as long as i is greater than 0
i = 1
while i>0:
    mylist = ["Frame1" , "Frame2" , "Frame3" , "Frame4" , "Frame3" , "Frame2"]
    for m in mylist:
        time.sleep(1)
        print(m)


