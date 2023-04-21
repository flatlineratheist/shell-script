from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class RegQuestionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('question_for', 'language','question_text','question_code')
    list_filter = ('question_code',)

class IFAAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    pass



# Question Module
#######################
admin.site.register(WAPILanguage,IFAAdmin)
admin.site.register(WAPIRoleName,IFAAdmin)
admin.site.register(WAPIValidationType,IFAAdmin)
admin.site.register(WAPIRegistrationStep,IFAAdmin)
admin.site.register(WAPIQuestion,IFAAdmin)
admin.site.register(WAPIQuestionType,IFAAdmin)
admin.site.register(WAPIQuesManagement,IFAAdmin)





admin.site.register(WAPIRegistration,IFAAdmin)
admin.site.register(RegASHA,IFAAdmin)
admin.site.register(RegANM,IFAAdmin)
admin.site.register(RegBeneficiary,IFAAdmin)
admin.site.register(WapiGame,IFAAdmin)
admin.site.register(WapiGameController,IFAAdmin)
admin.site.register(RegQuestion,RegQuestionAdmin)

