import sys
from time import sleep
import requests
import json
import datetime
import copy
import urllib

ServiceUrl = ''
query_skeleton = {
  "database": {
    "id": ""
  },
  "mode": "once",
  "definition": {}
}

######### helper functions to retrieve results from orion ########
def get_databases_url():
  return ServiceUrl + "/databases"

def get_header():
  return {
    'Content-Type': 'application/json'
  }

def get_db_id_url(id):
  return get_databases_url() + "/" + str(id)

def get_db_write_url(id):
  return get_databases_url() + "/" + str(id) + "/write"

def get_query_url(id):
  return ServiceUrl + "/queries"

def do_query(query, db_id):
  query_data = copy.copy(query_skeleton)
  query_body = copy.copy(query)
  query_data['database']['id'] = db_id
  query_data['definition'] = query_body
  response = requests.post(get_query_url(db_id), headers=get_header(), json=query_data)
  if response.status_code != 200:
    print ('Error perform orion res-request- Get query data, status code: ' + str(response.status_code))
    return {}
  else:
    return response.json()

######### queries to orion for various results ########
# these queries are copied from standard view in web UI
query_bgp_session_live =   {
  "multi_result": {
    "filters": [],
    "groups": [],
    "orders": [],
    "projections": [
      "view.port_name as port_name",
      "view.emulated_device_name as emulated_device_name",
      "view.bgp_session_session_index as bgp_session_session_index",
      "view.state as state",
      "view.tx_advertised_route_count as tx_advertised_route_count",
      "view.rx_advertised_route_count as rx_advertised_route_count",
      "view.tx_withdrawn_route_count as tx_withdrawn_route_count",
      "view.rx_withdrawn_route_count as rx_withdrawn_route_count",
      "view.tx_notification_count as tx_notification_count",
      "view.rx_notification_count as rx_notification_count",
      "view.tx_advertised_update_count as tx_advertised_update_count",
      "view.rx_advertised_update_count as rx_advertised_update_count",
      "view.tx_withdrawn_update_count as tx_withdrawn_update_count",
      "view.tx_keepalive_count as tx_keepalive_count",
      "view.rx_keepalive_count as rx_keepalive_count",
      "view.tx_open_count as tx_open_count",
      "view.rx_open_count as rx_open_count",
      "view.tx_route_refresh_count as tx_route_refresh_count",
      "view.rx_route_refresh_count as rx_route_refresh_count",
      "view.outstanding_route_count as outstanding_route_count",
      "view.last_rx_update_route_count as last_rx_update_route_count",
      "view.tx_notify_code as tx_notify_code",
      "view.tx_notify_sub_code as tx_notify_sub_code",
      "view.rx_notify_code as rx_notify_code",
      "view.rx_notify_sub_code as rx_notify_sub_code",
      "view.tx_rt_constraint_count as tx_rt_constraint_count",
      "view.rx_rt_constraint_count as rx_rt_constraint_count",
      "view.session_up_count as session_up_count"
    ],
    "subqueries": [
      {
        "alias": "view",
        "filters": [
          "bgp_session_live_stats$last.is_deleted = false"
        ],
        "groups": [],
        "orders": [],
        "projections": [
          "port.name as port_name",
          "emulated_device.name as emulated_device_name",
          "bgp_session.session_index as bgp_session_session_index",
          "(bgp_session_live_stats$last.state) as state",
          "(bgp_session_live_stats$last.tx_advertised_route_count) as tx_advertised_route_count",
          "(bgp_session_live_stats$last.rx_advertised_route_count) as rx_advertised_route_count",
          "(bgp_session_live_stats$last.tx_withdrawn_route_count) as tx_withdrawn_route_count",
          "(bgp_session_live_stats$last.rx_withdrawn_route_count) as rx_withdrawn_route_count",
          "(bgp_session_live_stats$last.tx_notification_count) as tx_notification_count",
          "(bgp_session_live_stats$last.rx_notification_count) as rx_notification_count",
          "(bgp_session_live_stats$last.tx_advertised_update_count) as tx_advertised_update_count",
          "(bgp_session_live_stats$last.rx_advertised_update_count) as rx_advertised_update_count",
          "(bgp_session_live_stats$last.tx_withdrawn_update_count) as tx_withdrawn_update_count",
          "(bgp_session_live_stats$last.tx_keepalive_count) as tx_keepalive_count",
          "(bgp_session_live_stats$last.rx_keepalive_count) as rx_keepalive_count",
          "(bgp_session_live_stats$last.tx_open_count) as tx_open_count",
          "(bgp_session_live_stats$last.rx_open_count) as rx_open_count",
          "(bgp_session_live_stats$last.tx_route_refresh_count) as tx_route_refresh_count",
          "(bgp_session_live_stats$last.rx_route_refresh_count) as rx_route_refresh_count",
          "(bgp_session_live_stats$last.outstanding_route_count) as outstanding_route_count",
          "(bgp_session_live_stats$last.last_rx_update_route_count) as last_rx_update_route_count",
          "(bgp_session_live_stats$last.tx_notify_code) as tx_notify_code",
          "(bgp_session_live_stats$last.tx_notify_sub_code) as tx_notify_sub_code",
          "(bgp_session_live_stats$last.rx_notify_code) as rx_notify_code",
          "(bgp_session_live_stats$last.rx_notify_sub_code) as rx_notify_sub_code",
          "(bgp_session_live_stats$last.tx_rt_constraint_count) as tx_rt_constraint_count",
          "(bgp_session_live_stats$last.rx_rt_constraint_count) as rx_rt_constraint_count",
          "(bgp_session_live_stats$last.session_up_count) as session_up_count"
        ]
      }
    ]
  }
}

query_bgp_session_eot = {
  "multi_result": {
    "filters": [],
    "groups": [],
    "orders": [
      "view.test_snapshot_name_order ASC",
      "view.port_name_str_order ASC",
      "view.port_name_num_order ASC",
      "view.port_name_ip_order ASC",
      "view.port_name_hostname_order ASC",
      "view.port_name_slot_order ASC",
      "view.port_name_port_num_order ASC",
      "view.emulated_device_name_str_order ASC",
      "view.emulated_device_name_num_order ASC",
      "view.bgp_session_session_index ASC"
    ],
    "projections": [
      "view.test_snapshot_name as test_snapshot_name",
      "view.port_name as port_name",
      "view.emulated_device_name as emulated_device_name",
      "view.bgp_session_session_index as bgp_session_session_index",
      "view.state as state",
      "view.tx_advertised_route_count as tx_advertised_route_count",
      "view.rx_advertised_route_count as rx_advertised_route_count",
      "view.tx_withdrawn_route_count as tx_withdrawn_route_count",
      "view.rx_withdrawn_route_count as rx_withdrawn_route_count",
      "view.tx_notification_count as tx_notification_count",
      "view.rx_notification_count as rx_notification_count",
      "view.tx_advertised_update_count as tx_advertised_update_count",
      "view.rx_advertised_update_count as rx_advertised_update_count",
      "view.tx_withdrawn_update_count as tx_withdrawn_update_count",
      "view.tx_keepalive_count as tx_keepalive_count",
      "view.rx_keepalive_count as rx_keepalive_count",
      "view.tx_open_count as tx_open_count",
      "view.rx_open_count as rx_open_count",
      "view.tx_route_refresh_count as tx_route_refresh_count",
      "view.rx_route_refresh_count as rx_route_refresh_count",
      "view.outstanding_route_count as outstanding_route_count",
      "view.last_rx_update_route_count as last_rx_update_route_count",
      "view.tx_notify_code as tx_notify_code",
      "view.tx_notify_sub_code as tx_notify_sub_code",
      "view.rx_notify_code as rx_notify_code",
      "view.rx_notify_sub_code as rx_notify_sub_code",
      "view.tx_rt_constraint_count as tx_rt_constraint_count",
      "view.rx_rt_constraint_count as rx_rt_constraint_count",
      "view.session_up_count as session_up_count"
    ],
    "subqueries": [
      {
        "alias": "view",
        "filters": [],
        "groups": [],
        "orders": [],
        "projections": [
          "test.snapshot_name as test_snapshot_name",
          "port.name as port_name",
          "emulated_device.name as emulated_device_name",
          "bgp_session.session_index as bgp_session_session_index",
          "(bgp_session_stats.state) as state",
          "(bgp_session_stats.tx_advertised_route_count) as tx_advertised_route_count",
          "(bgp_session_stats.rx_advertised_route_count) as rx_advertised_route_count",
          "(bgp_session_stats.tx_withdrawn_route_count) as tx_withdrawn_route_count",
          "(bgp_session_stats.rx_withdrawn_route_count) as rx_withdrawn_route_count",
          "(bgp_session_stats.tx_notification_count) as tx_notification_count",
          "(bgp_session_stats.rx_notification_count) as rx_notification_count",
          "(bgp_session_stats.tx_advertised_update_count) as tx_advertised_update_count",
          "(bgp_session_stats.rx_advertised_update_count) as rx_advertised_update_count",
          "(bgp_session_stats.tx_withdrawn_update_count) as tx_withdrawn_update_count",
          "(bgp_session_stats.tx_keepalive_count) as tx_keepalive_count",
          "(bgp_session_stats.rx_keepalive_count) as rx_keepalive_count",
          "(bgp_session_stats.tx_open_count) as tx_open_count",
          "(bgp_session_stats.rx_open_count) as rx_open_count",
          "(bgp_session_stats.tx_route_refresh_count) as tx_route_refresh_count",
          "(bgp_session_stats.rx_route_refresh_count) as rx_route_refresh_count",
          "(bgp_session_stats.outstanding_route_count) as outstanding_route_count",
          "(bgp_session_stats.last_rx_update_route_count) as last_rx_update_route_count",
          "(bgp_session_stats.tx_notify_code) as tx_notify_code",
          "(bgp_session_stats.tx_notify_sub_code) as tx_notify_sub_code",
          "(bgp_session_stats.rx_notify_code) as rx_notify_code",
          "(bgp_session_stats.rx_notify_sub_code) as rx_notify_sub_code",
          "(bgp_session_stats.tx_rt_constraint_count) as tx_rt_constraint_count",
          "(bgp_session_stats.rx_rt_constraint_count) as rx_rt_constraint_count",
          "(bgp_session_stats.session_up_count) as session_up_count",
          "test.snapshot_name_order as test_snapshot_name_order",
          "port.name_str_order as port_name_str_order",
          "port.name_num_order as port_name_num_order",
          "port.name_ip_order as port_name_ip_order",
          "port.name_hostname_order as port_name_hostname_order",
          "port.name_slot_order as port_name_slot_order",
          "port.name_port_num_order as port_name_port_num_order",
          "emulated_device.name_str_order as emulated_device_name_str_order",
          "emulated_device.name_num_order as emulated_device_name_num_order"
        ]
      }
    ]
  }
}

######### Start demo here ########
from StcPython import StcPython
stc = StcPython()
print ('---- STC started')

print ('---- load config file...')
stc.perform("LoadFromXMLCommand", FileName="./bgp-b2b-sample.xml")

# NOTE: The config file used in this sample (bgp-b2b-sample.xml) already created necessary objects to enable Magellan.  However, Magellan may not be enabled under two scenarios:
# (1) the test is created from scratch
# (2) the test is loaded from files exported from old scripts (with commands like stc::perform SaveToTcc etc.)
# One way to verify if Magellan is disabled is to print out the database id. (see line 248)  If Magellan is disabled, no db id will be printed.
# To enable Magellan, add following two lines (replacing 'ResultSetName' when creating 'EnhancedResultsGroupFilter' with appropriate result set name):

# rs_profile = stc.create('spirent.results.EnhancedResultsSelectorProfile', under=system1))
# rs_filter = stc.create("spirent.results.EnhancedResultsGroupFilter", under=rs_profile, ResultSetName='bgp_session_stats')

# Note that the script above subscribes to all live facts (i.e., counters) supported in the result set. 'EnhancedResultsGroupFilter' has a property 'LiveFacts' which can be used to specify a subset of facts to be subscribed.

print ('---- relocate ports...')
## get all the ports
project = stc.get('system1', 'children-project')
ports = stc.get(project, 'children-port')
portLst = ports.split(' ')

port_addrs = ["//10.109.123.178/1/1", "//10.109.122.105/1/1"]

stc.config(portLst[0], location=port_addrs[0])
stc.config(portLst[1], location=port_addrs[1])

## bring all ports online
print ('---- connecting to ports and apply...')
stc.perform("AttachPortsCommand", portList=portLst, autoConnect='TRUE')
stc.apply()

## get url
print ('---- get URL')
resultConfig = stc.get('system1','children-TemevaResultsConfig')
ServiceUrl = stc.get(resultConfig,'ServiceUrl')

## get orion database id
test_info = stc.get(project, 'children-testinfo')
dbId = stc.get(test_info,'resultdbid')
print ('---- Retrieved db id: ' + dbId)

## start traffic for 10 second
print ('---- Start all devices now...')
## start all device
stc.perform("DevicesStartAllCommand")

print ('---- Start traffic now...')
generator1 = stc.get('port1', 'children-generator')
generatorList = [generator1]
stc.perform("GeneratorStartCommand", GeneratorList=generatorList)

keep_running = 5
print ('---- Keep traffic running for %d seconds...'%keep_running)
stc.sleep(keep_running)

## get live results
print ('---- Query for live bgp session result:')
res_live = do_query(query_bgp_session_live, dbId)

## res_live is a dict, get columns
col_name = res_live['result']['columns']
print ('---- column names:')
for n in col_name:
    print (n)

## get state
rows = res_live['result']['rows']
print ('---- total number of rows in result: %d'%(len(rows)))
for r in rows:
    print ("%s state: %s"%(r[0], r[3]))

## stop traffic
print ('---- Stop traffic')
stc.perform("GeneratorStopCommand", GeneratorList=generatorList)
stc.sleep(3)

## take a snapshot
print ('---- take a snapshot')
stc.perform("SaveEnhancedResultsSnapshotCommand")

## get snapshot result
print ('---- query for bgp session snapshot result:')
res_eot = do_query(query_bgp_session_eot, dbId)

## get tx route count of rows
rows = res_eot['result']['rows']
for r in rows:
    print ("tx advertised route count for %s: %s"%(r[1], r[5]))

## termination
print ('---- detach and clean up: ')
stc.perform("ChassisDisconnectAllCommand")
stc.perform("ResetConfigCommand")
print ('---- the end')