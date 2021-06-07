import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd
import lib.tiktok_network as nx
import lib.challenges as challenges

p_challenges_list = [
    "bussitchallenge",
    "copinesdancechallenge",
    "emojichallenge",
    "colpiditesta",
    "boredinthehouse",
    "ITookANap",
    "plankchallenge"
]
n_challenges_list = [
    "silhouettechallenge",
    "bugsbunnychallenge",
    "strippatiktok",
    "firewroks",
    "fightchallenge",
    "sugarbaby",
    "updownchallenge"
]

perc_to_sum = 5
def split_in_perc(video_published):
    total_days = len(video_published)
    video_published['% lifespan'] = video_published['life_day'].apply(lambda day: ((day+1)*100)/total_days)
    video_published_d = {}
    for row in video_published.itertuples():
        video_count = row[2]
        lifespan_perc = row[3]
        video_published_d[lifespan_perc] = video_count
    video_published_splitted = {}
    video_published_splitted[0] = 0
    current_index = perc_to_sum
    _sum = 0
    for perc in video_published_d:
        if perc < current_index:
            try:
                video_published_splitted[current_index] += video_published_d[perc]
            except:
                video_published_splitted[current_index] = video_published_d[perc]
        else:
            try:
                video_published_splitted[current_index] += video_published_d[perc]
            except:
                video_published_splitted[current_index] = video_published_d[perc]
            current_index += perc_to_sum 
    df = pd.DataFrame.from_dict(video_published_splitted, orient='index', columns=['video_published'])
    return df

p_changes_by_day = {}
for p in p_challenges_list:
    #current = pd.read_csv('./dataset/dataset_{}_connections_etl.csv'.format(p), sep=";", header=0)
    current = nx.graphCalculation(p)[-3]
    #print(current.shape[0])
    current['createTime'] =  pd.to_datetime(current['createTime'], format='%Y%m%d %H:%M:%S')
    video_published = current.set_index('createTime').groupby(pd.Grouper(freq='D'))["author_uniqueId"].count().to_frame()
    video_published.reset_index(inplace=True)
    video_published.columns = ['date', 'video_count']
    video_published.drop('date', axis=1, inplace=True)
    video_published.reset_index(inplace=True)
    video_published.columns = ['life_day', 'video_count']
    p_changes_by_day[p] = split_in_perc(video_published)
    
n_changes_by_day = {}
for p in n_challenges_list:
    #current = pd.read_csv('./dataset/dataset_{}_connections_etl.csv'.format(p), sep=";", header=0)
    current = nx.graphCalculation(p)[-3]
    #print(current.shape[0])
    current['createTime'] =  pd.to_datetime(current['createTime'], format='%Y%m%d %H:%M:%S')
    video_published = current.set_index('createTime').groupby(pd.Grouper(freq='D'))["author_uniqueId"].count().to_frame()
    video_published.reset_index(inplace=True)
    video_published.columns = ['date', 'video_count']
    video_published.drop('date', axis=1, inplace=True)
    video_published.reset_index(inplace=True)
    video_published.columns = ['life_day', 'video_count']
    n_changes_by_day[p] = split_in_perc(video_published)
'''
chall_ = 'bussitchallenge'
current = p_changes_by_day[chall_]
current.to_csv("dataset/dfcurves_"+chall_+".csv", sep=';', index=False)
'''
intervals = {}
intervals["challenge"] = []
intervals["n_intervals"] = []
intervals["points"] = []
intervals["diff_videos_intervals"] = []

for challenge in p_changes_by_day:
    intervals["challenge"].append(challenge)
    current = p_changes_by_day[challenge]
    s =100000000
    if challenge == 'ITookANap':
        s = 410
    function = interpolate.UnivariateSpline(current.index,current["video_published"], k=4, s=s)
    first_derivate = function.derivative(n=1)
    #second_derivate = function.derivative(n=2)
    inf_points = first_derivate.roots()
    intervals["n_intervals"].append(len(inf_points))
    points = [5 * round(p/5) for p in inf_points]
    intervals["points"].append(points)
    punti_andamenti = [0]
    punti_andamenti.extend(inf_points)
    punti_andamenti.extend([100])
    valori_punti = [function(p) for p in punti_andamenti]
    differenze = [j-i for i, j in zip(valori_punti[:-1], valori_punti[1:])]
    intervals["diff_videos_intervals"].append(differenze)
    plt.title(challenge, fontsize=20)    
    xnew = np.arange(0, 105, perc_to_sum)
    ynew = function(xnew)
    plt.plot(xnew, ynew)
    for inf in inf_points:
        plt.axvline(x=inf)
    plt.xlabel("% of lifespan", fontsize=16)
    plt.ylabel("Number of nodes", fontsize=16)
    plt.show()
    
for challenge in n_changes_by_day:
    intervals["challenge"].append(challenge)
    current = n_changes_by_day[challenge]
    s =100000000
    if challenge == 'strippatiktok':
        s = 200
    if challenge == 'updownchallenge':
        s = 11700
    function = interpolate.UnivariateSpline(current.index,current["video_published"], k=4, s=s)
    first_derivate = function.derivative(n=1)
    #second_derivate = function.derivative(n=2)
    inf_points = first_derivate.roots()
    intervals["n_intervals"].append(len(inf_points))
    points = [5 * round(p/5) for p in inf_points]
    intervals["points"].append(points)
    punti_andamenti = [0]
    punti_andamenti.extend(inf_points)
    punti_andamenti.extend([100])
    valori_punti = [function(p) for p in punti_andamenti]
    differenze = [j-i for i, j in zip(valori_punti[:-1], valori_punti[1:])]
    intervals["diff_videos_intervals"].append(differenze)
    plt.title(challenge, fontsize=20)    
    xnew = np.arange(0, 105, perc_to_sum)
    ynew = function(xnew)
    plt.plot(xnew, ynew)
    for inf in inf_points:
        plt.axvline(x=inf)
    plt.xlabel("% of lifespan", fontsize=16)
    plt.ylabel("Number of nodes", fontsize=16)
    plt.show()
    
intervals_d = pd.DataFrame.from_dict(intervals)
intervals_d.to_csv('dataset/intervals.csv', index=False)

'''
plt.figure(figsize=(20, 15))
#for method in interpolations_methods:
function = interpolate.UnivariateSpline(current.index,current["video_published"], k=5, s=100000000)
first_derivate = function.derivative()
second_derivate = function.derivative(n=2)

plt.title(chall_, fontsize=20)    
xnew = np.arange(0, 100, perc_to_sum)
ynew = function(xnew)
plt.plot(xnew, ynew)
plt.xlabel("% of lifespan", fontsize=16)
plt.ylabel("Number of nodes", fontsize=16)
plt.show()

   
fig=plt.figure(figsize=(20, 15))
fig.suptitle('Derivata seconda', fontsize=20)
xnew = np.arange(0, 100, perc_to_sum)
ynew = second_derivate(xnew)
plt.plot(xnew, ynew)
plt.xlabel('% of lifespan', fontsize=16)
plt.ylabel('Number of nodes', fontsize=16)
plt.show()
print("INFLECTION POINTS: {}".format(second_derivate.roots()))
'''
