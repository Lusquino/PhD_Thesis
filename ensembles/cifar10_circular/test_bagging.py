import wisard_bagging as bg
import numpy
import wisardpkg as wp
import statistics as st
import time
from sklearn.metrics import accuracy_score

bits = ["15"]
#bits = ["10", "15", "20"]

for bit in bits:
    ds_train = wp.DataSet("../../datasets/cifar_circular/circular_cifar_train_" + bit + ".wpkds")
    ds_test = wp.DataSet("../../datasets/cifar_circular/circular_cifar_test_" + bit + ".wpkds")

    y_test = []
    for i in range(len(ds_test)):
        y_test.append(ds_test.getLabel(i))

    #for learners in range(10, 30, 10):
    for learners in [20]:
        #for partitions in [0.6, 0.8]:
        for partitions in [0.8]:
            #for models in ["wisard", "clus", "heterogeneous"]:
            for models in ["wisard"]:
                writer = open("test_bagging_test_" + bit + ".txt", "w+")
                total_training_time = []
                total_test_time = []
                total_accuracy = []
                for i in range(1):
                    ensemble = bg.Bagging(ds_train, learners, partitions, models)
                    print("ENSEMBLOU")
                    total_training_time.append(ensemble.get_training_time())
                    test_time = time.time()
                    out = ensemble.classify(ds_test)
                    test_time = time.time() - test_time
                    total_test_time.append(test_time)
                    acc = accuracy_score(y_test, out)
                    total_accuracy.append(acc)
                writer.write(models + ", " + str(learners) + ", " + str(partitions) + ", " + 
                str(st.mean(total_training_time)) + ", "  +
                str(st.mean(total_test_time)) +
                str(st.mean(total_accuracy)) + "\n")
                writer.close()