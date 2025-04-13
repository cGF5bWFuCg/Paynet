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
If ECMP is enabled, FortiGate can share traffic among up to 10 of these BGP routes.

```bash
⚠️
config router bgp
    set ebgp-multipath enable
end
```
