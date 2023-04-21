from django.db import models

class WAPILanguage(models.Model):
    name = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class WAPIRoleName(models.Model):
    role_name = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.role_name

class WAPIValidationType(models.Model):
    validationname = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.validationname

class WAPIRegistrationStep(models.Model):
    resgistration_step = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.validationname



class WAPIQuestionType(models.Model):
    questionText = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.questionText

class WAPIQuestion(models.Model):
    lang = models.ForeignKey(WAPILanguage,on_delete=models.CASCADE,default = None)
    questionType = models.ForeignKey(WAPIQuestionType,on_delete=models.CASCADE,default = None)
    ques_validation = models.ForeignKey(WAPIValidationType,on_delete=models.CASCADE,default = None)
    answer_text_length = models.CharField(max_length=30,null=True,default = 'NA')
    question = models.TextField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('lang', 'questionType', 'ques_validation','answer_text_length','question')
    def __str__(self):
        return self.question
    

class WAPIQuesManagement(models.Model):
    lang = models.ForeignKey(WAPILanguage,on_delete=models.CASCADE)
    roleName = models.ForeignKey(WAPIRoleName,on_delete=models.CASCADE)
    reg_step = models.ForeignKey(WAPIRegistrationStep,on_delete=models.CASCADE)
    question = models.ForeignKey(WAPIQuestion,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('lang', 'roleName','reg_step','question')
    def __str__(self):
        return self.question


# class WAPIBeneficiaryQuestion(models.Model):
#     name = models.CharField(max_length=30,null=True,default = 'NA')
#     reg_mobile = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
#     reg_role = models.CharField(max_length=30,null=True,default = 'NA')
#     reg_status = models.CharField(max_length=30,null=True,default = 'NA')
#     language = models.CharField(max_length=30,null=True,default = 'NA')
#     current_stage = models.CharField(max_length=30,null=True,default = 'NA')
#     request_for_previous_stage = models.CharField(max_length=30,null=True,default = 'NA')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    








class WAPIRegistration(models.Model):
    name = models.CharField(max_length=30,null=True,default = 'NA')
    reg_mobile = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    reg_role = models.CharField(max_length=30,null=True,default = 'NA')
    reg_status = models.CharField(max_length=30,null=True,default = 'NA')
    language = models.CharField(max_length=30,null=True,default = 'NA')
    current_stage = models.CharField(max_length=90,null=True,default = 'NA')
    request_for_previous_stage = models.CharField(max_length=30,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + "       "+self.reg_mobile

class RegASHA(models.Model):
    place = models.OneToOneField(WAPIRegistration,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=30,null=True,default = 'NA')
    mobile_number = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    state = models.CharField(max_length=30,null=True,default = 'NA')
    district =models.CharField(max_length=30,null=True,default = 'NA')
    block = models.CharField(max_length=30,null=True,default = 'NA')
    village = models.CharField(max_length=30,null=True,default = 'NA')
    village_population = models.CharField(max_length=30,null=True,default = 'NA')
    facility_name = models.CharField(max_length=30,null=True,default = 'NA')
    no_pragnant_women = models.CharField(max_length=30,null=True,default = 'NA')
    

    first_trimester = models.CharField(max_length=30,null=True,default = 'NA')
    second_third_trimester = models.CharField(max_length=30,null=True,default = 'NA')
    no_lactating_women = models.CharField(max_length=30,null=True,default = 'NA')
    lakshit_dumpati = models.CharField(max_length=30,null=True,default = 'NA')
    no_ifa = models.CharField(max_length=30,null=True,default = 'NA')
    no_cal = models.CharField(max_length=30,null=True,default = 'NA')
    no_folic_acid = models.CharField(max_length=30,null=True,default = 'NA')


    no_wra_women = models.CharField(max_length=30,null=True,default = 'NA')
    existing_stock = models.CharField(max_length=30,null=True,default = 'NA')
    estimated_stock = models.CharField(max_length=30,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class RegANM(models.Model):
    place = models.OneToOneField(WAPIRegistration,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=30,null=True,default = 'NA')
    mobile_number = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    state = models.CharField(max_length=30,null=True,default = 'NA')
    district =models.CharField(max_length=30,null=True,default = 'NA')
    block = models.CharField(max_length=30,null=True,default = 'NA')
    facility_name = models.CharField(max_length=30,null=True,default = 'NA')
    id_number = models.CharField(max_length=30,null=True,default = 'NA')
    no_pragnant_women = models.CharField(max_length=30,null=True,default = 'NA')
    
    first_trimester = models.CharField(max_length=30,null=True,default = 'NA')
    second_third_trimester = models.CharField(max_length=30,null=True,default = 'NA')
    no_lactating_women = models.CharField(max_length=30,null=True,default = 'NA')
    lakshit_dumpati = models.CharField(max_length=30,null=True,default = 'NA')
    no_ifa = models.CharField(max_length=30,null=True,default = 'NA')
    no_cal = models.CharField(max_length=30,null=True,default = 'NA')
    no_folic_acid = models.CharField(max_length=30,null=True,default = 'NA')

    annual_pragnant_women = models.CharField(max_length=30,null=True,default = 'NA')
    annual_lactating_women = models.CharField(max_length=30,null=True,default = 'NA')
    annual_lakshit_women = models.CharField(max_length=30,null=True,default = 'NA')


    no_wra_women = models.CharField(max_length=30,null=True,default = 'NA')
    existing_stock = models.CharField(max_length=30,null=True,default = 'NA')
    estimated_stock = models.CharField(max_length=30,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class RegBeneficiary(models.Model):
    place = models.OneToOneField(WAPIRegistration,on_delete=models.CASCADE,primary_key=True)
    rch_number = models.CharField(max_length=30,null=True,default = 'NA')
    name = models.CharField(max_length=30,null=True,default = 'NA')
    mobile_number = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    age = models.CharField(max_length=30,null=True,default = 'NA')
    state = models.CharField(max_length=30,null=True,default = 'NA')
    district =models.CharField(max_length=30,null=True,default = 'NA')
    block = models.CharField(max_length=30,null=True,default = 'NA')
    village = models.CharField(max_length=30,null=True,default = 'NA')
    user_type = models.CharField(max_length=30,null=True,default = 'NA')
    hb_count = models.CharField(max_length=30,null=True,default = 'NA')
    user_type_status = models.CharField(max_length=30,null=True,default = 'NA')
    pragnancy_month = models.CharField(max_length=30,null=True,default = 'NA')
    health_checkup_status = models.CharField(max_length=30,null=True,default = 'NA')
    ifa_tablet_status = models.CharField(max_length=30,null=True,default = 'NA')
    calcium_tablet_status = models.CharField(max_length=30,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)




QUESTION_ROLE_TYPE = (
    ('ALL','ALL'),
    ('ASHA', 'ASHA'),
    ('ANM','ANM'),
    ('BENEFICIARY','BENEFICIARY'),

)

LANGUAGE_TYPE = (
    ('HINDI','HINDI'),
    ('ENGLISH', 'ENGLISH'),
    ('GUJRATI','GUJRATI'),
)



class RegQuestion(models.Model):
    question_for = models.CharField(max_length=50, choices=QUESTION_ROLE_TYPE,default = 'NA')
    language = models.CharField(max_length=50, choices=LANGUAGE_TYPE,default = 'NA')
    question_text = models.TextField(default = 'NA')
    question_code = models.CharField(max_length=30,null=True,unique=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    # ######################################################################################################
    #########################################################################################################

class WapiGame(models.Model):
    language = models.CharField(max_length=50, choices=LANGUAGE_TYPE,default = 'NA')
    questionNo = models.TextField(null=True,unique=True,default = 'NA')
    questionText = models.TextField(null=True,default = 'NA')
    optionOne = models.CharField(max_length=80,null=True,default = 'NA')
    optionTwo = models.CharField(max_length=80,null=True,default = 'NA')
    optionThree = models.CharField(max_length=80,null=True,default = 'NA')
    optionFour = models.CharField(max_length=80,null=True,default = 'NA')
    rightAnswer = models.CharField(max_length=80,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class WapiGameController(models.Model):
    place = models.OneToOneField(WAPIRegistration,on_delete=models.CASCADE,primary_key=True)
    level = models.CharField(max_length=80,null=True,default = 'NA')
    total_win = models.CharField(max_length=80,null=True,default = 'NA')
    total_score = models.CharField(max_length=80,null=True,default = 'NA')
    total_rightAnswer = models.CharField(max_length=80,null=True,default = 'NA')
    total_wrongAnswer = models.CharField(max_length=80,null=True,default = 'NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

