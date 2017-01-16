#### AWS Essential

##### 1. AWS Core Infrastructure and Services

* Security: Security Groups, NACLs, AWS IAM (vs. Firewall, ACLs, Administators)
* Networking: ELB, VPC (vs. Routers, Network pipeline, Switch)
* Server: AMI -> EC2 instances
* Storage and DB: Amazon EBS, EFS, S3, Amazon RDS


##### 2. AWS Regions and Zones

**Regions:**
* Geographic locations
* Consits of at least 2 availablity zones

**Availability zones**
* Clutser of data centers
* Isolated from failures in other Availability zones

##### 3. EBS vs. EC2

**EC2**
* Data stored on local instance store persists only as long as instance is aliave
* storage is ephemeral

**EBS**
* Data stored can persist independently of the life of instance
* Storage is persistent


##### 4. Instance metadata vs. user data

**Instance metadata**
* Data about your instance
* Can be used to configure or manage running instance

**User data**
* Can be passed to instance at launch
* used to perform common automated configure tasks
* run scripts after instance start


##### 5. AWS S3

* IAM security
* Versioning
* Storage classes (Standard, IA, Glacier -- not for real time, restore before access)


##### 6. RDS best practice
* Monitor memory, CPU & storage usage
* Use multi-az deployments to automatically provision and maintain synchrounous standby in different AZ
* Enable automatic backup
* set backup window to occur during daily low in WriteIOPS

* To increare I/O capacity

* TTL less than 30s if cahcing DNS data
* Test failover of DB instance


##### 7. Dynamo DB
* Store any amout of data with no limits
* Fast, predictable performance of SSD
* Easily provision and change the request capacity
* NoSQL: collection of item with primary keys values

* Partition key
* Sort key
* Secondary index key

**Provision throughput**

Read capacity unit
* One strongly consistent read per second for items as large as 4KB
* Two eventually consistent reads per second for items as large as 4KB

Write capacity unit
* One write per second for item as large as 1KB

##### 8. Elastic load balancing

* Distribute traffice
* support health checks
* HTTP, HTTPS, TCP traffic support

##### 9. AWS Trusted Advisor
* Best practice & recommendation engine
* Cost optimization, security, fault tolerance & performance improvements
