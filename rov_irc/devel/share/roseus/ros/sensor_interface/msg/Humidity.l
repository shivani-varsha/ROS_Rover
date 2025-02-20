;; Auto-generated. Do not edit!


(when (boundp 'sensor_interface::Humidity)
  (if (not (find-package "SENSOR_INTERFACE"))
    (make-package "SENSOR_INTERFACE"))
  (shadow 'Humidity (find-package "SENSOR_INTERFACE")))
(unless (find-package "SENSOR_INTERFACE::HUMIDITY")
  (make-package "SENSOR_INTERFACE::HUMIDITY"))

(in-package "ROS")
;;//! \htmlinclude Humidity.msg.html


(defclass sensor_interface::Humidity
  :super ros::object
  :slots (_relative_humidity ))

(defmethod sensor_interface::Humidity
  (:init
   (&key
    ((:relative_humidity __relative_humidity) 0.0)
    )
   (send-super :init)
   (setq _relative_humidity (float __relative_humidity))
   self)
  (:relative_humidity
   (&optional __relative_humidity)
   (if __relative_humidity (setq _relative_humidity __relative_humidity)) _relative_humidity)
  (:serialization-length
   ()
   (+
    ;; float32 _relative_humidity
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _relative_humidity
       (sys::poke _relative_humidity (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _relative_humidity
     (setq _relative_humidity (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get sensor_interface::Humidity :md5sum-) "798d3911e6b40189d397e11e08a9ad8c")
(setf (get sensor_interface::Humidity :datatype-) "sensor_interface/Humidity")
(setf (get sensor_interface::Humidity :definition-)
      "float32 relative_humidity


")



(provide :sensor_interface/Humidity "798d3911e6b40189d397e11e08a9ad8c")


