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

1. `diag debug disable`  
   – Disables debugging (a good habit to start clean).

2. `diag debug flow trace stop`  
   – Stops any currently running debug flow traces.

3. `diag debug flow filter clear`  
   – Clears any previous flow filters.

4. `diag debug reset`  
   – Resets all debug settings to default.

5. `diag debug flow filter addr 10.1.10.1`  
   – Sets a debug filter for traffic to/from IP address `10.1.10.1`.

6. `diag debug flow filter proto 1`  
   – Filters for protocol 1 (ICMP — useful for ping/traceroute troubleshooting).

7. `diag debug flow show function-name enable`  
   – Shows the names of the functions involved in the flow (helpful for deeper insight into processing).

8. `diag debug flow show iprope en`  
   – Enables the display of IP policy route information.

9. `diag debug console timestamp en`  
   – Enables timestamping of debug output for better log tracing.

10. `diag debug flow trace start 10`  
   – Starts capturing 10 packets (or flows) that match the above filters.

11. `diag debug en`  
   – Enables the debug output.