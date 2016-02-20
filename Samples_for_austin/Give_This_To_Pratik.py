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
q = 0;
# Once file number is determined we open it.
lookup = '%';
with open(file) as myFile:
        sub_array = []
        for num, line in enumerate(myFile, 1):
           #num is the line number. an integer
	  #line is the line. a string
            #for i in enumerate (line, 1):

            if lookup in line:
                index_of_percent = [i for i,x in enumerate(line) if x == lookup];
                q=0;
                for element in index_of_percent:
                    if(q < len(index_of_percent)):
                        sub_array.append(line[index_of_percent[q] + 1]);
                        i = i+1;
                        q = q+1;
                        continue
                    else:
                        break;
        print sub_array












