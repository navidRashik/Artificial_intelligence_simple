# Problem Set 11: Simulating robots
# Version 3: Sumulation (With the option to run the visualizer)
# Name: Mohammad Ehsanul Karim
# Collaborators: None
# Start: July 1, 2016; 11:20pm

from Robot import *
from Position import *
from ps6_visualize import *
from RectangularRoom import *
from datetime import time
import matplotlib.pyplot as plt


# Implement the following code based on the pdf, and code documentation.
# I am just showing you some sample coding tricks so to get you started.
Target_Cleaning_Percentage = 100


def _status_string(time, RectangularRoom):
    "Returns an appropriate status string to print."
    num_clean_tiles = RectangularRoom.getNumCleanedTiles()
    percent_clean = 100 * num_clean_tiles / (RectangularRoom.width * RectangularRoom.height)
    #return "Time: %04d; %d tiles (%d%%) cleaned" % \
    return (time, num_clean_tiles, percent_clean)


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                 robot_type, visualize = False, AllStepListFlag_On = False):
   """
   Runs NUM_TRIALS trials of the simulation and returns the mean number of
   time-steps needed to clean the fraction MIN_COVERAGE of the room.
 
   The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
   speed SPEED, in a room of dimensions WIDTH x HEIGHT.
 
   num_robots: an int (num_robots > 0)
   speed: a float (speed > 0)
   width: an int (width > 0)
   height: an int (height > 0)
   min_coverage: a float (0 <= min_coverage <= 1.0)
   num_trials: an int (num_trials > 0)
   robot_type: class of robot to be instantiated (e.g. Robot or
               RandomWalkRobot)
   """
   global Target_Cleaning_Percentage
   totalTimeStepsInNumTrials = 0
   allStepsList = []
   allStepsAvg_list = []
   for num_trail in xrange(num_trials):
       robotRoom = RectangularRoom(width, height)
       robotCollection = [robot_type(robotRoom, speed) for ind in range(num_robots)]
       timeCounter_EachTrail = 0
       # Initialize visualizer.
       if(visualize):
           anim = RobotVisualization(num_robots, width, height, min_coverage)
           anim.update(robotRoom, robotCollection)
           
       while True:
           timeCounter_EachTrail += 1
           totalTimeStepsInNumTrials += 1 
           
           for robot in robotCollection:
               robot.updatePositionAndClean()
               
           if(visualize):
               anim.update(robotRoom, robotCollection)
               
           timeMoved , numbberOfCleanTiles, percentClean = _status_string(timeCounter_EachTrail, robotRoom)
           if(percentClean==Target_Cleaning_Percentage) :
               if(visualize):
                   anim.done()
               break
       if AllStepListFlag_On and (num_trail+1)%10==0 :
           num_trail_original = num_trail+1
           allStepsList.append(num_trail_original)
           res = totalTimeStepsInNumTrials/num_trail_original
           allStepsAvg_list.append(res)
           
#        
   if AllStepListFlag_On:
       return allStepsList, allStepsAvg_list
   return totalTimeStepsInNumTrials/(num_trials+1)

def changeTargetPercentage(TargetPercentage):
    global Target_Cleaning_Percentage
    Target_Cleaning_Percentage = TargetPercentage
    
def No4_Ans1(Target_percentage,width,height):
    changeTargetPercentage(Target_percentage)
    plot_x = []
    plot_y = []
    for i in range(10):
        plot_x.append(i+1)
        plot_y.append(runSimulation(i+1, 1, width, height, 0.005, 40, StandardRobot, False))
    plt.plot(plot_x, plot_y)
    plt.xlabel(' number of robots ')
    plt.ylabel('time')
    plt.show()
        
def No4_Ans2(Target_percentage,No_of_robot):
    changeTargetPercentage(Target_percentage)
    plot_x = []
    plot_y_std = []
    plot_y_rnd = []
    width = [20, 25, 40, 50, 80, 100]
    height = [20, 16, 10, 8, 5, 4]
    for i in range(len(width)):
        roomArea = 1.0*width[i]/height[i]
        plot_x.append(roomArea)
        plot_y_std.append(runSimulation(No_of_robot, 1, width[i], height[i], 0.25, 100, StandardRobot, False))
        plot_y_rnd.append(runSimulation(No_of_robot, 1, width[i], height[i], 0.25, 100, RandomWalkRobot, False))
    plt.subplot()
    plt.plot(plot_x, plot_y_std , label="Standard")
    plt.plot(plot_x, plot_y_rnd, label="random")
    plt.legend()
    plt.xlabel(' Room area ')
    plt.ylabel('Time / steps')   
    plt.show() 
     
def showPlot3(Target_percentage,No_of_trail):
    changeTargetPercentage(Target_percentage)
    plot_x_std, plot_y_std = runSimulation(1, 1, 10, 10, 0.25, No_of_trail, StandardRobot, False,True)
    plot_x_rand, plot_y_rand = runSimulation(1, 1, 10, 10, 0.25, No_of_trail, RandomWalkRobot, False,True) 
    plt.subplot()
    plt.plot(plot_x_std, plot_y_std, label= "standard")
    plt.plot(plot_x_rand,plot_y_rand, label= "random")
    plt.legend()
    plt.xlabel(' no of trail ')
    plt.ylabel('Time / steps')
    plt.show() 
    
def assignments(Target_percentage,No_of_trail):
    changeTargetPercentage(Target_percentage)
    plot_x_std, plot_y_std = runSimulation(1, 1, 10, 10, 0.25, No_of_trail, StandardRobot, False,True)
    plot_x_rand, plot_y_rand = runSimulation(1, 1, 10, 10, 0.25, No_of_trail, RandomWalkRobot, False,True) 
    
    end_y_std = plot_y_std[-1]
    PercentOf_end_y_std = int(round(end_y_std *.005))
    StartIndex_y_std = 0
    found = False
    for i in range(len(plot_y_std)):
        item = plot_y_std[i]
        if item in range(end_y_std-PercentOf_end_y_std, end_y_std+PercentOf_end_y_std) and not found:
            StartIndex_y_std = i
            found = True
        elif item not in range(end_y_std-PercentOf_end_y_std, end_y_std+PercentOf_end_y_std) and found:
            found = False
            StartIndex_y_std = 0
         
    print "For standard robot after the point ", plot_x_std[StartIndex_y_std], "on x axis line is straight "

    end_y_rand = plot_y_rand[-1]
    PercentOf_end_y_rand = int(round(end_y_rand *.005))
    StartIndex_y_rand = 0
    found = False
    for i in range(len(plot_y_rand)):
        item = plot_y_rand[i]
        if item in range(end_y_rand-PercentOf_end_y_rand, end_y_rand+PercentOf_end_y_rand) and not found:
            StartIndex_y_rand = i
            found = True
        elif item not in range(end_y_rand-PercentOf_end_y_rand, end_y_rand+PercentOf_end_y_rand) and found:
            found = False
            StartIndex_y_rand = 0
        
    print "For random robot after the point ", plot_x_rand[StartIndex_y_rand], "on x axis line is straight "
    
    
    plt.subplot()
    plt.plot(plot_x_std, plot_y_std, label= "standard")
    plt.plot(plot_x_rand,plot_y_rand, label= "random")
    plt.legend()
    plt.xlabel(' no of trail ')
    plt.ylabel('Time / steps')
    plt.show() 

 
print runSimulation(1, 1, 10, 10, 0.25, 1000, StandardRobot, False)
No4_Ans1(80, 20, 20) 
No4_Ans2(80,2)
showPlot3(100,1000)
assignments (100, 1000)






# End: July 12, 2016; 11:20pm
