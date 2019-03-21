def evaluate(answer, predict):
    tn, fp, fn, tp = confusion_matrix(answer, predict).ravel()
    print(tp)
    print(fp)
    print(float(tp)/(tp + fp))


# print evaluate(answer, predict)
