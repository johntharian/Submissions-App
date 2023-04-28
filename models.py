from datetime import date

from enum import Enum

from pydantic import BaseModel, Field, EmailStr


# input schema for user
class Userin(BaseModel):
    email: EmailStr
    password: str


# output schema for user
class Userout(BaseModel):
    id: str
    email: EmailStr


# enum for submission type
class SubmissionType(str, Enum):
    image = "image"
    file = "file"
    link = "link"


# input schema for hackathon
class HackathonIn(BaseModel):
    title: str = Field(example="AI Hack")
    description: str = Field(example="Hackathon  on AI")
    submissiontype: SubmissionType = Field(example="image")
    s_date: date = Field(example="2023-04-06")
    e_date: date = Field(example="2023-04-07")
    reward_price: str = Field(example="cash")
    bg_img: str = Field(example="dd.pmg")
    h_img: str = Field(example="dd.pmg")


# output schema for hackathon
class HackathonOut(HackathonIn):
    id: str = Field(example="1")


#  input schema for hackathon registrations
class HackathonRegistrationsIn(BaseModel):
    user_id: str = Field(example="3")
    hack_id: str = Field(example="2")


# output schema for hackathon registrations
class HackathonRegistrationsOut(HackathonRegistrationsIn):
    id: str = Field(example="2")


# input schema for submissions
class SubmissionsIn(BaseModel):
    user_id: str = Field(example="1")
    hack_id: str = Field(example="3")
    sub: str = Field(example="sdfsad")
    name: str = Field(example=" MNIST Classifier ")
    summary: str = Field(example="Classifies hanwritten images of digits from 0-9")
