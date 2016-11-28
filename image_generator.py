from PIL import Image, ImageDraw, ImageFont
import sys
from node import TreeNode


class ImgGen(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_single(self, world_state, height, width, obstacles, id, debug):
        img = Image.new('RGB', (self.width, self.height), "white")  # create a new black image

        font = ImageFont.truetype("arial.ttf", 40)
        fill = 0

        draw = ImageDraw.Draw(img)
        for j in range(height):
            draw.line((0, j*self.height/height, self.width, j*self.height/height), fill=fill)
        for i in range(width):
            draw.line((i*self.width/width, 0, i*self.width/width, self.height), fill=fill)

        draw.line((0, self.height-1, self.width-1, self.height-1), fill=fill)
        draw.line((self.width-1, 0, self.width-1, self.height-1), fill=fill)

        for key in world_state:
            if key == "agent":
                draw.text((world_state[key][0]*self.width/width + 5, world_state[key][1]*self.height/height),
                          text="@", fill=fill, font=font)
            else:
                draw.text((world_state[key][0]*self.width/width + 13, world_state[key][1]*self.height/height + 5),
                          text=key.upper(), fill=fill, font=font)

        for pos in obstacles:
            draw.text((pos[0]*self.width/width + 15, pos[1]*self.height/height + 5), text="#", fill=fill, font=font)

        del draw

        if debug == 0:
            img.save(id+".png")
        elif debug == 1:
            img.show()

    def draw(self, world, node, folder, debug):
        count = 0
        while True:
            self.draw_single(node.world_state, world.h, world.w, world.obstacles,
                             "images/" + str(folder) + "/img" + str(count), debug)
            count += 1
            if node.parent is None:
                break
            node = node.parent
