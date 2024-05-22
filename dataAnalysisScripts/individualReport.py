import pandas as pd
import AHP_AnalysisRunner
import SAW_AnalysisRunner

from datetime import datetime

def getIndividualReport():
    toPrint = ['id']
    for item in SAW_AnalysisRunner.aspects:
        toPrint.append(item)
    toPrint.append('\n')

    for i in range(len(allProcessedSaws)):
        ahpPtr = -1
        toPrint.append(str(i + 1))

        for j in range(len(allProcessedSaws[0])):
            if (j in SAW_AnalysisRunner.higherLevel):
                ahpPtr += 1
            score = allProcessedAhps[i].priorityVector[ahpPtr] * allProcessedSaws[i][j].value
            toPrint.append("{:.4f}".format(score))
        toPrint.append('\n')

    date = datetime.today().strftime('%Y-%m-%d')
    with open(f'Individual_Report_{date}.csv', 'w') as fhand:
        fhand.write("\t".join(toPrint))

df = pd.read_excel("Factors Influencing Developer Velocity(1-50).xlsx")

ahpAnswers = df.iloc[:, -7:-1]
sawAnswers = df.iloc[:, 10: 29]

ahpCriteria = ("T", "WP", "OE", "WE")
AHP_AnalysisRunner.ahpReport(ahpCriteria, ahpAnswers, df.iloc[:, 6], df.iloc[:, 8])

ignoreAnswers = set([1, 2, 3, 15, 19, 32, 34, 37, 41])
SAW_AnalysisRunner.sawReport(sawAnswers, ignoreAnswers)

allProcessedAhps = AHP_AnalysisRunner.scoreTranslator(ahpCriteria, ahpAnswers)
allProcessedSaws, _ = SAW_AnalysisRunner.scoreTranslator(sawAnswers, None)
getIndividualReport()