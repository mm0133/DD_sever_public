import os
from uuid import uuid4


def customProfileImagePath(instance, filename):
    return f'users/CustomProfile/image/user{instance.user.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}.jpeg'


def customProfileSmallImage(instance, filename):
    return f'users/CustomProfile/smallImage/user{instance.user.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}'


def teamImagePath(instance, filename):
    return f'users/Team/image/team{instance.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}'


def teamSmallImagePath(instance, filename):
    return f'users/CustomProfile/smallImage/team{instance.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}'


def contestFileFilePath(instance, filename):
    extension = os.path.splitext(filename)[-1].lower()
    return f'contests/ContestFile/file/contest{instance.contest}/{filename}'


def contestContestAnswerPath(instance, filename):
    extension = os.path.splitext(filename)[-1].lower()
    return f'contests/Contest/contestAnswer/contest{instance.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}{extension}'


def contestProfileThumbPath(instance, filename):
    return f'contests/Contest/contestProfileThumb/contest{instance.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}'


def contestBackThumbPath(instance, filename):
    return f'contests/Contest/contestBackThumb/contest{instance.id}/{uuid4().hex}/{instance.id}_{uuid4().hex}'


def contestParticipantAnswerFilePath(instance, filename):
    # 개인 제출과 팀 제출을 구분함. 안 그러면 instance 에 user 나 team 이 없을 경우 error 가 발생함
    if instance.user:
        return f'contests/ContestParticipantAnswer/file/user{instance.user.id}-contest{instance.contest}/{uuid4().hex}\
        /{instance.id}_{uuid4().hex}/{filename}'
    else:
        return f'contests/ContestParticipantAnswer/file/team{instance.team.id}-contest{instance.contest}/{uuid4().hex}\
        /{instance.id}_{uuid4().hex}/{filename}'
