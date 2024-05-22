class SAW_Instance():
    def __init__(self, value:float, count = 1) -> None:
        self.value = value
        self.count = count
        pass

    def add(self, toAdd) -> None:
        self.value += toAdd.value
        self.count += toAdd.count
        return
    
    def divideBy(self, item) -> None:
        self.value /= item.value
        return

    def getString(self):
        tmpStr = ['{:.4f}'.format(self.value)]
        tmpStr.append('{:.0f}'.format(self.count))
        return ",\t".join(tmpStr)

def getAverageItem(item:SAW_Instance):
    if item.count > 1:
        return SAW_Instance(item.value / item.count,
                            item.count)
    return item

def addAll(items):
    ans = SAW_Instance(0, 0)
    for item in items:
        ans.add(item)
    return ans


def textProcess(choice: str, reversed: bool) -> SAW_Instance:
    choiceSets = (
        {"strongly disagree": 0,
        "somewhat disagree": 1,
        "neutral": 2,
        "somewhat agree": 3,
        "strongly agree": 4
        },
        {"very low": 0,
        "low": 1,
        "medium": 2,
        "very high": 4
        })
    
    scores = (0, 0.3, 0.5, 0.7, 1)
    
    choice = choice.strip().lower()
    if choice == "high":
        return buildSAW(scores[3], reversed)

    for i in range(len(choiceSets)):
        if choice in choiceSets[i].keys():
            return buildSAW(scores[choiceSets[i][choice]], reversed)
        
def buildSAW(score, reversed:bool) -> SAW_Instance:
    if reversed:
        return SAW_Instance(1 - score, 1)
    else:
        return SAW_Instance(score, 1)
    