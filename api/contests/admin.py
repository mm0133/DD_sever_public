from django.contrib import admin, messages
from django.shortcuts import get_object_or_404
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api.contests.models import Contest, ContestFile, ContestParticipantAnswer

admin.site.register(ContestFile)
admin.site.register(ContestParticipantAnswer)


def finish_contest_and_assign_rank(modeladmin, request, queryset):
    for query in queryset:
        if not query.isFinished:
            messages.error(request, f'대회 {query.name}는 아직 종료되지 않았습니다. 대회를 종료시키려면 deadline을 변경하십시오.')
        contest_id = query.id
        contest = get_object_or_404(Contest, pk=contest_id)
        if contest.evaluationMethod == "Accuracy":
            contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest=contest).order_by('-accuracy')
        # 인기도 평가의 경우
        else:
            contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest=contest).order_by('-likes.count')
        contestParticipantAnswerList = list(contestParticipantAnswer)
        contestParticipantAnswerList[0].rank = 1
        contestParticipantAnswerList[1].rank = 2
        contestParticipantAnswerList[2].rank = 3

        # 상위 30%에게는 메달을 수여
        medalCutLine = int(round(len(contestParticipantAnswerList) * 0.3))
        for answer in contestParticipantAnswerList[3:medalCutLine]:
            answer.rank = 4
        for answer in contestParticipantAnswerList[medalCutLine:]:
            answer.rank = 5


finish_contest_and_assign_rank.short_description = "순위/메달 부여하기"


class ContestResource(resources.ModelResource):
    class Meta:
        model = Contest


class ContestAdmin(ImportExportModelAdmin):
    resource_class = ContestResource
    actions = [finish_contest_and_assign_rank]


admin.site.register(Contest, ContestAdmin)