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


def contestParticipantAnswerFilePath(instance, filename):
    return f'contests/ContestParticipantAnswer/file/user{instance.writer.id}-contest{instance.contest}/{uuid4().hex}/{instance.id}_{uuid4().hex}/{filename}'


