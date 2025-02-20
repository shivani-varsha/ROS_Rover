; Auto-generated. Do not edit!


(cl:in-package sensor_interface-msg)


;//! \htmlinclude Temperature.msg.html

(cl:defclass <Temperature> (roslisp-msg-protocol:ros-message)
  ((temperature
    :reader temperature
    :initarg :temperature
    :type cl:float
    :initform 0.0))
)

(cl:defclass Temperature (<Temperature>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Temperature>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Temperature)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor_interface-msg:<Temperature> is deprecated: use sensor_interface-msg:Temperature instead.")))

(cl:ensure-generic-function 'temperature-val :lambda-list '(m))
(cl:defmethod temperature-val ((m <Temperature>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_interface-msg:temperature-val is deprecated.  Use sensor_interface-msg:temperature instead.")
  (temperature m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Temperature>) ostream)
  "Serializes a message object of type '<Temperature>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'temperature))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Temperature>) istream)
  "Deserializes a message object of type '<Temperature>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'temperature) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Temperature>)))
  "Returns string type for a message object of type '<Temperature>"
  "sensor_interface/Temperature")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Temperature)))
  "Returns string type for a message object of type 'Temperature"
  "sensor_interface/Temperature")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Temperature>)))
  "Returns md5sum for a message object of type '<Temperature>"
  "694ab1a51fd38693b5cadd94c1ae252d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Temperature)))
  "Returns md5sum for a message object of type 'Temperature"
  "694ab1a51fd38693b5cadd94c1ae252d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Temperature>)))
  "Returns full string definition for message of type '<Temperature>"
  (cl:format cl:nil "float32 temperature~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Temperature)))
  "Returns full string definition for message of type 'Temperature"
  (cl:format cl:nil "float32 temperature~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Temperature>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Temperature>))
  "Converts a ROS message object to a list"
  (cl:list 'Temperature
    (cl:cons ':temperature (temperature msg))
))
