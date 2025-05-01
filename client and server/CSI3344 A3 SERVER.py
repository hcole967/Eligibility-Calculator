#Distributed Systems Assignment 3 SERVER
#made by:
#Harrison Cole, 10632167
#James Scott, 981832


import socket
import json
import pyodbc



def calcFails(units, fail_threshold=50):           #Fail handing for evaluation() (score less than 50 = fail)
    return sum(1 for grade in units.values() if grade < fail_threshold)



def SQLdata(student_id, First_Name):        #PHASE 2 CONNECTION TO SQL SERVER

    #ASSUMING MICROSOFT SQL SERVER MANAGEMENT STUDIO IS USED

    #query to access specific tables in SQL database (Create_tables.sql)
    query = f"SELECT su.unit_code, su.result_score FROM student_unit su \
            INNER JOIN student_info si ON su.person_id = si.person_id \
            WHERE su.person_id = {student_id} AND si.first_name = '{First_Name}'"
    

    #define server name and database
    server = 'localhost\SQLEXPRESS'
    database = 'master'

    #define connection string (allows access into the sql database)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER=' + server + '; \
                        DATABASE=' + database +';\
                        Trusted_Connection=yes;')

    #create connection cursor
    cursor = cnxn.cursor()
    #execute the query stated above (access the SQL server and get the person_id and first_name)
    cursor.execute(query)

    # select all rows from the query result
    OUSTdata = cursor.fetchall()
    
    #Check if data is empty or not (or if the student id/first name does not match with anything)
    if not OUSTdata:
        print(f"No data found for student ID {student_id}")
    else:
        #close connection
        cnxn.close()
        return OUSTdata 


#calculating the average score for evaluation()
def calcAverage(units):
    total_score = sum(units.values())
    return total_score / len(units)

#calculating the average score of the top 8 scores for evaluation()
def best8average(units):
    sorted_units = sorted(units.values(), reverse=True)[:8]  
    return sum(sorted_units) / min(len(sorted_units), 8) 

#evaluates scores entered and prints corresponding HEPaS message
def evaluator(numUnits, student_id, course_avg, best_8_avg, fails_count):
    if numUnits < 16:
        return f"{student_id}, {course_avg:.1f}, completed less than 16 units!\nDOES NOT QUALIFY FOR HONOURS STUDY\n"
    if fails_count >= 6:
        return f"{student_id}, {course_avg:.1f}, with 6 or more Fails! DOES NOT QUALIFY FOR HONOURS STUDY!\n"
    elif course_avg >= 70:
        return f"{student_id}, {course_avg:.1f}, QUALIFIES FOR HONOURS STUDY!\n"
    elif course_avg >= 65 and best_8_avg >= 80:
        return f"{student_id}, {course_avg:.1f}, {best_8_avg:.1f}, QUALIFIES FOR HONOURS STUDY!\n"
    elif course_avg >= 65:
        return f"{student_id}, {course_avg:.1f}, {best_8_avg:.1f}, MAY HAVE GOOD CHANCE! Need further assessment!\n"
    elif course_avg >= 60 and best_8_avg >= 80:
        return f"{student_id}, {course_avg:.1f}, {best_8_avg:.1f}, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission!\n"
    else:
        return f"{student_id}, {course_avg:.1f}, DOES NOT QUALIFY FOR HONORS STUDY!\n"

#get data entered on the client side for use in the server side
def handleClientData(data):
    OUST = data.get("OUST")
    
    try:
        if OUST == False:                   #if 'n' is entered in the client OUST prompt
            numUnits = data.get('numUnits')
            student_id = data.get('student_id')
            email = data.get('email')
            units = data.get('units')
            course_avg = calcAverage(units)
            best_8_avg = best8average(units)
            fails_count = calcFails(units)

            result = evaluator(numUnits, student_id, course_avg, best_8_avg, fails_count) #send entered data into the evaluator()
            return f"result: {result}" #send the result back to the client side
        else:                               #if 'y' is entered in the client OUST prompt
            student_id = data.get('student_id')
            email = data.get('email')
            First_Name = data.get("username")
            Last_Name = data.get("Last_Name")
            print("Sending query...")
            SQLresult = SQLdata(student_id, First_Name) #use the student_id and First_Name to authenticate the user
            units = dict(SQLresult)
            numUnits = len(units)
            course_avg = calcAverage(units)
            best_8_avg = best8average(units)
            fails_count = calcFails(units)
            result = evaluator(numUnits, student_id, course_avg, best_8_avg, fails_count)
            return f"result: {result}"  #return results to client side
            


    except Exception as e:
        return "\nError: Invalid Credentials\nNo Evaluation Avaliable\nExiting...\n"

def run_server():           #2-tier architecture connection between Server and Client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))  # Listen on all available interfaces (on port 5000)
    server_socket.listen(1)

    local_ip = socket.gethostbyname(socket.gethostname())       #find the local ip of the device and use that
    server_address = (local_ip, 5000)
    print(f'Server is running on \nIP: {local_ip}\nPORT: 5000') #show the ip and port so the client can connect manually

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data = client_socket.recv(1024)
        if not data:
            continue

        try:
            data_dict = json.loads(data.decode('utf-8'))
            response = handleClientData(data_dict)
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            client_socket.send(json.dumps({'error': str(e)}).encode('utf-8'))

        client_socket.close()



#run the server
if __name__ == '__main__':
    run_server()
