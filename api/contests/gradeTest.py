# 여기서 질의응답 list 받아서 평균점수 계산해서, 초중고 등급 판별.
# views에 할 계산을 아껴줌. 그냥 간이로 해놓음.
questionList = [{1, "당신의 이름은?"}, {2, "당신의 나이는?"}]


def mean(*args):
    return sum(args) / len(args)
