import pandas as pd
import pickle

def read_csv(filename, sep=",", header=0, missing=""):
    df = pd.read_csv(filename, sep=sep, header=header, na_values=missing, engine='python')
    return df

def read_songs(filename='songs.csv'):
    print('Reading', filename)
    df = read_csv(filename)
    songid_lst = df['song_id'].values.tolist()
     
    df['genre_ids'].fillna('-1', inplace=True)
    df['language'].fillna('-1', inplace=True)
    df['artist_name'].fillna('Various Artists', inplace=True)
    df.drop(['song_id', 'song_length', 'lyricist', 'composer'], axis=1, inplace=True)
 
    return df, songid_lst

def df_genre(df,N=200):      
    genres = df['genre_ids'].value_counts()[:N]
    genres = list(genres.index)
    df = df.sort_values('artist_name', axis=0)
    columns = [i for i in genres]
    columns.append('language')
    new_df = pd.DataFrame(columns=columns)
    for artist in df['artist_name'].unique():
        cur_df = df.loc[df['artist_name'] == artist]
        new_df = new_df.append(artist_by_genre(cur_df,genres))
    return new_df

def artist_by_genre(df,genres):
    
    template_df = pd.DataFrame(data={i:[0] for i in genres})
    
    columns = genres.copy()
    columns.append('language')
    res = pd.DataFrame(columns=columns)
    
    probs = template_df.copy()
    for index, row in df.iterrows():
        if row['genre_ids'] in genres:
            probs[row['genre_ids']]+=1
    summ = int(probs.sum(axis = 1))
    if summ!=0:
        for index, row in probs.iteritems():
            row/=summ
    else:
        probs['-1']=1
        
    for index, row in df.iterrows():
        a = pd.DataFrame(data={'language':[row['language']]})
        if row['genre_ids'] in genres:
            a = a.join(template_df)
            a[row['genre_ids']]=1
        else:
            a = a.join(probs)
        res = res.append(a)
    return res
    

df,sid = read_songs('songs.csv')
df = df_genre(df)  
# df
filename = 'artist_by_genre.df'
pickle.dump(df, open(filename,'wb'))