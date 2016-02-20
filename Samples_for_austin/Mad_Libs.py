# We use random class to randomly select a mad lib file.
import random
randomInt = random.randint(1,2)
if randomInt == 1:
    file = "ML_1.txt"
elif randomInt == 2:
    file = "ML_2.txt"
else:
    print "Broken"
i = 0
j = 0
# Once file number is determined we open it.
lookup = '%';
with open(file) as myFile:
        for num, line in enumerate(myFile, 1):
           #num is the line number. an integer
	  #line is the line. a string
            #for i in enumerate (line, 1):
            sub_array = [[0]*(len(line)+1),[0]*2]
            for i in xrange(len(line)):
                if lookup in line:
                    print lookup
                    print type(lookup)
                    print 'line =', line
                    print 'line.find =', line.find(lookup)
                    index_of_percent = int(line.find(lookup)) #Will give us the index
                    print i, j, type(i), type(j)
                    sub_array[i][j] = index_of_percent + 1
                    sub_array[i][j + 1] = index_of_percent + 2
                    continue
















madFile.close()
