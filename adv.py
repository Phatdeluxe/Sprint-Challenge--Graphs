from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited_graph = {}
# reverse_path = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# previous_room = 0

def check_adjacency(cur_room, check_room):
    if cur_room == check_room:
        return 'same'
    elif cur_room.n_to == check_room:
        return 'n'
    elif cur_room.s_to == check_room:
        return 's'
    elif cur_room.e_to == check_room:
        return 'e'
    elif cur_room.w_to == check_room:
        return 'w'

def bfs(cur_room, target_room):
    # if not adjacent, BFS to find shortest path to new node
    qq = Queue()
    qq.enqueue([cur_room])
    # create a set of traversed vertices
    visited = set()
    # while queue is not empty:
    while qq.size() > 0:
        # dequeue/pop first vertex
        qq_path = qq.dequeue()
        # if not visited
        if qq_path[-1] not in visited:
            # DO THE THING!!!!!!!
            if qq_path[-1] == target_room:
                return qq_path
            # mark as visited
            visited.add(qq_path[-1])
            # enqueue all neighbors
            for option in qq_path[-1].get_exits():
                new_qq_path = list(qq_path)
                new_qq_path.append(qq_path[-1].get_room_in_direction(option))
                qq.enqueue(new_qq_path)

# DFS
ss = Stack()
ss.push([player.current_room])
visited = set()
while ss.size() > 0:
    path = ss.pop()
    player_spacing = check_adjacency(player.current_room, path[-1])
    
    if path[-1].id not in visited: # change to visited
        if player_spacing != None and player_spacing != 'same':
            player.travel(player_spacing)
            traversal_path.append(player_spacing)
        # creating the room entry in our graph
        visited_graph[path[-1].id] = {}
        visited.add(path[-1].id) # added
        for option in path[-1].get_exits():
            visited_graph[player.current_room.id].update({option: None})
        # Each time a node is removed, check adjacency to current position
        player_spacing = check_adjacency(player.current_room, path[-1])
        if player_spacing == 'same':
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                ss.push(new_path)
        # elif player_spacing != None:
        #     # if adjacent, continue on as normal
        #     # move player to room
        #     player.travel(player_spacing)
        #     # add direction to traversal_path
        #     traversal_path.append(player_spacing)
        else:
            # if not adjacent, BFS to find shortest path to our new room
            shortest = bfs(player.current_room, path[-1])
            # print(shortest)
            # now that we have the shortest path to our new room, we need to figure out direction to get there
            # empty list to track directions
            reposition = []
            # checking the adjacency of each room in our shortest path
            for room in shortest:
                direction = check_adjacency(player.current_room, room)
                # adding the correct direction to the list
                if direction != 'same':
                    reposition.append(direction)
                    # moving in the direction
                    player.travel(direction)
            # adding those movements to the list
            traversal_path += reposition
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                ss.push(new_path)
            



# Check adjacency
# If not adjacent






'''
def find_nearest(cur_room):
    qq = Queue()
    qq.enqueue([cur_room])
    visited = set()
    while qq.size() > 0:
        path = qq.dequeue()
        if path[-1] not in visited:
            for keys in visited_graph[path[-1].id]:
                if visited_graph[path[-1].id][keys]:
                    return path
            visited.add(path[-1])
            for neighbor in path[-1].get_exits():
                new_path = path + [path[-1].get_room_in_direction(neighbor)]
                qq.enqueue(new_path)

def next_room(previous_room, traversal_path):
    # next room
    # get all directions
    exit_paths = player.current_room.get_exits()
    cur_room = player.current_room
    prev_dir = reverse_path[traversal_path[-1]]
    # set each avaliable direction to None in the graph
    if cur_room.id not in visited_graph:
        visited_graph[cur_room.id] = {}
        for option in exit_paths:
            visited_graph[cur_room.id].update({option: None})
    # update direction to reflect previous room
    if visited_graph[cur_room.id][prev_dir] is None:
        visited_graph[cur_room.id][prev_dir] = previous_room
    # choose a random avaliable direction to go
    move = random.choice(exit_paths)
    while len(exit_paths) > 0:
        if visited_graph[cur_room.id][move] != None:
            exit_paths.remove(move)
            # if none are unexplored, move in the opposite of path[-1]
            if exit_paths == []:
                path = find_nearest(cur_room)
                card_path = []
                for i in range(len(path)-1):
                    if path[i].n_to == path[i+1]:
                        card_path.append('n')
                    if path[i].s_to == path[i+1]:
                        card_path.append('s')
                    if path[i].e_to == path[i+1]:
                        card_path.append('e')
                    if path[i].w_to == path[i+1]:
                        card_path.append('w')
                traversal_path += card_path
                for i in card_path:
                    if i == card_path[-1]:
                        previous_room = player.current_room.id
                        player.travel(i)
                    else:
                        player.travel(i)
                return previous_room, traversal_path
            else:
                move = random.choice(exit_paths)
        else:
            break

    # get room and update graph to reflect that relationship
    move_room = player.current_room.get_room_in_direction(move)
    visited_graph[cur_room.id][move] = move_room.id
    previous_room = player.current_room.id
        # move in that direction
    traversal_path.append(move)
    player.travel(move)
        # repeat next room
    return previous_room, traversal_path



# Starting room
# get all directions
exit_paths = player.current_room.get_exits()
cur_room_id = player.current_room.id
# create empty dict for index room id
visited_graph[cur_room_id] = {}
# set each avaliable direction to None in the graph
for option in exit_paths:
    visited_graph[cur_room_id].update({option: None})
# choose a random avaliable direction to go
move = random.choice(exit_paths)
# get that room and update graph to reflect that relationship
move_room = player.current_room.get_room_in_direction(move)
visited_graph[cur_room_id][move] = move_room.id
previous_room = player.current_room.id
# move in that direction
traversal_path.append(move)
player.travel(move)
previous_room, traversal_path = next_room(previous_room, traversal_path)
while len(visited_graph) < 9:
    print('next room')
    previous_room, traversal_path = next_room(previous_room, traversal_path)
'''

    
    


print('visited graph')
print(visited_graph)
print('path')
print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
