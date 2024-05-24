#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <std_msgs/String.h>
#include <opencv2/opencv.hpp>
#include <zbar.h>
#include <book_find/FindBookAction.h>
#include <string>

class BookServer
{
protected:
    ros::NodeHandle nh_;
    actionlib::SimpleActionServer<book_find::FindBookAction> as_;
    std::string action_name_;
    book_find::FindBookFeedback feedback_;
    book_find::FindBookResult result_;
    cv::VideoCapture cap_;
    ros::Publisher order_pub_;

public:
    BookServer(const std::string &name) :
        as_(nh_, name, boost::bind(&BookServer::executeCB, this, _1), false),
        action_name_(name)
    {
        cap_.open(0);
        if (!cap_.isOpened()) {
            ROS_ERROR("Failed to open video device");
            return;
        }
        order_pub_ = nh_.advertise<std_msgs::String>("order", 10);
        as_.start();
    }

    ~BookServer() {
        cap_.release();
    }

    void executeCB(const book_find::FindBookGoalConstPtr &goal) {
        ROS_INFO("Book name is %s, book storage is %s", goal->book_name.c_str(), goal->book_storage.c_str());
        nh_.setParam("/service_server/book_storage", goal->book_storage);

        bool detect_book = false;
        int distance_count = 0;

        while (ros::ok()) {
            cv::Mat frame;
            cap_ >> frame;
            if (frame.empty()) break;

            cv::resize(frame, frame, cv::Size(600, frame.rows * 600 / frame.cols));
            std::vector<zbar::Symbol> barcodes = decode(frame);

            for (auto &barcode : barcodes) {
                if (barcode.get_data() == goal->book_name) {
                    detect_book = true;
                    int x = barcode.get_location_x(0);
                    int y = barcode.get_location_y(0);
                    int w = barcode.get_location_x(2) - x;
                    int h = barcode.get_location_y(2) - y;

                    int frame_width = frame.cols;
                    int frame_height = frame.rows;
                    int section_width = frame_width / 6;

                    for (int i = 1; i < 6; ++i) {
                        int line_x = i * section_width;
                        cv::line(frame, cv::Point(line_x, 0), cv::Point(line_x, frame_height), cv::Scalar(0, 255, 0), 2);
                    }

                    int barcode_center_x = x + w / 2;
                    int third_line_x = 3 * section_width;
                    int distance_to_third_line = barcode_center_x - third_line_x;

                    if (distance_to_third_line <= -71 && distance_to_third_line >= -79) {
                        feedback_.distance = distance_to_third_line;
                        as_.publishFeedback(feedback_);
                        distance_count += 1;

                        if (distance_count > 15) {
                            ROS_INFO("HERE1");
                            ros::Duration(3.0).sleep();
                            publishOrder();
                            result_.arrived = true;
                            as_.setSucceeded(result_);
                            return;
                        }
                    } else {
                        distance_count = 0;
                        feedback_.distance = distance_to_third_line;
                        as_.publishFeedback(feedback_);
                    }
                }
            }

            if (as_.isPreemptRequested() || !ros::ok()) {
                as_.setPreempted();
                return;
            }

            if (cv::waitKey(1) == 'q') {
                break;
            }
        }
    }

    void publishOrder() {
        std_msgs::String order_msg;
        nh_.getParam("/service_server/book_storage", order_msg.data);
        order_pub_.publish(order_msg);
    }

    std::vector<zbar::Symbol> decode(cv::Mat &frame) {
        zbar::ImageScanner scanner;
        scanner.set_config(zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1);

        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);

        zbar::Image image(frame.cols, frame.rows, "Y800", gray.data, frame.cols * frame.rows);
        scanner.scan(image);

        std::vector<zbar::Symbol> symbols;
        for (auto symbol = image.symbol_begin(); symbol != image.symbol_end(); ++symbol) {
            symbols.push_back(*symbol);
        }

        return symbols;
    }
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "find_book_action_server");
    BookServer server("book_action");
    ros::spin();
    return 0;
}