import random
import logging
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("ann_test.log"),
                              logging.StreamHandler()])

class ANN(Sequential):
    def __init__(self, child_weights=None):
        super().__init__()

        if child_weights is None:
            layer1 = Dense(8, input_shape=(8,), activation='sigmoid')
            layer2 = Dense(1, activation='sigmoid')
            self.add(layer1)
            self.add(layer2)
        else:
            self.add(
                Dense(
                    8,
                    input_shape=(8,),
                    activation='sigmoid',
                    weights=[child_weights[0], np.ones(8)])
            )
            self.add(
                Dense(
                    1,
                    activation='sigmoid',
                    weights=[child_weights[1], np.zeros(1)])
            )

    def forward_propagation(self, train_feature, train_label):
        predict_label = self.predict(train_feature.values)
        self.fitness = accuracy_score(train_label, predict_label.round())

def crossover(nn1, nn2):
    nn1_weights = []
    nn2_weights = []
    child_weights = []

    for layer in nn1.layers:
        nn1_weights.append(layer.get_weights()[0])

    for layer in nn2.layers:
        nn2_weights.append(layer.get_weights()[0])

    for i in range(len(nn1_weights)):
        split = random.randint(0, np.shape(nn1_weights[i])[1]-1)
        for j in range(split, np.shape(nn1_weights[i])[1]-1):
            nn1_weights[i][:, j] = nn2_weights[i][:, j]

        child_weights.append(nn1_weights[i])

    mutation(child_weights)

    child = ANN(child_weights)
    return child

def mutation(child_weights):
    selection = random.randint(0, len(child_weights)-1)
    mut = random.uniform(0, 1)
    if mut <= .05:
        child_weights[selection] *= random.randint(2, 5)
    else:
        pass

# Preprocess Data
df = pd.read_table('./diabetes.txt', header=None, encoding='gb2312', sep='\t')
df.astype(float)
df.pop(10)
df.pop(0)
label = df.pop(9)
train_feature = df[:576]
train_label = label[:576]
test_feature = df[576:]
test_label = label[576:]

networks = []
pool = []
generation = 0
population = 10

for i in range(population):
    networks.append(ANN())

max_fitness = 0
optimal_weights = []

epochs = 10

for i in range(epochs):
    generation += 1
    logging.debug("Generation: " + str(generation) + "\r\n")

    for ann in networks:
        ann.forward_propagation(train_feature, train_label)
        pool.append(ann)

    networks.clear()
    pool = sorted(pool, key=lambda x: x.fitness)
    pool.reverse()

    for i in range(len(pool)):
        if pool[i].fitness > max_fitness:
            max_fitness = pool[i].fitness
            logging.debug("Max Fitness: " + str(max_fitness) + "\r\n")

            optimal_weights = []
            for layer in pool[i].layers:
                optimal_weights.append(layer.get_weights()[0])
            logging.debug('optimal_weights: ' + str(optimal_weights)+"\r\n")

    for i in range(5):
        for j in range(2):
            temp = crossover(pool[i], random.choice(pool))
            networks.append(temp)

ann = ANN(optimal_weights)
predict_label = ann.predict(test_feature.values)
print('Test Accuracy: %.2f' % accuracy_score(test_label, predict_label.round()))
