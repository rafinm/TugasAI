import decision_tree
import random

class RFModel:
    def __init__(self, forest, accuracy, differences):
        self.forest = forest
        self.accuracy = accuracy
        self.differences = differences

def bagged(data):
    rand_num_features = random.randint(1,len(data[0])-1)
    feature_indices = []
    while rand_num_features != 0:
        random_feature_index = random.randint(0,len(data[0])-2)
        if random_feature_index not in feature_indices:
            feature_indices.append(random_feature_index)
        else:
            continue
        rand_num_features -= 1
    feature_indices.append(len(data[0])-1)
    bagged_data = [[data[0][i] for i in feature_indices]]
    
    for y in range(1,len(data)):
        index = random.randint(1,len(data)-1)
        bagged_data.append([data[index][i] for i in feature_indices])
    return bagged_data

def buildForest(original_data,acceptedAccuracy,numTrees):
    differences = [['Actual','Predicted']]
    data = sorted(original_data[1:], key = lambda x: random.random())
    data.insert(0,original_data[0])
    training_data = data[:int(.6*len(data))]
    testing_data = data[int(.6*len(data)):]
    testing_data.insert(0,data[0])
    forest = [decision_tree.buildTree(training_data)]
    for x in range(numTrees-2):
        forest.append(decision_tree.buildTree(bagged(training_data)))

    
    def model_accuracy(forest,testing_data):
        count = 0
        
        for y in range(1,len(testing_data)):
            input = {}
            
            for x in range(len(testing_data[0])-1):
                input.update({testing_data[0][x]:testing_data[y][x]})
            
            actual = testing_data[y][len(testing_data[y])-1]
            predictions = []
            
            for tree in forest:
                predictions.append(decision_tree.traverseTree(input,tree.node))
            distinct_prediction = {}
            
            for x in predictions:
                if not (isinstance(x,dict)):
                    if x not in distinct_prediction:
                        distinct_prediction.update({x:predictions.count(x)})
                    else:
                      continue
                else:
                    for i in x:
                        try:
                            val = distinct_prediction[i] + x[i]
                            distinct_prediction.pop(i,None)
                            distinct_prediction.update({i:val})
                        except KeyError:
                            continue
            predicted = max(distinct_prediction, key=distinct_prediction.get)
            differences.append([actual,predicted])
            
            if actual == predicted:
                count += 1
        return float(count)/float((len(testing_data)-1))

    accuracy = model_accuracy(forest,testing_data)
    if accuracy < acceptedAccuracy:
        print("Tes Akurasi Gagal: "+ str(round(accuracy*100,2))+"%" + " Dibuat ulang...")
        return buildForest(data,acceptedAccuracy,numTrees)
    else:
        print("Berhasil! Model dibuat dengan akurasi w/ " + str(round(accuracy*100,2)) + "%")
        forest.append(decision_tree.buildTree(data))
        return RFModel(forest,accuracy,differences)
