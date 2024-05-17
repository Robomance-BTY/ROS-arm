
(cl:in-package :asdf)

(defsystem "book_find-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "FindBookAction" :depends-on ("_package_FindBookAction"))
    (:file "_package_FindBookAction" :depends-on ("_package"))
    (:file "FindBookActionFeedback" :depends-on ("_package_FindBookActionFeedback"))
    (:file "_package_FindBookActionFeedback" :depends-on ("_package"))
    (:file "FindBookActionGoal" :depends-on ("_package_FindBookActionGoal"))
    (:file "_package_FindBookActionGoal" :depends-on ("_package"))
    (:file "FindBookActionResult" :depends-on ("_package_FindBookActionResult"))
    (:file "_package_FindBookActionResult" :depends-on ("_package"))
    (:file "FindBookFeedback" :depends-on ("_package_FindBookFeedback"))
    (:file "_package_FindBookFeedback" :depends-on ("_package"))
    (:file "FindBookGoal" :depends-on ("_package_FindBookGoal"))
    (:file "_package_FindBookGoal" :depends-on ("_package"))
    (:file "FindBookResult" :depends-on ("_package_FindBookResult"))
    (:file "_package_FindBookResult" :depends-on ("_package"))
  ))