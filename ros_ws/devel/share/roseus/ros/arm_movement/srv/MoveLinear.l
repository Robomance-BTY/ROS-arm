;; Auto-generated. Do not edit!


(when (boundp 'arm_movement::MoveLinear)
  (if (not (find-package "ARM_MOVEMENT"))
    (make-package "ARM_MOVEMENT"))
  (shadow 'MoveLinear (find-package "ARM_MOVEMENT")))
(unless (find-package "ARM_MOVEMENT::MOVELINEAR")
  (make-package "ARM_MOVEMENT::MOVELINEAR"))
(unless (find-package "ARM_MOVEMENT::MOVELINEARREQUEST")
  (make-package "ARM_MOVEMENT::MOVELINEARREQUEST"))
(unless (find-package "ARM_MOVEMENT::MOVELINEARRESPONSE")
  (make-package "ARM_MOVEMENT::MOVELINEARRESPONSE"))

(in-package "ROS")





(defclass arm_movement::MoveLinearRequest
  :super ros::object
  :slots (_command ))

(defmethod arm_movement::MoveLinearRequest
  (:init
   (&key
    ((:command __command) "")
    )
   (send-super :init)
   (setq _command (string __command))
   self)
  (:command
   (&optional __command)
   (if __command (setq _command __command)) _command)
  (:serialization-length
   ()
   (+
    ;; string _command
    4 (length _command)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _command
       (write-long (length _command) s) (princ _command s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _command
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _command (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass arm_movement::MoveLinearResponse
  :super ros::object
  :slots (_success _message ))

(defmethod arm_movement::MoveLinearResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional __success)
   (if __success (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass arm_movement::MoveLinear
  :super ros::object
  :slots ())

(setf (get arm_movement::MoveLinear :md5sum-) "c348f8d8cd3a80f54328aa4159009109")
(setf (get arm_movement::MoveLinear :datatype-) "arm_movement/MoveLinear")
(setf (get arm_movement::MoveLinear :request) arm_movement::MoveLinearRequest)
(setf (get arm_movement::MoveLinear :response) arm_movement::MoveLinearResponse)

(defmethod arm_movement::MoveLinearRequest
  (:response () (instance arm_movement::MoveLinearResponse :init)))

(setf (get arm_movement::MoveLinearRequest :md5sum-) "c348f8d8cd3a80f54328aa4159009109")
(setf (get arm_movement::MoveLinearRequest :datatype-) "arm_movement/MoveLinearRequest")
(setf (get arm_movement::MoveLinearRequest :definition-)
      "string command
---
bool success
string message

")

(setf (get arm_movement::MoveLinearResponse :md5sum-) "c348f8d8cd3a80f54328aa4159009109")
(setf (get arm_movement::MoveLinearResponse :datatype-) "arm_movement/MoveLinearResponse")
(setf (get arm_movement::MoveLinearResponse :definition-)
      "string command
---
bool success
string message

")



(provide :arm_movement/MoveLinear "c348f8d8cd3a80f54328aa4159009109")


