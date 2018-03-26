#!/usr/bin/python
# setup.py
# --------
# Reads the setup.ini file and produces the hosts file for ansible
# 
#
import boto3
import ConfigParser
import sys
import os
import stat

output_file_name = "hosts"

#
# If the setup.ini file doesn't exist, create a skeleton with examples
#
if os.path.exists("setup.ini") == False:
    outfile = open("setup.ini","w")
    sample = ConfigParser.ConfigParser(allow_no_value=True)
    sample.optionxform(str())
    outfile.write("# ------------------------------------------------------------------------------\n")
    outfile.write("#  setup.ini\n")
    outfile.write("# ---------\n")
    outfile.write("#  Please update samples in the various sections\n")
    outfile.write("# \n")
    outfile.write("#  Rules\n")
    outfile.write("#  -----\n")
    outfile.write("#    Lines beginning with # or ; are treated as comments\n")
    outfile.write("#    There should be at least 3 instance ids - one for each RS member\n")
    outfile.write("#    replicaSetName - must be at least 4 characters long\n")
    outfile.write("#    Port           - is ignored - so the default of 27000 should be unchanged\n")
    outfile.write("#                     No apprent way to change the port that Cloud Manager uses \n")
    outfile.write("#                     for the Mongod instances.\n")
    outfile.write("# \n")
    outfile.write("#                     Port given here IS used to create the connection strings\n")
    outfile.write("#                     so only change it if the instances show up using a different\n")
    outfile.write("#                     port\n")
    outfile.write("# ------------------------------------------------------------------------------\n")
    sample.add_section("aws instances")
    sample.set("aws instances","# instance-id-1")
    sample.set("aws instances","# instance-id-2")
    sample.set("aws instances","# instance-id-3")
    sample.add_section("cloud manager")
    sample.set("cloud manager","replicaSetName", "demoRS")
    sample.set("cloud manager","port","27000")
    sample.set("cloud manager","apiKey","myapidkey")
    sample.set("cloud manager","mmsGroupID","mymmsgroupid")
    sample.write(outfile)
    outfile.close()
    print "no INI file found -- a sample has been created with the name setup.ini"
    quit()

ini = ConfigParser.ConfigParser(allow_no_value=True)
ini.read("setup.ini")
instance_ids = []
instance_id_string = "{'"
for id in ini.items("aws instances"):
    instance_ids.append(id[0])
    instance_id_string += id[0] + "','"
pos = instance_id_string.rfind(",")
instance_id_string = instance_id_string[0:pos]
instance_id_string += "}"

#
# Creating some helper scripts to deal with the instances
#

# Start all instances script
start_file = open("start-instances","w")
start_file.write("aws ec2 start-instances --instance-ids " + instance_id_string + "\n")
start_file.close()

# Stop all instances script
stop_file = open("stop-instances","w")
stop_file.write("aws ec2 stop-instances --instance-ids " + instance_id_string + "\n")
stop_file.close()

# terminate/destroy all instances script
stop_file = open("terminate-instances","w")
stop_file.write("aws ec2 terminate-instances --instance-ids " + instance_id_string + "\n")
stop_file.close()


# Set the helpers to be executable
os.chmod("start-instances", stat.S_IRWXU)
os.chmod("stop-instances", stat.S_IRWXU)
os.chmod("terminate-instances", stat.S_IRWXU)




for id in instance_ids:
    print id

replica_set_name = ini.get("cloud manager", "replicaSetName")
api_key = ini.get("cloud manager", "apiKey")
port = ini.get("cloud manager", "port")
mms_group_id = ini.get("cloud manager","mmsGroupID")

# ------------------------------------------
# Get the Public DNS name for our instances
# ------------------------------------------
client = boto3.client('ec2')
dns_names = []
try:
    for id in instance_ids:
        response = client.describe_instances(InstanceIds = [id])
        dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        print "Instance: " + id + " is at " + dns_name
        dns_names.append(dns_name)
except:
    print "All Instances do not appear to be running."
    print "please start all instance and retry"
    quit()
# ----------------------------------------------
# Create the connection string for the script
# ----------------------------------------------
conn_string = replica_set_name + "/"
for host in dns_names:
    conn_string += host + ":" + port + ","
pos = conn_string.rfind(",")
conn_string = conn_string[0:pos]
print "conn_string: ", conn_string


#
# Create the output config
#
out_file = file(output_file_name,"w")
out_parms = ConfigParser.ConfigParser(allow_no_value=True)
out_parms.add_section("local")
out_parms.set("local", "127.0.0.1")
out_parms.add_section("demo")
for host_name in dns_names:
    out_parms.set("demo",host_name)
out_parms.add_section("demo:vars")
out_parms.set("demo:vars","conn_string", conn_string)
out_parms.set("demo:vars","api_key", api_key)
out_parms.set("demo:vars","mmsGroupID", mms_group_id)
out_parms.write(out_file)
out_file.close()

#
# Create scripts to ssh into the instances as the ec2-user
#
# scripts will be named "ssh-x" where x is 1 - number of instances
#

# terminate/destroy all instances script
stop_file = open("mongo-shell","w")
stop_file.write("mongo --host " + conn_string + "\n")
stop_file.close()


# Set the helpers to be executable
os.chmod("mongo-shell", stat.S_IRWXU)
count = 0
for host in dns_names:
    count += 1
    filename = "ssh-" + str(count)
    my_file = open(filename, "w")
    my_file.write("ssh ec2-user@" + host + "\n")
    my_file.close()
    os.chmod(filename, stat.S_IRWXU)


