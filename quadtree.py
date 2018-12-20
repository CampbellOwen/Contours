import math
import numpy as np

class QuadTree:

    def msb(self, x):
        msb = 0
        while not x==0:
            x = x >> 1
            msb += 1
        return msb-1


    def __init__(self, img, x, y, dx, dy):
        self.has_children = False
        self.x = x
        self.y = y
        self.img = img
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        # (dx_q, dx_r) = divmod(dx, 2)
        # dx_left = dx_q
        # dx_right = dx_q
        # if not dx_r == 0:
        #     dx_left = math.floor(dx_q)
        #     dx_right = math.ceil(dx_q)

        # (dy_q, dy_r) = divmod(dy, 2)
        # dy_top = dy_q
        # dy_bottom = dy_q
        # if not dy_r == 0:
        #     dy_top = math.floor(dy_q)
        #     dy_bottom = math.ceil(dy_q)
        msb_x = 0
        msb_y = 0

        if dx > 1:
            msb_x = self.msb(dx)
            if (1 << msb_x) == dx:
                msb_x -= 1
        if dy > 1:
            msb_y = self.msb(dy)
            if (1 << msb_y) == dy:
                msb_y -= 1

        new_dx = (1 << msb_x)
        new_dy = (1 << msb_y)

        if dx == 1 and dy == 1:
            self.lower_bound = min(img[y, x], img[y, x+1], img[y+1, x], img[y+1, x+1])
            self.upper_bound = max(img[y, x], img[y, x+1], img[y+1, x], img[y+1, x+1])
        else:
            self.has_children = True
            children = []
            self.a = QuadTree(img, x, y, new_dx, new_dy)
            children.append(self.a)

            if (dx - new_dx) > 0:
                self.b = QuadTree(img, x+new_dx, y, dx-new_dx, new_dy)
                children.append(self.b)

                if (dy - new_dy) > 0:
                    self.c = QuadTree(img, x+new_dx, y+new_dy, dx-new_dx, dy-new_dy)
                    children.append(self.c)
            if (dy-new_dy) > 0:
                self.d = QuadTree(img, x, y+new_dy, new_dx, dy-new_dy)
                children.append(self.d)

            self.lower_bound = min([n.lower_bound for n in children])
            self.upper_bound = max([n.upper_bound for n in children])

        # if dx_left >= 1 and dx_right >= 1 and dy_top >= 1 and dy_bottom >= 1:
        #     self.a = QuadTree(img, x, y, dx_left, dy_top)
        #     self.b = QuadTree(img, x + dx_left, y, dx_right, dy_top)
        #     self.c = QuadTree(img, x, y+dy_top, dx_left, dy_bottom)
        #     self.d = QuadTree(img, x+dx_left, y+dy_top, dx_right, dy_bottom)

        #     self.lower_bound = min(self.a.lower_bound, self.b.lower_bound, self.c.lower_bound, self.d.lower_bound)
        #     self.upper_bound = max(self.a.upper_bound, self.b.upper_bound, self.c.upper_bound, self.d.upper_bound)
        # else:
        #     self.lower_bound = min(img[y, x], img[y, x+1], img[y+1, x], img[y+1, x+1])
        #     self.upper_bound = max(img[y, x], img[y, x+1], img[y+1, x], img[y+1, x+1])

    def get_cells_above_threshold(self, threshold):
        if self.upper_bound < threshold:
            return []
        cells = []
        if not self.has_children:
            cells.append([self.x, self.y])
        else:
            if not self.a is None:
                cells += self.a.get_cells_above_threshold(threshold)
            if not self.b is None:
                cells += self.b.get_cells_above_threshold(threshold)
            if not self.c is None:
                cells += self.c.get_cells_above_threshold(threshold)
            if not self.d is None:
                cells += self.d.get_cells_above_threshold(threshold)


        return cells

if __name__ == "__main__":
    g = np.array([[1,2,3,2,1],[2,3,4,3,2], [3,4,5,4,3], [2,3,4,3,2],[1,2,3,2,1]])
    # print("\n".join([",  ".join([str(x) for x in row]) for row in g]))
    for row in range(g.shape[0]-1, -1, -1):
        print(",  ".join([str(x) for x in g[row,:]]))
    tree = QuadTree(g, 0, 0, 4, 4)
    threshold = 5
    cells = tree.get_cells_above_threshold(threshold)
    print("Done")

