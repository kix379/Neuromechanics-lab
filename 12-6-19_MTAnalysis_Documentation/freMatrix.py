import pickle
import matplotlib.pyplot as plt
import matplotlib
from classes import *

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts




with open("allObjects.pkl", "rb") as fp:
    proc_data = pickle.load(fp)

with open("allWords.pkl","rb") as fp:
    words=pickle.load(fp)

letters={'A':0,'E':1,'H':2,'I':3,'N':4,'O':5,'R':6,'S':7,'T':8}
letters1=['A','E','H','I','N','O','R','S','T']

#Apriori probability

print(len(words))
matrix=[[0 for m in range(9)]for n in range(9)]
sum=0
for i in words:
    for m,n in zip(i[0:-1],i[1:]):
        matrix[letters[m]][letters[n]]=matrix[letters[m]][letters[n]]+1
        sum=sum+1

print(matrix,sum)
matrix=np.array(matrix)
fig, ax = plt.subplots()

im, cbar = heatmap(matrix, letters1, letters1, ax=ax,
                   cmap="YlGn", cbarlabel="Transition Frequency matrix")
texts = annotate_heatmap(im, valfmt="{x}")

fig.tight_layout()
plt.savefig('HeatMapTransitionMatrix/Apriori Probability Transition')


#Posterior probability

for p in range(8):
    start=p
    end=p+1
    for d in range(15):
        matrix=[[0 for m in range(9)]for n in range(9)]

        for i in proc_data[start:end]:
            for j in i.blocks[(d*12):(d*12+12)]:
                for k in j.words:
                    let=k.letters
                    for m,n in zip(let[0:-1],let[1:]):
                        matrix[letters[m]][letters[n]]=matrix[letters[m]][letters[n]]+1

        print(matrix)
        matrix=np.array(matrix)
        fig, ax = plt.subplots()

        im, cbar = heatmap(matrix, letters1, letters1, ax=ax,
                           cmap="YlGn", cbarlabel="Transition Frequency matrix")
        texts = annotate_heatmap(im, valfmt="{x}")

        fig.tight_layout()
        plt.savefig('HeatMapTransitionMatrix/Person'+str(p+1)+'/Day'+str(d+1))


#plot the frequency of the transitions across Days
#posterior

for p in range(8):
    start=p
    end=p+1
    alldays=[]
    combi={}

    for i in range(len(letters)):
        for j in range(len(letters)):
            combi[letters1[i]+letters1[j]]=0

    for d in range(15):
        matrix=[[0 for m in range(9)]for n in range(9)]

        for i in proc_data[start:end]:
            for j in i.blocks[(d*12):(d*12+12)]:
                for k in j.words:
                    let=k.letters
                    for m,n in zip(let[0:-1],let[1:]):
                        combi[m+n]=combi[m+n]+1
                        matrix[letters[m]][letters[n]]=matrix[letters[m]][letters[n]]+1

        print(matrix)
        alldays.append(matrix)
    rank=[]
    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):

        if(i[1]!=0):
            rank.append(i)
    print(rank)

    x=np.arange(1,len(rank)+1).tolist()
    new_x = [2*i for i in x]

    x_labels=np.array(rank)[:,0].tolist()
    y=[]
    for i in np.array(rank)[:,1]:
        y.append(int(i))
    print(x,x_labels,y)
    plt.figure(figsize=(20, 5))

    plt.bar(new_x, y, align='center')
    plt.xticks(new_x, x_labels, rotation='vertical')
    plt.legend()
    plt.savefig('HeatMapTransitionMatrix/Person'+str(p+1)+'/rankOrderingAllDays')



#Apriori

print(len(words))
combi={}

for i in range(len(letters)):
    for j in range(len(letters)):
        combi[letters1[i]+letters1[j]]=0

matrix=[[0 for m in range(9)]for n in range(9)]
sum=0
for i in words:
    for m,n in zip(i[0:-1],i[1:]):
        combi[m+n]=combi[m+n]+1
        matrix[letters[m]][letters[n]]=matrix[letters[m]][letters[n]]+1
        sum=sum+1

rank=[]
for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):

    if(i[1]!=0):
        rank.append(i)
print(rank)

for i in range(4):
    print(rank[i])

for i in range(len(rank)-1,len(rank)-5,-1):
    print(rank[i])

x=np.arange(1,len(rank)+1).tolist()
new_x = [2*i for i in x]

x_labels=np.array(rank)[:,0].tolist()
y=[]
for i in np.array(rank)[:,1]:
    y.append(int(i))
print(x,x_labels,y)
plt.figure(figsize=(20, 5))

plt.bar(new_x, y, align='center')
plt.xticks(new_x, x_labels, rotation='vertical')
plt.savefig('HeatMapTransitionMatrix/AprioriRankOrdering')



"""
Result:
('ER', 47)
('ES', 46)
('TE', 44)
('RE', 43)
('TT', 1)
('AO', 1)
('RH', 1)
('RR', 1)
"""
