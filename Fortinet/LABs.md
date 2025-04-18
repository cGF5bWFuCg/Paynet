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
### Anylting 