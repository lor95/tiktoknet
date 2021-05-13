import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

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
            current_index += perc_to_sum
    df = pd.DataFrame.from_dict(video_published_splitted, orient='index', columns=['video_published'])
    return df

p_changes_by_day = {}
for p in p_challenges_list:
    current = pd.read_csv('./dataset/dataset_{}_connections_etl.csv'.format(p), sep=";", header=0)
    current['createTime'] =  pd.to_datetime(current['createTime'], format='%Y%m%d %H:%M:%S')
    video_published = current.set_index('createTime').groupby(pd.Grouper(freq='D'))["id"].count().to_frame()
    video_published.reset_index(inplace=True)
    video_published.columns = ['date', 'video_count']
    video_published.drop('date', axis=1, inplace=True)
    video_published.reset_index(inplace=True)
    video_published.columns = ['life_day', 'video_count']
    p_changes_by_day[p] = split_in_perc(video_published)
    
n_changes_by_day = {}
for p in n_challenges_list:
    current = pd.read_csv('./dataset/dataset_{}_connections_etl.csv'.format(p), sep=";", header=0)
    current['createTime'] =  pd.to_datetime(current['createTime'], format='%Y%m%d %H:%M:%S')
    video_published = current.set_index('createTime').groupby(pd.Grouper(freq='D'))["id"].count().to_frame()
    video_published.reset_index(inplace=True)
    video_published.columns = ['date', 'video_count']
    video_published.drop('date', axis=1, inplace=True)
    video_published.reset_index(inplace=True)
    video_published.columns = ['life_day', 'video_count']
    n_changes_by_day[p] = split_in_perc(video_published)

current = p_changes_by_day['bussitchallenge']
plt.figure(figsize=(20, 15))

#for method in interpolations_methods:
function = interpolate.UnivariateSpline(current.index,current["video_published"], k=5, s=100000000)
first_derivate = function.derivative()
second_derivate = function.derivative(n=2)
    
xnew = np.arange(0, 100, perc_to_sum)
ynew = function(xnew)
plt.plot(xnew, ynew)
plt.xlabel("% of lifespan", fontsize=24)
plt.ylabel("Number of videos published", fontsize=24)
plt.show()

plt.figure(figsize=(20, 15))
xnew = np.arange(0, 100, perc_to_sum)
ynew = second_derivate(xnew)
plt.plot(xnew, ynew)
plt.show()
print("INFLECTION POINTS: {}".format(second_derivate.roots()))

