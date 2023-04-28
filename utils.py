import psycopg2
from config import config

from models import *


# connecting the db
def get_conn():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# helper function to execute a query
def insert(query, values):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, values)
    result = cur.fetchone()

    cur.close()
    conn.commit()
    return result


# helper function to execute a query
def get_data(query):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()

    cur.close()
    conn.commit()
    return result


# function to insert into hackathon table
def insert_into_hackathon(hackathon: HackathonOut):
    query = """
        INSERT INTO hackathons (title, description, background_image, hackathon_image, submission_type, start_datetime, end_datetime, reward_prize)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, title, description, background_image, hackathon_image, submission_type, start_datetime, end_datetime, reward_prize
        """
    values = (
        hackathon.title,
        hackathon.description,
        hackathon.bg_img,
        hackathon.h_img,
        hackathon.submissiontype,
        hackathon.s_date,
        hackathon.e_date,
        hackathon.reward_price,
    )
    result = insert(query, values)

    return dict(
        zip(
            (
                "id",
                "title",
                "description",
                "background_image",
                "hackathon_image",
                "submission_type",
                "start_datetime",
                "end_datetime",
                "reward_prize",
            ),
            result,
        )
    )


# function to get all hackathons
def get_all_hackathons():
    query = """
        SELECT id, title, description, background_image, hackathon_image, submission_type, start_datetime, end_datetime, reward_prize
        FROM hackathons
    """
    result = get_data(query)
    results = []
    fields = [
        "id",
        "title",
        "description",
        "background_image",
        "hackathon_image",
        "submission_type",
        "start_datetime",
        "end_datetime",
        "reward_prize",
    ]
    for hackathons in result:
        results.append(dict(zip(fields, hackathons)))
    return results


# function to insert into users table
def insert_into_users(user: Userin):
    query = """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        RETURNING id, email, password
    """
    values = (user.email, user.password)
    result = insert(query, values)

    return dict(zip(("id", "email", "password"), result))


# function to get all users
def get_all_users():
    query = """
        SELECT id, email FROM users
    """
    result = get_data(query)
    results = []
    fields = ["id", "email"]
    for users in result:
        results.append(dict(zip(fields, users)))
    return results


# function to check if a hackathon exists
def check_hackathon(hack_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id FROM hackathons WHERE id = %s
    """,
        (hack_id),
    )

    registrations = cur.fetchone()

    if registrations == None:
        flag = False
    else:
        flag = True

    conn.close()
    return flag


#  function to insert into registration table
def register_to_hackathon(registration: HackathonRegistrationsIn):
    query = """
        INSERT INTO registrations (hackathon_id, user_id)
        VALUES (%s, %s)
        RETURNING id, hackathon_id, user_id
    """
    values = (registration.hack_id, registration.user_id)
    result = insert(query, values)
    return dict(zip(("id", "hack_id", "user_id"), result))


# function to check if a  user registered to a hackathon
def check_user(sub: SubmissionsIn):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM registrations WHERE user_id = %s AND hackathon_id=%s
    """,
        (sub.user_id, sub.hack_id),
    )

    registrations = cur.fetchall()

    if len(registrations) > 0:
        f = True
    else:
        f = False

    conn.close()
    return f


# function to get submission type
def get_submissiontype(hack_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT submission_type FROM hackathons WHERE id = %s 
    """,
        (hack_id),
    )

    submissiontype = cur.fetchone()

    conn.close()

    return submissiontype


# function to insert into submissions table
def insert_to_submissions(submission: SubmissionsIn):
    query = """
        INSERT INTO submissions (name, summary, submission, hackathon_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, summary, submission, hackathon_id, user_id
        """
    values = (
        submission.name,
        submission.summary,
        submission.sub,
        submission.hack_id,
        submission.user_id,
    )
    result = insert(query, values)

    return dict(
        zip(("id", "name", "summary", "submission", "hackathon_id", "user_id"), result)
    )


# function to get all hackathons a user registered to


def get_all_user_hackathons(user_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT hackathon_id,title,description FROM hackathons JOIN registrations ON hackathons.id = registrations.hackathon_id WHERE registrations.user_id = %s 
    """,
        (user_id),
    )

    result = cur.fetchall()
    results = []
    fields = ["hackathon_id", "title", "description"]
    for data in result:
        results.append(dict(zip(fields, data)))
    if results == []:
        return {"user did not register for any  hackathon"}
    return results


# function to get the user  submissions
def get_user_submissions(user_id: str, hack_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT hackathon_id,title,name, summary,submission FROM hackathons JOIN submissions ON hackathons.id = submissions.hackathon_id WHERE submissions.user_id = %s 
    """,
        (user_id),
    )

    result = cur.fetchall()
    results = []
    fields = ["hackathon_id", "title", "name", "summary", "submission"]
    for data in result:
        results.append(dict(zip(fields, data)))
    if results == []:
        return {"user did not register for any  hackathon"}
    return results
