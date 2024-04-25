import logging
from tuya_helpers import TuyaOpenAPI, TUYA_LOGGER
import dlt
from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD, DEVICE_ID
import streamlit as st

if 'schema' not in st.session_state:
    st.session_state['schema'] = 'value'

TUYA_LOGGER.setLevel(logging.DEBUG)

# Init
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "86", 'tuyaSmart')

@dlt.resource(name='status')
def get_status():
    yield openapi.get(f'/v1.0/devices/{DEVICE_ID}')

@dlt.resource(name='specs')
def get_specs():
    yield openapi.get(f'/v1.0/devices/{DEVICE_ID}/specifications')

@dlt.resource(name='properties')
def get_properties():
    yield openapi.get(f'/v2.0/cloud/thing/{DEVICE_ID}/shadow/properties')


pipeline = dlt.pipeline(
    pipeline_name="smart_plug",
    destination="duckdb",
    dataset_name="smart_plug_data",
)


pipeline.run(get_status())
pipeline.run(get_specs())
pipeline.run(get_properties())


info = pipeline.run(get_status())
print(info)
info = pipeline.run(get_specs())
print(info)
info = pipeline.run(get_properties())
print(info)


#dashboard.write_data_explorer_page(pipeline)
'''
# Receive device message
def on_message(msg):
    print("on_message: %s" % msg)

print(openapi)
openapi.token_info.expire_time = 0

openmq = TuyaOpenMQ(openapi)
openmq.start()
openmq.add_message_listener(on_message)
'''

