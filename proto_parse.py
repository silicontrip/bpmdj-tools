#!/usr/bin/python
import sys
import struct

# Helper functions ------------------------------------------------------------
# this comes largely straight out of the google protocol-buffers code for DecodeVarint(internal\decoder.py)
# with a few tweaks to make it work for me
def readVarInt(buffer, pos):
  mask = (1 << 64) - 1
  result = 0
  shift = 0
  startPos = pos
  while 1:
    b = ord(buffer[pos])
    result |= ((b & 0x7f) << shift)
    pos += 1
    if not (b & 0x80):
      if result > 0x7fffffffffffffff:
        result -= (1 << 64)
        result |= ~mask
      else:
        result &= mask
      return (result, pos, pos-startPos)
    shift += 7
    if shift >= 64:
      raise Error('Too many bytes when decoding varint.')

def readQWORD(d, pos):
    try:
        v = struct.unpack("<Q", d[pos:pos+8])[0]
    except:
        print "Exception in readQWORD"
        print sys.exc_info()
        return (None, pos)
    pos += 8
    return (v, pos);

def readDWORD(d, pos):
    try:
        v = struct.unpack("<L", d[pos:pos+4])[0]
    except:
        print "Exception in readDWORD"
        print sys.exc_info()
        return (None, pos)
    pos += 4
    return (v, pos);

def readBYTE(d, pos):
    try:
        v = struct.unpack("<B", d[pos:pos+1])[0]
    except:
        print "Exception in readBYTE"
        print sys.exc_info()
        return (None, pos)
    pos += 1
    return (v, pos);

# returns (value, new position, data type, field ID, and value's length)
def readField(d, pos):
    # read field and type info
    (v, p) = readBYTE(d, pos);
    datatype = v & 7;
    fieldnum = v >> 3;

    if datatype == 0:       # varint
        (v, p, l) = readVarInt(d, p)
        return (v, p, datatype, fieldnum, l)    
    elif datatype == 1: # 64-bit
        (v,p) = readQWORD(d, p)
        return (v, p, datatype, fieldnum, 8)    
    elif datatype == 2: # varlen string/blob
        (v, p, l) = readVarInt(d, p)    # get string length
        return (d[p:p+v], p+v, datatype, fieldnum, v)       
    elif datatype == 5: # 32-bit value
        (v,p) = readDWORD(d, p)
        return (v, p, datatype, fieldnum, 4)
    else:
        print "Unknown type: %d [%x]\n" % (datatype, pos)
        return (None, p, datatype, fieldnum, 1);

# PARSERS ---------------------------------------------------------------------

#  Parse DescriptorProto field
def PrintDescriptorProto(data, size, prefix):
    pos = 0

    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p

        if fid == 1: print "%smessage %s {" % (prefix,d)
        elif fid == 2: PrintFieldDescriptorProto(d, l, prefix+"\t") # FieldDescriptorProto
        elif fid == 3: PrintDescriptorProto(d, l, prefix+"\t") # DescriptorProto
        elif fid == 4: PrintEnumDescriptorProto(d, l, prefix+"\t") # EnumDescriptorProto
        elif fid == 5: 
            print "%sextension_range:" % (prefix)
            PrintDescriptorProto(d, l, prefix+"\t") # ExtensionRange
        elif fid == 6: print "%sextension: %s" % (prefix,d) # FieldDescriptorProto
        elif fid == 7: print "%soptions: %s" % (prefix,d) # MessageOptions
        else: print "***UNKNOWN fid in PrintDescriptorProto %d" % fid

    print "%s}" % prefix

# Parse EnumDescriptorProto
def PrintEnumDescriptorProto(data, size, prefix):
    pos = 0
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p

        if fid == 1: print "%senum %s {" % (prefix,d)
        elif fid == 2: PrintEnumValueDescriptorProto(d, l, prefix+"\t") # EnumValueDescriptorProto
        elif fid == 3: # EnumOptions
            print "%soptions" % prefix
        else: print "***UNKNOWN fid in PrintDescriptorProto %d" % fid
    print "%s};" % prefix


# Parse EnumValueDescriptorProto
def PrintEnumValueDescriptorProto(data, size, prefix):
    pos = 0
    enum = {"name": None, "number": None}
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p
        if fid == 1: enum['name'] = d
        elif fid == 2: enum['number'] = d
        elif fid == 3: # EnumValueOptions
            print "%soptions: %s" % (prefix,d)
        else: print "***UNKNOWN fid in PrintDescriptorProto %d" % fid

    print "%s%s = %s;" % (prefix, enum['name'], enum['number'])

# Parse FieldDescriptorProto
def PrintFieldDescriptorProto(data, size, prefix):
    pos = 0
    field = {"name": None, "extendee": None, "number": None, "label": None, "type": None, "type_name": None, "default_value": None, "options": None}
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p

        if fid == 1: field['name'] = d
        elif fid == 2: field['extendee'] = d
        elif fid == 3: field['number'] = d
        elif fid == 4: 
            if d == 1: field['label'] = "optional"
            elif d == 2: field['label'] = "required"
            elif d == 3: field['label'] = "repeated"
            else: print "{{Label: UNKNOWN (%d)}}" % (prefix,d)

        elif fid == 5: 
            types = {1: "double", 
                             2: "float", 
                             3: "int64", 
                             4: "uint64", 
                             5: "int32", 
                             6: "fixed64",
                             7: "fixed32",
                             8: "bool",
                             9: "string",
                             10: "group", 
                             11: "message",
                             12: "bytes",
                             13: "uint32",
                             14: "enum",
                             15: "sfixed32",
                             16: "sfixed64",
                             17: "sint32",
                             18: "sint64" }
            if d not in types:
                print "%sType: UNKNOWN(%d)" % (prefix,d)
            else:
                field['type'] = types[d]


        elif fid == 6: field["type_name"] = d
        elif fid == 7: field["default_value"] = d
        elif fid == 8: field["options"] = d
        else: print "***UNKNOWN fid in PrintFieldDescriptorProto %d" % fid

    output = prefix

    if field['label'] is not None: output += " %s" % field['label']
    output += " %s" % field['type']
    output += " %s" % field['name']
    output += " = %d" % field['number']
    if field['default_value']: output += " [DEFAULT = %s]" % field['default_value']
    output += ";"
    print output


#  Parse ExtensionRange field
def PrintExtensionRange(data, size, prefix):
    pos = 0
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p
        print "%stype %d, field %d, length %d" % (prefix, t, fid, l)

        if fid == 1: print "%sstart: %d" % (prefix,d)
        elif fid == 2: print "%send: %d" % (prefix,d)
        else: print "***UNKNOWN fid in PrintExtensionRange %d" % fid


def PrintFileOptions(data, size, prefix):
    pos = 0
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p

        if fid == 1: print "%soption java_package = \"%s\";" % (prefix,d)
        elif fid == 8: print "%soption java_outer_classname = \"%s\"" % (prefix,d)
        elif fid == 10: print "%soption java_multiple_files = %d" % (prefix,d)
        elif fid == 20: print "%soption java_generate_equals_and_hash = %d" % (prefix,d)
        elif fid == 9: print "%soption optimize_for = %d" % (prefix,d)
        elif fid == 16: print "%soption cc_generic_services = %d" % (prefix,d)
        elif fid == 17: print "%soption java_generic_services = %d" % (prefix,d)
        elif fid == 18: print "%soption py_generic_services = %d" % (prefix,d)
        elif fid == 999: print "%soption uninterpreted_option = \"%s\"" % (prefix,d)        # UninterpretedOption
        else: print "***UNKNOWN fid in PrintFileOptions %d" % fid

# -----------------------------------------------------------------------------
# Main function. 
def ParseProto(filename, offset, size):
    f = open(filename, "rb").read()

    data = f[offset:offset+size]

    pos = 0
    while pos < size:
        (d, p, t, fid, l)  = readField(data, pos);
        pos = p
        #print "type %d, field %d, length %d" % (t, fid, l)

        if fid == 1: print "// source filename: %s" % d
        elif fid == 2: print "package %s;" % d
        elif fid == 3: print "import \"%s\"" % d
        elif fid == 4: PrintDescriptorProto(d, l, "")
        elif fid == 5: print "EnumDescriptorProto: %s" % d
        elif fid == 6: print "ServiceDescriptorProto: %s" % d
        elif fid == 7: print "FieldDescriptorProto: %s" % d
        elif fid == 8: PrintFileOptions(d, l, "")
        else: print "***UNKNOWN fid in ParseProto %d" % fid
    return {}



# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: %s binaryfile offset size" % sys.argv[0]
        sys.exit(0)

    ParseProto(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
