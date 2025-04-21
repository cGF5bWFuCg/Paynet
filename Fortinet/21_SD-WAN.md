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
___
## **Performance Service Level Agreements (SLAs)** 

**Monitor the health and performance of SD-WAN members**. 
While configuring them is **<ins>optional**</ins>, it is recommended to ensure that **<ins>members meet the necessary requirements**</ins> for steering traffic effectively.

*   **Purpose and Function**:
    *   They <ins>**monitor the health**</ins> (state: alive or dead) and <ins>**performance (packet loss, latency, and jitter)</ins>** of SD-WAN members. They can also monitor the <ins>**Mean Opinion Score (MOS)** for voice quality.
    *   Performance SLAs can also **<ins>detect situations where an interface is physically up but FortiGate cannot reach the desired destination</ins>**, flagging the link as dead.
*   **Health Check Methods (Probe Modes)**:
    *   **Active:** FortiGate periodically sends probes through the member to monitor its health and performance against configured servers (beacons).
    *   **Passive:** FortiGate monitors the actual network traffic flowing through the member to determine its performance. This requires <ins>**enabling</ins>** `passive-wan-health-measurement` <ins>**in at least one firewall policy</ins>** with an <ins>**SD-WAN zone as source or destination</ins>**. You can also specify the service for passive measurement in the SD-WAN rule.
    *   **Prefer Passive:** FortiGate uses <ins>**passive mode</ins>** first and switches to <ins>**active mode</ins>** if there's no TCP traffic across the member <ins>**for three minutes</ins>**. If there is a TCP Session, change probe too passive mode

*   **Probe Protocols (for Active Monitoring)**:
    *   **General-purpose (IPv4 & IPv6):** Ping (ICMP echo requests), UDP echo (sends UDP requests on port X and expects an identical copy back), TCP connect (uses a full TCP connection to test the link). TWAMP (Two-Way Active Measurement Protocol - client-side implementation on FortiGate). IPv4 only: TCP echo (sends TCP requests on port X and expects a copy back).
    *   **Application-specific (IPv4 & IPv6):** DNS, FTP. IPv4 only: HTTP, HTTPS. IPv6 only: No TCP echo, HTTP, or TWAMP support.

*   **SLA Targets**:
    *   Used by <ins>**Lowest Cost (SLA)**</ins> SD-WAN rules to determine preferred members.
    *   Members that meet one or more SLA targets are preferred for steering traffic in "Lowest Cost (SLA)" rules.
    *   These targets specify acceptable thresholds for metrics such as latency, jitter, and packet loss.

Absolutely! Here's a comprehensive and realistic **SLA target values table** for SD-WAN, specifically tailored to key applications like **Microsoft 365 (including Outlook and Teams)**, **general internet browsing**, and **collaboration tools like Webex**.

These values are great for configuring **Fortinet SD-WAN Performance SLAs** to ensure optimal application performance and user experience.

---

## **SLA Target Table for Fortinet SD-WAN – Typical & Application-Specific**

| **Application / Use Case**   | **Latency (ms)** | **Jitter (ms)** | **Packet Loss (%)** | **Notes** |
|-----------------------------|------------------|------------------|----------------------|----------|
| **General Internet Surfing**| ≤ 250            | ≤ 50             | ≤ 2%                 | Includes browsing, cloud dashboards, non-critical HTTP/S |
| **Microsoft 365 (Office Apps)** | ≤ 150        | ≤ 30             | ≤ 1%                 | Word, Excel, SharePoint, OneDrive online performance depends on region/CDN |
| **Outlook / Exchange Online** | ≤ 120         | ≤ 20             | ≤ 1%                 | Includes mail sync, Outlook online – latency-sensitive |
| **Microsoft Teams – Voice/Video** | ≤ 100     | ≤ 20             | ≤ 1%                 | Real-time traffic; prefer low jitter and consistent path |
| **Webex (Voice/Video)**     | ≤ 150            | ≤ 30             | ≤ 1%                 | Sensitive to jitter, similar to MS Teams |
| **Microsoft Teams – Chat & Collaboration** | ≤ 150 | ≤ 30         | ≤ 1%                 | Less sensitive than audio/video, but important for experience |
| **Cloud-Based SaaS (general)** | ≤ 200         | ≤ 40             | ≤ 1.5%               | Generic guidance for popular cloud apps like Dropbox, Box, Slack |
*   **SLA Map**:
    ```bash
    diagnose sys sdwan health-check status
    ```
    *   The `sla_map` value in the output of indicates whether a member meets the configured SLA targets using a **bitmask representation**.
    *   Each configured SLA target is assigned a bit (first target is bit 0, second is bit 1, etc.).
    *   If a member meets an SLA target, the corresponding bit is set to **1**; otherwise, it's **0**.
    *   The `sla_map` value is the **hexadecimal representation** of this binary number. For example, with two SLA targets, 
        + `0x3` means both are met (11), 
        + `0x2` means the second is met but the first is not (10), 
        + `0x1` means the first is met but the second is not (01),
        + `0x0` means neither is met (00). `0x0` can also mean that no SLA targets are configured.

*   **Integration with SD-WAN Rules**:
    *   SD-WAN rules, particularly those using the **"Lowest Cost (SLA)" strategy**, rely on Performance SLAs and their targets to select the best outgoing interface. Members that meet the configured SLA targets are preferred.
    *   The **"Best Quality" strategy** in SD-WAN rules uses the performance metrics (latency, packet loss, jitter, bandwidth, or a custom link quality index) measured by Performance SLAs to choose the best performing link, without considering SLA targets.
    *   Even with manual SD-WAN rules, configuring Performance SLAs improves the detection of alive or dead members.

*   **Monitoring Member State and Performance**:
    *   **FortiGate CLI:**
```bash
diagnose sys sdwan health-check status <SLA_name>
```
Displays the status of a specific Performance SLA, including the state (alive/dead) and measured metrics (packet loss, latency, jitter, MOS, bandwidth) for each member, as well as the `sla_map`.
```bash
diagnose sys link-monitor interface <interface_name>
```
Shows detailed metrics measured by the link-monitor process for a specific member.
```bash
diagnose sys sdwan sla-log <SLA_name> <member_id>
```
 Displays historical SLA metrics for a specific member over the last 10 minutes. The member ID can be found in the `health-check status` output.
```bash
diagnose sys sdwan intf-sla-log <interface_name>
```
Shows SLA logs per interface.
```bash
diagnose sys sdwan service4
```
Displays the status of IPv4 SD-WAN rules, including the health check used.

*   **Advanced Performance SLA Settings**:
    *   **Warning and Alert Thresholds:** You can configure thresholds for packet loss, latency, and jitter. Exceeding these thresholds can trigger visual notifications in the GUI and generate log messages.
    *   **SLA Fail/Pass Logging:** By default, SLA health-check results are not logged. You can enable logging and set the frequency (in seconds) for generating logs when a member fails (`sla-fail-log-period`) or passes (`sla-pass-log-period`) its SLA targets. These settings are under **Advanced Options** in the Performance SLA configuration.
    *   **Probe Settings:** You can adjust the `probe-timeout` (time to wait for a probe response) and `probe-count` (number of recent probes used for metric calculation).
    *   **DSCP Code:** You can set a DSCP (Differentiated Services Code Point) value for health-check probes, which can be useful when monitoring links that prioritize traffic based on DSCP markings (e.g., some MPLS links).
    *   **Link Cost Factor:** For MOS SLAs, you can set the `link-cost-factor` to `mos`. For latency, there's a `link-cost-factor latency` setting.
    *   **Initial State:** Initially, all configured members are assigned the alive state.

*   **Mean Opinion Score (MOS)**:
    *   Used to measure the perceived quality of voice communication, taking into account latency, jitter, packet loss, and the codec.
    *   The MOS score ranges from 1 (poor) to 5 (very good).
    *   You can configure Performance SLAs with MOS criteria, selecting the MOS codec (G.711, G.729, or G.722 - default is G.711). The chosen codec should match the one used for voice traffic.
    *   A MOS threshold (between 1.0 and 5.0, default 3.6) determines the minimum acceptable voice quality.
    *   MOS-based SLAs can only be used with SD-WAN rules using the **Lowest Cost (SLA)** strategy.

*   **Remote Health Checks and Embedded SLA Information**:
    *   Involves the hub using SLA results provided by the spoke (remote device).
    *   On the spoke, you enable embedding measured health in probes (typically ICMP) using `set embed-measured-health enable`.
    *   On the hub, you set the `detect-mode` to `remote` in the Performance SLA configuration. You can also define priority for IKE routes based on whether the overlay is in SLA (`set priority-in-sla`) or out of SLA (`set priority-out-sla`).
    *   This method is useful with static routing or BGP, especially with loopback topologies, but not compatible with IKE option mode-cfg.

*   **Link Cost and Tie-breaking**:
    *   In "Lowest Cost (SLA)" rules, if multiple members meet the SLA targets, the **member cost** (configured for each member) is used as a tiebreaker (lower cost is preferred).
    *   If members have the same SLA status and cost, the **configuration priority (interface preference order)** is used as the next tiebreaker.
    *   The `service-sla-tie-break` setting in the SD-WAN member configuration allows for different tie-breaking methods when multiple members meet the SLA in "Lowest Cost (SLA)" rules, such as `cfg-order` (configuration order - default), `fib-best-match`, and `input-device`.

*   **Troubleshooting Performance SLAs**:
    *   Use the `diagnose sys sdwan health-check status` command to get a real-time overview of SLA status and metrics.
    *   The `diagnose sys link-monitor interface` command provides similar but more detailed information from the link monitor process.
    *   Analyze SLA pass and fail logs in FortiAnalyzer if logging is enabled.
    *   Check the `sla_map` value to understand which SLA targets are being met.

By configuring and monitoring Performance SLAs, administrators can ensure that SD-WAN traffic is steered across links that meet the required performance criteria for various applications, leading to improved user experience and network reliability.