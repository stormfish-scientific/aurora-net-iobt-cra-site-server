from pprint import pprint
import ucla_cellphone_telemetry_pb2

phone_record = ucla_cellphone_telemetry_pb2.CellPhoneTelemetry()

phone_record.event_time = "2020-01-17_12-14-35-843"
phone_record.magnetic_field.x = -14.157902
phone_record.magnetic_field.y = -18.413792
phone_record.magnetic_field.z = 21.960579

pprint(phone_record)

