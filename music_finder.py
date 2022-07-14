from apis import spotify
from apis import twilio

user_selections = {
    'genres': [],
    'artists': [],
    'artist_id': [],
    'tracks': []
}


def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Search and select your favorite genres
2 - Search and select your favorite artists
3 - Search and select your favorite tracks
4 - Discover new music
5 - Quit
---------------------------------------------------------------------

Your genres: {genre}
Your artists: {artist}
Your tracks: {track}

---------------------------------------------------------------------
    '''.format(genre = user_selections['genres'], artist = user_selections['artists'], track = user_selections['tracks']))


def handle_genre_selection():
    # 1. Allow user to select one or more genres using the
    #    spotify.get_genres_abridged() function
    # 2. Allow user to store / modify / retrieve genres
    #    in order to get song recommendations
    genres = []
    
    for genre in (spotify.get_genres_abridged()):
        genres.append(genre.lower())
        print(genre) 
    
    while True:
        
        try:
            choose_genre = input('Type the name of a genre from the list. Press enter to continue. You may clear current selections by typing "clear". ')
            if choose_genre.lower() == 'clear':
                user_selections['genres'] = []
                break
            
            elif choose_genre.lower() in genres:
                for item in choose_genre.split(','):
                        user_selections['genres'].append(item)
                break 
            
            else:       
                print('Your input is invalid. Please try again. ')                
        
        except:
            print('Your input is invalid. Please try again. ')
            continue


def handle_artist_selection():
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations
    query_artist = input('Enter the name of an artist: ')
    artists = spotify.get_artists(search_term = query_artist)
    count = 1
    
    if len(artists) == 0:
            print('The artist does not exist. You will be redirected to the main menu. ')
    
    else:
        for artist in artists:
            print(count, artist.get('name'))
            count += 1
        
        while True:
            try:
                choose_artist = input('Enter the number corresponding to an artist. Type "clear" to clear your current artist selections. ')
                
                if choose_artist.lower() == 'clear':
                    user_selections['artists'] = []
                    user_selections['artist_id'] = []
                    break
                
                elif (int(choose_artist) <= count) & (int(choose_artist) > 0):
                    i = int(choose_artist) - 1
                    user_selections['artists'].append(artists[i].get('name'))
                    user_selections['artist_id'].append(artists[i].get('id'))
                    break

                else:
                     print('Your input is invalid. Please try again. ')
            
            except:
                print('Your input is invalid. Please try again. ')
                continue

def handle_track_selection():
    
    query_track = input('Enter the name of a song: ')
    tracks = spotify.get_tracks(search_term = query_track)
    count = 1
    
    if len(tracks) == 0:
            print('The artist does not exist. You will be redirected to the main menu. ')
    
    else:
        for track in tracks:
            print(count, track.get('name'), 'by', track.get('artist').get('name'))
            count += 1
        
        while True:
            try:
                choose_track = input('Enter the number corresponding to a track. Type "clear" to clear your current track selections. ')
                
                if choose_track.lower() == 'clear':
                    user_selections['tracks'] = []
                    break
                
                elif (int(choose_track) <= count) & (int(choose_track) > 0):
                    i = int(choose_track) - 1
                    user_selections['tracks'].append(tracks[i].get('name'))
                    break

                else:
                     print('Your input is invalid. Please try again. ')
            
            except:
                print('Your input is invalid. Please try again. ')
                continue

def get_recommendations():
    # 1. Allow user to retrieve song recommendations using the
    #    spotify.get_similar_tracks() function
    # 2. List them below
    try:
        rec = spotify.get_similar_tracks(artist_ids = user_selections['artist_id'], genres = user_selections['genres'])
        content = spotify.get_formatted_tracklist_table_html(rec)
        
        for r in rec:
            print(r.get("name"), "by", r.get("artist").get("name"))
    
        while True:
            choose_email = input('Would you like to email this table to a friend? (y/n): ')
        
            if choose_email.lower() == 'y':
                from_email = input('What is your email address?: ')
                to_email = input('Who would you like to send to?: ')
                
                twilio.send_mail(from_email = from_email,
                                    to_emails = to_email,
                                    subject = 'Your Song Recommendations from Spotify ',
                                    html_content = content)
                break
            
            elif choose_email.lower()=='n':
                break
            
            else:
                print('Your input is invalid. Please try again. ')
                continue
                
    except:
        print('Spotify only allows 5 seed values (in any combination). Please clear some selections out to proceed. ')


# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? (Enter a number) ')
    
    if choice == '1':
        handle_genre_selection()
    
    elif choice == '2':
        handle_artist_selection()
    
    elif choice == '3':
        handle_track_selection()

    elif choice == '4':
        get_recommendations()

    elif choice == '5':
        print('Quitting...')
        break
    
    else:
        print(choice, 'Your choice is invalid. Please try again. ')
    
    print()
    
    input('Press enter to continue...')
