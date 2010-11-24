import test_helper
import roguepy.dungeons.rogue

maker = roguepy.dungeons.rogue.RogueDungeonMaker(78, 24)
dungeon = maker.make_dungeon()

print dungeon

