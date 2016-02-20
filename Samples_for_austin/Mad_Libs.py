# We use random class to randomly select a mad lib file.
import random
randomInt = random.randint(1,2)
if randomInt == 1:
    file = "ML_1.txt"
elif randomInt == 2:
    file = "ML_2.txt"
else:
    print "Broken"
file = "ML_1.txt" #for now
i = 0
j = 0
q=0;
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
                    index_of_percent = [i for i, x in enumerate(line) if x == lookup];
                    print "Going through indexes"
                    print "Indexes -> ", index_of_percent
                    for element in index_of_percent:
                        if((q != len(index_of_percent))):
                            print "Element -> ",q
                            print "For index ->", index_of_percent[q]
                            print 'Text = ', line
                            print 'Type -> ', line[index_of_percent[q]+1]
                            print 'Unique ID -> ', line[index_of_percent[q]+2]
                            print i, j, type(i), type(j)
                            sub_array[i][j] = line[index_of_percent + 1];
                            sub_array[i][j + 1] = line[index_of_percent + 2];
                            i = i+1;
                            q=q+1;
                            continue
                        else:
                            print "BREAK";
                            break;















madFile.close()
