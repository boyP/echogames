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

def alexaSay(someArray):
    #someArray = sub_array;
    #print sub_array
    if(len(someArray) != len(sub_array)):
        print "Array size mismatch. The array you passed is not equal in length to the array I passed"
    lineBuffer = '';
    indexPos = 0;
    lineBuffer = open(file,'r').read();
    #Now must remove the percent things and replace with the strings from the array
    #print lineBuffer
    while lookup in lineBuffer:
        #Kill the percents off
        next_target = lineBuffer.find('%');
        lineBuffer = lineBuffer[:next_target] + someArray[indexPos] +lineBuffer[(next_target+3):]
        indexPos = indexPos + 1;
    #print lineBuffer
    #print '\n\nPercents removed'
    return lineBuffer



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
        #print sub_array
        item = 0
        for element in sub_array:
            if('n' in sub_array[item]):
                sub_array[item] = 'noun';
            elif('v' in sub_array[item]):
                sub_array[item] = 'verb';
            elif('a' in sub_array[item]):
                sub_array[item] = 'adjective';

            item = item+1;


        #At this point, Echo will take in the sub_array which contains the parts of speech

        #get user inputs

        #Put into function below

        alexaSay(sub_array); #This is how you pass your array of things to read to the program. Replace with the array you make, Pratik












