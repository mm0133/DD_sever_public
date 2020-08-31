from django.contrib import admin

from api.educations.models import EduVideoLecture, LecturePackage, LecturePackageComment, EduVideoLectureComment

admin.site.register(EduVideoLecture)
admin.site.register(LecturePackage)
admin.site.register(LecturePackageComment)
admin.site.register(EduVideoLectureComment)