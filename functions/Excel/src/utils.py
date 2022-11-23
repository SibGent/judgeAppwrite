def getScore(scoreList, judgeIds, competitorId):
    result = {}
       
    for judgeId in judgeIds:
        for score in scoreList:
            if (score['judgeId'] == judgeId and score['competitorId'] == competitorId):
                result[judgeId] = score['value']
                break
            
    return result


def getDeduction(deductionList, arbitratorIds, competitorId):
    result = {}
       
    for arbitratorId in arbitratorIds:
        for score in deductionList:
            if (score['arbitratorId'] == arbitratorId and score['competitorId'] == competitorId):
                result[arbitratorId] = score['value']
                break
            
    return result


def getMeanScore(scoreDic):
    s = sum(scoreDic.values())
    l = len(scoreDic)
    return  float(s) / l


def getTotal(meanArtistic, meanExecution, meanDifficult, deduction):
    return meanArtistic + meanExecution + meanDifficult - sum(deduction.values())