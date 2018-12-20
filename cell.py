class Cell:
    def __init__(self, img, x, y, threshold):
        self.edges = {}
        self.x = x
        self.y = y
        self.img = img

        corners = [img[y, x], img[y, x+1], img[y+1, x+1], img[y+1, x]] 
        # corners = [img[y+1, x], img[y+1, x+1], img[y, x+1], img[y,x]]
        case = 0
        for i, corner in enumerate(corners):
            within_threshold = 0 if corner >= threshold else 1
            case = case | (within_threshold << i)

        self.cell_type = case
        tl = 3
        tr = 2
        br = 1
        bl = 0

        top = interpolate(corners[tl], corners[tr], threshold)
        right = interpolate(corners[br], corners[tr], threshold)
        left = interpolate(corners[bl], corners[tl], threshold)
        bottom = interpolate(corners[bl], corners[br], threshold)
        center = get_center(corners)

        if case == 1:
            self.edges['bottom'] = {
                "next_entry": "right",
                "dx": -1,
                "dy": 0,
                "path": [
                    [bottom, 0],
                    [0, left]
                ]
            }
        elif case == 2:
            self.edges['right'] = {
                "next_entry": "top",
                "dx": 0,
                "dy": -1,
                "path": [
                    [1, right],
                    [bottom, 0]
                ]
            }
        elif case == 3:
            self.edges['right'] = {
                "next_entry": "right",
                "dx": -1,
                "dy": 0,
                'path': [
                    [1, right],
                    [0, left]
                ]
            }
        elif case == 4:
            self.edges['top'] = {
                'next_entry': 'left',
                'dx': 1,
                'dy': 0,
                'path': [
                    [ top, 1 ],
                    [ 1, right ]
                ]
            }
        elif case == 5:
            if center >= threshold:
                self.edges['top'] = {
                    'next_entry': 'left',
                    'dx': 1,
                    'dy': 0,
                    'path': [
                        [top, 1],
                        [1, right]
                    ]
                }
                self.edges['bottom'] = {
                    'next_entry': 'right',
                    'dx': -1,
                    'dy': 0,
                    'path': [
                        [bottom, 0],
                        [0, left]
                    ]
                }
            else:
                self.edges['top'] = {
                    'next_entry': 'right',
                    'dx': -1,
                    'dy': 0,
                    'path': [
                        [top, 1],
                        [0, left]
                    ]
                }
                self.edges['bottom'] = {
                    'next_entry': 'left',
                    'dx': 1,
                    'dy': 0,
                    'path': [
                        [bottom, 0],
                        [1, right]
                    ]
                }
        elif case == 6:
            self.edges['top'] = {
                'next_entry': 'top',
                'dx': 0,
                'dy': -1,
                'path': [
                    [top, 1],
                    [bottom, 0]
                ]
            }
        elif case == 7:
            self.edges['top'] = {
                'next_entry': 'right',
                'dx': -1,
                'dy': 0,
                'path': [
                    [top, 1],
                    [0, left]
                ]
            }
        elif case == 8:
            self.edges['left'] = {
                'next_entry': 'bottom',
                'dx': 0,
                'dy': 1,
                'path': [
                    [0, left],
                    [top, 1]
                ]
            }
        elif case == 9:
            self.edges['bottom'] = {
                'next_entry': 'bottom',
                'dx': 0,
                'dy': 1,
                'path': [
                    [bottom, 0],
                    [top, 1]
                ]
            }
        elif case == 10:
            if center >= threshold:
                self.edges['right'] = {
                    'next_entry': 'top',
                    'dx': 0,
                    'dy': -1,
                    'path': [
                        [1, right],
                        [bottom, 0]
                    ]
                }
                self.edges['left'] = {
                    'next_entry': 'bottom',
                    'dx': 0,
                    'dy': 1,
                    'path': [
                        [0, left],
                        [top, 1]
                    ]
                }
            else:
                self.edges['right'] = {
                    'next_entry': 'bottom',
                    'dx': 0,
                    'dy': 1,
                    'path': [
                        [1, right],
                        [top, 1]
                    ]
                }

                self.edges['left'] = {
                    'next_entry': 'top',
                    'dx': 0,
                    'dy': -1,
                    'path': [
                        [0, left],
                        [bottom, 0]
                    ]
                }
        elif case == 11:
            self.edges['right'] = {
                    'next_entry': 'bottom',
                    'dx': 0,
                    'dy': 1,
                    'path': [
                        [1, right],
                        [top, 1]
                    ]
                }
        elif case == 12:
            self.edges['left'] = {
                'next_entry': 'left',
                'dx': 1,
                'dy': 0,
                'path': [
                    [0, left],
                    [1, right]
                ]
            }
        elif case == 13:
            self.edges['bottom'] = {
                    'next_entry': 'left',
                    'dx': 1,
                    'dy': 0,
                    'path': [
                        [bottom, 0],
                        [1, right]
                    ]
                }
        elif case == 14:
            self.edges['left'] = {
                    'next_entry': 'top',
                    'dx': 0,
                    'dy': -1,
                    'path': [
                        [0, left],
                        [bottom, 0]
                    ]
                }

def get_center(corners):
    top_middle = corners[3] + ((corners[2] - corners[3]) * 0.5)
    bottom_middle = corners[0] + ((corners[1] - corners[0]) * 0.5)

    return bottom_middle + ((top_middle - bottom_middle) * 0.5)

def interpolate(x, y, v):
    return abs((v - x) / (y - x))
   

if __name__ == "__main__":
    print(interpolate(1, 10, 10))
    print(interpolate(10, 1, 10))
    print(interpolate(0, 10, 5))
    print(interpolate(10, 0, 5))

    corners = [1, 2, 3, 4]
    print(corners)
    print(get_center(corners))
