# We use random class to randomly select a mad lib file.
import random
randomInt = random.randint(1,2)
if randomInt == 1:
    file = "ML_1.txt"
elif randomInt == 2:
    file = "ML_2.txt"
else
    print "Broken"
# Once file number is determined we open it.
 with open('./htmls/' + file + ".html", 'r') as myFile:
        for num, line in enumerate(myFile, 1):
           #num is the line number. an integer
	  #line is the line. a string
            if lookup in line:
                index_of_percent = line.find(lookup) #Will give us the index
                sub_array[] = #Austin do this pls
		#Get index of lookup string
		#Add %Xt to sub_array (which is going to be index + 1 and index + 2)
















madFile.close()
