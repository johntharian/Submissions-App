from datetime import date, datetime

from enum import Enum
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Any, Union
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import Annotated

from models import *
from utils import *

app = FastAPI()


# POST endpoint to create a new hackathon
@app.post(
    "/createhackathon/",
    summary="Create a hacathon",
    description="Authorized users can create a hackathon",
)
async def createHackathon(
    title: str = Form(...),
    description: str = Form(...),
    submissiontype: SubmissionType = Form(...),
    s_date: str = Form(...),
    e_date: str = Form(...),
    reward_price: str = Form(...),
    bg_img: UploadFile = File(...),
    h_img: UploadFile = File(...),
):
    return insert_into_hackathon(
        HackathonIn(
            title=title,
            description=description,
            submissiontype=submissiontype,
            s_date=datetime.strptime(
                s_date, "%Y-%m-%d"
            ).date(),  # converts string to date
            e_date=datetime.strptime(e_date, "%Y-%m-%d").date(),
            reward_price=reward_price,
            bg_img=bg_img.filename,
            h_img=h_img.filename,
        )
    )


# GET endpoint to retrive all hackathons
@app.get("/hackathons")
async def getAllHackathons() -> List[HackathonOut]:
    return get_all_hackathons()


# POST endpoint to register a user
@app.post("/registeruser", response_model=Userout)
async def registerUser(user: Userin) -> Any:
    return insert_into_users(user)


# GET endpoint to retrieve all users
@app.get("/users")
async def getllUsers() -> List[Userout]:
    return get_all_users()


# POST endpoint to register a user for a hackathon
@app.post("/registerHackathon")
async def register(registration: HackathonRegistrationsIn):
    if check_hackathon(registration.hack_id):
        return register_to_hackathon(registration)
    else:
        return {"hackathon does not exist"}


# POST endpoint to submit a user's entry to a hackathon
@app.post("/submit")
async def submissions(sub: SubmissionsIn):
    # check if user registered for hackathon
    if check_user(sub):
        # Determine submission type based on hackathon submission type
        if get_submissiontype(sub.hack_id)[0] == "file":
            submissiontype = "file"
        elif get_submissiontype(sub.hack_id)[0] == "image":
            submissiontype = "image"
        elif get_submissiontype(sub.hack_id)[0] == "link":
            submissiontype = "link"

        return insert_to_submissions(sub)
    else:
        return {"user not registered for hackathon"}


# GET endpoint to retrieve all hackathons a particular user has registered for
@app.get("/user/{user_id}")
async def user_registrations(user_id: str):
    return get_all_user_hackathons(user_id)


# GET endpoint to retrieve all submissions a particular user has made for a particular hackathon
@app.get("/user/{user_id}/{hack_id}")
async def user_submissions(user_id: str, hack_id: str):
    return get_user_submissions(user_id, hack_id)
