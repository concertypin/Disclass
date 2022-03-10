import os

# noinspection PyPackageRequirements
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly"]
creds = None
service = None


class ClassroomNotReady(Exception):
    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "creds or service is None. call classroom.auth() to fix these."

    def __str__(self):
        return self.msg


def is_ready(msg=None):
    if creds is None or service is None:
        raise ClassroomNotReady(msg)


def auth(
    redirect_port: int = 1108,
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
) -> None:
    global creds
    global service

    # noinspection DuplicatedCode
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # (creds is existing) and (creds is expired) and (refresh_token is existing)
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=redirect_port)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    service = build("classroom", "v1", credentials=creds)


# noinspection PyUnresolvedReferences
def list_course(max_size: int = 50) -> list:
    global service
    is_ready()
    # Call the Classroom API
    results = service.courses().list(pageSize=max_size).execute()
    courses = results.get("courses", [])

    if not courses:  # if there is no courses
        return []

    r = []
    for course in courses:
        r.append(course)  # put each course in the list r
    return r


def list_coursework(course_id, max_size=50):
    # noinspection PyUnresolvedReferences
    return (
        service.courses()
        .courseWork()
        .list(courseId=str(course_id), pageSize=max_size)
        .execute()["courseWork"]
    )
