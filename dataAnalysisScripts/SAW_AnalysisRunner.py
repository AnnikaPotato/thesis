import numpy as np
import SAW as s

from datetime import datetime

""" 
Technology: system architecture, data structure, infrastructure & platform, testing, tools

Working Practice: code review, secruity test, compliance checking, wheels available

Organizational Enablement: frequency of cross-functional pods, ability to deliver expected goals, capabilities of managers, requirement understanding, culture, talent management

Work environment: wfh, planning of the workplace, happiness
"""

def scoreTranslator(rawAnswers, ignoreAnswers = None):
    if rawAnswers is None:
        raise ValueError("rawAnswers should not be None")
    
    numPeople = len(rawAnswers) - len(ignoreAnswers) if ignoreAnswers is not None else len(rawAnswers)
    numAspects = len(aspects)
    overallResponse = np.ndarray(shape=(numPeople, numAspects), dtype=float)
    ids = []

    peoplePtr = 0
    for i in range(len(rawAnswers)):
        if (ignoreAnswers != None) and (i in ignoreAnswers):
            print(f"ignore No.{i + 1} answer due to inconsitency") 
            continue

        ids.append(i)
        for j in range(numAspects):
            overallResponse[peoplePtr, j] = s.textProcess(rawAnswers.iat[i, j], reversedQuestion[j]).value
        
        peoplePtr += 1

    return overallResponse, ids


def sawReport(rawAnswers, ignoreAnswers):
    overallResponse, ids = scoreTranslator(rawAnswers, ignoreAnswers)

    toWrite = ["Individual Response:"]
    for r, row in enumerate(overallResponse):
        tmpStr = [str(ids[r] + 1)]
        for _, val in enumerate(row):
            tmpStr.append('{:.2f}'.format(val))
        toWrite.append(f'{",\t".join(tmpStr)}')
    
    sawScores = np.sum(overallResponse, axis=0) / np.sum(overallResponse)
    
    higherLevelPtr = 0
    for idx, val in enumerate(aspects):
        if idx in higherLevel:
            toWrite.append(f"\n{higherLevelNames[higherLevelPtr]}")
            higherLevelPtr += 1
        toWrite.append(f"{val}\t{'{:.5f}'.format(sawScores[idx])}")

    date = datetime.today().strftime('%Y-%m-%d')
    with open(f'SAW_Result_{date}.csv', 'w') as fhand:
        fhand.write("\n".join(toWrite))

aspects = (
    'Application Architecture',
    'Data Architecture',
    'Using Cloud',
    'Change Deployment',
    'DevOps Tools',
    'Test Automation',

    'Code Review',
    'Security Test',
    'Compliance Check',
    'Wheels Available',

    'Cross-functional Pods',
    'Expected Goal Delivery',
    'Team Culture',
    'Manager Management Capability',
    'Requirement Understanding',
    'Talent Management',

    'Remote Working',
    'Office Plan',
    'Happiness'
)

reversedQuestion = (
    False, True, False, True, False, True,
    False, False, False, False,
    True, False, True, False, False, True,
    True, False, False
)

higherLevel = (0, 6, 10, 16, 19)
higherLevelNames = ('Technology', 
                    'Work Practice', 
                    'Organizational Enablement', 
                    'Working Environment')