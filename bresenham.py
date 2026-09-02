def bresenham_line_algo(start_x, start_y, end_x, end_y):
    """
    Get a list of tiles for drawing a straight line 
    using Bresenham's line algorithm
    """

    tiles = []
    # calc the distance between the relative points
    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)

    # calc the step direction between the relative points
    sx = 1 if start_x < end_x else -1
    sy = 1 if start_y < end_y else -1

    """
    Error driver parameter: decides if the map tile 
    should be part of the line based on its distance
    from the true mathematical line
    """
    err = dx - dy

    while True:
        tiles.append((start_x, start_y))

        # break loop once the "destination" tile is reached
        if start_x == end_x and start_y == end_y:
            break

        e2 = 2 * err

        # walk along x axis
        if e2 > - dy:
            err -= dy
            start_x += sx

        # walk along y axis
        if e2 < dx:
            err += dx
            start_y += sy

    return tiles


		

