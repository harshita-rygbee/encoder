import pandas as pd
import pickle
def read_csv(filename, sep=",", missing=""):
	df = pd.read_csv(filename, sep=sep, header=0, na_values=missing, engine='python')

	return df
dfs = [] 
filenames = ['artist_by_genre_temp_100_1.df', 'artist_by_genre_temp_100_2.df','artist_by_genre_temp_100_3.df',
'artist_by_genre_temp_100_4.df','artist_by_genre_temp_100_5.df','artist_by_genre_temp_100_6.df','artist_by_genre_temp_100_7.df','artist_by_genre_temp_100_8.df']
# filenames = ['artist_by_genre_temp_100_1.df']
for filename in filenames:
	df = pickle.load(open(filename,'rb'))
	df.to_csv(filename+'.csv')

 
