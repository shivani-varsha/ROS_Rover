; Auto-generated. Do not edit!


(cl:in-package sensor_interface-msg)


;//! \htmlinclude Pressure.msg.html

(cl:defclass <Pressure> (roslisp-msg-protocol:ros-message)
  ((pressure
    :reader pressure
    :initarg :pressure
    :type cl:float
    :initform 0.0))
)

(cl:defclass Pressure (<Pressure>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Pressure>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Pressure)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor_interface-msg:<Pressure> is deprecated: use sensor_interface-msg:Pressure instead.")))

(cl:ensure-generic-function 'pressure-val :lambda-list '(m))
(cl:defmethod pressure-val ((m <Pressure>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_interface-msg:pressure-val is deprecated.  Use sensor_interface-msg:pressure instead.")
  (pressure m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Pressure>) ostream)
  "Serializes a message object of type '<Pressure>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'pressure))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Pressure>) istream)
  "Deserializes a message object of type '<Pressure>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'pressure) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Pressure>)))
  "Returns string type for a message object of type '<Pressure>"
  "sensor_interface/Pressure")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Pressure)))
  "Returns string type for a message object of type 'Pressure"
  "sensor_interface/Pressure")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Pressure>)))
  "Returns md5sum for a message object of type '<Pressure>"
  "d08eeab8c09d2ba14f8144e3bbf40d21")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Pressure)))
  "Returns md5sum for a message object of type 'Pressure"
  "d08eeab8c09d2ba14f8144e3bbf40d21")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Pressure>)))
  "Returns full string definition for message of type '<Pressure>"
  (cl:format cl:nil "float32 pressure~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Pressure)))
  "Returns full string definition for message of type 'Pressure"
  (cl:format cl:nil "float32 pressure~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Pressure>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Pressure>))
  "Converts a ROS message object to a list"
  (cl:list 'Pressure
    (cl:cons ':pressure (pressure msg))
))
