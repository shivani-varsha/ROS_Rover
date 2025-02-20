// Auto-generated. Do not edit!

// (in-package sensor_interface.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Humidity {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.relative_humidity = null;
    }
    else {
      if (initObj.hasOwnProperty('relative_humidity')) {
        this.relative_humidity = initObj.relative_humidity
      }
      else {
        this.relative_humidity = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Humidity
    // Serialize message field [relative_humidity]
    bufferOffset = _serializer.float32(obj.relative_humidity, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Humidity
    let len;
    let data = new Humidity(null);
    // Deserialize message field [relative_humidity]
    data.relative_humidity = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'sensor_interface/Humidity';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '798d3911e6b40189d397e11e08a9ad8c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 relative_humidity
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Humidity(null);
    if (msg.relative_humidity !== undefined) {
      resolved.relative_humidity = msg.relative_humidity;
    }
    else {
      resolved.relative_humidity = 0.0
    }

    return resolved;
    }
};

module.exports = Humidity;
