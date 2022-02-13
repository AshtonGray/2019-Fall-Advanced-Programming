import random
from SongLibrary import *
from Graph import *

class ArtistConnections:

    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.graph = Graph()


    """
    Load the artist connections graph based on a given song database
    Add the edges based on the last column of the collaborative artists 

    """

    def load_graph(self, songLibrary):

        for i in range(songLibrary.size):
            for k in range(len(songLibrary.songArray[i].coArtist)):
                self.graph.addEdge(songLibrary.songArray[i].artist,songLibrary.songArray[i].coArtist[k],1) # add edge creates vertices if not already there
                self.graph.addEdge(songLibrary.songArray[i].coArtist[k],songLibrary.songArray[i].artist,1)
            # add songs, add all songs to list from the single artist
            self.graph.vertList[songLibrary.songArray[i].artist].songs.append(songLibrary.songArray[i].title)


        self.numVertices = self.graph.numVertices
        self.vertList = self.graph.vertList
        return self.numVertices

    """
    Return song libary information
    """

    def graph_info(self):
        return "Vertex Size: " + str(self.numVertices)

    """
    Search the information of an artist based on the artist name
    Return a tuple (the number of songs he/she wrote, the collaborative artist list)
    """

    def search_artist(self, artist_name):
        numSongs = 0
        artistLst = []
        numSongs = len(self.vertList[artist_name].songs)  # number of songs is length of songs artist worked on
        for artist in self.vertList.keys(): # go through list of keys (artists) of vertex list
            for key in self.vertList[artist].getConnections(): # use key to access connections of the artist
                if artist_name == key.id:
                    artistLst.append(artist)

        return numSongs, artistLst

    """
    Return a list of two-hop neighbors of a given artist
    """

    def find_new_friends(self, artist_name):
        two_hop_friends = []
        #artobj = []
        artistfriends = []
        artistfriendsfriends = []
        artistfriendsfriendsfriends = []
        # go through entire vertex list and add artists friends
        for artist in self.vertList:
            if self.vertList[artist].id == artist_name:
                artobj = self.vertList[artist].getConnections()
                for key in artobj:
                    artistfriends.append(key.id)
        # go through the artists friends and get their friends, these are the ones we want
        for artist in artistfriends:
            for artist1 in self.vertList:
                if self.vertList[artist1].id == artist:
                    artobj = self.vertList[artist1].getConnections()
                    for key in artobj:
                        artistfriendsfriends.append(key.id)

        # get all friends friends friends
        for artist in artistfriendsfriends:
            for artist1 in self.vertList:
                if self.vertList[artist1].id == artist:
                    artobj = self.vertList[artist1].getConnections()
                    for key in artobj:
                        artistfriendsfriendsfriends.append(key.id)

                    if artist_name not in artistfriendsfriendsfriends and artist != artist_name and artist not in two_hop_friends:
                        two_hop_friends.append(artist)
                    artistfriendsfriendsfriends = []

        return two_hop_friends

    """
    Search the information of an artist based on the artist name
    """

    def recommend_new_collaborator(self, artist_name):
        hopfriends = ArtistConnections.find_new_friends(self, artist_name)  # get the two hop friends of artist
        artist = ""
        numSongs = 0
        count = 0
        for collab in hopfriends:
            if collab not in hopfriends:
                break
            for i in self.graph.getVertex(artist_name).coArtists: # go through coartists of the artist
                if i in self.graph.getVertex(collab).coArtists: # if coartist is in collabs coartist
                    count = count + self.graph.getVertex(collab).coArtists[i] # add to counter
            if count > numSongs: # reset
                numSongs = count
                artist = collab
            count = 0
        return numSongs, artist

    """
    Search the information of an artist based on the artist name

    """

    def shortest_path(self, artist_name):
        path = {}
        queue = []
        queue.append(self.graph.getVertex(artist_name)) # put starting vertex
        weight0 = 1
        weight1 = 0
        temp = 0
        while queue != []:
            while weight0 > 0:
                artist = queue.pop(0)
                for next in artist.getConnections():
                    if next not in queue and next.id not in path.keys(): # check if surrounding vertices have been visited
                        queue.append(next)
                        weight1 += 1 # branching out on graph
                path[artist.id] = temp
                weight0 -= 1
            weight0 = weight1 # reset
            weight1 = 0 # reset
            temp +=1
        weight0 = 1
        weight1 = 0
        temp = 0
        return path


# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':
    songLib = SongLibrary()
    songLib.loadLibrary("TenKsongs_proj2.csv")
    artistGraph = ArtistConnections()
    artistGraph.load_graph(songLib)
    #print(artistGraph.numVertices)
    #print(artistGraph.search_artist('Green Day'))
    #print(artistGraph.find_new_friends('Santana'))
    print(artistGraph.shortest_path('Santana'))
    #print(artistGraph.recommend_new_collaborator('Santana'))

    '''Song lib is an object thats attribute 'list' contains a list of objects of songs, of which each contain it's data'''


    # ArtistConnections.generate_data("TenKsongs_proj2.csv")
