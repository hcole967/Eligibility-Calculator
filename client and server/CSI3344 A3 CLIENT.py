#Distributed Systems Assignment 3 CLIENT
#made by:
#Harrison Cole, 10632167
#James Scott, 981832

#Using an RPC method, a combination between Synchronous and Asynchronous system design (recommendation (ii))

import socket
import json
 

#send relevent data to the server side in the form of a dictionary
def send_request(OUST, numUnits, student_id, email, units, authUser, authPassword, server_address):
    if OUST == False:           #if answer is 'n' to the OUST prompt
        data = {
            "OUST" : OUST,
            "numUnits" : numUnits,
            "username" : authUser,
            "password" : authPassword,
            "student_id": student_id,
            "email": email,
            "units": dict(units)
        }
    else:                       #if answer is 'y' to the OUST prompt
        data = {
            "OUST" : OUST,
            "numUnits" : numUnits,
            "username" : authUser,
            "password" : authPassword,
            "student_id": student_id,
            "email": email
        }

    # ---------- Connection code to connect Client to Server (Phase 1) ----------

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    client_socket.send(json.dumps(data).encode('utf-8'))

    response = client_socket.recv(1024)
    client_socket.close()

    serverload = json.loads(response.decode('utf-8'))
    return serverload





if __name__ == '__main__':
    try:
        #info to put into the socket connection above
        server_ip = input("Enter Server IP Address: ")
        server_port = int(input("Enter Server Port Number: "))
        server_address = (server_ip, server_port)
    except ValueError:      #if the port is not a number
        print("System failed to connect\nExiting...\n")
        exit()
#------------------------------------------------------------------------
    authUser = "Admin"                                                 #|
    username = input("Enter your authenticator username: ")            #|
    authPass = "Admin1"                                                #|       AUTHENTICATION
    if username == authUser:                                           #|       TO START THE
        password = input ("Enter your authenticated password: ")       #|       SYSTEM
#------------------------------------------------------------------------
        if password == authPass:
            print("\nAuthentication Complete\n")  
            numUnits = None
            email = None
            units = {}
            auth = input("Are you a former or current OUST student? (Y/N): ")
            if auth.lower() == 'y':                   # FOR PHASE 2
                OUST = True
            elif auth.lower() == 'n':                   # FOR PHASE 1
                OUST = False
                print("\nFollow the next steps to enter your scores")              
            else:
                print("Invalid string entered")
                exit()
        else:
            print("Authentication Failed.\nExiting system...")
            exit()
    else:
        print("Authentication Failed.\nExiting system...")
        exit()

    

# ---------- STRICTLY FOR PHASE 1 (NON-OUST) ------------
    
    if OUST == False:
        student_id = input("Enter your 8-digit Student ID: ")
        if len(student_id) > 8:
            print("Student ID is too long, try again") 
        else:
            
            First_Name = input("Enter your first name: ") 
            Last_Name = input("Enter your surname: ")
            email = input("Enter Email Address: ")

            units = {}
            numUnits = int(input("How many units did you complete?: "))
            for i in range(numUnits):
                while True:
                    unitCode = input("Enter the unit code: ")
                    if len(unitCode) > 7:
                        print("Unrecognisable unit code, enter a code of up to 7 digits.")
                    else:
                        break
                while True:
                    grade = float(input("Enter the achieved grade: "))
                    if grade < 0 or grade > 100:
                        print("Grade is not possible, please try again")
                    else:
                        break
                units[unitCode] = grade
                
            
                
            result = send_request(OUST, numUnits, student_id, email, units, First_Name, Last_Name, server_address)
            print("\nDictionary after user input: \n", end='')
            for unitCode, grade in units.items():
                print("{", f"'{unitCode}': {grade} ", end='')
                print("};")
            print("\n-------------- HEPaS Result --------------\n")
            print(f"Results for {First_Name} {Last_Name}, {email}")
            print(result)
    
# ---------- STRICTLY FOR PHASE 2 (OUST) ------------

    else:
        
        student_id = input("Enter your 8-digit Student ID: ")
        if len(student_id) > 8:
            print("Student ID is too long, try again") 
        else:
            First_Name = input("Enter your first name: ") 
            Last_Name = input("Enter your surname: ")
            email = input("Enter Email Address: ")
            try:
                result = send_request(OUST, None, student_id, email, None, First_Name, Last_Name, server_address)
                print("\n-------------- HEPaS Result --------------\n")
                print(f"Results for {First_Name} {Last_Name}, {email}")
                print(result)
            except json.JSONDecodeError or ConnectionRefusedError:
                print("System Failure, Possible Invalid Entry\nExiting...\n")
                
        

            
                
            
            

