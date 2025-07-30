package require SpirentTestCenter
package require http
package require rest
package require json

puts "---- STC started"

set portList [ list "//10.28.236.65/1/1" "//10.28.236.51/1/1" ]

# load config
puts "---- load config file..."
stc::perform LoadFromXML -FileName "bgp-b2b-sample.xml"

# NOTE: The config file used in this sample (bgp-b2b-sample.xml) already created necessary objects to enable Magellan.  However, Magellan may not be enabled under two scenarios:
# (1) the test is created from scratch
# (2) the test is loaded from files exported from old scripts (with commands like stc::perform SaveToTcc etc.)
# One way to verify if Magellan is disabled is to print out the database id. (see line 248)  If Magellan is disabled, no db id will be printed.
# To enable Magellan, add following two lines (replacing 'ResultSetName' when creating 'EnhancedResultsGroupFilter' with appropriate result set name):

# set spirent_results_EnhancedResultsSelectorProfile [stc::create "spirent.results.EnhancedResultsSelectorProfile" -under system1]
# set spirent_results_EnhancedResultsGroupFilter [stc::create "spirent.results.EnhancedResultsGroupFilter" \
        -under $spirent_results_EnhancedResultsSelectorProfile \
        -ResultSetName {bgp_session_stats} ]

# Note that the script above subscribes to all live facts (i.e., counters) supported in the result set. 'EnhancedResultsGroupFilter' has a property 'LiveFacts' which can be used to specify a subset of facts to be subscribed.

# update ports
puts "---- relocate ports..."
array set cmdResult [ stc::perform GetObjects -ClassName Port -Condition IsVirtual=false]
set ports $cmdResult(-ObjectList)
set idx 0
foreach port $ports {
    stc::config $port -location [ lindex $portList $idx ]
    incr idx
}

# connect and apply
puts "---- connecting to ports and apply..."
stc::perform AttachPorts -autoConnect true -portList [ stc::get project1 -children-Port ]
stc::apply

# get test database id
set testInfo [ stc::get project1 -children-testinfo ]
set db_id [stc::get $testInfo -resultdbid]
puts "---- retrieved db id: $db_id"

# start traffic 
puts "---- start traffic..."
stc::perform DevicesStartAll
set genList [list [stc::get port1 -children-generator]]
stc::perform generatorstart -generatorList $genList

set keep_running 5
puts "---- traffic is running... wait for $keep_running seconds"
stc::sleep $keep_running

# build query
set query_string_whole { {"database": {"id": "db_id_here"}, "mode":"once", "definition": query_def } }
# template string to be replaced with real db id and query body
set db_temp "db_id_here"
set query_temp "query_def"

# this is a sample live result query copied from bgp view, and removed unnecessary spaces
set query_live { { "multi_result": { "filters": [], "groups": [], "orders": [], "projections": [ "view.port_name as port_name", "view.emulated_device_name as emulated_device_name", "view.bgp_session_session_index as bgp_session_session_index", "view.state as state", "view.tx_advertised_route_count as tx_advertised_route_count", "view.rx_advertised_route_count as rx_advertised_route_count", "view.tx_withdrawn_route_count as tx_withdrawn_route_count", "view.rx_withdrawn_route_count as rx_withdrawn_route_count", "view.tx_notification_count as tx_notification_count", "view.rx_notification_count as rx_notification_count", "view.tx_advertised_update_count as tx_advertised_update_count", "view.rx_advertised_update_count as rx_advertised_update_count", "view.tx_withdrawn_update_count as tx_withdrawn_update_count", "view.tx_keepalive_count as tx_keepalive_count", "view.rx_keepalive_count as rx_keepalive_count", "view.tx_open_count as tx_open_count", "view.rx_open_count as rx_open_count", "view.tx_route_refresh_count as tx_route_refresh_count", "view.rx_route_refresh_count as rx_route_refresh_count", "view.outstanding_route_count as outstanding_route_count", "view.last_rx_update_route_count as last_rx_update_route_count", "view.tx_notify_code as tx_notify_code", "view.tx_notify_sub_code as tx_notify_sub_code", "view.rx_notify_code as rx_notify_code", "view.rx_notify_sub_code as rx_notify_sub_code", "view.tx_rt_constraint_count as tx_rt_constraint_count", "view.rx_rt_constraint_count as rx_rt_constraint_count", "view.session_up_count as session_up_count" ], "subqueries": [ { "alias": "view", "filters": [ "bgp_session_live_stats$last.is_deleted = false" ], "groups": [], "orders": [], "projections": [ "port.name as port_name", "emulated_device.name as emulated_device_name", "bgp_session.session_index as bgp_session_session_index", "(bgp_session_live_stats$last.state) as state", "(bgp_session_live_stats$last.tx_advertised_route_count) as tx_advertised_route_count", "(bgp_session_live_stats$last.rx_advertised_route_count) as rx_advertised_route_count", "(bgp_session_live_stats$last.tx_withdrawn_route_count) as tx_withdrawn_route_count", "(bgp_session_live_stats$last.rx_withdrawn_route_count) as rx_withdrawn_route_count", "(bgp_session_live_stats$last.tx_notification_count) as tx_notification_count", "(bgp_session_live_stats$last.rx_notification_count) as rx_notification_count", "(bgp_session_live_stats$last.tx_advertised_update_count) as tx_advertised_update_count", "(bgp_session_live_stats$last.rx_advertised_update_count) as rx_advertised_update_count", "(bgp_session_live_stats$last.tx_withdrawn_update_count) as tx_withdrawn_update_count", "(bgp_session_live_stats$last.tx_keepalive_count) as tx_keepalive_count", "(bgp_session_live_stats$last.rx_keepalive_count) as rx_keepalive_count", "(bgp_session_live_stats$last.tx_open_count) as tx_open_count", "(bgp_session_live_stats$last.rx_open_count) as rx_open_count", "(bgp_session_live_stats$last.tx_route_refresh_count) as tx_route_refresh_count", "(bgp_session_live_stats$last.rx_route_refresh_count) as rx_route_refresh_count", "(bgp_session_live_stats$last.outstanding_route_count) as outstanding_route_count", "(bgp_session_live_stats$last.last_rx_update_route_count) as last_rx_update_route_count", "(bgp_session_live_stats$last.tx_notify_code) as tx_notify_code", "(bgp_session_live_stats$last.tx_notify_sub_code) as tx_notify_sub_code", "(bgp_session_live_stats$last.rx_notify_code) as rx_notify_code", "(bgp_session_live_stats$last.rx_notify_sub_code) as rx_notify_sub_code", "(bgp_session_live_stats$last.tx_rt_constraint_count) as tx_rt_constraint_count", "(bgp_session_live_stats$last.rx_rt_constraint_count) as rx_rt_constraint_count", "(bgp_session_live_stats$last.session_up_count) as session_up_count" ] } ] } } }

# insert the db id and query body to create the full query
set req_live [string map [list $db_temp $db_id $query_temp $query_live] $query_string_whole]

# set url and http message config
set resultConfig [stc::get system1 -children-TemevaResultsConfig]
set url [stc::get $resultConfig -ServiceUrl]
append url "/queries"
set config { method post content-type application/json }

puts "---- query for live bgp session result..."
set res_live [::rest::simple $url $req_live $config ]

# convert json response to a dict and get result of interest
set js_res [::json::json2dict $res_live]

# print all column names
set cols [dict get [dict get $js_res result] columns]
set col_len [llength $cols]
puts "---- column names:"
for {set i 0} {$i < $col_len} {incr i} {
    puts "column $i: [lindex $cols $i]"
}

# get all result rows
set rows [dict get [ dict get $js_res result ] rows]
set row_len [llength $rows]
puts "---- total number of rows in result: $row_len"

# get state of rows
for {set i 0} {$i < $row_len} {incr i} {
    puts "[ lindex [ lindex $rows $i ] 0] state: [ lindex [ lindex $rows $i ] 3]"
}


# stop traffic
puts "---- stop traffic..."
stc::perform GeneratorStop -generatorList $genList
stc::sleep 3

puts "---- take a snapshot"
# take a snapshot, default snapshot name is 'Snapshot 1'
stc::perform SaveEnhancedResultsSnapshot

# check eot result, this query is also copied from view. If the snapshot is saved with a customized name, replace 'Snapshot 1' below with the specified name.
set query_eot { { "multi_result": { "filters": [ "view.test_snapshot_name = 'Snapshot 1'" ], "groups": [], "orders": [], "projections": [ "view.test_snapshot_name as test_snapshot_name", "view.port_name as port_name", "view.emulated_device_name as emulated_device_name", "view.bgp_session_session_index as bgp_session_session_index", "view.state as state", "view.tx_advertised_route_count as tx_advertised_route_count", "view.rx_advertised_route_count as rx_advertised_route_count", "view.tx_withdrawn_route_count as tx_withdrawn_route_count", "view.rx_withdrawn_route_count as rx_withdrawn_route_count", "view.tx_notification_count as tx_notification_count", "view.rx_notification_count as rx_notification_count", "view.tx_advertised_update_count as tx_advertised_update_count", "view.rx_advertised_update_count as rx_advertised_update_count", "view.tx_withdrawn_update_count as tx_withdrawn_update_count", "view.tx_keepalive_count as tx_keepalive_count", "view.rx_keepalive_count as rx_keepalive_count", "view.tx_open_count as tx_open_count", "view.rx_open_count as rx_open_count", "view.tx_route_refresh_count as tx_route_refresh_count", "view.rx_route_refresh_count as rx_route_refresh_count", "view.outstanding_route_count as outstanding_route_count", "view.last_rx_update_route_count as last_rx_update_route_count", "view.tx_notify_code as tx_notify_code", "view.tx_notify_sub_code as tx_notify_sub_code", "view.rx_notify_code as rx_notify_code", "view.rx_notify_sub_code as rx_notify_sub_code", "view.tx_rt_constraint_count as tx_rt_constraint_count", "view.rx_rt_constraint_count as rx_rt_constraint_count", "view.session_up_count as session_up_count" ], "subqueries": [ { "alias": "view", "filters": [], "groups": [], "orders": [], "projections": [ "test.snapshot_name as test_snapshot_name", "port.name as port_name", "emulated_device.name as emulated_device_name", "bgp_session.session_index as bgp_session_session_index", "(bgp_session_stats.state) as state", "(bgp_session_stats.tx_advertised_route_count) as tx_advertised_route_count", "(bgp_session_stats.rx_advertised_route_count) as rx_advertised_route_count", "(bgp_session_stats.tx_withdrawn_route_count) as tx_withdrawn_route_count", "(bgp_session_stats.rx_withdrawn_route_count) as rx_withdrawn_route_count", "(bgp_session_stats.tx_notification_count) as tx_notification_count", "(bgp_session_stats.rx_notification_count) as rx_notification_count", "(bgp_session_stats.tx_advertised_update_count) as tx_advertised_update_count", "(bgp_session_stats.rx_advertised_update_count) as rx_advertised_update_count", "(bgp_session_stats.tx_withdrawn_update_count) as tx_withdrawn_update_count", "(bgp_session_stats.tx_keepalive_count) as tx_keepalive_count", "(bgp_session_stats.rx_keepalive_count) as rx_keepalive_count", "(bgp_session_stats.tx_open_count) as tx_open_count", "(bgp_session_stats.rx_open_count) as rx_open_count", "(bgp_session_stats.tx_route_refresh_count) as tx_route_refresh_count", "(bgp_session_stats.rx_route_refresh_count) as rx_route_refresh_count", "(bgp_session_stats.outstanding_route_count) as outstanding_route_count", "(bgp_session_stats.last_rx_update_route_count) as last_rx_update_route_count", "(bgp_session_stats.tx_notify_code) as tx_notify_code", "(bgp_session_stats.tx_notify_sub_code) as tx_notify_sub_code", "(bgp_session_stats.rx_notify_code) as rx_notify_code", "(bgp_session_stats.rx_notify_sub_code) as rx_notify_sub_code", "(bgp_session_stats.tx_rt_constraint_count) as tx_rt_constraint_count", "(bgp_session_stats.rx_rt_constraint_count) as rx_rt_constraint_count", "(bgp_session_stats.session_up_count) as session_up_count" ] } ] } } }

set req_eot [string map [list $db_temp $db_id $query_temp $query_eot] $query_string_whole]
puts "---- query for eot bgp session result..."
set res_eot [::rest::simple $url $req_eot $config ]

# convert json response to a dict and get result of interest
set js_res [::json::json2dict $res_eot]

# print all column names
set cols [dict get [dict get $js_res result] columns]
set col_len [llength $cols]
puts "---- column names:"
for {set i 0} {$i < $col_len} {incr i} {
    puts "column $i: [lindex $cols $i]"
}

# get all result rows
set rows [dict get [ dict get $js_res result ] rows]
set row_len [llength $rows]
puts "---- total number of rows in result: $row_len"

# get tx route count of rows
for {set i 0} {$i < $row_len} {incr i} {
    puts "tx advertised route count for [ lindex [ lindex $rows $i ] 1]: [ lindex [ lindex $rows $i ] 5]"
}

# clean up
puts "---- detach and clean up"
stc::perform chassisDisconnectAll 
stc::perform resetConfig
puts "---- the end"