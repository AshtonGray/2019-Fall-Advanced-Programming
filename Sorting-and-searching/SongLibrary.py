"""
Ashton Gray
32000589
UMass ECE 241 - Advanced Programming
Project #1     Fall 2019
SongLibrary.py - SongLibrary class
"""
from AVLTree import AvlTree
from binarySearchTree import TreeNode, BinarySearchTree
from Song import Song
import random
import time

class SongLibrary:
    """
    Intialize your Song library here.
    You can initialize an empty songArray, empty BST and
    other attributes such as size and whether the array is sorted or not
    """

    def __init__(self):
        self.songArray = list()
        self.songBST = None
        self.isSorted = False
        self.size = 0

    """
    load your Song library from a given file. 
    It takes an inputFilename and store the songs in songArray
    """

    def loadLibrary(self, inputFilename):
        file = open(inputFilename,'r')
        self.songArray = file.readlines() # self.songArray is list of all songs complete data: ["0,Qing Yi Shi,Leon Lai,203.38893,5237536",...]
        for i in range(len(self.songArray)):
            self.songArray[i] = Song(self.songArray[i]) # for each song in the list, create an object in place with the data of each song
        file.close()
        self.size = len(self.songArray) # size of the list

    """
    Linear search function.
    It takes a query string and attibute name (can be 'title' or 'artist')
    and return the number of songs fonud in the library.
    Return -1 if no songs is found.
    Note that, Each song name is unique in the database,
    but each artist can have several songs.
    """

    def linearSearch(self, query, attribute):
        found = 0
        for i in range(len(self.songArray)): # go through array
            if attribute == 'title':
                if self.songArray[i].title == query:
                    found = 1
                    break # only one song from title
            elif attribute == 'artist':
                if self.songArray[i].artist == query:
                    found += 1 # keep searching through the array
        if found == 0:
            found = -1 # if still 0 (nothing found by the time go through entire list)
        return found

    """
    Build a BST from your Song library based on the song title. 
    Store the BST in songBST variable
    """

    def buildBST(self):
        self.songBST = AvlTree() # instantiate bst
        if not self.isSorted:
            songLib.quickSort() # sort the array if not already
        for i in range(self.size):
            self.songBST.put(self.songArray[i].title,self.songArray[i]) # go through the array and add to the tree, key: title data: object

    """
    Implement a search function for a query song (title) in the songBST.
    Return the song information string
    (After you find the song object, call the toString function)
    or None if no such song is found.
    """

    def searchBST(self, query):
        if self.songBST == None: # if no bst, return nothing
            return
        temp = self.songBST.get(query) # find the song object in the tree
        if temp == None: # if doesn't exist
            return None
        else:
            return temp.toString() # print the print statement from the object

    """
    Return song libary information
    """

    def libraryInfo(self):
        return "Size: " + str(self.size) + ";  isSorted: " + str(self.isSorted)

    """
    Sort the songArray using QuickSort algorithm based on the song title.
    The sorted array should be stored in the same songArray.
    Remember to change the isSorted variable after sorted
    """

    def quickSort(self):
        alist = self.songArray
        self.quickSortHelper(alist,0,self.size-1)
        self.isSorted = True

    def quickSortHelper(self,alist,first,last):
        if first < last:
            splitpoint = self.partition(alist,first,last)
            self.quickSortHelper(alist,first,splitpoint-1)
            self.quickSortHelper(alist,splitpoint+1,last)

    def partition(self,alist,first,last):
        pivotvalue = alist[first].title

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and alist[leftmark].title <= pivotvalue:
                leftmark = leftmark + 1

            while alist[rightmark].title >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp

        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp

        return rightmark

# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':
    songLib = SongLibrary()
    songLib.loadLibrary("TenKsongs.csv")
    print(songLib.libraryInfo())
    '''
    print(songLib.linearSearch("Alice In Chains", "artist")) # should return 7
    print(songLib.linearSearch("My Man's Gone Now", "title")) # should return 1
    print(songLib.linearSearch("---", "title")) # should return -1
    print(songLib.libraryInfo()) # should be: size 9709 isSorted: False'''
    songLib.quickSort() # sort
    print(songLib.libraryInfo()) # should be: size 9709 isSorted: True
    songLib.buildBST() # build bst
    print(songLib.searchBST("My Man's Gone Now")) # should be "Title: My Man's Gone Now; Artist: Rhian Lois'''
'''
    test = random.sample(songLib.songArray,100) # grab 100 random samples of songs and put them in new class
    a = time.time() # start timer for linear search
    for i in range(len(test)):
        songLib.linearSearch(test[i].title,'title') # perform linear search with 100 songs
    print("Time Takes Linear Search (s):")
    print(time.time() - a) # time elapsed for linear search

    b = time.time() # start timer for building bst
    songLib.buildBST()  # build bst for 100 songs
    print("Time Takes to Build BST (s):")
    print(time.time() - b) # time elapsed for building bst

    c = time.time() # start timer for searching bst
    for i in range(len(test)):
        songLib.searchBST(test[i].title) # perform bst search with 100 songs
    print("Time Takes to Search BST (s):")
    print(time.time() - c) # time elapsed for searching bst'''




