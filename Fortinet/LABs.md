# Network Security Support Engineer - Lab Guide 7.4

## Lab 1: Troubleshooting Concepts

### Exercise 1: Using The Debug Flow to Filter Traffic

#### Analyze the debug Flow Output on ISFW

```
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

#### Modify the Debug Flow Filter

```
diag debug flow filter proto 6
diag debug flow filter port 443
diag debug flow trace start 10
```

```
diag firewall iprope list 00004320 
```

> diag firewall iprope list — This diagnostic command shows the internal IPROPE handler table (how traffic is matched and handled in FortiOS).  
> 00004320 — This is the IPROPE index or handler ID. Each flow or type of traffic gets its own IPROPE handler.

#### Disable and Reset the Debug Flow

```
diag debug disable
diag debug flow trace stop
diag debug flow filter clear
diag debug reset
```

## Lab 2: System Resources

### Exercise 1: Analyzing System Information

#### Check Resource Usage

```
get system status
get system performance status
```

```
diag hardware sysinfo memory
diag hardware sysinfo shm
diag hardware sysinfo slab
diag hardware sysinfo conserve
```

### Exercise 2: Analyzing a Crash Log

#### Display the Processes

```
diag sys top
```

> The processe that ate running with a high priority are with a < .

#### Kill Process

```
diag sys kill 11 <process_id>
```

#### Check the Crash Log

```
diag debug crachlog read
```

## Lab 3: Sessions, Traffic Flow, and Networking

### Exercise 1: Exploring the Session Table

#### Analyze the Session Table

```
diag sys session filter clear
diag sys session filter dport 22
diag sys session filter dst 10.1.10.254
diag sys session list
```

#### Create a Dirty Session

```
diagnose sys session list
```

### Exercise 2: Troubleshooting Connectivity Issues

#### Tips for Troubleshooting

```
diag sniffer packet any "port 23 and host 10.1.10.1" 4
diag sniffer packet any "port 80 and host 10.1.10.1" 4
diag sniffer packet any "icmp and host 10.1.10.1" 4
```

```
diag sys session filter clear
diag sys session filter src 10.1.10.1
diag sys session filter dport <port_number>
diag sys session list
```

```
diag sys session filter clear
diag sys session filter dport <port_number>
diag sys session filter addr 10.1.10.1
diag sys session filter start 10.1.10.1
diag sys session lis
```

## Lab 4: Security Fabric

### Exercise 1: Troubleshooting Downstream Communication

#### Tips for Troubleshooting

```
diagnose test application csfd 1
diagnose sys csf upstream
diagnose sys csf downstream
```

```
diagnose debug application csfd -1
diagnose debug enable
```

```
diagnose debug reset
```

## Lab 5: Authentication

### Exercise 1: Troubleshooting LDAP Authentication

```
diagnose debug application fnbamd -1
diagnose debug enable
diagnose test authserver ldap External-LDAP aduser1 password
diagnose test authserver ldap External-LDAP student Fort1net
```

```
diagnose firewall auth list
```

```
diagnose sys session filter dport 80
diagnose sys session filter policy 1
diagnose sys session list
```

```
diagnose sys session filter dport 80
diagnose sys session filter policy <policy ID>
diagnose sys session clear
```

```
diagnose firewall auth clear
```

### Exercise 2: Troubleshooting SAML Authentication

```
diagnose debug application fnbamd -1
diagnose debug enable
```

```
diagnose firewall auth clear
```
