# SD-WAN
## Underlay & Overlay Network
+ **Underlay:** Physical connections provided by Internet Service Providers (ISPs).
+ **Overlay:** Virtual links that are built on top of the physical underlay links
## Network Quality Parameters
**Congestion,** When we want to send a high volume of internal traffic through the WAN link, we will encounter congestion problems in the WAN link due to lack of bandwidth.

**Delay** 
+ **Transmission Delay,** Which is the time it takes to prepare a packet for transmission over the link.
+ **Propagation Delay,** Which is the time it takes to transfer to a node.
+ **Processing Delay,** Which is the amount of delay in processing information for transmission, and other types of delays, collectively known as Latency.

**Jitter** is the variation in packet arrival time. It is one of the key performance metrics monitors to assess the quality of network links. Along with latency and packet loss, jitter is used to evaluate the health of SD-WAN members.

**Monitoring Packet Loss**
Provides an instant value for packet loss for each SD-WAN member.
```bash
diagnose sys sdwan health-check status
```
## SD-WAN Rules

+ Instruct FortiGate how to <ins>**steer network traffic**</ins> across different WAN links.
+ Service that is used to control the **<ins>Path Selection</ins>** process in the SD-WAN architecture.
+ Unlike firewall policies which determine which traffic is allowed.
+ They use link quality measured by SD-WAN **<ins>health checks</ins>** to steer traffic through the **<ins>best-performing</ins>** link based on **<ins>metrics</ins>** like **<ins>latency, packet loss, or link utilization</ins>**.
+ SD-WAN rules are essentially **<ins>policy routes</ins>.**

*   **Configuration:**
```bash
config system sdwan config service
```
*   **Implicit SD-WAN Rule:**
    *   The implicit rule is a default rule that is applied if no user-defined rules are matched.
    *   By default, the implicit rule **<ins>performs standard routing (FIB lookup)</ins>** on the traffic.

*   **Strategies for Outgoing Interface Selection:**
    *   SD-WAN rules allow you to define a **strategy** for selecting the preferred egress members or zones. Examples from the sources include:
        *   **Manual:** Administrators manually select the preferred order of outgoing interfaces.
        *   **Best Quality:** The member with the best quality based on a chosen metric (default is latency, but can also be packet loss, jitter, bandwidth, or a link quality index) is preferred. **<ins>SLA targets are not considered**<ins> in this strategy.
        *   **Lowest Cost (SLA):** Traffic is steered based on members meeting defined **<ins>Performance SLA targets**<ins>.
        *   **Manual with Load Balancing:** Load balances sessions across all alive members in the manual preference list.

*   **Relationship with Other Features:**
    *   **Firewall Policies:** Even if traffic matches an SD-WAN rule and is steered, it **<ins>must also be allowed by a corresponding firewall policy**<ins>. 
    *   **Routing:** SD-WAN rules are policy routes, and regular policy routes have precedence over them. SD-WAN requires a valid route in the Forwarding Information Base (FIB) for a member to be used for steering traffic. This route can be static or dynamic (like BGP).
    *   **Performance SLAs (Health Checks):** SD-WAN rules, especially those using "Best Quality" or "Lowest Cost (SLA)" strategies, rely on the performance metrics (latency, jitter, packet loss) measured by performance SLAs to make traffic steering decisions. A member is considered down by an SD-WAN rule only when *all* of its performance SLAs report it as down.

*   **Monitoring SD-WAN Rule Status:**

```bash
diagnose sys sdwan service4
``` 
This command shows information like the rule's flags, tie-breaking method, and the status (alive/selected) of its members.
