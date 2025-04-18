# FSSE 7.4
## Troubleshooting Concepts
### Using The Debug Flow to Filter Traffic
```bash
diag debug disable
diag debug flow trace stop
diag debug flow filter clear
diag debug reset
diag debug flow filter addr 10.1.10.1
diag debug flow filter proto 1
diag debug flow show function-name enable
diag debug flow show iprope enable
diag debug console timestamp enable
diag debug flow trace start 10
diag debug enable
```
### Modify the Debug Flow Filter
```bash
diag debug flow filter proto 6
diag debug flow filter port 443
diag debug flow trace start 10
```
```bash
diag firewall iprope list 00004320 
```
> `diag firewall iprope list` — This diagnostic command shows the internal IPROPE handler table (how traffic is matched and handled in FortiOS).<br />
> `00004320` — This is the IPROPE index or handler ID. Each flow or type of traffic gets its own IPROPE handler.

### Disable and Reset the Debug Flow
```bash
diag debug disable
diag debug flow trace stop
diag debug flow filter clear
diag debug reset
```
## System Resources
### Check Resource Usage
```bash
get system status
get system performance status
```
```bash
diag hardware sysinfo memory
diag hardware sysinfo shm
diag hardware sysinfo slab
diag hardware sysinfo conserve
```
### Analyzing a Crach Log 
```bash
diag sys top
```
The processe that ate running with a high priority are with a < .
### Kill Process
```bash
diag sys kill 11 <process_id>
```
### Check the Crash Log
```bash
diag debug crachlog read
```
## Sessions, Traffic Flow, and Networking
### Analyze the Session Table
```bash
diag sys session filter clear
diag sys session filter dport 22
diag sys session filter dst 10.1.10.254
diag sys session list
```
### Troubleshooting Connectivity Issues
```bash
diag sniffer packet any "port 23 and host 10.1.10.1" 4
diag sniffer packet any "port 80 and host 10.1.10.1" 4
diag sniffer packet any "icmp and host 10.1.10.1" 4
```
```bash
diag sys session filter clear
diag sys session filter src 10.1.10.1
diag sys session filter dport <port_number>
diag sys session list
```
```bash
diag sys session filter clear
diag sys session filter dport <port_number>
diag sys session filter addr 10.1.10.1
diag sys session filter start 10.1.10.1
diag sys session lis
```