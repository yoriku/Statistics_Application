import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import brunnermunzel, ttest_ind
import effect_size as es
import classification as cf
import itertools

def return_mode(stat_mode):
    if stat_mode == 0:
        return "nonpara"
    else:
        return "para"

def plot(df, target_name):
    header = df.columns.to_list()
    header.remove(target_name)

    df_melt = pd.melt(df, id_vars=[target_name],
                      value_vars=header, var_name='Indexes')

    fig = px.box(df_melt, x="Indexes", y="value", color=target_name)
    return fig


def calc_stat(df, target_name, mode="nonpara"):
    # Non-parametric stat
    # return list header, p_value, effect_size, effect_size_indication
    header = df.columns.to_list()
    header.remove(target_name)

    tmp = []
    for head in header:
        items = np.unique(df[target_name].values)
        for item in itertools.combinations(items, 2):
            df1 = df[df[target_name] == item[1]][head].values
            df0 = df[df[target_name] == item[0]][head].values
            print(es.cohen_d(df1, df0))
            
            if(mode == "nonpara"):
                data =  [f"{head}({item[1]} vs {item[0]})",
                        brunnermunzel(df1, df0)[1],
                        es.cliffs_delta(df1, df0)[0],
                        es.cliffs_delta(df1, df0)[1]]
                tmp.append(data)
            else:
                data =  [f"{head}({item[1]} vs {item[0]})",
                        ttest_ind(df1, df0)[1],
                        es.cohen_d(df1, df0)[0],
                        es.cohen_d(df1, df0)[1]]
                tmp.append(data)
    return tmp

def eval_model(df, target_name, class_weight):
    X = df.drop(target_name, axis=1).values
    y = df[target_name].values

    if(len(y) <= 50):
        pred, test = cf.mode_loo(X, y, class_weight)
    else:
        pred, test = cf.mode_hold(X, y, class_weight)
    
    label = np.unique(test)
    cm, metr, header = cf.calc_metric(test, pred, label)
    cm = pd.DataFrame(cm, columns=label, index=label)
    # metr = pd.DataFrame(metr, 
    #                     columns=["Accuracy", "Micro Recall", "Macro Recall", "Micro Precision", 
    #                              "Macro Precision", "Micro F-measure", "Macro F-measure"])
    return cm, metr, header

def plot_cm(cm):
    fig = px.imshow(cm.values,
                labels=dict(x="Predict label", y="Correct label"),
                x=cm.columns.tolist(), y=cm.index.tolist(), text_auto=True, color_continuous_scale='Blues')
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)
    return fig
    
def convart_table(nd):
    table = '<table>'
    for row in nd:
        table += '<tr>'
        for val in row:
            table += '<td>{}</td>'.format(val)
        table += '</tr>'
    table += '</table>'
    return table
