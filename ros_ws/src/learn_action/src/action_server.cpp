#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include "learn_action/DoDishesAction.h"

typedef actionlib::SimpleActionServer<learn_action::DoDishesAction> Server;

// Callback function called after receiving the action's goal
void execute(const learn_action::DoDishesGoalConstPtr& goal, Server* as)
{
    ros::Rate r(1);
    learn_action::DoDishesFeedback feedback;

    ROS_INFO("Dishwasher %d is working.", goal->dishwasher_id);

    // Assume the progress of washing dishes, and publish progress feedback at a frequency of 1hz
    for(int i=1; i<=10; i++)
    {
        feedback.percent_complete = i * 10;
        as->publishFeedback(feedback);
        r.sleep();
    }

    // When the action is completed, the result is returned to the client.
    ROS_INFO("Dishwasher %d finish working.", goal->dishwasher_id);
    as->setSucceeded();
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "do_dishes_server");
    ros::NodeHandle n;

    // Define a server
    Server server(n, "do_dishes", boost::bind(&execute, _1, &server), false);
    
    // Server started running
    server.start();

    ros::spin();

    return 0;
}