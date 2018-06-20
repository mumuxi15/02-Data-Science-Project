def plot_confusion_matrix(y_test,y_pred):
    M = confusion_matrix(y_test,y_pred)
    M = M/M.sum(axis=1)[:,None]
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(M, annot=True,fmt='.0%',cmap="YlGnBu")
    ax.set_xticklabels(weather_tags)
    ax.set_yticklabels(weather_tags)
    plt.show()
