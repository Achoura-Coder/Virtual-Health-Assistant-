import requests
import pymongo
import logging
import bcrypt
"""
# MongoDB connection  
# In this section we are creating a part that will allow user to register with his account 
# Also allow users to manage appointments # We use the pymongo library 
# So this statement below is used to allow the server to store user data, possibility to shedule an appointment 
# and interact with him by way 

client = pymongo.MongoClient("mongodb://localhost:27017/")          # 27017 : default port for MongoDB  
                                                                    # IN sum this connection string has been used to specify the location and the port 
                                                                   # of the MongoDB we want to connect to
# MongoClient is class provided by PyMongo that allows me to here to create a connection to the MongoDB server 
# This statement below accesses  the "health_assistant" collection
# using this collection to insert docs, query data...
db = client["health_assistant"]                         # By using the client[] function, we can effectively navigate through the database hierarchy and interact 
users_collection = db["users"]                          # with specific databases and collections within our MongoDB server.
appointments_collection = db["appointments"]    

# API endpoint for retrieving health information
# SToring medical infos in this variable
HEALTH_API_URL = "https://api.healthprovider.com/health-info"

# Logging configuration
# basicConfig method is used to configure the logging system 
# And "INFO" means that the file will record general information msg 
logging.basicConfig(filename="assistant.log", level=logging.INFO)           # By using this statement we allow user to login in the VHA databases that will be stored in assistant.log file  

# Function to get health information based on a given query
def get_health_info(query):
#   response = requests.get(HEALTH_API_URL, params={'query': query})        # The params argument allows to pass the query in the url
#    if response.status_code == 200:
#        health_info = response.json()       # The Json() module parses if the response is correct or no
#        return health_info
#    else:
#        logging.error(f"Failed to retrieve health information. Status code: {response.status_code}")
#        return None
    
    try:
        response = requests.get(HEALTH_API_URL, params={'query': query})
        response.raise_for_status()  # Raises an exception for non-200 status codes
        health_info = response.json()
        return health_info
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve health information: {str(e)}")
        return None

#   Get health information based on a given query.

#    Args:
#        query (str): The query string to search for health information.

#    Returns:
#        dict or None: A dictionary containing the health information if successful, or None otherwise.
    
# ...


# Function to track symptoms
def track_symptoms(symptoms):
    # Implement the code to track symptoms
    # ...
    success = False

    # Perform necessary operations to track symptoms
    # For example, save the symptoms to a database or log them

    # Check if the tracking operation was successful
    if success:
        return "Symptoms tracked successfully."
    else:
        logging.error("Failed to track symptoms.")
        return "An error occurred while tracking symptoms. Please try again later."
    
    
#    try:
        # Perform necessary operations to track symptoms
        # For example, save the symptoms to a database or log them

        # Return a success message or perform additional actions
#       return "Symptoms tracked successfully."
#    except Exception as e:
#        # Log the error or handle it in an appropriate manner
#        logging.error(f"Failed to track symptoms: {str(e)}")
#        return "An error occurred while tracking symptoms. Please try again later."


# Function to schedule an appointment
# insert.one() is a function in PyMongo 
def schedule_appointment(user_id, date, time):
    appointment = {
        "user_id": user_id,
        "date": date,
        "time": time
            }
#   appointments_collection.insert_one(appointment)         # Appointment dictionary is seted into the appoitment_collection
#    return "Appointment accepted."                  # appointment_collection is an instance MongoDB where the appointent are stored 

    # Insert the appointment document into the appointments_collection
    result = appointments_collection.insert_one(appointment)
    # Check if the insertion was successful
    if result.acknowledged:
        return f"Appointment scheduled successfully with id {result.inserted_id}."
    else:
        logging.error(f"Failed to schedule appointment for user {user_id}.")
        return "An error occurred while scheduling appointment. Please try again later."


# Function to answer questions
def answer_question(question):
    # Implement the code to answer questions

    # This code is build for answering health-related questions
    if "symptoms" in question.lower():
        return "It's important to consult a healthcare professional for accurate diagnosis and guidance regarding symptoms."
    elif "healthy diet" in question.lower():
        return "A healthy diet should include a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats."
    elif "exercise" in question.lower():
        return "Regular exercise, such as aerobic activities, strength training, and flexibility exercises, is beneficial for overall health."
    else:
        return "I apologize, but I don't have the answer to that health-related question at the moment."

    # Placeholder code for answering questions related to health information
#    if "treatment" in question.lower():
#        return "Treatment options for specific health conditions vary and should be discussed with a healthcare professional."
#    elif "medication" in question.lower():
#        return "Prescription medications should be taken as directed by a healthcare professional. Do not self-medicate."
#    elif "prevention" in question.lower():
#        return "Preventive measures such as regular handwashing, vaccination, and healthy lifestyle choices can help maintain good health."
#    else:
#        return "I'm sorry, I don't have the information to answer that question. It's best to consult a healthcare professional for accurate advice."


# Function we used to give users possibility to register themselves
# We have used bcrypt library to secure the password hashing from attacks 
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_password
    }
    users_collection.insert_one(user)
    logging.info(f"New user registered: {username}")
    return "User registered successfully."

# Function to authenticate a user by checking wether the user information are true or no
# find.one() function is used to verify in the database the u_n and the p_w
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user:
        hashed_password = user["password"]
        if bcrypt.checkpw(password.encode(), hashed_password):
            return True
    return False

# Main function to handle user queries and route them to the appropriate functionality
def virtual_health_assistant(query, user_id):
    if query.lower() == "help":
        return "How can I assist you today?"
    elif query.lower() == "exit":
        return "I hope I will you again! Take care!"
    elif query.lower().startswith("get health info"):
        info_query = query[len("get health info"):].strip()         # we used strip() to ensure that any unnecessary space in the query 
        health_info = get_health_info(info_query)
        if health_info:
            return health_info
        else:
            return "Sorry, I couldn't have retrieved health information at the moment for you."
    elif query.lower().startswith("track symptoms"):
        symptoms = query[len("track symptoms"):].strip().split(",")
        response = track_symptoms(symptoms)
        return response
    elif query.lower().startswith("schedule appointment"):
        appointment_details = query[len("schedule appointment"):].strip().split(",")
        date = appointment_details[0].strip()
        time = appointment_details[1].strip()
        response = schedule_appointment(user_id, date, time)
        return response
    elif query.lower().startswith("answer question"):
        question = query[len("answer question"):].strip()
        answer = answer_question(question)
        return answer
    else:
        return "Sorry, I didn't understand your query. How can I assist you?"

# Example usage of the virtual_health_assistant function
if __name__ == "__main__":
    print("Welcome to the Virtual Health Assistant!")
    print("You can ask for help or type exit' to quit.")

    while True:
        user_query = input("User: ")

        if user_query.lower() == "register":
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = register_user(username, password)
        else:
            username = input("Enter username: ")
            password = input("Enter password: ")

            authenticated = authenticate_user(username, password)
            if authenticated:
                user_id = users_collection.find_one({"username": username})["_id"]
                response = virtual_health_assistant(user_query, user_id)
            else:
                response = "Authentication failed. Please try again or register a new account."

        print("Virtual Assistant:", response)

        # Log the user query and assistant response
        logging.info(f"User query: {user_query}")
        logging.info(f"Assistant response: {response}")

        if response.lower() == "goodbye! take care.":
            break



import logging
import bcrypt

# Logging configuration
logging.basicConfig(filename="assistant.log", level=logging.INFO)

# Function to answer questions
def answer_question(question):
    if "symptoms" in question.lower():
        return "It's important to consult a healthcare professional for accurate diagnosis and guidance regarding symptoms."
    elif "healthy diet" in question.lower():
        return "A healthy diet should include a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats."
    elif "exercise" in question.lower():
        return "Regular exercise, such as aerobic activities, strength training, and flexibility exercises, is beneficial for overall health."
    else:
        return "I apologize, but I don't have the answer to that health-related question at the moment."

# Function to track symptoms
def track_symptoms(symptoms):
    success = False

    # Perform necessary operations to track symptoms
    # For example, save the symptoms to a database or log them

    # Check if the tracking operation was successful
    if success:
        return "Symptoms tracked successfully."
    else:
        logging.error("Failed to track symptoms.")
        return "An error occurred while tracking symptoms. Please try again later."

# Function to schedule an appointment
def schedule_appointment(user_id, date, time):
    # Perform necessary operations to schedule an appointment
    # For example, save the appointment details to a database

    return "Appointment scheduled successfully."

# Function to register a user
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # Perform necessary operations to register the user
    # For example, save the user details to a database

    return "User registered successfully."

# Main function to handle user queries
def virtual_health_assistant(query, user_id=None):
    if query.lower() == "help":
        return "How can I assist you today?"
    elif query.lower() == "exit":
        return "I hope I will see you again! Take care!"
    elif query.lower().startswith("answer question"):
        question = query[len("answer question"):].strip()
        answer = answer_question(question)
        return answer
    elif query.lower().startswith("track symptoms"):
        symptoms = query[len("track symptoms"):].strip().split(",")
        response = track_symptoms(symptoms)
        return response
    elif query.lower().startswith("schedule appointment"):
        appointment_details = query[len("schedule appointment"):].strip().split(",")
        date = appointment_details[0].strip()
        time = appointment_details[1].strip()
        response = schedule_appointment(user_id, date, time)
        return response
    else:
        return "Sorry, I didn't understand your query. How can I assist you?"

# Example usage of the virtual_health_assistant function
if __name__ == "__main__":
    print("Welcome to the Virtual Health Assistant!")
    print("You can ask for help or type 'exit' to quit.")

    while True:
        user_query = input("User: ")

        if user_query.lower() == "register":
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = register_user(username, password)
        else:
            username = input("Enter username: ")
            password = input("Enter password: ")

            user_id = None  # Placeholder for user ID (fetch from database if authentication is implemented)
            response = virtual_health_assistant(user_query, user_id)

        print("Virtual Assistant:", response)

        # Log the user query and assistant response
        logging.info(f"User query: {user_query}")
        logging.info(f"Assistant response: {response}")

        if response.lower() == "i hope i will see you again! take care.":
            break
"""



import logging
import bcrypt

# Logging configuration
logging.basicConfig(filename="assistant.log", level=logging.INFO)

# Function to answer questions
def answer_question(question):
    if "symptoms" in question.lower():
        return "It's important to consult a healthcare professional for accurate diagnosis and guidance regarding symptoms."
    elif "healthy diet" in question.lower():
        return "A healthy diet should include a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats."
    elif "exercise" in question.lower():
        return "Regular exercise, such as aerobic activities, strength training, and flexibility exercises, is beneficial for overall health."
    else:
        return "I apologize, but I don't have the answer to that health-related question at the moment."

# Function to track symptoms
def track_symptoms(symptoms):
    success = False

    # Perform necessary operations to track symptoms
    # For example, save the symptoms to a database or log them

    # Check if the tracking operation was successful
    if success:
        return "Symptoms tracked successfully."
    else:
        logging.error("Failed to track symptoms.")
        return "An error occurred while tracking symptoms. Please try again later."

# Function to schedule an appointment
def schedule_appointment(user_id, date, time):
    # Perform necessary operations to schedule an appointment
    # For example, save the appointment details to a database

    return "Appointment scheduled successfully."

# Function to register a user
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # Perform necessary operations to register the user
    # For example, save the user details to a database

    return "User registered successfully."

# Main function to handle user queries
def virtual_health_assistant(query, user_id=None):
    if query.lower() == "help":
        return "How can I assist you today?"
    elif query.lower() == "exit":
        return "I hope I will see you again! Take care!"
    elif query.lower().startswith("answer question"):
        question = query[len("answer question"):].strip()
        answer = answer_question(question)
        return answer
    elif query.lower().startswith("track symptoms"):
        symptoms = query[len("track symptoms"):].strip().split(",")
        response = track_symptoms(symptoms)
        return response
    elif query.lower().startswith("schedule appointment"):
        appointment_details = query[len("schedule appointment"):].strip().split(",")
        date = appointment_details[0].strip()
        time = appointment_details[1].strip()
        response = schedule_appointment(user_id, date, time)
        return response
    else:
        return "Sorry, I didn't understand your query. How can I assist you?"

# Example usage of the virtual_health_assistant function
if __name__ == "__main__":
    print("Welcome to the Virtual Health Assistant!")
    print("You can ask for help or type 'exit' to quit.")

    while True:
        user_query = input("User: ")

        if user_query.lower() == "register":
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = register_user(username, password)
        else:
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Perform authentication here using username and password

            user_id = None  # Placeholder for user ID (fetch from database if authentication is implemented)
            response = virtual_health_assistant(user_query, user_id)

        print("Virtual Assistant:", response)

        # Log the user query and assistant response
        logging.info("User Query: %s", user_query)
        logging.info("Assistant Response: %s", response)

