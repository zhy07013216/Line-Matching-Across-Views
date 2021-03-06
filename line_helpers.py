import numpy as np
import cv2

# Constants
LINE_FINITE = 0
LINE_INFINITE = 1


def length(segment):
    """
    Finds length of line segment
    :param segment: 4 tuple representing 2 points
    :return: length of line segment
    """
    x1, y1 = [segment[0], segment[1]]
    x2, y2 = [segment[2], segment[3]]
    dx = x2 - x1
    dy = y2 - y1
    return (dx*dx+dy*dy)**0.5


def points_on_segment(segment):
    # Segment endpoints
    """
    Implements Bresenham's algorithm to get all points on a line segment
    :param segment: 4 tuple representing 2 points
    :return: all points on the line segment
    """
    x1, y1 = [segment[0], segment[1]]
    x2, y2 = [segment[2], segment[3]]
    dx = x2 - x1
    dy = y2 - y1

    # Check segment steepness
    steep = abs(dy) > abs(dx)

    # Rotate if necessary
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap if necessary
    swap = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swap = True

    # New dx, dy
    dx = x2 - x1
    dy = y2 - y1

    # Error needed to determine threshold
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Bresenham's algorithm
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Swaps if necessary
    if swap:
        points.reverse()
    return points


def draw_line(img, line, color, thickness, line_type):
    """
    Draws line on image, handling both line segments and infinite lines
    :param img: 3-channel image
    :param line: either 3- or 4-tuple
    :param color: 3-tuple (R, G, B)
    :param thickness: thickness of line
    :param line_type: either finite line or infinite line
    """
    if line_type == LINE_FINITE:
        cv2.line(img, (int(line[0]), int(line[1])), (int(line[2]), int(line[3])), color, thickness, cv2.LINE_AA)
    # Infinite lines ax + by + c = 0 are represented by a homogeneous 3-vector (a, b, c)
    elif line_type == LINE_INFINITE:
        _, c, _ = img.shape
        x0, y0 = map(int, [0, -line[2] / line[1]])
        x1, y1 = map(int, [c, -(line[2] + line[0] * c) / line[1]])
        cv2.line(img, (x0, y0), (x1, y1), color, thickness, cv2.LINE_AA)


def __segment2line(segment):
    x0, y0 = [segment[0], segment[1]]
    x1, y1 = [segment[2], segment[3]]
    return np.asarray([y0-y1, x1-x0, y1*x0-x1*y0]).astype(float)


def intersect_lines(line1, line2):
    """
    Finds intersection of 2 lines
    :param line1: 3-tuple ax+by+c=0
    :param line2: 3-tuple ax+by+c=0
    :return: x,y, the intersection of the lines
    """
    homogeneous = np.cross(line1, line2)
    homogeneous = homogeneous.astype(float)
    homogeneous /= homogeneous[2]
    return homogeneous[0:2]


def intersect_segment_line(segment, line):
    """
    Returns whether segment and line intersect, and if so, the point of intersection
    :param segment: 4-tuple representing 2 endpoints
    :param line: 3-tuple ax+by+c=0
    :return: boolean representing whether they intersect, and the point
    """
    x0, y0 = [segment[0], segment[1]]
    x1, y1 = [segment[2], segment[3]]
    segment = __segment2line(segment)
    x, y = intersect_lines(segment, line)
    if (x0 <= x <= x1 or x0 >= x >= x1) and (y0 <= y <= y1 or y0 >= y >= y1):
        return True, (x, y)
    else:
        return False, None


def intersects_beam(segment, line1, line2):
    """
    Returns whether a segment intersects 2 epilines
    :param segment: 4-tuple representing 2 endpoints
    :param line1: 3-tuple ax+by+c=0
    :param line2: 3-tuple ax+by+c=0
    :return: boolean representing whether they intersect
    """
    intersects1, _ = intersect_segment_line(segment, line1)
    intersects2, _ = intersect_segment_line(segment, line2)
    if intersects1 or intersects2:
        return True
    else:
        return False
