# cm-setup

## Setup
1. Make a clone of this repository using git clone xxxxx where xxx is the URL for this repository
1. change to the cm-setup directory and run setup.py
- this script will check to see if you already have a setup.ini file.  If not, a sample one will be created
- Edit the setup.ini file and make sure to:
   - list your AWS EC2 instances (one instance-id per line)
   - create an API key in your Cloud Manager projects security section and past that value in here
1. Sign into Cloud Manager UI and:
- Create a new project
- Build a new Deployment (Build New button)
- select "Deploy in other remote"
- select "Create Replica Set"
1. You should now be at the "Provide details for your replica set" page.  Enter the values.
- Enter (or copy) the Replica Set Name into the replicaSetName value in setup.ini
- The number of Nodes should match the number of instance-ids in the file
- Do not change the Data Dairectory Prefix - for now the ansible script will always assume /data
  - FYI - the /data directory will be create by the ansible script with the proper permissions in each EC2 instance

  



