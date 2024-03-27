#include <actionlib/client/simple_action_client.h>
#include "learn_action/DoDishesAction.h"

typedef actionlib::SimpleActionClient<learn_action::DoDishesAction> Client;

// When the action is completed, the callback function will be called once
void doneCb(const actionlib::SimpleClientGoalState& state,
        const learn_action::DoDishesResultConstPtr& result)
{
    ROS_INFO("Yay! The dishes are now clean");
    ros::shutdown();
}

// When the action is activated, the callback function will be called once.
void activeCb()
{
    ROS_INFO("Goal just went active");
}

// Callback function called after receiving feedback
void feedbackCb(const learn_action::DoDishesFeedbackConstPtr& feedback)
{
    ROS_INFO(" percent_complete : %f ", feedback->percent_complete);
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "do_dishes_client");

    // Define a client
    Client client("do_dishes", true);

    // Waiting for server side
    ROS_INFO("Waiting for action server to start.");
    client.waitForServer();
    ROS_INFO("Action server started, sending goal.");

    // Create an action goal
    learn_action::DoDishesGoal goal;
    goal.dishwasher_id = 1;

    // Send the action goal to the server and set the callback function
    client.sendGoal(goal,  &doneCb, &activeCb, &feedbackCb);

    ros::spin();

    return 0;
}