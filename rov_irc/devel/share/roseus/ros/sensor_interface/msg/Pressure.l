;; Auto-generated. Do not edit!


(when (boundp 'sensor_interface::Pressure)
  (if (not (find-package "SENSOR_INTERFACE"))
    (make-package "SENSOR_INTERFACE"))
  (shadow 'Pressure (find-package "SENSOR_INTERFACE")))
(unless (find-package "SENSOR_INTERFACE::PRESSURE")
  (make-package "SENSOR_INTERFACE::PRESSURE"))

(in-package "ROS")
;;//! \htmlinclude Pressure.msg.html


(defclass sensor_interface::Pressure
  :super ros::object
  :slots (_pressure ))

(defmethod sensor_interface::Pressure
  (:init
   (&key
    ((:pressure __pressure) 0.0)
    )
   (send-super :init)
   (setq _pressure (float __pressure))
   self)
  (:pressure
   (&optional __pressure)
   (if __pressure (setq _pressure __pressure)) _pressure)
  (:serialization-length
   ()
   (+
    ;; float32 _pressure
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _pressure
       (sys::poke _pressure (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _pressure
     (setq _pressure (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get sensor_interface::Pressure :md5sum-) "d08eeab8c09d2ba14f8144e3bbf40d21")
(setf (get sensor_interface::Pressure :datatype-) "sensor_interface/Pressure")
(setf (get sensor_interface::Pressure :definition-)
      "float32 pressure


")



(provide :sensor_interface/Pressure "d08eeab8c09d2ba14f8144e3bbf40d21")


