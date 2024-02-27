"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/25/2024

Purpose:

Details:

Description:

Notes:
    A Math solution to drawing the spiral.

    Adding to the grid DOES take in account invalid grid positions
    as valid positions to place numbers.

IMPORTANT NOTES:
    A GigaChad solution

Explanation:

Reference:

"""
from typing import Tuple

from common import Grid
from common import Position
from common import get_grid
from common import print_grid

"""
An algorithm to add numbers to the spiral mathematically

Notes:

    (0a) Recall that going right on the grid increases the indexes and going down the grid also increases the
    indexes. Basically we start from the top left and we go left to right then down and then we repeat to get a
    bigger (x, y) position.

    (0b) Let the center of the spiral be the origin or the Center position and
    any Given position will be relative to that Center position.

    (1) If you think about a spiral, you see that most of the of numbers logical follow along a
    direction of a circle / ring. You can see that the numbers on the circle / ring have a difference of 1.
        Example
            Ring 0 -> 1  # Size 1
            Ring 1 -> 2 3 4 5 6 7 8 9  # Size 8
            Ring 2 -> 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  # Size 16
            Ring 3 -> 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49  # Size 24
            ...
    * Notice the size of each ring, it will be important for making a formula

    (2a) Notice that the spiral will go Right -> Down -> Left -> Up and then it will repeat.
    If you count how many numbers a direction covers in a circle / ring (recall that the numbers logically follow),
    then you can see that each direction takes the same amount except for the Down direction and
    Right direction.
    The Down direction takes 1 less because of the previous ring's Right direction.
    The Right direction takes 1 more because it goes into the next ring.
        So the pattern is:
            Right 1  # Starting at value = 1, Count how many times we can go Right logically = 1  # Ring 0 to Ring 1
            Down 1   # Starting at value = 2, Count how many times we can go Down logically = 1
            Left 2   # Starting at value = 3, Count how many times we can go Left logically = 2
            Up 2     # Starting at value = 5, Count how many times we can go Up logically = 2
            Right 3  # Starting at value = 7, Count how many times we can go Right logically = 3  # Ring 1 to Ring 2
            Down 3
            Left 4
            Up 4
            Right 5  # Staring value = 21, Count logically Right = 5  # Ring 2 to Ring 3
            Down 5   # Staring value = 26, Count logically Down = 5
            Left 6   # Staring value = 31, Count logically Left = 6
            Up 6     # Staring value = 37, Count logically Up = 6
            Right 7  # Staring value = 43, Count logically Right = 7  # Ring 3 to Ring 4
            Down 7
            ...
    * Notice that there is a pattern with the Starting values in the above pattern,
    I have no idea what that pattern is... Maybe later, I will figure it out.

    (2b) For ring movement, it goes Down -> Left -> Up -> Right. Recall the pattern from (2a),
    if we now start from the Down direction where the first position is the last position from the previous
    ring's Right direction and WE INCLUDE THAT POSITION IN OUR COUNT, we can see a better pattern.
        Better pattern:
            ----  # Ring 0 (Center position)
            Down 0  # Staring at ring 0 which is just the Center position
            Left 0
            Up 0
            Right 0
            -----  # Ring 1
            Down 2   # Includes numbers: 2 3  # Starting at the logically following position Right of Ring 0
            Left 2   # Includes numbers: 4 5
            Up 2     # Includes numbers: 6 7
            Right 2  # Includes numbers: 8 9
            -----  # Ring 2
            Down 4   # Includes numbers: 10 11 12 13  # Starting at the logically following position Top Right of Ring 1
            Left 4   # Includes numbers: 14 15 16 17
            Up 4     # Includes numbers: 18 19 20 21
            Right 4  # Includes numbers: 12 13 24 25
            ...

    (3a) We can make an equation based on (2b) ring movement to get the size of each ring based on the ring index.
        Size of each ring equation:

            size_of_ring = get_size_of_ring_index(index_ring) = (4 * (index_ring * 2)) if index_ring > 0 else 1

            Obviously in the above equation there is no negative ring indexes.
            * Notice that the equation is more representative and intuitive when relating a side of a Ring
            based on a index_ring, this means you could modify the equation to somehow tell you what
            number you are on in a ring based on the side you are on in the ring.
    
    (3b) We can modify the equation in (3a) to include the index of a side or the side count by replacing the 4 in 
    the equation. By replacing 4 with a variable, the functionality and name of the function should changes as well.
        Length of ring by side
        
            length_of_ring = get_length_of_ring_by_side_accumulative(index_ring, index_side) = (
                (index_side * (index_ring * 2)) if index_ring > 0 else 1
            )
    
    (3c) If we look at sizes of each ring from (1) we see they are all multiples of 8 except for the side of Ring 0
        Pattern
            Ring 0  # Size 0
            Ring 1  # Size 8 <- Multiple of 8
            Ring 2  # Size 16 <- Multiple of 8
            Ring 3  # Size 24 <- Multiple of 8

        Size of each ring equation better:
            size_of_ring = get_size_of_ring_index_v2(index_ring) = 8 * index_ring if index_ring > 0 else 1

            Alternatively, we could have simplified get_size_of_ring_index to get get_size_of_ring_index_v2 from (3a).
            Also, no negative ring indexes.

    (4a) Notice that a Given position relative to the Center position (recall that we decided this in (0b))
    tells us what ring we are in based on the highest absolute value of a component in a Given position.
        Example
            (x, y)
            (2, 5)  # We are on Ring 5
            (5, 2)  # We are on Ring 5
            (-5, 2)  # We are on Ring 5
            (3, 23)  # We are on Ring 23
    The reason why the above is true is that if you make the smaller component of the position greater than the
    highest component of the position, then you will notice that you just moved in to a higher level ring.
        Example
            (1, 0)  # Ring 1, Value = 2, Small component = y
            (1, 1)  # Ring 1, Value = 3, Bottom Right Corner of Ring 1
            (1, 2)  # Ring 2, Value = 14, Small component = x
            (1, 3)  # Ring 3, Value = 33, Small component = x

    (4b) Notice from (4a) that most of the time the numbers logically follow when you increase or decrease
    the absolute value of the smaller component to be <= absolute value of the bigger component.
        Example
            (-4, -3) -> 72  # Ring 4, this does not logically follow the next number
            (-3, -3) -> 43  # Ring 3, Top Left Corner of Ring 3
            (-2, -3) -> 44  # Ring 3
            (-1, -3) -> 45  # Ring 3
            (0, -3) -> 46  # Ring 3
            (1, -3) -> 47  # Ring 3
            (2, -3) -> 48  # Ring 3
            (3, -3) -> 49  # Ring 3, Top Right Corner of Ring 3
            (4, -3) -> 50  # Ring 4, Special case where the numbers do logically follow
            (5, -3) -> 83  # Ring 5, this does not logically follow the previous number

    (4c) Notice in the examples for (4a) and (4b), Corners of a Ring, we'll call Ring Corners, exist when
    the absolute value of each of their components are the same.
        Pattern
            (+, -)  # Top Right Corner
            (+, +)  # Bottom Right Corner
            (-, +)  # Bottom Left Corner
            (-, -)  # Top Left Corner
        Example
            (1, -1)     # Ring 1, Top Right Corner
            (1, 1)      # Ring 1, Bottom Right Corner
            (-1, 1)     # Ring 1, Bottom Left Corner
            (-1, -1)    # Ring 1, Top Left Corner

    * This can be useful for determining where a corner of each side starts and thus what direction you should go.
    * This can be useful for determining the starting value of each ring's corner.

    (5a) Notice that the sign of any position relative to the Center position (recall that we decided this in (0b))
    tells us which Math Quadrant we are in (the quadrants are relative to how the grid works stated in (0a)
    because going down vertically is positive and going up vertically is negative).
    Look at (5b) for the pattern.

    (5b) The comparison of the absolute value of each component tells us which direction we are going.
    The component with the highest absolute value tells us the smaller absolute value component moves along
    the perpendicular axis of the component with the highest absolute value.
        Pattern
            (x, y)
            (-, -) -> Quadrant 3 (Top Left), Going Up or Right
                        Going Up if abs(y) < abs(x)
                        Going Right if abs(x) < abs(y)
                        Going Right if abs(x) == abs(y)  # Numbers don't logically follow when going Up

            (-, +) -> Quadrant 2 (Bottom Left), Going Left or Up
                        Going Left if abs(x) < abs(y)
                        Going Up if abs(y) < abs(x)
                        Going Up if abs(y) == abs(x)  # Numbers don't logically follow when going Left

            (+, -) -> Quadrant 4 (Top Right), Going Right or Down
                        Going Right if abs(x) < abs(y)
                        Going Right if abs(x) == abs(y)  # Going Right again goes to the next ring
                        Going Down if abs(y) < abs(x)

            (+, +) -> Quadrant 1 (Bottom Right), Going Down or Left
                        Going Left if abs(x) < abs(y)
                        Going Left if abs(x) == abs(y)  # Numbers don't logically follow when going Down
                        Going Down if abs(y) < abs(x)
        Example
            (-4, 3)
                (-, +)
                Quadrant 2 (Bottom Left)
                Going Up since abs(y) < abs(x)
            (-4, 4)
                (-, +)
                Quadrant 2 (Bottom Left)
                Going Up since abs(y) == abs(x)
            (-3, 4)
                (-, +)
                Quadrant 2 (Bottom Left)
                Going Left since abs(x) < abs(y)

    An easier way to understand the above pattern is to think of the RIGHT SIDE of the inequality as
    the bounding row or column and the LEFT SIDE of the inequality as the number that slides along perpendicular
    to that row or column.
        Explanation:
            Given
                abs(y) < abs(x)
                (4, 2)  # Position given, Ring 4

            1. x is the bound, so go to the correct x column and ignore the y component by setting y = 0.
            You get (x, 0) where x is whatever the x value is from a given (x, y) position.
            So
                x = 4 and 4 is the bound.
                Think of it as (4, 0)

            2. If you don't change the x value (Make it constant), and you vary the y component where
            abs(y) < abs(x) then you know which side of the ring you are on.
            So
                (4, y) where abs(y) < abs(x)
                You vary y, so you are sliding along x = 4 which is vertical which means that you are on
                the right or left side of the ring.
                Since x = 4 is positive, then you automatically know that you are on the right side of Ring 4
                because x = 4 is greater than x = 0 and x = 0 is the Center position.

            3. If you recall that we move in a ring from Down -> Left -> Up -> Right from (2b)
            then you know what direction you are going which is based on the side you are on.
            So
                We are on the Right side of Ring 4 (Which is on the right side of the spiral) because of x = 4.
                So we are going Down.

            Given
                abs(y) == abs(x)
                (5, -5)  # Position given, Ring 5

            1. We are at a corner, recall that ring movement is Down -> Left -> Up -> Right from (2b), recall
            what quadrant we are in based on the signs of the component (+, -) from (5a) and (5b).
            So
                (5, -5) is (+, -) which is Quadrant 4 (Top Right) on Ring 5
                We must go logically Right because the numbers logically follow and we will go into the next
                ring.

    (5c) Based on (5b) we can make a more useful pattern for determining what side we are on any ring.
    Looking at the pattern stated in (5b) we can see any direction is stated in 2 quadrants.
    We can simplify the pattern in (5b) by forgoing the quadrants and only caring about the signs of components and
    which component has the higher absolute value.
        Pattern for directions:
        
            if abs(x) <= abs(y)
                if y is Negative
                    Top side
                        Must go Right to logically follow numbers
                        return
                        
                else if y is Positive
                    Bottom side
                        Must go Left to logically follow numbers
                        return
                        
            if abs(y) <= abs(x)
                if x is Negative
                    Left side
                        Must go Up to logically follow numbers
                        return
                        
                else if x is Positive
                    Right side
                        Must go Down to logically follow numbers
                        return
                        
        * Note that "<=" is used for both conditionals to take in account the corners which is why you cannot use 
        "else if" on the second outer if statement because sides share the same corners.         
        
        Example:
            (-5, 4)
                abs(y) <= abs(x)
                    x is Negative
                        Left side
                            Must go Up to logically follow numbers
                            return
                            
    (6a) We need an equation to give us the total sum of the previous rings which we will call the total count size.
    The Current ring we are on is based on a Given position's highest absolute value component,
    refer to (4a) to know what a Given position's ring is and you can see it being used in (4b), (5b), and (5c).
    Also refer to (0b) to know that a Given position is relative to the Center position.
    Recall the equations from (3a), (3b), and (3c), we can use one of those equations to find the sum of all 
    the ring sizes before the current ring.
    We will use the below equation from (3b) because it is the most versatile equation:

        length_of_ring = get_length_of_ring_by_side_accumulative(index_ring, index_side) = (
            (index_side * (index_ring * 2)) if index_ring > 0 else 1
        )

    Now we need a Summation of the above equation to give us the total count from the previous rings except for the
    current ring. We don't want the summation to run on the Current ring because that value is based on the
    total count size of the previous rings plus converting a Given position into a value on the current ring.

        1 + Summation from i=1 to index_ring-1 of (4 * (index_ring * 2))

        a. The plus 1 at the beginning comes from "if index_ring > 0 else 1" because
        get_size_of_ring_index(0) should equal 1 and not 0

        b. "Summation from i=1 to index_ring-1" is the summation. "i" is 1 because the plus 1 at the
        beginning is "i=0". The "index_ring-1" is because we want to solve for the total size of the previous rings.

        c. "(4 * (index_ring * 2))" comes from get_size_of_ring_index(index_ring)

    Finding the closed-form solution of the summation using the "I don't know how to solve this properly because
    i'm to lazy to figure it out" method.

        1 + Summation from i=1 to index_ring-1 of (4 * (index_ring * 2)) where index_ring = [0, 1, 2, 3, 4, 5]

        we get [1, 1, 9, 25, 49, 81]

        The above pattern has its values squared, and it has the sequence of 0, 1, 3, 5, 7, 9
        The closed-form solution of the summation is

        ((2 * index_ring) - 1)^2

        So

        1 + Summation from i=1 to index_ring-1 of (4 * (index_ring * 2)) = ((2 * index_ring) - 1)^2
    
    (6b) Alternatively, for a cleaner summation and thus a better closed-form solution you can remove the -1 from the 
    upper bound of the summation; however, you need to keep in mind that this will give you the size of all rings 
    including index_ring.
    
        1 + Summation from i=1 to index_ring of (4 * (index_ring * 2)) where index_ring = [0, 1, 2, 3, 4, 5]
    
        we get [1, 9, 25, 49, 81, 121]

        The above pattern has its values squared, and it has the sequence of 1, 3, 5, 7, 9, 11
        The closed-form solution of the summation is

        ((2 * index_ring) + 1)^2

        So

        1 + Summation from i=1 to index_ring of (4 * (index_ring * 2)) = ((2 * index_ring) + 1)^2
    
    (7) Now we have to make an equation when given a relative position to the Center position, we will get
    the length or the current distance from the start of the Current ring.
    Recall values and size of a ring from (1).
    Recall Ring movement Down -> Left -> Up -> Right from (2b).
    Recall Ring Corners and their signs from (4c).

        (+, -)  # Top Right Corner
        (+, +)  # Bottom Right Corner
        (-, +)  # Bottom Left Corner
        (-, -)  # Top Left Corner

    Recall the closed-form solution for the total size of the rings before the current ring from (6a) and (6b)
    respectively.

        ((2 * index_ring) - 1)^2
        ((2 * index_ring) + 1)^2

    Recall the pattern for finding what side of a ring you are on based on a Given position from (5c).

        if abs(x) <= abs(y)
            if y is Negative
                Top side
                    Must go Right to logically follow numbers
                    return
                    
            else if y is Positive
                Bottom side
                    Must go Left to logically follow numbers
                    return
                    
        if abs(y) <= abs(x)
            if x is Negative
                Left side
                    Must go Up to logically follow numbers
                    return
                    
            else if x is Positive
                Right side
                    Must go Down to logically follow numbers
                    return
                    
    Recall the versatile equation for finding the length of a ring from (3b).

        length_of_ring = get_length_of_ring_by_side_accumulative(index_ring, index_side) = (
            (index_side * (index_ring * 2)) if index_ring > 0 else 1
        )
            
    Let's find a pattern in Ring 1 and Ring 2

        Ring 1 values: 2 3 4 5 6 7 8 9  # Size = 8
        Ring 1 values by direction:
            Down    [2 3]     # abs(y) < abs(x), x is constant, y has to change in the positive direction
                    [(1, 0), (1, 1)]
                    Changing y components in positive direction
                        [0, 1]

            Left    [4 5]     # abs(x) < abs(y), y is constant, x has to change in the negative direction
                    [(0, 1), (-1, 1)]
                    Changing x components in negative direction
                        [0, -1]

            Up      [6 7]     # abs(y) < abs(x), x is constant, y has to change in the negative direction
                    [(-1, 0), (-1,-1)]
                    Changing y components in negative direction
                        [0, -1]

            Right   [8 9]     # abs(x) < abs(y), y is constant, x has to change in the positive direction
                    [(0, -1), (1, -1)]
                    Changing x components in positive direction
                        [0, 1]

        Ring 2 values: 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  # Size = 16
        Ring 2 values by direction:
            Down    [10 11 12 13]  # abs(y) < abs(x), x is constant, y has to change in the positive direction
                    [(2, -1), (2, 0), (2, 1), (2, 2)]
                    Changing y components in positive direction
                        [-1, 0, 1, 2]

            Left    [14 15 16 17]  # abs(x) < abs(y), y is constant, x has to change in the negative direction
                    [(1, 2), (0, 2), (-1, 2), (-2, 2)]
                    Changing x components in negative direction
                        [1, 0, -1, -2]

            Up      [18 19 20 21]  # abs(y) < abs(x), x is constant, y has to change in the negative direction
                    [(-2, 1), (-2, 0), (-2, -1), (-2, -2)]
                    Changing y components in negative direction
                        [1, 0, -1, -2]

            Right   [22 23 24 25]  # abs(x) < abs(y), y is constant, x has to change in the positive direction
                    [(-1, -2), (0, -2), (1, -2), (2, -2)]
                    Changing x components in positive direction
                        [-1, 0, 1, 2]
        Notes:
            1. When going vertical,     lock the x value and vary the y value
            2. When going horizontal,   lock the y value and vary the x value
            3. When going Down,  y values go in the positive direction
            4. When going Left,  x values go in the negative direction
            5. When going Up,    y values go in the negative direction
            6. When going Right, x values go in the positive direction

            7. End of a ring is always at a the top right diagonal so going right on a diagonal will start on the
            new ring.
            8a. The end of a ring has the signs (+, -)
            8b. The end of a ring has the position format (i, -1 * i)
            9a. The start of a ring has the signs (+, -)
            9b. The start of a new ring has the position format (i, -1 * (i-1)) where i is the
            current index_ring and index_ring > 0

            10. The Changing x or y components have the same absolute numbers but just different
            signs because of direction movement and starting position.
            11. The Changing x or y components between Ring 1 and Ring 2 show that Ring 2 expands
            outward in both the negative and positive directions which also encompasses the
            Changing x or y components of Ring 1
            12. The Changing x or y components going Down or Right go in the positive direction, while
            The Changing x or y components going Up or Left go in the negative direction.

    There are 2 relationships that are useful from the above,
        Relationship 1
            Using the algorithm to determine what side you are on based on a Given position from (5c)
            and using and renaming variables from the equation from (3b), we can make an algorithm to count
            the length of the previous sides before the side of the Given position.
            Because the algorithm from (5c) uses returns to escape the conditionals, if you want to continue
            without exiting immediately, you need to replace the returns with exit conditionals, in this case
            we use "_done" to signify that the conditional checking is done.

                number_of_sides_before_side_current = 0

                x_abs_position_given = abs(position_given[0])
                y_abs_position_given = abs(position_given[1])
                
                _done = False
                
                if x_abs_position_given <= y_abs_position_given and not _done
                    if y of position_given is Negative
                        Top side
                            Must go Right to logically follow numbers
                            number_of_sides_before_side_current = 3
                            _done = True

                    else if y of position_given is Positive
                        Bottom side
                            Must go Left to logically follow numbers
                            number_of_sides_before_side_current = 1
                            _done = True

                if y_abs_position_given <= x_abs_position_given and not _done
                    if x of position_given is Negative
                        Left side
                            Must go Up to logically follow numbers
                            number_of_sides_before_side_current = 2
                            _done = True

                    else if x of position_given is Positive
                        Right side
                            Must go Down to logically follow numbers
                            number_of_sides_before_side_current = 0
                            _done = True

                length_before_side_current = get_length_of_ring_by_side_accumulative(
                    index_ring,
                    number_of_sides_before_side_current
                ) = (number_of_sides_before_side_current * (index_ring * 2)) if index_ring > 0 else 1
            
        Relationship 2
            Recall the pattern for finding what side of a ring you are on based on a Given position from (5c).
            Recall Ring Corners have the same absolute value components and recall Ring Corner signs from (4c)

                (+, -)  # Top Right Corner
                (+, +)  # Bottom Right Corner
                (-, +)  # Bottom Left Corner
                (-, -)  # Top Left Corner

            The difference between
                1. A Given position's component that does not decide what side a Given position
                is on (the component that does not have the greater absolute value), we'll call this the varying
                component. 
                2. The Ring Corner's corresponding component, the same componenet position as the varying component,
                that is on the opposite end of the Given position's side's direction.
            gives us the distance between a Given position and the Ring Corner that is on the opposite end
            of the Given position's side's direction. Basically, it's the distance from the Ring Corner
            that has numbers that logically follow up to the Given position. Note that this distance is relative
            to the side where numbers logically follow in the positive direction. 
            For example, if a Given position was at the top left corner of a ring, the side would be the 
            Top side because numbers logically follow going in the Right direction.  
            
            To make the algorithm slightly better, we'll incorporate the above logic into the algorithm from
            Relationship 1

                number_of_sides_before_side_current = 0

                x_abs_position_given = abs(x of position_given)
                y_abs_position_given = abs(y of position_given)

                component_varying_position_given = 0
                component_corresponding_position_corner = 0
                
                _done = False

                if x_abs_position_given <= y_abs_position_given and not _done

                    component_varying_position_given = position_given[0]

                    if y of position_given is Negative
                        Top side
                            Must go Right to logically follow numbers
                            number_of_sides_before_side_current = 3
                            component_corresponding_position_corner = -y_abs_position_given  # (-, -) Top Left Corner
                            _done = True

                    else if y of position_given is Positive
                        Bottom side
                            Must go Left to logically follow numbers
                            number_of_sides_before_side_current = 1
                            component_corresponding_position_corner = y_abs_position_given  # (+, +) Bottom Right Corner
                            _done = True
                            
                if y_abs_position_given <= x_abs_position_given and not _done

                    component_varying_position_given = position_given[1]

                    if x of position_given is Negative
                        Left side
                            Must go Up to logically follow numbers
                            number_of_sides_before_side_current = 2
                            component_corresponding_position_corner = x_abs_position_given  # (-, +) Bottom Left Corner
                            _done = True
                            
                    else if x of position_given is Positive
                        Right side
                            Must go Down to logically follow numbers
                            number_of_sides_before_side_current = 0
                            component_corresponding_position_corner = -x_abs_position_given  # (+, -) Top Right Corner
                            _done = True
                            
                length_before_side_current = get_length_of_ring_by_side_accumulative(
                    index_ring,
                    number_of_sides_before_side_current
                ) = (number_of_sides_before_side_current * (index_ring * 2)) if index_ring > 0 else 1

                difference_abs__component_varying_position_given__component_corresponding_position_corner = (
                    component_varying_position_given - component_corresponding_position_corner
                )
    
    (8) In order to make the complete algorithm, we need to merge the algorithm from Relationship 2 in (7)
    with the equation from (6b).
    Notes:
        
        1. The equation from (6b) 
            
                ((2 * index_ring) + 1)^2
            
            gives us the total sum of size of the rings up to index_ring. By inputting (index_ring - 1) as
            index_ring and making index_ring > 0 will give us the total sum of the size of the rings up to
            but not including the index_ring, we'll call this result sum_of_ring_sizes_before_index_ring
          
        2. The algorithm from Relationship 2 in (7) gives us            
            a. length_before_side_current
                This is the length of the Ring based on the index_ring in terms of the the sides that have
                been traversed or have been passed. This does not take in account the current side that the 
                Given position is on.
                
            b. difference_abs__component_varying_position_given__component_corresponding_position_corner
                This is the distance between the Ring Corner that is on the opposite end of the
                Given position's side's direction and the Given position.
        
        By adding the variables below
            sum_of_ring_sizes_before_index_ring +
            length_before_side_current +
            difference_abs__component_varying_position_given__component_corresponding_position_corner
        We get the exact number for ANY Given position.
        
        Recall that a Given position is relative to the Center position and the Center position is relative to the
        grid. So if you want the place the value of the Given position in the correct place on the grid, you need to
        convert the Given position to be relative to the grid.
    
"""


def get_length_of_ring_by_side_accumulative(index_ring: int, number_of_sides_before_side_current: int = 4) -> int:
    """
    Based on the last portion of the algorithm from Relationship 2 from (7)

        length_before_side_current = get_length_of_ring_by_side_accumulative(
            index_ring,
            number_of_sides_before_side_current
        ) = (number_of_sides_before_side_current * (index_ring * 2)) if index_ring > 0 else 1

    The last portion of the algorithm from Relationship 2 is based on the equation from (3b)

        length_of_ring = get_length_of_ring_by_side_accumulative(index_ring, index_side) = (
            (index_side * (index_ring * 2)) if index_ring > 0 else 1
        )

    """

    if index_ring > 0:
        return number_of_sides_before_side_current * (index_ring * 2)

    return 1


def get_sum_of_ring_sizes_up_to_index_ring(index_ring: int) -> int:
    """
    Based on the closed-form solution from (6b)

        1 + Summation from i=1 to index_ring of (4 * (index_ring * 2)) = ((2 * index_ring) + 1)^2

    """
    return ((2 * index_ring) + 1) ** 2


def put_spiral_number_on_grid(grid: Grid,
                              position_center_absolute: Position,
                              position_given_absolute: Position) -> None:
    """
    Put the correct spiral number on grid based on absolute position of where the center of the spiral is
    the absolute position of where you want ot put the number.

    :param grid:
    :param position_center_absolute:
    :param position_given_absolute:
    :return:
    """

    """
    ####################################################################################################
    The below makes the necessary variables for the algorithm to work
    ####################################################################################################
    """

    position_given = (
        position_given_absolute[0] - position_center_absolute[0],
        position_given_absolute[1] - position_center_absolute[1],
    )

    index_ring = max(abs(position_given[0]), abs(position_given[1]))

    """
    ####################################################################################################
    The below gets the total sum of the size of the rings up to but not including the index_ring
    ####################################################################################################
    """

    sum_of_ring_sizes_before_index_ring = 0

    if index_ring > 0:
        sum_of_ring_sizes_before_index_ring = get_sum_of_ring_sizes_up_to_index_ring(index_ring - 1)

    """
    ####################################################################################################
    The below gets 
        1.The length of the Ring based on the index_ring in terms of the the sides that have 
        been traversed or have been passed.
        
        2. The distance between the Ring Corner that is on the opposite end of the 
        Given position's side's direction and the Given position.
    ####################################################################################################
    """

    number_of_sides_before_side_current = 0

    x_abs_position_given = abs(position_given[0])
    y_abs_position_given = abs(position_given[1])

    component_varying_position_given = 0
    component_corresponding_position_corner = 0

    _done = False

    if x_abs_position_given <= y_abs_position_given and not _done:
        component_varying_position_given = position_given[0]

        if position_given[1] < 0:  # Top side
            number_of_sides_before_side_current = 3
            component_corresponding_position_corner = -y_abs_position_given
            _done = True

        elif position_given[1] > 0:  # Bottom side
            number_of_sides_before_side_current = 1
            component_corresponding_position_corner = y_abs_position_given
            _done = True

    if y_abs_position_given <= x_abs_position_given and not _done:
        component_varying_position_given = position_given[1]

        if position_given[0] < 0:  # Left side
            number_of_sides_before_side_current = 2
            component_corresponding_position_corner = x_abs_position_given
            _done = True

        elif position_given[0] > 0:  # Right side
            number_of_sides_before_side_current = 0
            component_corresponding_position_corner = -x_abs_position_given
            _done = True

    length_before_side_current = get_length_of_ring_by_side_accumulative(
        index_ring,
        number_of_sides_before_side_current
    )

    difference_abs__component_varying_position_given__component_corresponding_position_corner = abs(
        component_varying_position_given - component_corresponding_position_corner
    )

    """
    ####################################################################################################
    The below does the sum of the size + length + distance and places that result on the grid 
    ####################################################################################################
    """

    sum_final = (
            sum_of_ring_sizes_before_index_ring +
            length_before_side_current +
            difference_abs__component_varying_position_given__component_corresponding_position_corner
    )

    grid[position_given_absolute[1]][position_given_absolute[0]] = sum_final

    # DEBUGGING
    # print("#" * 50)
    # print(f'{position_given=}')
    # print(f'{x_abs_position_given=}')
    # print(f'{y_abs_position_given=}')
    # print(f'{sum_of_ring_sizes_before_index_ring=}')
    # print(f'{length_before_side_current=}')
    # print(f'    {number_of_sides_before_side_current=}')
    # print(f'{difference_abs__component_varying_position_given__component_corresponding_position_corner=}')
    # print(f'    {component_varying_position_given=}')
    # print(f'    {component_corresponding_position_corner=}')
    # print(f'{sum_final=}')
    # print_grid(grid)
    # print()


def math_solution_add_numbers_to_grid_independent_of_grid(grid: Grid, position_start: Position) -> None:
    for index_row, row in enumerate(grid):
        for index_column, element in enumerate(row):
            position_given_absolute = (index_column, index_row)
            put_spiral_number_on_grid(grid, position_start, position_given_absolute)

    # DEBUGGING
    # fill_in_grid_position(grid, position_start, (5, 5))
    # fill_in_grid_position(grid, position_start, (6, 5))
    # fill_in_grid_position(grid, position_start, (6, 6))
    # fill_in_grid_position(grid, position_start, (5, 6))
    # fill_in_grid_position(grid, position_start, (4, 6))
    # fill_in_grid_position(grid, position_start, (4, 5))
    # fill_in_grid_position(grid, position_start, (4, 4))
    # fill_in_grid_position(grid, position_start, (5, 4))
    # fill_in_grid_position(grid, position_start, (6, 4))


def main() -> None:
    x = 10
    y = 20
    grid = get_grid(x, y)

    position_start: Tuple[int, int] = (5, 5)

    math_solution_add_numbers_to_grid_independent_of_grid(grid, position_start)

    print_grid(grid)


if __name__ == '__main__':
    main()
