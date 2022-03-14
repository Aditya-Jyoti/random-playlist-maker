from PlaylistMaker.api_interaction import API_Interaction
from PlaylistMaker.user_interaction import first_load 
import argparse
import sys


parser = argparse.ArgumentParser(description='Creates a random curated playlist')
parser.add_argument('-n','--number', help='number of songs to add to playlist, default is 10 songs')
args = vars(parser.parse_args())

if __name__ == "__main__":
    print("Please Note: Due to some issues with the api responses, the program will also count one")
    print("             of your spotify blend playlists as well")

    load = first_load()
    if not load:
        print("something went wrong, please open up a issue on github along with bug replication details or try running program again")
        sys.exit(0)
    
    if args["number"]:
        api = API_Interaction(int(args["number"].strip()))
        api.add_songs_to_playlist()
    else:
        api = API_Interaction()
        api.add_songs_to_playlist()

    print("\nThe Curated Random Playlist Was Created")

