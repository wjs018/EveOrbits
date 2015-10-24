#===============================================================================
# 
# Basic simulation of the orbits of ships in Eve Online.
#
# contact: wjs018@gmail.com
# 
#===============================================================================

import math
import numpy as np


def calcForce(maxForce, velocity, agility):
    """
    Calculates the current force on a ship given the maximum
    force possible by a ship, the current velocity, and the
    inertia of the ship.

    Input:

        maxForce    Maximum force capable of being generated
                    by the ship. Given by maxSpeed/inertia

        velocity    Current velocity of the ship. This is
                    important due to the drag force imposed
                    on ships in EVE.

        agility     Agility multiplier of the ship. Calculated
                    using the libdogma engine

    Returns:

        force       Current force acting upon the ship. A 
                    combination of the force generated by the
                    engines and the drag force due to velocity.
    """

    force = maxForce - velocity / agility

    return force


def createRotMatrix(theta):
    """
    Creates a rotation matrix for the x-y plane that rotates
    a vector by the angle theta in radians.
    """

    # Rab is the a'th row and b'th column of the matrix

    R11 = math.cos(theta)
    R12 = - math.sin(theta)
    R21 = math.sin(theta)
    R22 = math.cos(theta)

    rotMat = np.array([(R11, R12), (R21, R22)])

    return rotMat


def simulateOrbit(maxSpeed, mass, agility, radius, throttle=1.0):
    """
    Simulates the orbit of a ship in EVE at a given radius.

    Input:

        maxSpeed    The maximum speed of the ship in m/s. This
                    should take into account any modules or implants
                    that are in use.
                    
        mass        Mass of the ship in millions of kgs. Like
                    maxSpeed, this should take into account modules.
                    
        agility     The agility multiplier of the ship.

        radius      The desired radius to set the orbit (m). This
                    is not necessarily the radius at which the
                    ship will orbit, just the radius at which
                    it will try to orbit.
                    
        throttle    By default this is 1.0 (maximum throttle). This
                     is the fraction possible force you want the 
                    ship to apply. This is linearly related to the
                    maximum speed of the ship.

    Returns:

        simRadius   The radius at which the ship ended up
                    reaching a stable orbit in m.

        velocity    The speed of the ship at which the orbit was
                    stable. Given in m/s.

        angular     The angular velocity of the ship traveling
                    in the stable orbit.
    """
    
    inertia = 1 / agility

    # Calculate the maximum force our ship can generate

    maxForce = maxSpeed * inertia * throttle
    
    # Get the new maxSpeed of the ship, taking throttle into account
    
    maxSpeed = maxForce * agility

    # Set an initial position for the ship at 2*radius

    x = radius + maxSpeed * 10
    y = 0
    position = np.array([[x], [y]])

    # Now we need to find the initial heading for our ship.

    distToOrbit = math.sqrt(x**2 - radius**2)
    angleToOrbit = math.atan(radius / distToOrbit)

    rotMat = createRotMatrix(-angleToOrbit)

    heading = rotMat.dot(-position) / \
        np.sqrt(np.transpose(position).dot(position))

    # We are now ready for the simulation, but first we need to
    # initialize some constants

    # timestep for simulations

    dt = 0.1

    # Percent change in orbit radius that is tolerated to be
    # considered a stable orbit

    radTol = 0.001

    # The amount of time steps between checking radTol

    interval = 200

    # List of radii that will be checked for stability

    stableCheckList = []

    # Counter that will be used to check for stability over time

    stableCheckCount = 0

    # Value counter needs to reach for stability condition

    stableCheckThresh = 20
    
    # Minimum time steps to elapse before checking for stability
    
    stableCheckStart = (2 * radius) / (maxSpeed * dt)

    #=========================================================================
    # Table containing the data ouput from the simulation. It has the following
    # format:
    #
    # | i | t | r | x | y | v | vx | vy | a | ax | ay | f | fx | fy |
    #
    # i is the current iteration number
    # t is the current time (i * dt)
    # r is distance from origin
    # x is x position
    # y is y position
    # v is velocity magnitude
    # vx is x-component of velocity
    # vy is y-component of velocity
    # a is acceleration magnitude (f / mass)
    # ax is x-component of acceleration (fx / mass)
    # ay is y-component of acceleration (fy / mass)
    # f is the magnitude of force
    # fx is the x-component of force
    # fy is the y-component of force
    #
    # For now, just create the first row and populate it
    #=========================================================================

    data = np.zeros((1, 14))
    data[0, 2] = np.sqrt(np.transpose(position).dot(position))
    data[0, 3] = x
    data[0, 4] = y

    # Counter to keep track of iterations

    i = 0
    proceed = 0

    # Run the simulation as long as the ship doesn't achieve a stable orbit for
    # three checks in a row

    while stableCheckCount < stableCheckThresh:

        # For all but the first iteration, we need to calculate the
        # heading we want to move the ship in. For our purposes, heading
        # will be a unit vector.

        if proceed == 1:

            # First thing to do each time step is iterate the counter and time

            data[i, 0] = i
            data[i, 1] = i * dt
            i += 1

            # First, find how far we are from our desired orbit radius
            # and use that to decide how to calculate our heading

            dist = np.sqrt(data[i, 3]**2 + data[i, 4]**2)
            position = np.array([[data[i, 3]], [data[i, 4]]])

            if radius < dist:

                # We are outside our desired radius of orbit

                distToOrbit = math.sqrt(dist**2 - radius**2)
                angleToOrbit = math.atan(radius / distToOrbit)

                rotMat = createRotMatrix(-angleToOrbit)

                heading = rotMat.dot(-position) / dist

            elif radius == dist:
                 
                # We are close to our desired orbit, so set a heading tangent to the
                # orbit path
                 
                neg3Position = np.array([[-data[i,3]], [-data[i,4]], [0]])
                 
                # Cross this vector with the z-axis to get our vector tangent to
                # the orbit
                 
                tangent = np.cross(neg3Position, np.array([[0],[0],[1]]), axis=0)
                 
                heading = tangent / np.sqrt(np.transpose(tangent).dot(tangent))

            elif dist < radius:

                # We are too close to our desired radius of orbit, set
                # heading directly away from origin

                heading = np.array([[data[i, 3]], [data[i, 4]]]) / dist

        # Now that we have calculated our heading, we can calculate the force for this
        # time step. Note, the force for the i'th time step is calculated using the
        # i'th values of velocity, while the velocity and position are calculated
        # for the i + 1 time step

        data[i, 12] = calcForce(maxForce * heading[0, 0], data[i, 6], agility)
        data[i, 13] = calcForce(maxForce * heading[1, 0], data[i, 7], agility)
        data[i, 11] = math.sqrt(data[i, 12]**2 + data[i, 13]**2)

        # Now acceleration is just Force / mass

        data[i, 8] = data[i, 11] / mass
        data[i, 9] = data[i, 12] / mass
        data[i, 10] = data[i, 13] / mass

        # Next, we need to calculate the velocity and position for the i+1 time step
        # based on the acceleration and velocity for the i'th time step

        nextRow = np.zeros((1, 14))
        data = np.vstack((data, nextRow))

        # Velocity

        data[i + 1, 6] = data[i, 6] + dt * data[i, 9]
        data[i + 1, 7] = data[i, 7] + dt * data[i, 10]
        data[i + 1, 5] = math.sqrt(data[i + 1, 6]**2 + data[i + 1, 7]**2)

        # Position

        data[i + 1, 3] = data[i, 3] + dt * data[i, 6]
        data[i + 1, 4] = data[i, 4] + dt * data[i, 7]
        data[i + 1, 2] = math.sqrt(data[i + 1, 3]**2 + data[i + 1, 4]**2)

        # The last thing we need to do is implement the stability check. We are
        # looking to maintain an orbit that is fluctuating less than
        # radTol * radius every interval time steps for stableCheckThresh times
        # in a row.
        
        if i > stableCheckStart:

            if i != 0 and i % interval == 0:
    
                # Add the current orbit radius to the list
    
                stableCheckList.append(data[i, 2])
    
                if len(stableCheckList) < stableCheckThresh:
    
                    # If the list isn't long enough, continue to next time step
    
                    continue
    
                elif len(stableCheckList) > stableCheckThresh:
    
                    # Remove the oldest element of this list
    
                    del stableCheckList[0]
    
                # Now we check that the stability condition is satisfied for each
                # item in stableCheckList
    
                delta = radTol * radius
                avg = sum(stableCheckList) / float(len(stableCheckList))
    
                for j in range(0, len(stableCheckList)):
    
                    if avg - delta < stableCheckList[j] < avg + delta:
    
                        # We are within tolerance for this entry
    
                        stableCheckCount += 1
    
                    else:
    
                        # We are not within tolerance. Reset the counter and break
    
                        stableCheckCount = 0
    
                        break

        if i == 0:

            proceed = 1

    # We have satisfied the while loop if we have gotten to this
    # point of the function

    data = np.delete(data, data.shape[0] - 1, axis=0)
    simRadius = np.mean(data[data.shape[0] - 100:, 2])
    velocity = np.mean(data[data.shape[0] - 100:, 5])

    angular = velocity / simRadius
    
    return(simRadius, velocity, angular)

if __name__ == '__main__':
    
    # call the Function with parameters for AB Harpy
    
    rad, vel, ang = simulateOrbit(835.0, 1.655, 2.452, 1500, throttle=1.0)
    
    print 'rad = ' + str(rad)
    print 'vel = ' + str(vel)
    print 'ang = ' + str(ang)
