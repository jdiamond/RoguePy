# This allows you to run the tests without installing the package
# or modifying your PYTHONPATH.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import roguepy.dungeons.rogue

maker = roguepy.dungeons.rogue.RogueDungeonMaker(78, 24)
dungeon = maker.make_dungeon()

print dungeon

