# We use random class to randomly select a mad lib file.
def selectFile():
    global theFile;
    import random
    randomInt = random.randint(1,2)
    if randomInt == 1:
        theFile = "ML_1.txt" #update
    elif randomInt == 2:
        theFile = "ML_2.txt"
    else:
        print "Broken"
    return theFile;
i = 0;
q = 0;
theFile = "";
# Once file number is determined we open it.
lookup = '%';
sub_array = [];

def alexaSay(someArray):
    global theFile;
    if(len(someArray) != len(sub_array)):
        print "Array size mismatch. The array you passed is not equal in length to the array I passed"
    lineBuffer = '';
    indexPos = 0;
    lineBuffer = open(theFile,'r').read();
    while lookup in lineBuffer:
        #Remove percents
        next_target = lineBuffer.find('%');
        lineBuffer = lineBuffer[:next_target] + someArray[indexPos] +lineBuffer[(next_target+3):]
        indexPos = indexPos + 1;
    return lineBuffer


def getSubArray():
    global sub_array
    with open(selectFile()) as myFile:
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
            item = 0
            for element in sub_array:
                if('n' in sub_array[item]):
                    sub_array[item] = 'noun';
                elif('v' in sub_array[item]):
                    sub_array[item] = 'verb';
                elif('a' in sub_array[item]):
                    sub_array[item] = 'adjective';

                item = item+1;
            return sub_array;

        #At this point, Echo will take in the sub_array which contains the parts of speech

        #get user inputs

        #Put into function below
        #print sub_array;
        #print alexaSay(sub_array);
        #get list of user inputs from echo and put them in the final script
        #final_string = alexaSay(responses_array);
        #This is how you pass your array of things to read to the program. Replace with the array you make, Pratik
print getSubArray()
print alexaSay(getSubArray())
