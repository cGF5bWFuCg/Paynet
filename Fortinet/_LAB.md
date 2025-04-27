# **Lab 1: Troubleshooting Concepts**

## **Exercise 1: Using The Debug Flow to Filter Traffic**

### **Setup and Start Debugging**

| Command                                   | Explanation                                                                                 |
|-------------------------------------------|---------------------------------------------------------------------------------------------|
| `diag debug disable`                        | Turns off any current debug (good to reset before starting new troubleshooting).            |
| `diag debug flow trace stop`                | Stops the debug flow trace if it’s running.                                                 |
| `diag debug flow filter clear`              | Clears any existing debug filters (address, ports, etc.).                                   |
| `diag debug reset`                          | Resets debug settings (clean start).                                                        |
| `diag debug flow filter addr 10.1.10.1`     | Filter debug output to only show traffic involving IP **10.1.10.1**.                            |
| `diag debug flow filter proto 1`            | Filter for traffic of **Protocol 1** (ICMP = ping).                                             |
| `diag debug flow show function-name enable` | Shows the **function names** in the debug output (more detailed where the packet is processed). |
| `diag debug flow show iprope enable`        | Displays **IPROPE** info (important for understanding packet handling).                         |
| `diag debug console timestamp enable`       | Adds **timestamps** to debug messages.                                                          |
| `diag debug flow trace start 10`            | Starts the debug and traces **10 packets** matching the filters.                                |
| `diag debug enable`                         | Enables the debug output (starts showing results).                                          |

---

### **Modify the Debug Flow Filter**

| Command                         | Explanation                                    |
|---------------------------------|------------------------------------------------|
| `diag debug flow filter proto 6`  | Change filter to **Protocol 6** (TCP).             |
| `diag debug flow filter port 443` | Filter for **TCP port 443** (HTTPS traffic).       |
| `diag debug flow trace start 10`  | Restart the packet tracing (10 packets again). |

---

### **Check IPROPE Handlers**

| Command                            | Explanation                                                                    |
|------------------------------------|--------------------------------------------------------------------------------|
| `diag firewall iprope list 00004320` | Shows how traffic matching IPROPE handler **ID 00004320** is processed internally. |

---

### **Disable and Reset the Debug Flow**

| Command                      | Explanation                       |
|------------------------------|-----------------------------------|
| `diag debug disable`           | Turns off debug.                  |
| `diag debug flow trace stop`   | Stops packet trace.               |
| `diag debug flow filter clear` | Clears all filters.               |
| `diag debug reset`             | Resets everything back to normal. |

---

# **Lab 2: System Resources**

## **Exercise 1: Analyzing System Information**

| Command                        | Explanation                                                             |
|--------------------------------|-------------------------------------------------------------------------|
| `get system status`              | Shows firmware version, serial number, system uptime, etc.              |
| `get system performance status`  | Shows CPU, memory usage, sessions, network statistics.                  |
| `diag hardware sysinfo memory`   | Shows **hardware memory** usage.                                            |
| `diag hardware sysinfo shm`      | Shows **shared memory** usage (system memory areas shared by processes).    |
| `diag hardware sysinfo slab`     | Shows kernel memory allocations ("slab" caches).                        |
| `diag hardware sysinfo conserve` | Shows memory conserve mode status (if system is running low on memory). |

---

## **Exercise 2: Analyzing a Crash Log**

| Command                                                    | Explanation                                                                |
|------------------------------------------------------------|----------------------------------------------------------------------------|
| `diag sys top`                                               | Displays real-time **CPU and memory usage** for each process (like Linux `top`). |
| *Tip: Processes with* `<` *symbol are running at **high priority**.* |                                                                            |
| `diag sys kill 11 <process_id>`                              | Kills a specific process using its ID.                                     |
| `diag debug crashlog read`                                   | Reads the **crash log** to investigate crashes and system faults.              |

---

# **Lab 3: Sessions, Traffic Flow, and Networking**

## **Exercise 1: Exploring the Session Table**

| Command                                 | Explanation                                                  |
|-----------------------------------------|--------------------------------------------------------------|
| `diag sys session filter clear`           | Clears existing session filters.                             |
| `diag sys session filter dport 22`        | Filters sessions where destination port is **22** (SSH traffic). |
| `diag sys session filter dst 10.1.10.254` | Further filters for destination IP **10.1.10.254**.              |
| `diag sys session list`                   | Lists sessions that match the above filters.                 |

---

## **Exercise 2: Troubleshooting Connectivity Issues**

| Command                                                | Explanation                                                                   |
|--------------------------------------------------------|-------------------------------------------------------------------------------|
| `diag sniffer packet any "port 23 and host 10.1.10.1" 4` | Packet capture for **port 23 (Telnet)** and host **10.1.10.1**, shows first 4 layers. |
| `diag sniffer packet any "port 80 and host 10.1.10.1" 4` | Same but for **port 80 (HTTP)**.                                                  |
| `diag sniffer packet any "icmp and host 10.1.10.1" 4`    | Same but for **ICMP (ping)**.                                                     |

| More Session Filters                        | Explanation                                     |
|---------------------------------------------|-------------------------------------------------|
| `diag sys session filter clear`               | Clear filters.                                  |
| `diag sys session filter src 10.1.10.1`       | Filter sessions with **source IP 10.1.10.1**.       |
| `diag sys session filter dport <port_number>` | Filter sessions to a specific **destination port**. |
| `diag sys session list`                       | List filtered sessions.                         |

| Another set of session commands             |                                                 |
|---------------------------------------------|-------------------------------------------------|
| `diag sys session filter clear`               | Clear filters.                                  |
| `diag sys session filter dport <port_number>` | Filter destination port.                        |
| `diag sys session filter addr 10.1.10.1`      | Filter sessions involving address **10.1.10.1**.    |
| `diag sys session filter start 10.1.10.1`     | Filter for sessions starting from **10.1.10.1**.    |
| `diag sys session lis`                        | (typo, should be `list`) Lists matching sessions. |

---

# **Lab 4: Security Fabric**

## **Exercise 1: Troubleshooting Downstream Communication**

| Command                            | Explanation                                         |
|------------------------------------|-----------------------------------------------------|
| `diagnose test application csfd 1`   | Tests CSF daemon (Security Fabric).                 |
| `diagnose sys csf upstream`          | Check **upstream** communication (to Fabric root).      |
| `diagnose sys csf downstream`        | Check **downstream** communication (to Fabric members). |
| `diagnose debug application csfd -1` | Enable debug logs for the CSFD application.         |
| `diagnose debug enable`              | Turns on debug output.                              |
| `diagnose debug reset`               | Resets debug settings.                              |

---

# **Lab 5: Authentication**

## **Exercise 1: Troubleshooting LDAP Authentication**

| Command                                                      | Explanation                                           |
|--------------------------------------------------------------|-------------------------------------------------------|
| `diagnose debug application fnbamd -1`                         | Enable debug logs for authentication daemon (**fnbamd**). |
| `diagnose debug enable`                                        | Turns on debugging.                                   |
| `diagnose test authserver ldap External-LDAP aduser1 password` | Test login using **LDAP** with user `aduser1`.              |
| `diagnose test authserver ldap External-LDAP student Fort1net` | Test login with another user `student`.                 |

| More Authentication Checks                 |                                                |
|--------------------------------------------|------------------------------------------------|
| `diagnose firewall auth list`                | Lists all authenticated firewall users.        |
| `diag sys session filter dport 80`           | Filter sessions to **port 80 (HTTP)**.             |
| `diag sys session filter policy 1`           | Filter sessions using **policy ID 1**.             |
| `diag sys session list`                      | Lists filtered sessions.                       |
| `diag sys session filter dport 80`           | Same (destination port 80).                    |
| `diag sys session filter policy <policy ID>` | Filter by specific policy.                     |
| `diag sys session clear`                     | Clear matching sessions (reset connection).    |
| `diagnose firewall auth clear`               | Clears all authenticated users (log them out). |

---

## **Exercise 2: Troubleshooting SAML Authentication**

| Command                              | Explanation                                   |
|--------------------------------------|-----------------------------------------------|
| `diagnose debug application fnbamd -1` | Debug **SAML** (authentication also uses fnbamd). |
| `diagnose debug enable`                | Enable debug output.                          |
| `diagnose firewall auth clear`         | Clear any existing authenticated users.       |
