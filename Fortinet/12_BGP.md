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

*   `diagnose ip router bgp all enable`/`disable`: **Enables or disables real-time debugging output for all BGP processes**.
*   `diagnose ip router bgp level <level>`: **Sets the level of detail for the BGP debug output** (e.g., info).
*   `diagnose debug enable`/`disable`: **Enables or disables the general debug output**. Remember that `diagnose debug reset` does not stop BGP real-time debug.
*   `execute router clear bgp all`/`<neighbor_ip>`/`as <as_number>` etc.: **Used to reset BGP sessions**. Using `soft [in|out]` performs a soft reset, forcing the exchange of complete BGP routing tables without tearing down the TCP connection.

### Use Case 1: Configure ECMP With BGP Routes

**OSPF Equal-Cost Multi-Path (ECMP) allows FortiGate to install external routes of the same cost in the routing database**. Similarly, when multiple BGP routes to the same destination have the same attributes based on the route selection process, and **if ECMP is enabled, FortiGate can share traffic among up to 10 of these BGP routes**.

To configure ECMP with BGP routes, you need to ensure that the multiple BGP paths to a destination have the same preferred attributes according to the BGP route selection tie-breakers. If these attributes are the same, FortiGate will install multiple paths in the routing table, and traffic will be load-balanced across them.

In a lab scenario, you might configure two external routes with the same cost on a router (like R2) when OSPF ECMP is enabled, and FortiGate (R2) will install both. For BGP ECMP, the concept is similar, but it's the BGP attributes that determine if routes are considered equal-cost.

### Use Case 2: Loopback Interfaces as BGP Source

Using a **loopback interface as the BGP source IP address** provides several benefits, especially in environments with redundant links. A loopback interface has a logical IP address that is independent of any physical interface and is always up as long as the device is running.

To configure a loopback interface as the BGP source:

1.  You **must explicitly configure the loopback interface in the same way as the source interface** in the `config neighbor` section of the BGP configuration.
2.  You **must enable multihop** for the BGP neighbor relationship because the loopback interface adds one logical hop.
3.  Since the BGP session on TCP port 179 might be traveling through a physical interface, you **must configure a corresponding firewall policy to allow traffic between the loopback interface and the physical interface** of the BGP peers.

This configuration ensures continuous BGP peering even if a physical interface goes down, as long as there is another path for the BGP session to reach the neighbor's loopback address. In a lab exercise, you might configure a loopback interface as the BGP source on an ISP router and a spoke device.

### Use Case 3: The neighbor-group Command

The `neighbor-group` command in BGP allows you to **apply common settings to a group of BGP peers**. This is particularly useful in scenarios like SD-WAN overlays where you have multiple spoke devices connecting to a central hub.

By using neighbor groups, you can configure parameters such as `remote-as` and other policies once for the entire group instead of configuring each neighbor individually, simplifying BGP configuration and management.

For example, in an SD-WAN overlay design with a hub and multiple spokes connected through different ISPs, you can create a neighbor group for spokes connected via a specific ISP and apply the relevant configuration to that group. The `config neighbor-range` command can then be used to define a range of peer IP addresses that belong to a specific neighbor group based on a prefix. When configuring IBGP for ADVPN, you must configure the hub as a **route-reflector-client** within the neighbor group so that routes learned from one spoke are forwarded to other spokes.

### Optimizing BGP for Rapid Convergence

**BGP convergence** is the time it takes for BGP to adapt to network changes, such as link failures or new route advertisements, and to propagate these changes throughout the network. Optimizing BGP for rapid convergence is crucial for maintaining network stability and minimizing disruption.

Several factors influence BGP convergence, including the size of the RIB, the number of hops, advertisement intervals, and failure detection delays. To improve BGP convergence:

*   **Ensure a stable network** without port flapping, which can trigger frequent BGP updates.
*   Consider using **BGP Peer Group Leader** to optimize the generation of outbound updates [Not directly in sources, this is general BGP knowledge].
*   Implement **Bidirectional Forwarding Detection (BFD)** to speed up failure detection [Not explicitly detailed in the provided excerpts for optimization, but mentioned as a negotiation status for OSPF].
*   Utilize the **graceful restart capability** to minimize the impact of BGP restarts on neighboring routers.
*   Optimize BGP timers, being cautious as aggressive timers can increase CPU utilization [Not directly in sources, this is general BGP knowledge].

FortiManager BGP templates can preconfigure settings like `graceful-restart` to aid in rapid convergence.

### BGP Convergence

**BGP convergence** refers to the process by which routers in a BGP network agree on the available paths to reach different destinations after a network topology change. This involves detecting the change, withdrawing old routes, advertising new routes, and updating their routing tables.

The time it takes for BGP to converge can impact network stability and the duration of service disruptions. Factors affecting BGP convergence include:

*   **BGP Timers**: Keepalive and Hold timers influence how quickly a router detects the loss of a neighbor [Not directly in sources, this is general BGP knowledge].
*   **Number of Routes**: A larger routing table can take longer to process and update.
*   **Network Stability**: Frequent changes (e.g., link flapping) can delay convergence.
*   **Route Advertisement Strategies**: The frequency and method of route advertisements affect propagation speed.
*   **Failure Detection Mechanisms**: How quickly a router detects a failure influences when it starts the convergence process (e.g., using BFD) [Not explicitly detailed in the provided excerpts for BGP convergence].

### Route Reflectors

**Route Reflectors (RRs) help to reduce the need for a full mesh of IBGP peerings within an Autonomous System (AS)**. In a traditional IBGP setup, every IBGP router needs to peer with every other IBGP router to ensure that routes learned from one internal router are propagated to all others. This full mesh can become administratively complex and not scalable in large networks.

An RR acts as a central point for IBGP peering. It has IBGP peers called **client routers**. An RR forwards (reflects) the routes it learns from one client to other clients, thus breaking the IBGP split horizon rule (which prevents an IBGP router from advertising routes learned from another IBGP peer to other IBGP peers).

When configuring IBGP for ADVPN, the hub is often configured as a route-reflector-client so that routes learned from one spoke are forwarded to other spokes. This eliminates the need for direct IBGP peering between all spokes.

### BFD Parameter

**Bidirectional Forwarding Detection (BFD)** is a low-overhead protocol used to quickly detect faults in the forwarding path between two adjacent routers [Not a primary topic in the provided excerpts for BGP, but mentioned in the context of OSPF].

While the excerpts don't extensively discuss BFD parameters specifically for BGP, BFD can be used to enhance the responsiveness of BGP by providing faster detection of neighbor failures than relying solely on BGP's keepalive mechanisms [General BGP knowledge]. When BFD is enabled on OSPF routers, you can check the BFD negotiation status using the command `get router info bfd neighbor`. Similar concepts apply to BGP where configuring BFD sessions between BGP peers can lead to quicker detection of link or neighbor failures, resulting in faster BGP convergence [General BGP knowledge].

### The graceful-restart Command

The **graceful restart** capability in BGP is designed to minimize disruption during a BGP router restart. When a BGP router with graceful restart enabled restarts, it informs its neighbors that it is going offline but intends to preserve the routing information it had before the restart.

The neighbors that also support graceful restart will keep the routes advertised by the restarting peer for a certain period. This allows traffic to continue to be forwarded based on the old routing information during the restart. Once the restarting router is back online, it can re-establish its BGP sessions and exchange updated routing information with its neighbors.

To enable graceful restart on a FortiGate:

1.  Enable the `graceful-restart` parameter under the `config router bgp` section.
2.  Enable the `capability-graceful-restart` parameter for each neighbor under the `config neighbor` section.

FortiManager BGP templates can preconfigure `graceful-restart` and `capability-graceful-restart`.

### Autonomous System

An **Autonomous System (AS) is a set of routers and networks under the same administration**. Each AS has a unique number assigned to it. An AS administrator has the freedom to choose any internal routing protocol (Interior Gateway Protocol or IGP) such as OSPF, RIP, or IS-IS to manage routing within the AS.

BGP uses AS numbers to identify the different administrative domains and to track the path a route takes through different ASs. **EBGP (External BGP) is used for routing between different ASs**, where BGP routers exchange AS path information for destination prefixes. **IBGP (Internal BGP) is used for routing within the same AS**.

There are different types of ASs, including stub ASs (with only one connection to another AS) and multihomed ASs (with multiple connections to different ASs).

### BGP Components

The main components of BGP include:

*   **BGP Speaker (or Peer)**: A **router that transmits and receives BGP routing information** and acts on those messages.
*   **BGP Session**: The **connectivity between two BGP peers** over a TCP connection (port 179).
*   **BGP Messages**: Different types of messages exchanged between BGP peers, such as OPEN, UPDATE, NOTIFICATION, KEEPALIVE, and ROUTE-REFRESH [Not detailed in these excerpts, but general BGP knowledge].
*   **Routing Information Base (RIB)**: As discussed earlier, BGP routers maintain RIB-in, local RIB, and RIB-out tables.
*   **BGP Attributes**: Information carried with each BGP route that describes its characteristics, such as AS path, next hop, and origin.
*   **BGP Route Selection Process**: The set of rules a BGP router uses to choose the best path to a destination when multiple paths are available.

### RIBs

(Covered earlier under "Routing Information Bases").

### BGP Attributes

**BGP attributes are pieces of information that are included with each route advertisement and provide details about the route**. BGP uses these attributes to select the best path to a destination. There are four main categories of BGP path attributes:

*   **Well-known mandatory**: These attributes must be included in every BGP update and are recognized by all BGP implementations. Examples include **ORIGIN**, **AS_PATH**, and **NEXT_HOP**.
*   **Well-known discretionary**: These attributes are also recognized by all BGP implementations but are not required in every update. An example is **LOCAL_PREF**.
*   **Optional transitive**: These attributes may or may not be accepted by an AS, but if accepted, they are passed along to other neighboring ASs. An example is **COMMUNITY**.
*   **Optional non-transitive**: These attributes may or may not be accepted by an AS, and they are not passed along to other ASs. An example is **MULTI_EXIT_DISC (MED)**.

FortiGate supports various BGP attributes and their types.

### Route Selection Tie Breakers

When a BGP router has multiple paths to the same destination, it uses a set of rules to select the best path. These rules are applied in a specific order, acting as tie-breakers:

1.  **Highest weight** (FortiGate specific, local to the router).
2.  **Highest local preference**.
3.  **Prefer the path that originated locally** (next hop = 0.0.0.0).
4.  **Shortest AS path**.
5.  **Lowest origin type** (IGP < EGP < Incomplete).
6.  **Lowest multi-exit discriminator (MED)**.
7.  **Lowest IGP metric to the BGP next hop**.
8.  **Prefer external paths (EBGP) over internal paths (IBGP)**.
9.  **If ECMP is enabled, insert up to 10 routes in the routing table**.
10. **Lowest router ID** (for IBGP paths).
11. **Lowest neighbor BGP router ID**.
12. **Lowest neighbor IP address**.
13. **Oldest route for EBGP paths**.
14. **Path through closest IGP neighbor**.

FortiGate uses a subset of these attributes during the route selection process.

### BGP Monitoring

You can monitor BGP on FortiGate using both the GUI and the CLI.

**GUI Monitoring**: The GUI provides dashboards and log views to check BGP status and events. You can navigate to **Log & Report > System Events > Router Events** to view BGP-related router events.

**CLI Monitoring**: The CLI offers several `get router info bgp` commands to check various aspects of BGP:

*   `get router info bgp summary`: Provides a summary of BGP status and neighbor information.
*   `get router info bgp neighbors`: Displays detailed information about each BGP neighbor.
*   `get router info bgp network`: Shows the BGP database.
*   `get router info routing-table bgp`: Displays the BGP routing table.
*   `get router info bgp neighbors <ip_address> route`: Shows routes advertised by a specific neighbor.

You can also use real-time debug commands for more detailed monitoring during troubleshooting.

### BGP States

A BGP neighbor relationship goes through several states during its establishment and maintenance:

*   **Idle**: Initial state, waiting for a start event.
*   **Connect**: Initiating a TCP connection to the peer.
*   **Active**: Unable to establish a TCP session; trying to connect.
*   **OpenSent**: TCP connection established; sent the OPEN message and waiting for a reply.
*   **OpenConfirm**: Received the OPEN message and sent a KEEPALIVE message; waiting for a KEEPALIVE or NOTIFICATION message.
*   **Established**: Peers have successfully exchanged OPEN and KEEPALIVE messages; BGP session is fully operational, and route updates can be exchanged.

The `get router info bgp summary` and `get router info bgp neighbors` commands display the current state of each BGP neighbor.

### BGP Summary

The `get router info bgp summary` command provides a concise overview of the BGP configuration and neighbor status. The output typically includes:

*   The local BGP router identifier and local AS number.
*   The BGP table version.
*   Counters for AS path and community entries.
*   For each neighbor:
    *   Neighbor IP address.
    *   BGP version.
    *   Remote AS number.
    *   Number of messages received (`MsgRcvd`) and sent (`MsgSent`).
    *   Table version for that neighbor (`TblVer`).
    *   Input queue (`InQ`) and output queue (`OutQ`) status.
    *   Uptime of the BGP session (`Up/Down`).
    *   **The current state of the BGP session or the number of prefixes received from the neighbor (`State/PfxRcd`)**. If the state is `Active`, it often indicates a problem establishing the TCP connection.
*   The total number of configured neighbors.

### BGP Neighbors

The `get router info bgp neighbors` command provides detailed information about a specific BGP neighbor or all neighbors. The output includes:

*   Neighbor IP address, remote AS, and local AS.
*   Whether it's an external or internal link.
*   BGP version and remote router ID.
*   The current **BGP state** and the duration the session has been up.
*   Timers: last read time, configured and negotiated hold time, and keepalive interval.
*   Neighbor capabilities (e.g., route refresh, graceful restart helper).
*   Nexthop information.
*   **Last reset information, including any error messages (like "Bad Peer AS")**.

### Prefixes Advertised by the Local FortiGate

To see the prefixes being advertised by the local FortiGate, you can use the command:

```
get router info bgp network
```

This command displays the BGP database, including the prefixes originated by the local router (often through the `network` command or redistribution) and those learned from neighbors. For the locally originated prefixes, the next hop will typically be `0.0.0.0`, and the origin code will often be `i` (IGP) if the `network` command was used. You can also see the status (e.g., valid, best, internal) and other BGP attributes associated with these prefixes.

### Prefixes Advertised by a Neighbor

To view the routes advertised by a specific BGP neighbor, use the command:

```
get router info bgp neighbors <neighbor_ip> route
```

Replace `<neighbor_ip>` with the actual IP address of the BGP neighbor. This command will display the BGP routing table entries that the specified neighbor is advertising to the local FortiGate. The output shows the network prefix, the next hop, metric, local preference, weight, route tag, AS path, and origin code for each route advertised by that neighbor.

### Prefixes Advertised by All BGP Peers

The `get router info bgp network` command shows the prefixes advertised by all BGP peers, as well as the locally originated prefixes. For each prefix, it lists the originating router's IP address (the "Next Hop" for received routes) and the associated BGP attributes like the AS path and origin code. This command provides a comprehensive view of all the routes known to the local BGP process from all its neighbors.

### BGP Event Logging

FortiGate can log various BGP events, which can be helpful for monitoring and troubleshooting. By default, BGP event logging is enabled. The types of events logged include:

*   Neighbor status changes (up or down).
*   Routing Information Base (RIB) updates.
*   BGP message exchanges.
*   Errors connecting to neighbors.

You can view these logs in the GUI under **Log & Report > System Events > Router Events**. Each log entry provides details about the event.

You can disable BGP event logging using the CLI command:

```
config router bgp
set log-neighbour-change disable
end
```

To re-enable it, use `set log-neighbour-change enable`.

### BGP Troubleshooting

Troubleshooting BGP issues between two peers involves a systematic approach:

1.  **Check Reachability**: Ensure the local router can reach the remote peer's IP address using `ping` or `traceroute`. An `Active` state in `get router info bgp summary` often indicates a lack of reachability.
2.  **Verify TCP Port 179**: Confirm that TCP port 179 is not blocked by any firewall (including local FortiGate policies between the source and destination IPs of the BGP peers).
3.  **Check TCP Session**: Verify the establishment of the TCP session on port 179 between the BGP peers using `diagnose tcp synack-stat` [Not in sources, general troubleshooting].
4.  **Check BGP Session**: Use `get router info bgp summary` and `get router info bgp neighbors` to check the BGP neighbor state and any error messages. States other than `Established` indicate a problem in the BGP negotiation. Errors like "Bad Peer AS" suggest a configuration mismatch.
5.  **Examine Prefixes**: If the BGP session is established, check the prefixes received and advertised by each peer using `get router info bgp neighbors <ip> route` and `get router info bgp network`. Ensure that the expected routes are being advertised and received.

Using real-time debug (`diagnose ip router bgp all enable`) can provide detailed information about the BGP negotiation process and any errors. Restarting the BGP session (`execute router clear bgp`) can sometimes resolve temporary issues.

### BGP Troubleshooting Tips

Here are some additional tips for troubleshooting BGP:

*   **Is there an active route to the remote peer?** Use `get router info routing-table all` to verify.
*   **Check whether TCP port 179 is blocked.** Review firewall policies.
*   **Check the status of the TCP session.** (Covered above).
*   **Check the status of the BGP session.** Use `get router info bgp summary` and `get router info bgp neighbors`.
*   **Check the prefixes received and advertised.** Use `get router info bgp neighbors <ip> route` and `get router info bgp network`.

### Real-Time Debug

Real-time BGP debug provides detailed output about BGP processes and neighbor interactions, which is very useful for troubleshooting. To enable it, use the following commands:

```
diagnose ip router bgp all enable
diagnose ip router bgp level info
diagnose debug enable
```

This will show detailed messages about BGP packet exchanges, state transitions, and errors. To disable the debug output, use:

```
diagnose ip router bgp all disable
diagnose ip router bgp level none
diagnose debug disable
```

Remember that `diagnose debug reset` does not stop BGP real-time debug. The debug output can show various events, such as incoming connections, state changes (e.g., Connect, OpenSent, OpenConfirm, Established), and error messages (e.g., "Bad Remote-AS", "No route to host").

### Troubleshooting Scenario 1—No Active Route

In this scenario, the local FortiGate cannot establish a BGP session with a neighbor because there is no active route to the neighbor's IP address in the routing table.

**Symptoms**:
*   `get router info bgp summary` shows the neighbor state as `Active`.
*   `get router info bgp neighbors` also shows the BGP state as `Active`.
*   Real-time BGP debug (`diagnose ip router bgp all enable`) might show a message like `Sock Status: 113-No route to host`.

**Solution**:
*   Ensure that there is an active route in the FortiOS forwarding information base (FIB) to the IP address of the BGP neighbor. This might involve configuring a static route or ensuring that a dynamic routing protocol is advertising a path to the neighbor's IP.

### BGP Neighbor Establishment

The establishment of a BGP neighbor relationship involves the exchange of several BGP messages after the underlying TCP connection on port 179 is established. The key states involved are `Connect`, `OpenSent`, `OpenConfirm`, and `Established`.

**Process and Debug Output Examples**:

1.  **Connect**: The local router initiates a TCP connection to the neighbor. Debug output might show `[FSM] State: Connect Event: 14`.
2.  **OpenSent**: Once the TCP connection is established, the local router sends an OPEN message to the neighbor, advertising its BGP capabilities (e.g., graceful restart). Debug output shows the encoding of the OPEN message and the transition to `State: OpenSent Event: 19`.
3.  **OpenConfirm**: The local router receives an OPEN message from the neighbor and responds with a KEEPALIVE message. Upon receiving a KEEPALIVE from the neighbor, the state transitions to `State: OpenConfirm Event: 26`.
4.  **Established**: After both peers have exchanged OPEN and KEEPALIVE messages, the BGP session is established, and they can begin exchanging routing updates. Debug output shows the transition to `State: Established Event: 26` and might include log messages indicating the neighbor is now up (`BGP: %BGP-5-ADJCHANGE: ... Up`). Subsequently, the debug might also show the reception of prefixes from the neighbor.

### Restart BGP

You can restart BGP sessions on a FortiGate using the `execute router clear bgp` command. The following options are available:

*   `all`: Clears all BGP peers, tearing down all BGP sessions and restarting the BGP process, requiring peering to be re-established.
*   `<neighbor_ip>`: Clears the BGP session with the specified neighbor.
*   `as <as_number>`: Clears all BGP peers within the specified AS.
*   `soft [in|out]`: Performs a **soft reset**, which forces both peers to exchange their complete BGP routing tables without tearing down the TCP connection. `soft in` applies new inbound policies, and `soft out` applies new outbound policies.
*   Other options like `dampening`, `external`, `flap-statistics`, `ipv6`.

Using `execute router clear bgp all` resets the BGP process and requires FortiGate to re-establish BGP peering. Soft resets are less disruptive as they don't interrupt the TCP connection.

### Troubleshooting Scenario 2—Prefix Not Received

In this scenario, a BGP peer is advertising a prefix, but the local FortiGate is not receiving it.

**Diagnosis**:
*   Use `get router info bgp summary` and `get router info bgp neighbors` to confirm the BGP session is established.
*   Use `get router info bgp neighbors <neighbor_ip> route` on the advertising peer to verify it is indeed advertising the prefix with the correct attributes.
*   Use `get router info bgp neighbors <local_fortigate_ip> route` on the advertising peer to see if the local FortiGate is listed as a neighbor and what routes are being sent to it.
*   Use `get router info bgp network` on the local FortiGate to see what prefixes it has learned from all neighbors.
*   Check the subnet mask configuration on the advertising peer for the network being advertised. A misconfigured subnet mask can prevent FortiOS from advertising the network. In the example, FGT-B had a `/16` mask configured for a `/24` local subnet, causing it not to advertise the more specific `/24` network.

**Solution**: Ensure the prefix being advertised accurately reflects the actual network configuration on the advertising peer.

### Prefix Not Received—Solution 1

One solution to the "Prefix Not Received" scenario (as seen in Troubleshooting Scenario 2) is to **correct the configuration on the advertising router so that the advertised prefix accurately matches the network it intends to announce**.

In the example, the subnet mask configured for the network being advertised on FGT-B was `/16` (`255.255.0.0`), while the actual subnet assigned to the interface was `/24` (`255.255.255.0`). FortiOS, in this case, did not advertise the more specific `/24` network because of this mismatch.

**The recommended solution is to modify the prefix configuration on the advertising router (FGT-B) to use the correct subnet mask (`255.255.255.0`) to represent the actual network assigned to its interface**. After this change, FGT-B will correctly advertise the `/24` prefix, and FGT-A should receive it.

### Prefix Not Received—Solution 2

Another (less recommended) way to potentially address the "Prefix Not Received" issue, especially if there's a mismatch in how networks are being advertised versus configured, might involve **adjusting filtering rules or policies** between the BGP peers [Not directly exemplified as a solution in the scenario, but a general BGP concept].

For instance, if there were inbound or outbound prefix lists or route maps configured on either the advertising or receiving router that were unintentionally filtering the specific prefix, modifying these filters could allow the prefix to be advertised and received. However, **the primary and more correct approach is to ensure the advertised prefix itself is accurate**, as described in Solution 1. Incorrect filtering rules should be investigated and corrected if they are the cause of a prefix not being received.

### Troubleshooting Scenario 3—Prefix Not Accepted

In this scenario, a BGP peer is advertising a prefix, the local FortiGate is receiving it, but it's not being accepted into the local BGP routing table as the best path or even a valid path.

**Possible Causes**:
*   **Incorrect Remote AS**: The receiving router might be expecting a different remote AS number for the advertised routes.
*   **Filtering Policies**: Inbound prefix lists or route maps on the receiving router might be configured to deny the advertised prefix based on its network address or attributes. In the example, a prefix list named "public" was configured to deny the specific route `8.8.8.8/32`.
*   **BGP Attributes**: Certain BGP attributes of the received route might be considered less desirable according to the local router's policies, causing it to prefer other paths.

**Diagnosis**:
*   Use `get router info bgp summary` and `get router info bgp neighbors` to ensure the session is established.
*   Use `get router info bgp neighbors <neighbor_ip> route` on the receiving router to see the prefixes being advertised by the peer. Check the attributes of these routes.
*   Use `get router info bgp network` on the receiving router to see all learned routes and their status (e.g., valid, best).
*   Examine the BGP configuration of the receiving router for any inbound filtering policies (prefix lists, route maps) applied to the neighbor from which the prefix is expected.

### Prefix Not Accepted—Solution

The solution to a "Prefix Not Accepted" scenario involves **identifying and correcting the reason why the receiving router is not accepting the advertised prefix**. This could include:

*   **Correcting the Remote AS**: If a "Bad Peer AS" error is seen during neighbor establishment or in debug output, ensure the `remote-as` configured on both peers is accurate.
*   **Modifying Filtering Policies**: If inbound prefix lists or route maps are denying the prefix, review their rules and adjust them to permit the desired prefix. In the example, to allow the `8.8.8.8/32` route, the prefix list "public" would need to be modified or removed from the neighbor configuration.
*   **Adjusting BGP Attributes**: If the attributes of the received route are causing it to be considered less desirable, you might need to influence these attributes on the advertising router or configure local policies on the receiving router (e.g., using route maps to set local preference).

In the provided example, the solution involved reviewing the prefix list "public" applied to the neighbor `100.64.2.254` and noting that it had a rule to deny the prefix `8.8.8.8 255.255.255.255`. The solution would be to either remove this rule or the entire prefix list if it was the reason for the prefix not being accepted.
