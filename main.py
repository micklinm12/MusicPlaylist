import numpy as np
import pandas as pd
import re

def create_playlist():

  music_df = pd.read_csv("data.csv")
  music_df.set_index('name', inplace=True)
  
  try:
    playlist_length = int(input('Length of Playlist: '))
  except ValueError:
    raise Exception("Playlist length must be an integer")

  artist = input('Artist: ')
  
  if artist:
    music_df = music_df[music_df['artists'] == "['" + artist + "']"]
    if music_df.empty:
      raise Exception("No songs for requested artist")
 
  music_df.sort_values(by=['valence'], inplace=True)
  bins = pd.cut(music_df['valence'], playlist_length, retbins=True)[1]
  songs = []

  for i in range(playlist_length):
    small_df = music_df[(music_df['valence'] >= bins[i]) & (music_df['valence'] <= bins[i+1])]
    
    if small_df.empty:
      small_df = music_df[(music_df['valence'] >= bins[i-1]) & (music_df['valence'] <= bins[i])]

    most_popular = small_df[small_df['popularity'] == small_df['popularity'].max()]

    if not most_popular.empty:
      music_df.drop(most_popular.index[0], inplace=True)
      songs.append(str(i) + ': "' + most_popular.index[0] + '" by ' + most_popular['artists'].iloc[0] + ', Valence: ' + str(most_popular['valence'].iloc[0]))

  print('\n')
  for song in songs:
    print(song)
    print('\n')
  print('\n')
  print('Length of Playlist: ' + str(len(songs)))
  
  return songs

create_playlist()