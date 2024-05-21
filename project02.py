json_value = {
    "issues": [
        {
            "id": 1,
            "description": "Unavailability of services in SAP HANA Database causing unplanned downtime.",
            "solution": '''Use case 1 – A service is stopped in HANA Database.
1.	Check the status of the HANA Database services using below command after logging in to the Primary DB server and using user <sid>adm.
sapcontrol -nr <instance no.> -function GetProcessList
2.	All the services should have the status “Green, running”. If any services have status as “Yellow, initializing” or “Red, stopped” then the service is down.

3.	Analyze the HANA DB traces to identify the root cause for the service being down. Traces for all services can be checked in below path.

/hana/shared/< SID >/HDB< Instance number >/< hostname >/trace 

4.	If a restart is required to fix the issue, perform a restart of HANA DB using the below commands after obtaining the required approvals. Ensure the SAP application is stopped correctly in the related SAP application servers first.

•	HDB stop 
•	HDB start

Use case 2 – If the database service unavailability alert is due to replication issues.
1.	The database service unavailability alert may also be triggered due to issues in replication sync between primary and secondary DB servers.
2.	Check the status of replication from the HANA studio under Landscape -> System Replication. The replication status should be “Active”.

3.	If replication is down, please enable it using below commands.

•	Secondary system - HDB stop
•	Secondary system - Execute below command to register system replication 
hdbnsutil -sr_register --name=siteW --remoteHost=<primary_host> --remoteInstance=<primary_systemnr> --replicationMode=async --operationMode=delta_datashipping
•	Secondary system -HDB start 
 Secondary system - Verify the status of replication at OS level - hdbnsutil -sr_state

4.	 Primary system - Verify the status of replication using HANA studio
'''
        },
        {
            "id": 2,
            "description": "High Disk Utilisation in SAP HANA Database causing SAP HANA database unplanned downtime.",
            "solution": '''Use case 1 – A service is stopped in HANA Database.
1.	Check the status of the HANA Database services using below command after logging in to the Primary DB server and using user <sid>adm.
sapcontrol -nr <instance no.> -function GetProcessList
2.	All the services should have the status “Green, running”. If any services have status as “Yellow, initializing” or “Red, stopped” then the service is down.

3.	Analyze the HANA DB traces to identify the root cause for the service being down. Traces for all services can be checked in below path.

/hana/shared/< SID >/HDB< Instance number >/< hostname >/trace 

4.	If a restart is required to fix the issue, perform a restart of HANA DB using the below commands after obtaining the required approvals. Ensure the SAP application is stopped correctly in the related SAP application servers first.

•	HDB stop 
•	HDB start

Use case 2 – If the database service unavailability alert is due to replication issues.
1.	The database service unavailability alert may also be triggered due to issues in replication sync between primary and secondary DB servers.
2.	Check the status of replication from the HANA studio under Landscape -> System Replication. The replication status should be “Active”.

3.	If replication is down, please enable it using below commands.

•	Secondary system - HDB stop
•	Secondary system - Execute below command to register system replication 
hdbnsutil -sr_register --name=siteW --remoteHost=<primary_host> --remoteInstance=<primary_systemnr> --replicationMode=async --operationMode=delta_datashipping
•	Secondary system -HDB start 
 Secondary system - Verify the status of replication at OS level - hdbnsutil -sr_state

4.	 Primary system - Verify the status of replication using HANA studio
'''
        },
        {
            "id": 3,
            "description": "Outage / unavailability of SAP systems causing unplanned downtime.",
            "solution": '''Use case 1 – When SAP system allows to login from SSO portal or SAP Logon pad. 
1.	Check if the outage is caused due to unavailability of one or more specific application servers using SM51 or SMLG T-codes.

2.	If outage is due to unavailability of specific application servers, login to the application server using the AWS console and check the root cause for the outage.

3.	If the application is down due to recent reboot of the application server, then start the SAP application using below command with the <sid>adm user.

startsap

Use case 2 – If the SAP application does not allow login due to DB issue.
1.	Check the status of the connectivity to the database using below command from SAP application server using <sid>adm user.

R3trans -d

Expected value is 0000. Any other return code will indicate the problem with database server.  

2.	If the application is not reachable due to DB being down, login to the related Primary DB server and start the Database services, or troubleshoot the DB issue accordingly.

Use case 3 – If the SAP application does not allow login, but there are no issues with the Database.

1.	Check the status of SAP application using below command from the primary application server.

sapcontrol -nr <instance no.> -function GetProcessList

2.	If the services are down, the system needs to be started using below command.

Startsap

3.	If the system is started and running, but does not allow login then check the work processes status using below command to identify if work processes occupancy is causing the login issue. 

dpmon pf=<profile_name>

4.	The problematic work processes would then need to be killed using below command.

kill -9 <PID>

5.	Check if we are able to login to the SAP system fine.
'''
        },
    ]
}

json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Schema for a simple issue solutioning system, you will have issue and its solution steps",
    "type": "object",
    "properties": {
        "issues": {
            "description": "List of issues",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "Unique identifier for the issue",
                        "type": "integer",
                    },
                    "description": {
                        "description": "Short description of the issue",
                        "type": "string",
                    },
                    "solution": {
                        "description": "Solution for the issue",
                        "type": "string",
                    },
                },
                "required": ["id", "description", "solution"]
            },
        },
    },
    "required": ["issues"]
}

from llama_index.core.indices.struct_store import JSONQueryEngine
import utils

llm = utils.aws_llm()
print(llm.complete("hello"))

# nl_query_engine = JSONQueryEngine(
#     json_value=json_value,
#     json_schema=json_schema,
#     llm=llm,
#     synthesize_response = False
# )

syn_query_engine = JSONQueryEngine(
    json_value=json_value,
    json_schema=json_schema,
    llm=llm,
    synthesize_response = True
)
# raw_query_engine = JSONQueryEngine(
#     json_value=json_value,
#     json_schema=json_schema,
#     llm=llm,
#     synthesize_response=False,
# )

description = llm.complete('''
from the given list of descriptions 
[
    Outage / unavailability of SAP systems causing unplanned downtime, 
    High Disk Utilisation in SAP HANA Database causing SAP HANA database unplanned downtime, 
    Unavailability of services in SAP HANA Database causing unplanned downtime
]

find the best match for "System Outage".

Just give the exact words from the given list, don't add or synthesize it.
''')
print(description)
print(syn_query_engine.query(f"What is the solution for the issue description {description}."))
