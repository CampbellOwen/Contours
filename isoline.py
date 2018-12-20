from quadtree import QuadTree
from cell import Cell

def get_lines(img_tree, threshold):
    paths = []
    width = img_tree.img.shape[1]
    height = img_tree.img.shape[0]
    grid = [[None for _ in range(width)] for _ in range(height)]
    for c in img_tree.get_cells_above_threshold(threshold):
        x = c[0]
        y = c[1]
        grid[y][x] = Cell(img_tree.img, x, y, threshold)
    entries = ['right', 'bottom', 'left', 'top']

    # for cell in grid:
    #     for entry in entries:
    #         if entry in cell.paths:
    #             path = []
    #             start = cell

    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                continue
            cell = grid[y][x]
            for entry in entries:
                if not cell.edges.get(entry) is None:
                    # Start new path
                    first_path = locate_path(x, y, cell.edges[entry]['path'])
                    path = []
                    if equal_path(first_path[0], first_path[1]):
                        path.append(first_path[0])
                    else:
                        path += first_path

                    start = cell
                    curr_cell = cell
                    curr_x = x
                    curr_y = y

                    next_entry = curr_cell.edges[entry]['next_entry']
                    next_x = curr_x + curr_cell.edges[entry]['dx']
                    next_y = curr_y + curr_cell.edges[entry]['dy']
                    finished = False
                    while not finished:
                        curr_x = next_x
                        curr_y = next_y
                        curr_entry = next_entry
                        if valid_path(grid, curr_x, curr_y, curr_entry):
                            curr_cell = grid[curr_y][curr_x]
                            if curr_cell == start:
                                path.append(path[0])
                                start.edges[entry] = None
                                break
                            next_entry = curr_cell.edges[curr_entry]['next_entry']
                            next_x = curr_x + curr_cell.edges[curr_entry]['dx']
                            next_y = curr_y + curr_cell.edges[curr_entry]['dy']
                            p = locate_path(curr_x, curr_y, curr_cell.edges[curr_entry]['path'])
                            if not equal_path(path[-1], p[1]):
                                path.append(p[1])
                            curr_cell.edges[curr_entry] = None

                        else:
                            finished = True
                    start.edges[entry] = None
                    deduped = remove_dups(path)
                    paths.append(deduped)
    merged = merge_paths(paths)
    return merged

def merge_paths(paths):
    num_paths = len(paths)
    count = 0
    while count < num_paths:
        currPath = paths.pop()
        for i in range(len(paths)):
            if equal_path(currPath[0], paths[i][-1]):
                count = 0
                other = paths.pop(i)
                currPath = other[:-1] + currPath
                break
            if equal_path(currPath[-1], paths[i][0]):
                count = 0
                other = paths.pop(i)
                currPath = currPath[:-1] + other
                break
        else:
            count += 1
        paths.insert(0, currPath)
        if len(paths) <= 1:
            return paths

    return paths

def remove_dups(path):
    new_path = []
    for i in range(len(path)-1):
        if not equal_path(path[i], path[i+1]):
            new_path.append(path[i])
    new_path.append(path[-1])

    return new_path

def equal_path(p1, p2):
    return equal_float(p1[0], p2[0]) and equal_float(p1[1], p2[1])
                          
def equal_float(a, b):
    epsilon = 0.000000000001  
    return abs(a - b) <= epsilon #see edit below for more info

def locate_path(x, y, path):
    return [ [path[0][0] + x, path[0][1] + y], [path[1][0] + x, path[1][1] + y]]

def valid_path(grid, x, y, entry):
    if grid[y][x] is None:
        return False
    if not grid[y][x].edges.get(entry) is None:
        return True
    return False
                

if __name__ == "__main__":
    paths = [ 
        [[1, 1], [1, 2]], 
        [[1, 2], [2, 3]],
        [[2, 3], [1, 1]],
        [[3, 4], [4, 1]]
    ]
    print(merge_paths(paths))
    paths = [[[1, 1], [1, 2]], [[1, 2], [2, 3]]]
    print(merge_paths(paths))