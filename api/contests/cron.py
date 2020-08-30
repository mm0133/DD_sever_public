from django.utils import timezone

from api.contests.models import Contest, ContestParticipantAnswer
import logging

logger = logging.getLogger("django")


def give_medal_auto():
    now = timezone.now()
    lecturePackage = LecturePackage.objects.get(pk=1)
    lecturePackage.hiNums += 1
    lecturePackage.save()

    logger.debug(f"give_medal_auto function is executed. dateTime: {now}")
    target_contest_ids = [contest.id for contest in Contest.objects.all() if
                          (not contest.isMedalGiven()) and (contest.isFinished())]
    contests = Contest.objects.filter(id__in=target_contest_ids)
    for contest in contests:
        contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest_id=contest.id)
        contestParticipantAnswerSorted = sorted(contestParticipantAnswer,
                                                key=lambda contestAnswer: contestAnswer.rating, reverse=True)
        cpaList = list(contestParticipantAnswerSorted)

        cpaList[0].rank = 1
        cpaList[0].save()

        # 동점자 체크를 위해 if 문을 몇 개 써 줌.
        if cpaList[0].rating == cpaList[1].rating:
            cpaList[1].rank = 1
        else:
            cpaList[1].rank = 2

        if cpaList[1].rating == cpaList[2].rating:
            if cpaList[0].rating == cpaList[1].rating:
                cpaList[2].rank = 1
            else:
                cpaList[2].rank = 2
        else:
            cpaList[2].rank = 3

        # 상위 30%에게는 메달을 수여
        # round: 반올림인데 0.5까지는 0으로 내림
        medalCutLine = int(round(len(cpaList) * 0.3))
        for answer in cpaList[3:medalCutLine]:
            if cpaList[2].rating == answer.rating:
                answer.rank = 3
            else:
                answer.rank = 4
            answer.save()

        # 나머지에게는 대회가 끝났다는 것을 표시하기 위해 기존의 0이 아닌 5 값을 부여.
        for answer in cpaList[medalCutLine:]:
            if cpaList[medalCutLine - 1].rating == answer.rating:
                answer.rank = 4
            else:
                answer.rank = 5
            answer.save()
