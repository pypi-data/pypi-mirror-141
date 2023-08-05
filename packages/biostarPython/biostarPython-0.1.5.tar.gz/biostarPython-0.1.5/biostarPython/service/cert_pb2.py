# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cert.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cert.proto',
  package='cert',
  syntax='proto3',
  serialized_options=_b('\n\027com.supremainc.sdk.certP\001Z\024biostar/service/cert'),
  serialized_pb=_b('\n\ncert.proto\x12\x04\x63\x65rt\"~\n\x07PKIName\x12\x0f\n\x07\x63ountry\x18\x01 \x01(\t\x12\x10\n\x08province\x18\x02 \x01(\t\x12\x0c\n\x04\x63ity\x18\x03 \x01(\t\x12\x14\n\x0corganization\x18\x04 \x01(\t\x12\x18\n\x10organizationUnit\x18\x05 \x01(\t\x12\x12\n\ncommonName\x18\x06 \x01(\t\"\x80\x01\n\x1e\x43reateServerCertificateRequest\x12\x1e\n\x07subject\x18\x01 \x01(\x0b\x32\r.cert.PKIName\x12\x13\n\x0b\x64omainNames\x18\x02 \x03(\t\x12\x0f\n\x07IPAddrs\x18\x03 \x03(\t\x12\x18\n\x10\x65xpireAfterYears\x18\x04 \x01(\x05\"H\n\x1f\x43reateServerCertificateResponse\x12\x12\n\nserverCert\x18\x01 \x01(\t\x12\x11\n\tserverKey\x18\x02 \x01(\t\"D\n\x1bSetServerCertificateRequest\x12\x12\n\nserverCert\x18\x01 \x01(\t\x12\x11\n\tserverKey\x18\x02 \x01(\t\"\x1e\n\x1cSetServerCertificateResponse\"G\n\x1cSetGatewayCertificateRequest\x12\x13\n\x0bgatewayCert\x18\x01 \x01(\t\x12\x12\n\ngatewayKey\x18\x02 \x01(\t\"\x1f\n\x1dSetGatewayCertificateResponse2\xaf\x02\n\x04\x43\x65rt\x12\x66\n\x17\x43reateServerCertificate\x12$.cert.CreateServerCertificateRequest\x1a%.cert.CreateServerCertificateResponse\x12]\n\x14SetServerCertificate\x12!.cert.SetServerCertificateRequest\x1a\".cert.SetServerCertificateResponse\x12`\n\x15SetGatewayCertificate\x12\".cert.SetGatewayCertificateRequest\x1a#.cert.SetGatewayCertificateResponseB1\n\x17\x63om.supremainc.sdk.certP\x01Z\x14\x62iostar/service/certb\x06proto3')
)




_PKINAME = _descriptor.Descriptor(
  name='PKIName',
  full_name='cert.PKIName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='country', full_name='cert.PKIName.country', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='province', full_name='cert.PKIName.province', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='city', full_name='cert.PKIName.city', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='organization', full_name='cert.PKIName.organization', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='organizationUnit', full_name='cert.PKIName.organizationUnit', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='commonName', full_name='cert.PKIName.commonName', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=146,
)


_CREATESERVERCERTIFICATEREQUEST = _descriptor.Descriptor(
  name='CreateServerCertificateRequest',
  full_name='cert.CreateServerCertificateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subject', full_name='cert.CreateServerCertificateRequest.subject', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='domainNames', full_name='cert.CreateServerCertificateRequest.domainNames', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='IPAddrs', full_name='cert.CreateServerCertificateRequest.IPAddrs', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expireAfterYears', full_name='cert.CreateServerCertificateRequest.expireAfterYears', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=277,
)


_CREATESERVERCERTIFICATERESPONSE = _descriptor.Descriptor(
  name='CreateServerCertificateResponse',
  full_name='cert.CreateServerCertificateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serverCert', full_name='cert.CreateServerCertificateResponse.serverCert', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serverKey', full_name='cert.CreateServerCertificateResponse.serverKey', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=351,
)


_SETSERVERCERTIFICATEREQUEST = _descriptor.Descriptor(
  name='SetServerCertificateRequest',
  full_name='cert.SetServerCertificateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serverCert', full_name='cert.SetServerCertificateRequest.serverCert', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serverKey', full_name='cert.SetServerCertificateRequest.serverKey', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=353,
  serialized_end=421,
)


_SETSERVERCERTIFICATERESPONSE = _descriptor.Descriptor(
  name='SetServerCertificateResponse',
  full_name='cert.SetServerCertificateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=423,
  serialized_end=453,
)


_SETGATEWAYCERTIFICATEREQUEST = _descriptor.Descriptor(
  name='SetGatewayCertificateRequest',
  full_name='cert.SetGatewayCertificateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gatewayCert', full_name='cert.SetGatewayCertificateRequest.gatewayCert', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gatewayKey', full_name='cert.SetGatewayCertificateRequest.gatewayKey', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=526,
)


_SETGATEWAYCERTIFICATERESPONSE = _descriptor.Descriptor(
  name='SetGatewayCertificateResponse',
  full_name='cert.SetGatewayCertificateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=528,
  serialized_end=559,
)

_CREATESERVERCERTIFICATEREQUEST.fields_by_name['subject'].message_type = _PKINAME
DESCRIPTOR.message_types_by_name['PKIName'] = _PKINAME
DESCRIPTOR.message_types_by_name['CreateServerCertificateRequest'] = _CREATESERVERCERTIFICATEREQUEST
DESCRIPTOR.message_types_by_name['CreateServerCertificateResponse'] = _CREATESERVERCERTIFICATERESPONSE
DESCRIPTOR.message_types_by_name['SetServerCertificateRequest'] = _SETSERVERCERTIFICATEREQUEST
DESCRIPTOR.message_types_by_name['SetServerCertificateResponse'] = _SETSERVERCERTIFICATERESPONSE
DESCRIPTOR.message_types_by_name['SetGatewayCertificateRequest'] = _SETGATEWAYCERTIFICATEREQUEST
DESCRIPTOR.message_types_by_name['SetGatewayCertificateResponse'] = _SETGATEWAYCERTIFICATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PKIName = _reflection.GeneratedProtocolMessageType('PKIName', (_message.Message,), dict(
  DESCRIPTOR = _PKINAME,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.PKIName)
  ))
_sym_db.RegisterMessage(PKIName)

CreateServerCertificateRequest = _reflection.GeneratedProtocolMessageType('CreateServerCertificateRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATESERVERCERTIFICATEREQUEST,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.CreateServerCertificateRequest)
  ))
_sym_db.RegisterMessage(CreateServerCertificateRequest)

CreateServerCertificateResponse = _reflection.GeneratedProtocolMessageType('CreateServerCertificateResponse', (_message.Message,), dict(
  DESCRIPTOR = _CREATESERVERCERTIFICATERESPONSE,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.CreateServerCertificateResponse)
  ))
_sym_db.RegisterMessage(CreateServerCertificateResponse)

SetServerCertificateRequest = _reflection.GeneratedProtocolMessageType('SetServerCertificateRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETSERVERCERTIFICATEREQUEST,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.SetServerCertificateRequest)
  ))
_sym_db.RegisterMessage(SetServerCertificateRequest)

SetServerCertificateResponse = _reflection.GeneratedProtocolMessageType('SetServerCertificateResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETSERVERCERTIFICATERESPONSE,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.SetServerCertificateResponse)
  ))
_sym_db.RegisterMessage(SetServerCertificateResponse)

SetGatewayCertificateRequest = _reflection.GeneratedProtocolMessageType('SetGatewayCertificateRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETGATEWAYCERTIFICATEREQUEST,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.SetGatewayCertificateRequest)
  ))
_sym_db.RegisterMessage(SetGatewayCertificateRequest)

SetGatewayCertificateResponse = _reflection.GeneratedProtocolMessageType('SetGatewayCertificateResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETGATEWAYCERTIFICATERESPONSE,
  __module__ = 'cert_pb2'
  # @@protoc_insertion_point(class_scope:cert.SetGatewayCertificateResponse)
  ))
_sym_db.RegisterMessage(SetGatewayCertificateResponse)


DESCRIPTOR._options = None

_CERT = _descriptor.ServiceDescriptor(
  name='Cert',
  full_name='cert.Cert',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=562,
  serialized_end=865,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateServerCertificate',
    full_name='cert.Cert.CreateServerCertificate',
    index=0,
    containing_service=None,
    input_type=_CREATESERVERCERTIFICATEREQUEST,
    output_type=_CREATESERVERCERTIFICATERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetServerCertificate',
    full_name='cert.Cert.SetServerCertificate',
    index=1,
    containing_service=None,
    input_type=_SETSERVERCERTIFICATEREQUEST,
    output_type=_SETSERVERCERTIFICATERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetGatewayCertificate',
    full_name='cert.Cert.SetGatewayCertificate',
    index=2,
    containing_service=None,
    input_type=_SETGATEWAYCERTIFICATEREQUEST,
    output_type=_SETGATEWAYCERTIFICATERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CERT)

DESCRIPTOR.services_by_name['Cert'] = _CERT

# @@protoc_insertion_point(module_scope)
