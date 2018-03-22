# cm-setup

## Setup
1. Make a clone of this repository using git clone xxxxx where xxx is the URL for this repository
1. Change to the cm-setup directory and run *setup.py*
  - this script will check to see if you already have a *setup.ini* file.  If not, a sample one will be created
  - Edit the setup.ini file and make sure to:
   list your AWS EC2 instances (**one** instance-id per line)
  - create an API key in your Cloud Manager project's security section and paste that value in *setup.ini*.
3. Sign into Cloud Manager UI and:
  - Create a new project
  - Build a new Deployment (Build New button)
   select "*Deploy in other remote*"
   select "*Create Replica Set*"
4. You should now be at the "Provide details for your replica set" page.  Enter the values.
  - Enter (or copy) the Replica Set Name into the replicaSetName value in *setup.ini*
  - The number of Nodes should match the number of instance-ids in the file
  - Do not change the Data Dairectory Prefix - for now the ansible script will always assume /data
    - FYI - the **/data** directory will be created by the ansible script with the proper permissions in each EC2 instance
5. On the next page, choose whether or not you want backups.  
  - Your selection has no bearing on the anisble scripts
6. You should finally be at the "Install an Automation Agent on each server" page.  
   
   Select the "*RHEL/CentOS (5.x, 6.x). SUSE11, Amazon Linux - RPM*" option from the "*Install Agent*" dropdown for the first server.
7. You should receive a pop-up that shows you the mmsGroup that you will need to copy into the set.ini file





