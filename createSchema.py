import psycopg2
from config import config


# function to create the necesarry tables
def create_tables():
    """create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )
        """,
        """
        CREATE TABLE hackathons (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            background_image TEXT NOT NULL,
            hackathon_image TEXT NOT NULL,
            submission_type VARCHAR(10) NOT NULL,
            start_datetime TIMESTAMP NOT NULL,
            end_datetime TIMESTAMP NOT NULL,
            reward_prize VARCHAR(100) NOT NULL
            )
        """,
        """ CREATE TABLE registrations (
                id SERIAL PRIMARY KEY,
                hackathon_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL
            )
        """,
        """
            CREATE TABLE submissions (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                summary TEXT NOT NULL,
                submission TEXT NOT NULL,
                hackathon_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL
            )
        """,
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
