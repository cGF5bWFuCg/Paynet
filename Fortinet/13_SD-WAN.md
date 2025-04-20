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
+ If it **<ins>does not match</ins>** any of the rules, there is an implicit rule that the traffic will match. When traffic matches an implicit rule, the **<ins>traffic will be forwarded based on the firewall's own routing</ins>**.

####################
*   **Configuration:**
```bash
config system sdwan config service
```
*   **Evaluation Process:**
    *   SD-WAN rules are **evaluated in descending order**, from top to bottom, and the **first rule that matches the traffic is applied**. This is similar to how firewall policies are evaluated.
    *   If a packet matches a rule's criteria, FortiGate looks for acceptable members in the outgoing interface list of that rule. This list is sorted by preference based on the configured strategy.
    *   If none of the user-defined SD-WAN rules are matched, the **implicit SD-WAN rule** is used.

*   **Implicit SD-WAN Rule:**
    *   The implicit rule is a default rule that is applied if no user-defined rules are matched.
    *   By default, the implicit rule **performs standard routing (FIB lookup)** on the traffic.
    *   In SD-WAN deployments, which often have multiple routes to the same destination (ECMP routes), traffic matching the implicit rule is usually **load balanced** across all available SD-WAN members.
    *   The **load balancing algorithm** for the implicit rule can be configured under `config system sdwan set load-balance-mode` with options like source IP, sessions, spillover, source-destination IP, and volume. This replaces the `v4-ecmp-mode` setting when SD-WAN is enabled.

*   **Strategies for Outgoing Interface Selection:**
    *   SD-WAN rules allow you to define a **strategy** for selecting the preferred egress members or zones. Examples from the sources include:
        *   **Manual:** Administrators manually select the preferred order of outgoing interfaces.
        *   **Best Quality:** The member with the best quality based on a chosen metric (default is latency, but can also be packet loss, jitter, bandwidth, or a link quality index) is preferred. SLA targets are not considered in this strategy.
        *   **Lowest Cost (SLA):** Traffic is steered based on members meeting defined Performance SLA targets.
        *   **Manual with Load Balancing:** Load balances sessions across all alive members in the manual preference list.

*   **Relationship with Other Features:**
    *   **Firewall Policies:** Even if traffic matches an SD-WAN rule and is steered, it **must also be allowed by a corresponding firewall policy**. Firewall policies for SD-WAN should reference SD-WAN **zones**, not individual members directly, for simplified configuration.
    *   **Routing:** SD-WAN rules are policy routes, and regular policy routes have precedence over them. SD-WAN requires a valid route in the Forwarding Information Base (FIB) for a member to be used for steering traffic. This route can be static or dynamic (like BGP).
    *   **Performance SLAs (Health Checks):** SD-WAN rules, especially those using "Best Quality" or "Lowest Cost (SLA)" strategies, rely on the performance metrics (latency, jitter, packet loss) measured by performance SLAs to make traffic steering decisions. A member is considered down by an SD-WAN rule only when *all* of its performance SLAs report it as down.

*   **Monitoring SD-WAN Rule Status:**
    *   The status of SD-WAN rules can be checked using the CLI command `diagnose sys sdwan service4` for IPv4 rules and `diagnose sys sdwan service6` for IPv6 rules. This command shows information like the rule's flags, tie-breaking method, and the status (alive/selected) of its members.
    *   Log messages can be analyzed in FortiAnalyzer to see which SD-WAN rule a particular traffic flow matched. The "SD-WAN Rule Name" and "SD-WAN Quality" columns in the traffic logs are useful for this.

In summary, SD-WAN rules are the core mechanism for implementing a software-defined WAN by allowing granular control over how traffic is routed across available network links based on defined criteria, strategies, and the real-time performance of those links.