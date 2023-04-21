def selectGujrantQuestionText(roleName,textLang,queryCode):
    dataT = RegQuestion.objects.get(question_for=roleName,language=textLang,question_code=queryCode)
    return dataT.question_text
