import random
import numpy as np
import noise
from PIL import Image
import math

seed = random.randrange(-9999, 9999)
threshold = 0

water = [106, 146, 169]
water1 = [125, 169, 198]
water2 = [143, 194, 223]
water3 = [184, 221, 247]
sand = [194, 178, 128]
grass = [92, 153, 0]
grass1 = [70, 119, 0]
stone = [121, 121, 121]
darkStone = [101, 101, 101]
snowNStone = [200, 200, 200]
snow = [250, 250, 250]

shape = (1024, 1024)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

a, b = shape[0] / 2, shape[1] / 2
n = 1024
r = 250
y, x = np.ogrid[-a:n - a, -b:n - b]
mask = x ** 2 + y ** 2 <= r ** 2

center_x, center_y = shape[1] // 2, shape[0] // 2

black = [0, 0, 0]

world = np.zeros(shape)
for x in range(shape[0]):
    for y in range(shape[1]):
        world[x][y] = noise.pnoise2(x / scale,
                                    y / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=500,
                                    repeaty=500,
                                    base=(seed / scale).__round__())


def add_color(arr):
    color_world = np.zeros(arr.shape + (3,))
    for x in range(shape[0]):
        for y in range(shape[1]):
            if arr[x][y] < .10:
                color_world[x][y] = water
            elif arr[x][y] < .20:
                color_world[x][y] = water1
            elif arr[x][y] < .30:
                color_world[x][y] = water2
            elif arr[x][y] < .40:
                color_world[x][y] = water3
            elif arr[x][y] < .475:
                color_world[x][y] = sand
            elif arr[x][y] < .60:
                color_world[x][y] = grass
            elif arr[x][y] < .70:
                color_world[x][y] = grass1
            elif arr[x][y] < .80:
                color_world[x][y] = stone
            elif arr[x][y] < .90:
                color_world[x][y] = darkStone
            elif arr[x][y] < .95:
                color_world[x][y] = snowNStone
            elif arr[x][y] < 1.0:
                color_world[x][y] = snow
    return color_world


# get world between 0 and 1
max_grad = np.max(world)
min_grad = np.min(world)
world = (world - min_grad) / (max_grad - min_grad)

# Show noise
im = Image.fromarray(np.uint8(world * 255), "L")
# im.save("../assets/resources/gen/imageHeight" + str(seed) + ".png")
# im.show()

# make world height colorful
color_world = add_color(world)

# Create colored world height map image to view
im = Image.fromarray(color_world.astype("uint8"), "RGB")
# im.save("../assets/resources/gen/imageColor" + str(seed) + ".png")
# im.show()

island_world = np.zeros_like(color_world)

for i in range(shape[0]):
    for j in range(shape[1]):
        if mask[i][j]:
            island_world[i][j] = color_world[i][j]
        else:
            island_world[i][j] = black

im = Image.fromarray(island_world.astype("uint8"), "RGB")
# im.show()

circle_grad = np.zeros_like(world)

for y in range(world.shape[0]):
    for x in range(world.shape[1]):
        distx = abs(x - center_x)
        disty = abs(y - center_y)
        dist = math.sqrt(distx * distx + disty * disty)
        circle_grad[y][x] = dist

# get it between -1 and 1
max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad
circle_grad -= 0.5
circle_grad *= 2.0
circle_grad = -circle_grad

# shrink gradient
for y in range(world.shape[0]):
    for x in range(world.shape[1]):
        if circle_grad[y][x] > 0:
            circle_grad[y][x] *= 20

# get it between 0 and 1
max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad

im = Image.fromarray(np.uint8(circle_grad * 255), "L")
# im.show()

world_noise = np.zeros_like(world)

for i in range(shape[0]):
    for j in range(shape[1]):
        world_noise[i][j] = (world[i][j] * circle_grad[i][j])
        if world_noise[i][j] > 0:
            world_noise[i][j] *= 20

# get it between 0 and 1
max_grad = np.max(world_noise)
world_noise = world_noise / max_grad

im = Image.fromarray(np.uint8(world_noise * 255), "L")
im.save("../assets/resources/gen/heightmap" + str(seed) + ".png")
im.show()


def add_color2(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < threshold + .10:
                color_world[i][j] = water
            elif world[i][j] < threshold + .20:
                color_world[i][j] = water1
            elif world[i][j] < threshold + .30:
                color_world[i][j] = water2
            elif world[i][j] < threshold + .40:
                color_world[i][j] = water3
            elif world[i][j] < threshold + .475:
                color_world[i][j] = sand
            elif world[i][j] < threshold + .60:
                color_world[i][j] = grass
            elif world[i][j] < threshold + .70:
                color_world[i][j] = grass1
            elif world[i][j] < threshold + .80:
                color_world[i][j] = stone
            elif world[i][j] < threshold + .90:
                color_world[i][j] = darkStone
            elif world[i][j] < threshold + .95:
                color_world[i][j] = snowNStone
            elif world[i][j] < threshold + 1.0:
                color_world[i][j] = snow

    return color_world


island_world_grad = add_color2(world_noise)
im = Image.fromarray(island_world_grad.astype("uint8"), "RGB")
im.save("../assets/resources/gen/colormap" + str(seed) + ".png")
im.show()
