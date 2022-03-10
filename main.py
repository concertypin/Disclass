import os

import classroom
import firebase


def init():
    firebase.auth("disclass-firebase-adminsdk-wnq74-3c6c6e0162.json")
    classroom.auth()


def is_db_newest():
    # todo db가 coruseWork를 모두 저장하고 있는지, 맞다면 True, 아니라면 불러온 classwork를 리턴
    pass


def main():
    if os.environ.get("debug") == "1":
        classroom_id = [477778351857]
    else:
        classroom_id = [
            460066820906,
            460136699199,
            459940525576,
            477757652069,
            477540756060,
            474641815720,
            283588260982,
            468161643733,
            474859166281,
        ]
    for i in classroom_id:
    """req = is_db_newest()
    if req == True:
        return
    else:
        firebase.write(
    """


if __name__ == "__main__":
    init()
    main()
