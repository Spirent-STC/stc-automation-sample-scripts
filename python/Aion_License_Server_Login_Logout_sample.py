# File Name:                 Aion_Licnese_Server_Login_Logout_sample.py
# Description:               This script demonstrates login Aion License Server,
#                            reserve stc ports and sign-out after completion of test suites 

# This loads the TestCenter library.
from StcPython import StcPython
stc = StcPython()

stc.log("INFO", "Starting Test")

# Retrieve and display the current API version.
print("SpirentTestCenter system version:\t", stc.get("system1", "version"))

#Sign in AION License Server
print("Signing AION License Server")
stc.perform("TemevaSignInCommand", Server=<server_ip>, Username=<user_name>, Password=<password>)
stc.perform("TemevaSetWorkspaceCommand", Workspace=<workspacename>)

#Alternative way to sign in AION License Server
print("Signing AION License Server using a refresh token")
stc.perform("TemevaSignInWithTokenCommand", Server=<server_ip>, RefreshToken=<refreshtoken>)

# Physical topology
szChassisIp1 = "10.29.0.49"
szChassisIp2 = "10.29.0.45"
txPortLoc = "//%s/%s/%s" % ( szChassisIp1, 1, 1)
rxPortLoc = "//%s/%s/%s" % ( szChassisIp2, 1, 1)

# Create the root project object
print("Creating project ...")
hProject = stc.create("project")

# Create ports
print("Creating ports ...")
hPortTx = stc.create("port", under=hProject, location=txPortLoc, useDefaultHost=False)
hPortRx = stc.create("port", under=hProject, location=rxPortLoc, useDefaultHost=False)

# Configure physical interface.
hPortTxCopperInterface = stc.create("EthernetCopper",  under=hPortTx)

# Attach ports. 
# Connects to chassis, reserves ports and sets up port mappings all in one step.
# By default, connects to all previously created ports.
print("Attaching ports ", txPortLoc, rxPortLoc)
stc.perform("AttachPorts")

# Apply the configuration.
print("Apply configuration")
stc.apply()

# Disconnect from chassis, release ports, and reset configuration.
print("Release ports and disconnect from chassis")
stc.perform("ChassisDisconnectAll")

# Delete configuration
print("Deleting project")
stc.delete(hProject)

#Sign out Aion License Server
#Note: It is recommended to sign out of the server after completing the test suites 
print("Sign out Aion license server")
stc.perform("TemevaSignOutCommand")

stc.log("INFO", "Ending Test")