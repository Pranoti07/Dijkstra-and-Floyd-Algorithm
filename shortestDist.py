#Implementation of Dijkstra’s algorithm (greedy) and Floyd’s algorithm (dynamic programming) to compute all-pair shortest paths (shortest path between every pair of vertices) in any given graph
import random
import sys
from datetime import datetime
import traceback
from itertools import permutations
max_int=sys.maxsize

class Graph:
  def __init__(self):
    self.vertices={}

  def add_vert(self,k):         #adding vertex to the graph
    vertex = Vertex(k)
    self.vertices[k] = vertex
  
  def ret_vertex(self,k):
    return self.vertices.get(k)
  
  def include(self,k):
    return k in self.vertices

  def __iter__(self):
    return iter(self.vertices.values())

  def print_(self):
    print(self.vertices)

  def add_edge(self,sr_k,dt_k,weight=1):    #adding edge from source to destination
    if not self.include(sr_k):
      self.vertices[sr_k]= vertex=Vertex(sr_k)

    if not self.include(dt_k):
      self.vertices[dt_k]= vertex=Vertex(dt_k)

    self.vertices[sr_k].add_next(self.vertices[dt_k],weight)

  def does_edge_exist(self,sr_k,dt_k):
    if not self.include(sr_k):
      return False
    if not self.include(dt_k):
      return False
    sr_vert=self.ret_vertex(sr_k)
    if sr_vert:
      return sr_vert.edge_exist(dt_k)
    return False
  
  def size(self):
    return len(self.vertices)

class Vertex:
  def __init__(self,k):
    self.k=k
    self.pointing={}
    self.shortest_parnt_vertex = None

  def get_k(self):
    return self.k
  
  def add_next(self,dt,weight):
    self.pointing[dt]=weight

  def next(self):
    return self.pointing.keys()

  def get_wght(self,dt):
    return self.pointing[dt]

  def edge_exist(self,dt):
    return dt in self.pointing

  def set_shortest_parnt_vertex(self,vertex):
    self.shortest_parnt_vertex=vertex

def extract_int(user_input):
  try:
    N=int(user_input)
    return N
  except:
    print("Invalid int values encountered. Terminating!!")
    return None

def terminate(msg):
  if msg:
    print(msg)
  else:
    print("Invalid input error")
  print("Terminating program")
  sys.exit(0)

def add_vert(graph):
  user_input=input("Enter vertex value: ")
  vertex=extract_int(user_input)
  if not vertex:
    terminate(None)
  if not graph.ret_vertex(vertex):
    graph.add_vert(vertex)
  else:
    print("Vertex {} already exists".format(vertex))

def add_edge(graph):
  user_input=input("Enter comma separated values for <src_vertex>, <dest_vertex>, <weight> all positive int values: ")
  src,dst,weight=user_input.split(",")

  src_int=extract_int(src)
  if not isinstance(src_int,int):
    terminate("src vertex needs to be an integer value")
  if src_int<0:
    terminate("src value cannot be negative")

  dst_int=extract_int(dst)
  if not isinstance(dst_int,int):
    terminate("dst vertex needs to be an int value")
  if dst_int<0:
    terminate ("dst value cannot be negative")

  weight_int=extract_int(weight)
  if not isinstance(weight_int,int):
    terminate("weight needs to be an int value")
  if weight_int<0:
    terminate("weight cannot be a negative")
    
  graph.add_edge(src_int,dst_int,weight_int)

def print_adjacency(graph):
  print('Vertices: ',end=' ')
  for v in graph:
    print(v.get_k(),end=' ')
  print()
  print('Edges: ')
  for v in graph:
    for dest in v.next():
      w=v.get_wght(dest)
      print('(src={}, dest={}, weight={})'.format(v.get_k(),dest.get_k(),w))
      print()

def run_dijkstra(graph):
  print("Running Dijkstra Algorithm")
  def dijkstra(graph,src):
    notvisited=set(graph)
    dist=dict.fromkeys(graph,float('inf'))
    dist[src]=0
    src.set_shortest_parnt_vertex(None)
    while len(notvisited)!=0:
      close_vert=min(notvisited,key=lambda v:dist[v]) #check for next short jump weight
      notvisited.remove(close_vert)
      for nxt in close_vert.next():
        if nxt in notvisited:
          new_dist=dist[close_vert]+close_vert.get_wght(nxt)
          if dist[nxt]>new_dist:
            dist[nxt]=new_dist
            nxt.set_shortest_parnt_vertex(close_vert)
    return dist

  user_input=input("Enter comma separated values for <src vertex>, <dst vertext> between which shortest path is to be found: ")
  src,dst=user_input.split(",")
  src_int=extract_int(src)
  if not isinstance(src_int,int):
    terminate("src vertex needs to be an integer value")
  if src_int<0:
    terminate("src value cannot be negative")

  dst_int=extract_int(dst)
  if not isinstance(dst_int,int):
    terminate("dst vertex needs to be an int value")
  if dst_int<0:
    terminate("dst value cannot be negative")
  
  source=graph.ret_vertex(src_int)
  distance=dijkstra(graph,source)
  print("shortest distance between {} and {} is {}".format(src_int,dst_int,distance[graph.ret_vertex(dst_int)]))
  print()

  #printing the path
  vertex=graph.ret_vertex(dst_int)
  backtrack=[str(vertex.get_k())]
  while vertex.shortest_parnt_vertex !=None:
    backtrack.append(str(vertex.shortest_parnt_vertex.get_k()))
    vertex=vertex.shortest_parnt_vertex

  msg=" -> ".join(backtrack[::-1])
  print(msg)

def run_floyd(graph):
    print("Running Floyd Algorithm")
    def floyd(graph):
      dist={v:dict.fromkeys(graph,float('inf')) for v in graph}
      nxt_vert={v:dict.fromkeys(graph,None) for v in graph}
      for v in graph:
        for a in v.next():
          dist[v][a]=v.get_wght(a)
          nxt_vert[v][a]=a
      for v in graph:
          dist[v][v]=0
          nxt_vert[v][v]=None
      for p in graph:
          for q in graph:
            for r in graph:
              if dist[q][r]>dist[q][p]+dist[p][r]:
                dist[q][r]=dist[q][p]+dist[p][r]
                nxt_vert[q][r]=nxt_vert[q][p]

      return dist,nxt_vert
  
    def print_floyd(nxt_vert,q,r):
      p=q
      while (nxt_vert[p][r]):
        print('{} -> '.format(p.get_k()),end='')
        p=nxt_vert[p][r]
      print('{}'.format(r.get_k()),end='')
      print()

    user_input = input('Enter comma separated values for <src vertex>, <dst vertext> between which shortest path is to be found: ')
    src, dst = user_input.split(",")
    src_int = extract_int(src)
    if not isinstance(src_int, int):
        terminate("src vertex needs to be an int value")
    if src_int < 0:
        terminate("src vertext cannot be negative")
    dst_int = extract_int(dst)
    if not isinstance(dst_int, int):
        terminate("dst vertex needs to be an int value")
    if dst_int < 0:
        terminate("src vertex cannot be negative")
    # run the algorithm with src_int as src vertext
    distance, next_v = floyd(graph)
    sh_path_distance = distance[graph.ret_vertex(src_int)][graph.ret_vertex(dst_int)]
    print('Shortest Distance between {} and {} is {}'.format(src_int, dst_int, sh_path_distance))
    print()
    print_floyd(next_v, graph.ret_vertex(src_int), graph.ret_vertex(dst_int))

def update_as_complete_graph(graph):
    user_input = input('Enter number of vertices (N): ')
    number_of_vertices = extract_int(user_input)
    if number_of_vertices <= 2:
        terminate("Ensure that N is greater than 2")
    vertices = [random.randint(0, max_int) for i in range(number_of_vertices)]
    for vertex_int in vertices:
        graph.add_vert(vertex_int)
    print("Done with vertices")
    # generating edges
    for idx1 in range(0, len(vertices)):
        for idx2 in range (0, len(vertices)):
            if vertices[idx1] == vertices[idx2]:
                continue
            if not graph.does_edge_exist(vertices[idx1], vertices[idx2]):
                # adding edge
                random_weight = random.randint(1, 200)
                graph.add_edge(vertices[idx1], vertices[idx2], random_weight)
                graph.add_edge(vertices[idx2], vertices[idx1], random_weight)
    print("Done with creating edges")
    # complete graph is updated for use
    print("Test Inputs for running algorithm:")
    random_src_idx = random.randint(0, len(vertices)-1)
    print("\tSrc vertex for testing: {}".format(vertices[random_src_idx]))
    random_dst_idx = random.randint(0, len(vertices)-1)
    while True:
        if random_src_idx == random_dst_idx:
            random_dst_idx = random.randint(0, len(vertices)-1)
        else:
            random_dst_idx = random.randint(0, len(vertices)-1)
            if random_src_idx == random_dst_idx:
                continue
            break
    print("\tDst vertex for testing: {}".format(vertices[random_dst_idx]))

def update_as_sparse(graph):
    user_input = input('Enter number of vertices (N): ')
    number_of_vertices = extract_int(user_input)
    if number_of_vertices <= 1:
        terminate("Ensure that N is greater than 1")
    vertices = [random.randint(0, max_int) for i in range(number_of_vertices)]
    for vertex_int in vertices:
        graph.add_vert(vertex_int)
    print("Done with vertices")
    # generate edges - let's make sure there that each edge has 1 hop
    for idx1 in range(0, len(vertices)):
        for idx2 in range (0, len(vertices)):
            if vertices[idx1] == vertices[idx2]:
                continue
            if len(graph.ret_vertex(vertices[idx1]).next()) == 0 and not graph.does_edge_exist(vertices[idx1], vertices[idx2]):
                random_weight = random.randint(1, 200)
                graph.add_edge(vertices[idx1], vertices[idx2], random_weight)
                graph.add_edge(vertices[idx2], vertices[idx1], random_weight)
    print("Done with creating edges")
    # sparse graph is updated for use
    print("Test Inputs for running algorithm:")
    random_src_idx = random.randint(0, len(vertices)//2)
    print("\tSrc vertex for testing: {}".format(vertices[random_src_idx]))
    random_dst_idx = random.randint(0, len(vertices)//2)
    while True:
        if random_src_idx == random_dst_idx:
            random_dst_idx = random.randint(0, len(vertices)-1)
        else:
            random_dst_idx = random.randint(0, len(vertices)-1)
            if random_src_idx == random_dst_idx:
                continue
            break
    print("\tDst vertex for testing: {}".format(vertices[random_dst_idx]))
    
    
