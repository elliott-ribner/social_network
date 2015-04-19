# --------------------------- #
# Intro to CS Final Project   #
# Gaming Social Network       #
# --------------------------- #
#
# For students who have subscribed to the course,
# please read the submission instructions in the Instructor Notes below.
# ----------------------------------------------------------------------------- 

# ----------------------------------------------------------------------------- 

# Example string input. Use it to test your code.
example_input=""

# ----------------------------------------------------------------------------- 


#splits string into sentences in list
def create_data_structure(string_input):
    #dictionary that will be returned for data structure
    splitDict = {}
    #we establish to variables to keep track of index while searching, all our searches will
    #be based on these, also we will use these as well nameEnd below to establish entries in data structure
    startPosition = 0
    nextStart = 0
    endPosition = len(string_input)
    while nextStart != -1:
        #this establishes location of next period thereby allowing us to split each sentence, below
        #we recycle this value by assigning statposition to the next index value after this location
        #thus allowing us to move to the next sentence.
        nextStart = string_input.find('.', startPosition, endPosition)
        if nextStart !=-1:
            #every name is at the begining of the sentence so we can identify name as the the letters 
            #between the start and the first space as seen below
            nameEnd= string_input.find(' ', startPosition, endPosition)
            if string_input[startPosition:nameEnd] not in splitDict:
                #if name is not yet in dictionary we can add it and assign the key friends as the result of the function below 
                splitDict[string_input[startPosition:nameEnd]] = splitFriends(string_input[nameEnd:nextStart + 1])
            else:
                #since friends always cames before games we can assume that if the name already exists that we
                #this sentence is describing games and we can update the string with (splitGames(string_input[nameEnd:nextStart + 1]))
                splitDict[string_input[startPosition:nameEnd]].update(splitGames(string_input[nameEnd:nextStart + 1]))
                None    
            startPosition = nextStart + 1
    return splitDict



#splits string of friends into list and applies that list to dictionary value of friends or lists respectively
def splitFriends(friends):
    tempList=[]
    #first we delete is connected to from string
    friends=friends.replace(" is connected to","")
    position = 0
    nextPosition = 0
    # everything left in the string is just the friends so we can loop through the string using commas
    #to determine the start/end of each friend
    while nextPosition != -1:
        nextPosition = friends.find(',' , position  , len(friends) )
        tempList.extend([friends[position+1 :nextPosition  ]])
        position = nextPosition + 1
    tempDict= { 'friends': tempList }
    return tempDict

def splitGames(games):
    tempList=[]
    #first we delete likes to play from string
    games=games.replace(" likes to play","")
    position = 0
    nextPosition = 0
    # everything left in the string is just the games so we can loop through the string using commas
    #to determine the start/end of each game
    while nextPosition != -1:
        nextPosition = games.find(',' , position  , len(games) )
        tempList.extend([games[position+1 :nextPosition]])
        position = nextPosition + 1
    tempDict= { 'games': tempList }
    return tempDict

# ----------------------------------------------------------------------------- # 
# Note that the first argument to all procedures below is 'network' This is the #
# data structure that you created with your create_data_structure procedure,    #
# though it may be modified as you add new users or new connections. Each       #
# procedure below will then modify or extract information from 'network'        # 
# ----------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------- 

def get_connections(network, user):
        #based on our data structure, as long as user exists in network we can return friends
        if user in network:            
                return network[user]['friends']
        return None

# ----------------------------------------------------------------------------- 

def get_games_liked(network,user):
          #based on our data structure, as long as user exists in network we can return games
          if user in network:            
                return network[user]['games']
          return None

# ----------------------------------------------------------------------------- 

def add_connection(network, user_A, user_B):
          #confirms users are in network
          if user_B not in network or user_A not in network:
               return False
          #user b is already in list so we can return network
          if user_B in network[user_A]['friends']:
                  return network
          #if not already in friends user b will be added to list
          else: network[user_A]['friends'].extend([user_B])
          return network


# ----------------------------------------------------------------------------- 
def add_new_user(network, user, games):
     #confirms user is not already in network
     if user not in network:
            
            #establishes games as the games fed in through function for the user
            network[user]={'games': games, 'friends': []}
     return network
		
# ----------------------------------------------------------------------------- 
def get_secondary_connections(network, user):
          if user not in network:
            return None
          #calls the get connections functions to return the first set of connections
          primary = get_connections(network, user)
          secondaryList = [] 
          
          #goes through results of get connections and then performs getconnections
          #on each of the results creating a secondary list
          for entry in primary:                                              
                tempvalue = get_connections(network, entry)   
                #makes sure secondary connecitons are not repeated
                for secondaryEntry in tempvalue:
                    if secondaryEntry not in secondaryList:
                        secondaryList.extend([secondaryEntry])       
       
          return secondaryList

# ----------------------------------------------------------------------------- 	

def connections_in_common(network, user_A, user_B):
     #checks if these users are in network
     if user_B not in network or user_A not in network:
          return False
     connections = 0
     #cycles through each set of connections to see if there is a match, if so the templist is extended and returned regardless
     for entrya in network[user_A]['friends']:
          for entryb in network[user_B]['friends']:
               if entrya == entryb:
                    connections = connections + 1
     return connections

# ----------------------------------------------------------------------------- 



def path_to_friend(network, user_A, user_B, theList= None ):
    #confirms users are actually in network
     if user_A not in network or user_B not in network:
            return None
    #this is work around to avoid defining list in default
     if theList == None:
            theList = []
    #each time we loop through recursive solution we are keeping record of path by adding user a
     theList = theList + [user_A]
    #this means connection has been made between original a and b so we will return the list
     #but first we must add B for clarity
     if user_B in network[user_A]['friends'] :              
               return theList + [user_B]
    #this is most important peice of code, forces recursive loop for every entry in friends
     for entry in network[user_A]['friends']:
          if entry not in theList:             
               newPath = path_to_friend(network, entry, user_B, theList)
               if newPath: return newPath
    #if every path has been checked with no solution there must be no possible path
     return None           
               
          

net = create_data_structure(example_input)     
# Make-Your-Own-Procedure (MYOP)
# ----------------------------------------------------------------------------- 
# Your MYOP should either perform some manipulation of your network data 
# structure (like add_new_user) or it should perform some valuable analysis of 
# your network (like path_to_friend). Don't forget to comment your MYOP. You 
# may give this procedure any name you want.

# Replace this with your own procedure! You can also uncomment the lines below
# to see how your code behaves. Have fun!

#this code gauges the "popularity" of each user by counting the number of other users
#that are connected to them and returns the popularity of any specified user.
#we could use this score for other functions kind of like search engines use number of links coming in
# to gauge importance of webpage (or users posts etc. in this case)
def count_popularity(network , person):
    popularityDictionary = {}
    #creates key in dictionary for each person in network and rates them at zero to start
    if person not in network:
        return False
    for entry in network:
        popularityDictionary[entry] = 0
    #for each user that is connected to the 'person', they will have 1 point added to their score
    #we do this separatey from the first for loop because we need ot make sure ever user has a key first
    for entry in network:
        for friend in network[entry]['friends']:                          
            popularityDictionary[friend] = popularityDictionary[friend] + 1
    return popularityDictionary[person]
                


