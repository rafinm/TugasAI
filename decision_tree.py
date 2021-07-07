from anytree import Node, RenderTree

def labels(data):
    l = list()
    col = len(data[0]) - 1
    for x in range(1, len(data)):
        l.append(data[x][col])
    return l

def generateQs(data):
    questions = dict()
    def uniqueFeatures(data, col):
        features = list()
        # Mulai loop dari y = 1 sehingga header diloncati
        for y in range(1, len(data)):
            if data[y][col] not in features:
                features.append(data[y][col])
        return features
    for x in range(len(data[0])-1):
        questions.update({data[0][x]:uniqueFeatures(data, x)})
    return questions

def partition(data, colName, question):
    fa, tr = [data[0]], [data[0]]
    if colName == None:
        return {True: [], False: []}
    col = data[0].index(colName)

    numeric = False
    if isinstance(question, int) or isinstance(question, float):
        numeric = True
    for y in range(1, len(data)):
        if numeric:
            if data[y][col] >= question:
                tr.append(data[y])
            else:
                fa.append(data[y])
        else:
            if data[y][col] == question:
                tr.append(data[y])
            else:
                fa.append(data[y])
    return {True: tr, False: fa}

def gini(data):
    if len(data) == 1:
        return 0
    l = labels(data)
    col = len(data[0]) - 1
    distinct = list()
    for x in l:
        if x not in distinct:
            distinct.append(x)
    sum = 0
    for x in distinct:
        p = (l.count(x)/float(len(l)))
        sum += p*(1-p)
    return sum

def leaf(data):
    if data == []:
        return True
    if gini(data) == 0:
        return True
    else:
        compare = data[1][0:len(data[1])-1]
        for y in range(1, len(data)):
            current = data[y][0:len(data[0])-1]
            if compare != current:
                return False
        return True

def predictions(leafData):
    if len(leafData) == 0:
        return dict()
    daft = labels(leafData)
    if daft.count(daft[0]) == len(daft):
        return daft[0]
    prediction = {}
    for x in daft:
        prediction.update({x:round((float(daft.count(x))/len(daft)),3)})
    return prediction

def bestQuestion(data):
    questions = generateQs(data)
    originalGini = gini(data)
    breakdown = []
    best = [0,None,None]
    for x in questions:
        for y in questions[x]:
            part = partition(data,x,y)
            false = part[False]
            true = part[True]
            length = len(false) + len(true) - 2
            g = float((((len(false)-1)/float(length))*gini(false)) + float((((len(true)-1)/float(length))*gini(true))))
            info = originalGini - g
            if info > best[0]:
                best = [info,x,y]
            elif info == best[0] and (isinstance(y,int) or isinstance(y,float)):
                best = [info,x,y]
    return best[1:]

def buildTree(data):
    head = Node(bestQuestion(data))
    def build(node,data):
        question = bestQuestion(data)
        try:
            parted = partition(data,question[0],question[1])
            false = parted[False]
            true = parted[True]
        #debugging
        except TypeError as err:
            print(data)
            print(err)
            return
        if leaf(false) and leaf(true):
            leafTrue = Node([True,predictions(true)],parent=node)
            leafFalse = Node([False,predictions(false)],parent=node)
            return RenderTree(head)

        elif leaf(false) and not leaf(true):
            leafFalse = Node([False,predictions(false)],parent=node)
            nodeTrue = Node([True,bestQuestion(true)],parent=node)
            return build(nodeTrue,true)

        elif not leaf(false) and leaf(true):
            leafTrue = Node([True,predictions(true)],parent=node)
            nodeFalse = Node([False,bestQuestion(false)],parent=node)
            return build(nodeFalse,false)

        elif not leaf(false) and not leaf(true):
            nodeTrue = Node([True,bestQuestion(true)],parent=node)
            nodeFalse = Node([False,bestQuestion(false)],parent=node)
            return build(nodeTrue,true) and build(nodeFalse,false)
    return build(head,data)

def checkConditional(input,conditional):
    if isinstance(conditional[len(conditional)-1],float) or isinstance(conditional[len(conditional)-1],int):
        if input[conditional[0]] >= conditional[len(conditional)-1]:
            return True
        else:
            return False
    else:
        if conditional == [None,None]:
            return False
        elif input[conditional[0]] == conditional[len(conditional)-1]:
            return True
        else:
            return False

def traverseTree(input,node):
    if node.parent == None:
        conditional = node.name
    else:
        conditional = node.name[1]
    if checkConditional(input,conditional):
        if node.children[0].name[0] == True:
            temp = node.children[0]
        else:
            temp = node.children[1]
        if len(temp.children) == 0:
            return temp.name[1]
        else:
            return traverseTree(input,temp)
    else:
        if node.children[0].name[0] == False:
            temp = node.children[0]
        else:
            temp = node.children[1]
        if len(temp.children) == 0:
            return temp.name[1]
        else:
            return traverseTree(input,temp)
