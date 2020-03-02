from pprint import pprint
import ucla_cellphone_telemetry_pb2

phone_record = ucla_cellphone_telemetry_pb2.CellPhoneTelemetry()

phone_record.event_time = "2020-01-17_12-14-35-843"
phone_record.magnetic_field.x = -14.157902
phone_record.magnetic_field.y = -18.413792
phone_record.magnetic_field.z = 21.960579

pprint(phone_record)

encoded_data = phone_record.SerializeToString()

pprint({'encoded_data': encoded_data})

decoded_data = ucla_cellphone_telemetry_pb2.CellPhoneTelemetry()
decoded_data.ParseFromString(encoded_data)

pprint({'decoded_data': decoded_data})

print('Has event_time    : ' + str(decoded_data.event_time != ''))
print('Has timestamp     : ' + str(decoded_data.timestamp != 0.0))
print('Has magnetic_field: ' + str(decoded_data.HasField('magnetic_field')))
print('Has gyroscope     : ' + str(decoded_data.HasField('gyroscope')))
