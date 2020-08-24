from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api.contests.models import Contest, ContestFile, ContestParticipantAnswer

admin.site.register(ContestFile)
admin.site.register(ContestParticipantAnswer)


def evaluation(Answer):
    if Answer.contest.evaluationMethod == "ACCURACY":
        return


def finish_contest_and_assign_rank(modeladmin, request, queryset):
    for query in queryset:
        if not query.isFinished:
            messages.error(request, f'대회 {query.name}는 아직 종료되지 않았습니다. 대회를 종료시키려면 deadline을 변경하십시오.')
        contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest_id=query.id)
        contestParticipantAnswerSorted = sorted(contestParticipantAnswer,
                                                key=lambda contestAnswer: contestAnswer.rating, reverse=True)
        contestParticipantAnswerList = list(contestParticipantAnswerSorted)

        contestParticipantAnswerList[0].rank = 1
        contestParticipantAnswerList[0].save()

        # 동점자 체크를 위해 if 문을 몇 개 써 줌.
        if contestParticipantAnswerList[0].rating == contestParticipantAnswerList[1].rating:
            contestParticipantAnswerList[1].rank = 1
        else:
            contestParticipantAnswerList[1].rank = 2
        contestParticipantAnswerList[1].save()

        if contestParticipantAnswerList[1].rating == contestParticipantAnswerList[2].rating:
            if contestParticipantAnswerList[0].rating == contestParticipantAnswerList[1].rating:
                contestParticipantAnswerList[2].rank = 1
            else:
                contestParticipantAnswerList[2].rank = 2
        else:
            contestParticipantAnswerList[2].rank = 3
        contestParticipantAnswerList[2].save()

        # 상위 30%에게는 메달을 수여
        medalCutLine = int(round(len(contestParticipantAnswerList) * 0.3))
        for answer in contestParticipantAnswerList[3:medalCutLine]:
            if contestParticipantAnswerList[2].rating == answer.rating:
                answer.rank = 3
            else:
                answer.rank = 4
            answer.save()

        # 나머지에게는 대회가 끝났다는 것을 표시하기 위해 기존의 0이 아닌 5 값을 부여.
        for answer in contestParticipantAnswerList[medalCutLine:]:
            if contestParticipantAnswerList[medalCutLine - 1].rating == answer.rating:
                answer.rank = 4
            else:
                answer.rank = 5
            answer.save()


finish_contest_and_assign_rank.short_description = "순위/메달 부여하기"


class ContestResource(resources.ModelResource):
    class Meta:
        model = Contest


class ContestAdmin(ImportExportModelAdmin):
    resource_class = ContestResource
    actions = [finish_contest_and_assign_rank]


admin.site.register(Contest, ContestAdmin)
