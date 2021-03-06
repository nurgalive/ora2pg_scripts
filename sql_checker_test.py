import psycopg2
import sys
import os
from datetime import datetime

con = None

#directory with files, that will be checked
directory = 'C:\\test\\check'
files = os.listdir(directory)
print("Number of files: " + str(len(files)))
#print all files in the directory \\check
print(files)


#count for naming the files
succ_count = 1
time = datetime.now().strftime('%Y-%m-%d_%H-%M')

for file_name in files:
    #open every file
    with open(directory + '/' + f, 'r') as file_in:
        text = file_in.read()
        print("Query:")
        print(text)
        print("_____________")
        try:
            #establishing connetction to db
            con = psycopg2.connect("host='localhost' dbname='dbname' user='postgres' password='1'")   
            cur = con.cursor()
            #query executing
            cur.execute(text)
            con.commit()
            while True:
                row = cur.fetchone()
 
                if row == None:
                    break
 
                print("Product: " + row[1] + "\t\tPrice: " + str(row[2]))
       # con.commit()
        except (psycopg2.DatabaseError as e):
            if con:
                con.rollback()

            print('Error %s' % e)    
            file_in.close()
            os.rename("C:\\test\\check\\" + file_name, "C:\\test\\error\\" + file_name)
            with open(directory + '/' + time + '.log', "a") as file_out:
                file_out.write(file_name + "\n")
                file_out.write(e + "\n")
                file_out.write("\n" + "\n" + "\n")
            
        else:
            file_in.close()
            os.rename("C:\\test\\check\\" + file_name, "C:\\test\\ready\\" + str(succ_count) + '_' + f)
            succ_count +=1
            

        finally:   
            if con:
                con.close()
        
        print("\n")
