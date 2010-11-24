import random
import roguepy.grid

def rnd(n):
    if n == 0:
        return 0
    return random.randrange(n)

class RogueDungeonMaker(object):

    AREAS = 3
    MIN_ROOM_SIZE = 4
    MIN_ROOM_PADDING = 1
    MIN_ROOMS = 5

    HORIZONTAL_WALL = '|'
    VERTICAL_WALL = '-'
    FLOOR = '.'
    PASSAGE = '#'
    DOOR = '+'

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def make_dungeon(self):
        dungeon = roguepy.grid.Grid(self.width, self.height)

        rooms = self.generate_rooms()
        self.remove_rooms(rooms)
        self.place_tiles(rooms, dungeon)
        self.connect_rooms(rooms, dungeon)

        return dungeon

    def generate_rooms(self):
        rooms = []

        area_width = self.width / self.AREAS
        area_height = self.height / self.AREAS

        g = roguepy.grid.Grid(self.AREAS, self.AREAS)

        i = 0

        for y in range(g.height):
            for x in range(g.width):
                room = g[x, y] = Room(i)
                rooms.append(room)
                i += 1

        i = 0

        for room in rooms:
                gx = i % self.AREAS
                gy = i / self.AREAS

                area_x = gx * area_width
                area_y = gy * area_height

                room.width = random.randrange(
                                self.MIN_ROOM_SIZE,
                                area_width - self.MIN_ROOM_PADDING + 1)
                room.height = random.randrange(
                                self.MIN_ROOM_SIZE,
                                area_height - self.MIN_ROOM_PADDING + 1)
                room.x = area_x + \
                         random.randrange(self.MIN_ROOM_PADDING,
                                          area_width - room.width + 1)
                room.y = area_y + \
                         random.randrange(self.MIN_ROOM_PADDING,
                                          area_height - room.height + 1)

                room.unconnected_neighbors = g.get_neighbors((gx, gy))

                i += 1

        return rooms

    def remove_rooms(self, rooms):
        existing_rooms = [room for room in rooms]
        for i in range(random.randrange(len(rooms) - self.MIN_ROOMS + 1)):
            room = random.choice(existing_rooms)
            existing_rooms.remove(room)
            room.exists = False

    def place_tiles(self, rooms, dungeon):
        for room in rooms:
            if room.exists:
                self.vert(dungeon, room, room.x)
                self.vert(dungeon, room, room.x + room.width - 1)
                self.horiz(dungeon, room, room.y)
                self.horiz(dungeon, room, room.y + room.height - 1)

                for y in range(room.y + 1, room.y + room.height - 1):
                    for x in range(room.x + 1, room.x + room.width - 1):
                        dungeon[x, y] = self.FLOOR

    def vert(self, m, room, x):
        for y in range(room.y + 1, room.y + room.height):
            m[x, y] = self.HORIZONTAL_WALL

    def horiz(self, m, room, y):
        for x in range(room.x, room.x + room.width):
            m[x, y] = self.VERTICAL_WALL

    def connect_rooms(self, rooms, dungeon):
        connected_rooms = []
        unconnected_rooms = [room for room in rooms]
        room1 = random.choice(unconnected_rooms)
        while unconnected_rooms:
            if room1.unconnected_neighbors:
                room2 = random.choice(room1.unconnected_neighbors)
                self.connect(room1, room2, rooms, dungeon)
                if room1 in unconnected_rooms:
                    unconnected_rooms.remove(room1)
                    connected_rooms.append(room1)
                if room2 in unconnected_rooms:
                    unconnected_rooms.remove(room2)
                    connected_rooms.append(room2)
            else:
                room1 = random.choice(connected_rooms)

    def connect(self, room1, room2, rooms, dungeon):
        room1.connected_neighbors.append(room2)
        if room1 not in room2.connected_neighbors:
            room2.connected_neighbors.append(room1)

        room1.unconnected_neighbors.remove(room2)
        if room1 in room2.unconnected_neighbors:
            room2.unconnected_neighbors.remove(room1)

        # Draw connection here!

        if room1.number < room2.number:
            from_room = room1
            to_room = room2
            if room1.number + 1 == room2.number:
                d = 'r'
            else:
                d = 'd'
        else:
            from_room = room2
            to_room = room1
            if room2.number + 1 == room1.number:
                d = 'r'
            else:
                d = 'd'

        if d == 'd': # down
            dx = 0
            dy = 1
            sx = from_room.x
            sy = from_room.y
            ex = to_room.x
            ey = to_room.y
            if from_room.exists:
                sx = from_room.x + random.randrange(from_room.width - 2) + 1
                sy = from_room.y + from_room.height - 1
            if to_room.exists:
                ex = to_room.x + random.randrange(to_room.width - 2) + 1
            distance = abs(sy - ey) - 1
            ty = 0
            tx = sx < ex and 1 or -1
            turn_distance = abs(sx - ex)
        else: # right
            dx = 1
            dy = 0
            sx = from_room.x
            sy = from_room.y
            ex = to_room.x
            ey = to_room.y
            if from_room.exists:
                sx = from_room.x + from_room.width - 1
                sy = from_room.y + random.randrange(from_room.height - 2) + 1
            if to_room.exists:
                ey = to_room.y + random.randrange(to_room.height - 2) + 1
            distance = abs(sx - ex) - 1
            ty = sy < ey and 1 or -1
            tx = 0
            turn_distance = abs(sy - ey)

        turn_spot = 0

        if distance == 1:
            turn_spot = random.randrange(1)
        elif distance == 2:
            turn_spot = random.randrange(2)
        else:
            turn_spot = random.randrange(distance - 2) + 1

        dungeon[sx, sy] = from_room.exists and self.DOOR or self.PASSAGE
        dungeon[ex, ey] = to_room.exists and self.DOOR or self.PASSAGE

        cx = sx
        cy = sy

        while distance > 0:
            cx += dx
            cy += dy
            distance -= 1
            if distance == turn_spot:
                while turn_distance > 0:
                    turn_distance -= 1
                    dungeon[cx, cy] = self.PASSAGE
                    cx += tx
                    cy += ty
            dungeon[cx, cy] = self.PASSAGE

class Room(object):
    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.exists = True
        self.unconnected_neighbors = None
        self.connected_neighbors = []

