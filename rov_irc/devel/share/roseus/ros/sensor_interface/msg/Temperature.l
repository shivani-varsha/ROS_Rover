;; Auto-generated. Do not edit!


(when (boundp 'sensor_interface::Temperature)
  (if (not (find-package "SENSOR_INTERFACE"))
    (make-package "SENSOR_INTERFACE"))
  (shadow 'Temperature (find-package "SENSOR_INTERFACE")))
(unless (find-package "SENSOR_INTERFACE::TEMPERATURE")
  (make-package "SENSOR_INTERFACE::TEMPERATURE"))

(in-package "ROS")
;;//! \htmlinclude Temperature.msg.html


(defclass sensor_interface::Temperature
  :super ros::object
  :slots (_temperature ))

(defmethod sensor_interface::Temperature
  (:init
   (&key
    ((:temperature __temperature) 0.0)
    )
   (send-super :init)
   (setq _temperature (float __temperature))
   self)
  (:temperature
   (&optional __temperature)
   (if __temperature (setq _temperature __temperature)) _temperature)
  (:serialization-length
   ()
   (+
    ;; float32 _temperature
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _temperature
       (sys::poke _temperature (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _temperature
     (setq _temperature (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get sensor_interface::Temperature :md5sum-) "694ab1a51fd38693b5cadd94c1ae252d")
(setf (get sensor_interface::Temperature :datatype-) "sensor_interface/Temperature")
(setf (get sensor_interface::Temperature :definition-)
      "float32 temperature


")



(provide :sensor_interface/Temperature "694ab1a51fd38693b5cadd94c1ae252d")


