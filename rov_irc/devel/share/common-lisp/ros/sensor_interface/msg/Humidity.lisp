; Auto-generated. Do not edit!


(cl:in-package sensor_interface-msg)


;//! \htmlinclude Humidity.msg.html

(cl:defclass <Humidity> (roslisp-msg-protocol:ros-message)
  ((relative_humidity
    :reader relative_humidity
    :initarg :relative_humidity
    :type cl:float
    :initform 0.0))
)

(cl:defclass Humidity (<Humidity>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Humidity>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Humidity)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor_interface-msg:<Humidity> is deprecated: use sensor_interface-msg:Humidity instead.")))

(cl:ensure-generic-function 'relative_humidity-val :lambda-list '(m))
(cl:defmethod relative_humidity-val ((m <Humidity>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_interface-msg:relative_humidity-val is deprecated.  Use sensor_interface-msg:relative_humidity instead.")
  (relative_humidity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Humidity>) ostream)
  "Serializes a message object of type '<Humidity>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'relative_humidity))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Humidity>) istream)
  "Deserializes a message object of type '<Humidity>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'relative_humidity) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Humidity>)))
  "Returns string type for a message object of type '<Humidity>"
  "sensor_interface/Humidity")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Humidity)))
  "Returns string type for a message object of type 'Humidity"
  "sensor_interface/Humidity")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Humidity>)))
  "Returns md5sum for a message object of type '<Humidity>"
  "798d3911e6b40189d397e11e08a9ad8c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Humidity)))
  "Returns md5sum for a message object of type 'Humidity"
  "798d3911e6b40189d397e11e08a9ad8c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Humidity>)))
  "Returns full string definition for message of type '<Humidity>"
  (cl:format cl:nil "float32 relative_humidity~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Humidity)))
  "Returns full string definition for message of type 'Humidity"
  (cl:format cl:nil "float32 relative_humidity~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Humidity>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Humidity>))
  "Converts a ROS message object to a list"
  (cl:list 'Humidity
    (cl:cons ':relative_humidity (relative_humidity msg))
))
