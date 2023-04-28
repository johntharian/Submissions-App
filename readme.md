# Submission-APP

submissions app where one can submit their hackathon submissions & see the list

Python version used : `3.9.7`

## Setup
1. Clone the repository 
2. Create a virtual environment
3. Install the requirements
4. Edit the `database.ini` file inside `Submissions-App` folder and make changes to the following variables
```bash
database=`url of database`
user=`username of database`
password=`password of database`

```
5. Run the `createSchema.py` inside the `Submissions-App` folder to create the required tables
```bash
cd Submissions-App
python createSchema.py

```

To install the required packages
```bash
pip  install -r requirements.txt
```
To Run the app
```bash
    uvicorn main:app --reload
```

The app will be availiable on http://localhost:8000

Go to http://localhost:8000/docs

## API Endpoints
<!-- 1. GET `/api/hackathons/` - -->
1. GET `/hackathons` -  Get all hackathons
2. POST `/createhackathon/` - Create a hackathon
3. POST `/registeruser` - Registers a User
4. GET `/users` - Shows all users
5. POST `/registerHackathon` - Registering for a hackathon
5. POST `/submit` - submits a user's submissions
6. GET `/user/{user_id}` - Get all hackathons user is participating in
7. GET `/user/{user_id}/{hack_id}` - Get a user's submissions