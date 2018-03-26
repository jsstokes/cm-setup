# cm-setup
The *setup.py* script provides three things:
1. Creates an empty *setup.ini* which will be needed for the next steps
2. Generates a proper *hosts* file for use with the included Ansible playbook script
3. A few helper scripts
- ```start-instances``` - will start all the EC2 instances
- ```stop-instances``` - will stop all the EC2 instances
- ```terminate-instances``` - will terminate all the EC2 instances
- "ssh-n" - simply starts ssh specifying the ec2-user and the public DNS name  
  one ssh script for each instance, numbered 1 to the number of instances specified   
  **use** ```ssh-add my-key-file.pem``` **to add the PEM key or the ssh-n scripts will not work**

**Note** 
The *setup.py* script is able to generate the start, stop, and terminate scripts regardless of the current state of the instances.  However, to properly generate the *hosts* file, all instances must be currently running.  This is because the public DNS names can only be obtained after an instance is started.
  

## Initial Setup
1. Make a clone of this repository 
   ```git clone xxxxx``` where xxx is the URL for this repository
1. Change to the cm-setup directory and run *setup.py*
  - this script will check to see if you already have a *setup.ini* file.  If not, a sample one will be created
  - Edit the setup.ini file and make sure to:
   list your AWS EC2 instances (**one** instance-id per line, all by itself)  
   **Remember** There should be **NO** # at the beginning of the line - those are treated as comments
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





