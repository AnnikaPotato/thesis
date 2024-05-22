import pandas as pd
import numpy as np
import AHP_Priority_Vector_Calculation as pvc

from datetime import datetime


""" 
answer matrix:
    T       WP       OE     WE
T
WP
OE
WE

question sequence: T vs WP, T vs OE, T vs WE, WP vs OE, WP vs WE, OE vs WE
"""

def scoreTranslator(criteria: list, ahpAnswers: pd.DataFrame):
    ans = []

    for i in range(len(ahpAnswers)):
        ahp = pvc.AHP_Priority_Vector_Calculation().initializeAnswerMatrix(criteria)
        for j in range(len(ahpAnswers.columns)):
            idx1, idx2, response = pvc.ahpTextProcess(ahpAnswers.iat[i, j])
            ahp.setResponse((idx1, idx2), response)
        ahp.getPriorityVector()
        ans.append(ahp)

    return ans

def ahpReport(criteria, ahpAnswers, experience_col, role_col):
    experienceBasedWeights = dict()
    roleBasedWeights = dict()
    overallWeights = np.zeros(len(criteria) + 1)
    toWrite = []
    toWrite.append('ID,\tCR,\tT,\tWP,\tOE,\tWE,')

    allProcessedAhps = scoreTranslator(criteria, ahpAnswers)

    for i in range(len(allProcessedAhps)):
        ahp = allProcessedAhps[i]
        consistency = ahp.verifyConsistency(4)

        ans = [f"{i + 1},\t{'{:.4f}'.format(consistency)}"]
        for item in ahp.priorityVector:
            ans.append("{:.4f}".format(item))

        if consistency > 0.2:
            ans.append("ignored")
            toWrite.append(",\t".join(ans))
            continue

        toWrite.append(",\t".join(ans))
        individualResponse = ahp.priorityVector 

        overallWeights[:-1] += individualResponse
        overallWeights[-1] += 1

        if experience_col[i] not in experienceBasedWeights:
            experienceBasedWeights[experience_col[i]] = np.zeros(len(criteria) + 1)
        experienceBasedWeights[experience_col[i]][: -1] += individualResponse
        experienceBasedWeights[experience_col[i]][-1] += 1

        for item in role_col[i].strip().lower().split(";"):
            if not item: continue
            if item not in roleBasedWeights:
                roleBasedWeights[item] = np.zeros(len(criteria) + 1)
            roleBasedWeights[item][: -1] += individualResponse
            roleBasedWeights[item][-1] += 1

    overallWeights[:-1] /= overallWeights[-1]
    for key in experienceBasedWeights.keys():
        experienceBasedWeights[key][:-1] /= experienceBasedWeights[key][-1]
    for key in roleBasedWeights.keys():
        roleBasedWeights[key][:-1] /= roleBasedWeights[key][-1]


    ans = [f"\n\nOverall Weights"]
    for item in overallWeights[:-1]:
        ans.append("{:.4f}".format(item))
    ans.append('{:.0f}'.format(overallWeights[-1]))
    toWrite.append(",\t".join(ans))

    toWrite.append("\n\nExperience-based:")
    for key in experienceBasedWeights.keys():
        ans = [key]
        for item in experienceBasedWeights[key][:-1]:
            ans.append("{:.4f}".format(item))
        ans.append('{:.0f}'.format(experienceBasedWeights[key][-1]))
        toWrite.append(",\t".join(ans))


    toWrite.append("\n\nRole-based:")
    for key in roleBasedWeights.keys():
        ans = [key]
        for item in roleBasedWeights[key][:-1]:
            ans.append("{:.4f}".format(item))
        ans.append('{:.0f}'.format(roleBasedWeights[key][-1]))
        toWrite.append(",\t".join(ans))

    date = datetime.today().strftime('%Y-%m-%d')
    with open(f'AHP_Result_{date}.csv', 'w') as fhand:
        fhand.write("\n".join(toWrite))
