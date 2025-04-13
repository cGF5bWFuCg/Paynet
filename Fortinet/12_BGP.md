## BGP Overview
**BGP (Border Gateway Protocol) is the protocol <ins>underlying</ins> the global routing system of the internet**

By default, **FortiGate BGP does not advertise any prefixes**. You need to explicitly configure FortiGate to advertise prefixes using either the **redistribution command** or the **network command**.
## Protocol Redistribution
Protocol redistribution allows you to advertise routes learned from non-BGP routing protocols (like connected, static, OSPF, RIP, IS-IS) into BGP.<br />
By default, FortiGate BGP doesn't advertise prefixes from other protocols.
```bash
config router bgp
    config redistribute "ospf"
        set status enable
        set route-map "ospf-to-bgp"
    end
end
```
To verify redistribution
```bash
get router info bgp network
get router info bgp neighbors
```
*   **Access lists** They can prevent injecting routes into the routing table using `distribute-list-in` or advertising routes to neighbors using `distribute-list-out`.
*   **Prefix lists** They can prevent injecting routes using `prefix-list-in` or advertising routes using `prefix-list-out`. Additionally, they can filter routes redistributed by other protocols and can modify BGP attributes.
*   **Route Maps** They can filter both injecting and advertising routes using `route-map-in` and `route-map-out` parameters. Access and prefix lists can be used as objects within route maps.

## BGP Commands Comparison
```bash
get router info bgp summary
```
**Provides a high-level overview of the BGP status**, including the local router ID, local AS number, BGP table version, and a summary of each neighbor's status, such as their AS, the number of messages sent and received, table version, queue status, uptime, and the number of prefixes received (`State/PfxRcd`).<br />
If the neighbor state is not established, the actual BGP state is displayed.
```bash
get router info bgp neighbors
```
**Displays detailed information about each BGP neighbor**. This includes the peer IP address, remote AS, local AS, BGP version, remote router ID, BGP state, uptime, last read time, hold time, keepalive interval, negotiated capabilities (like route refresh and graceful restart), and any error messages or last reset information.
```bash
get router info bgp network
```
**Displays the BGP database**, listing all prefixes advertised by all neighbors, as well as the local router. It shows the status codes (e.g., valid, best, internal, stale) and origin codes (IGP, EGP, incomplete) associated with each route. Routes advertised using the `network` command are typically marked with origin code 'i' (IGP), while redistributed routes are often marked with '?' (incomplete).
```bash
get router info routing-table bgp
```
**Displays the BGP routing table**, showing the best BGP paths that have been selected and installed in the routing table.
```bash
get router info bgp neighbors <neighbor_ip> route
```
**Displays the specific routes advertised by a particular BGP neighbor**.

For troubleshooting, you can use:

```bash
diagnose ip router bgp all enable disable
```
**Enables or disables real-time debugging output for all BGP processes**.
```bash
diagnose ip router bgp level <level>
```
**Sets the level of detail for the BGP debug output** (e.g., info).
```bash
diagnose debug enable | disable
```
**Enables or disables the general debug output**. Remember that `diagnose debug reset` does not stop BGP real-time debug.
```bash
execute router clear bgp all | <neighbor_ip> | as <as_number>
```
**Used to reset BGP sessions**. Using `soft [in|out]` performs a soft reset, forcing the exchange of complete BGP routing tables without tearing down the TCP connection.
## Configure ECMP With BGP Routes
If ECMP is enabled, FortiGate can share traffic among up to 10 of these BGP routes.<br />
⭕🔴
```bash
config router bgp
    set ebgp-multipath enable
end
```
## Loopback Interfaces as BGP Source
+ Using a loopback interface as the BGP source IP address.
+ Must explicitly configure the loopback interface in the same way as the source interface.
+ Must enable multihop.
+ Since the BGP session on TCP port 179 might be traveling through a physical interface, you must configure a corresponding firewall policy to allow traffic between the loopback interface and the physical interface of the BGP peers.
```bash
config router bgp
    set as 65100
    set router-id 172.16.1.254
    config neighbor
        edit 100.64.1.254
            set remote-as 65101
            set update-source Loopback_Interface
            set ebgp-enforce-multihop enable
        next
    end
end
```
## The `neighbor-group` Command
The neighbor-group command in BGP allows you to apply common settings to 
a group of BGP peers.
```bash
config router bgp
    set as 65100
    set router-id 172.16.1.254
    set ibgp-multipath enable
    config neighbor-group
        edit SpokeISP1
            set interface ISP1
            set remote-as 65100
        next
    end
    config neighbor-range
        edit 1
            set prefix 10.1.0.0 255.255.255.0
            set neighbor-group SpokeISP1
        next
    end
end
```
## Route Reflectors
Route Reflectors (RRs) help to reduce the need for a full mesh of IBGP peerings within an Autonomous System (AS).
```bash
config router bgp
    config neighbor
        edit 100.64.1.254
            set next-hop-self enable
            set route-reflector-client enable
        next
    end
end
```
## BFD Parameter
Bidirectional Forwarding Detection (BFD) is a low-overhead protocol used to quickly detect faults in the forwarding path between two adjacent routers
```bash
get router info bfd neighbor
```
Check the BFD negotiation status using the command.
```bash
config router bgp
    config neighbor
        edit 100.64.1.254
            set bfd enable
            set ebgp-enforce-multihop enable
        next
    end
end
```
```bash
config router bfd
    config multihop-template
        edit 1
            set src 100.64.2.0 255.255.255.0
            set dst 100.64.1.0 255.255.255.0
            set auth-mode md5
            set md5-key password
        next
    end
end
```
## The graceful-restart Command
⭕🔴
As the BGP router daemon process is only running on the primary unit, BGP peering needs to be reestablished upon HA failover. In a cluster, the FortiGate graceful-restart command allows BGP routes to remain in the routing tables. This is particularly important during a reboot or an upgrade maintenance window to avoid potential new BGP convergence and traffic interruption.
```bash
config router bgp
    set as 65100
    set graceful-restart enable
    set router-id 172.16.1.254
    config neighbor
        edit 100.64.1.254
            set capability-graceful-restart enable
            set remote-as 200
    next
    end
end
```