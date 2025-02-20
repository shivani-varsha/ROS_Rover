
(cl:in-package :asdf)

(defsystem "sensor_interface-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Humidity" :depends-on ("_package_Humidity"))
    (:file "_package_Humidity" :depends-on ("_package"))
    (:file "Pressure" :depends-on ("_package_Pressure"))
    (:file "_package_Pressure" :depends-on ("_package"))
    (:file "Temperature" :depends-on ("_package_Temperature"))
    (:file "_package_Temperature" :depends-on ("_package"))
  ))