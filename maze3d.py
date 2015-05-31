# maze3d.py: a 3-dimensional maze generator
# Copyright (C) 2015 Mike Bionchik
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import operator
import random


class Node:

    indeces = {'front': 0, 'back': 1, 'left': 2, 'right': 3, 'up': 4, 'down': 5}

    def __init__(self):
        self.ways = [False,False,False,False,False,False]
        self.visited = False

    def __repr__(self):
        return str([n[0]
            for n in zip(['front','back','left','right','up','down'], self.ways)
            if n[1]])

    def can_go(self, where):
        return self.ways[Node.indeces[where]]

    def go(self, where):
        self.ways[Node.indeces[where]] = True
        self.visited = True


class Maze3D:

    directions = {'front': (1,0,0), 'back': (-1,0,0), 'left': (0,1,0),
                  'right': (0,-1,0), 'up': (0,0,1), 'down': (0,0,-1)}

    opposites = {'front': 'back', 'back': 'front', 'left': 'right',
                 'right': 'left', 'up': 'down', 'down': 'up'}

    def __init__(self, max_dim, debug=False):
        self.maze = {n: Node()
                        for n in [(x,y,z)
                            for x in range(max_dim[0])
                            for y in range(max_dim[1])
                            for z in range(max_dim[2])]}
        self.stack = []
        self.total_pts = 0
        self.max_pts = max_dim[0]*max_dim[1]*max_dim[2]
        self.dim = max_dim
        self.debug = debug

    def is_inside(self, (x,y,z)):
        return not (x < 0 or x >= self.dim[0] or
                    y < 0 or y >= self.dim[1] or
                    z < 0 or z >= self.dim[2])

    def get_directions(self, node_key):
        return [n for n in Maze3D.directions.keys()
                if self.is_inside(tuple(map(operator.add,
                    node_key, Maze3D.directions[n])))]

    def get_unvisited_directions(self, node_key):
        return [n for n in self.get_directions(node_key)
                if not self.maze[tuple(map(operator.add,
                    node_key, Maze3D.directions[n]))].visited]

    def get_adjacent_nodes(self, node_key):
        return [tuple(map(operator.add, node_key, n))
                for n in [Maze3D.directions[val]
                    for val in self.get_directions(node_key)]]

    def get_unvisited_nodes(self, node_key):
        return [n for n in self.get_adjacent_nodes(node_key)
                if not self.maze[n].visited]

    def generate(self):
        #curr = (0,0,0)
        curr = (random.randint(0,self.dim[0]-1),
                random.randint(0,self.dim[1]-1),
                random.randint(0,self.dim[2]-1))
        self.total_pts += 1
        while self.total_pts < self.max_pts:
            unvisited = self.get_unvisited_directions(curr)
            while len(unvisited) > 0:
                where = random.choice(unvisited)
                if self.debug:
                    print str(curr)+' going '+where
                self.stack.append(where)
                self.maze[curr].go(where)
                curr = tuple(map(operator.add, curr, Maze3D.directions[where]))
                self.maze[curr].go(Maze3D.opposites[where])
                self.total_pts += 1
                unvisited = self.get_unvisited_directions(curr)

            while len(unvisited) == 0 and self.total_pts < self.max_pts:
                prev = curr
                curr = tuple(map(operator.sub,
                    curr, Maze3D.directions[self.stack.pop()]))
                if self.debug:
                    print str(prev)+' backtrack to '+str(curr)
                unvisited = self.get_unvisited_directions(curr)
