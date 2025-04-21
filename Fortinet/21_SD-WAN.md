# SD-WAN
## Underlay & Overlay Network
+ **Underlay:** Physical connections provided by Internet Service Providers (ISPs).
+ **Overlay:** Virtual links that are built on top of the physical underlay links
## Network Quality Parameters
**Congestion,** When we want to send a high volume of internal traffic through the WAN link, we will encounter congestion problems in the WAN link due to lack of bandwidth.

**Delay** / **Latency** 
Refers to the time it takes for data to travel from its source to its destination across a network. In networking, latency is typically measured in milliseconds (ms) and represents the delay between a user's action and the response from the network.

- **Propagation Delay**: The time it takes for a signal to travel through the transmission medium (e.g., fiber optic cables).
- **Transmission Delay**: The time required to push all the packet's bits onto the wire.
- **Processing Delay**: The time routers and switches take to process packet headers.
- **Queuing Delay**: The time a packet spends in routing queues due to congestion.

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
### **Application-Specific SLA Targets**

| **Application Category**    | **SLA Sensitivity** | **Latency (ms)**  | **Jitter (ms)** | **Packet Loss (%)** | **General Bandwidth Needs** |
|-----------------------------|---------------------|-------------------|-----------------|---------------------|-----------------------------|
| **Real-Time Communication**  | **Very High**        | ≤ 100             | ≤ 20            | ≤ 0.5%              | High (100 Kbps to several Mbps) |
| **Collaboration Tools**      | **High**             | ≤ 150             | ≤ 30            | ≤ 1%                | Medium (200 Kbps to 2 Mbps)  |
| **Email and Messaging**      | **Moderate**         | ≤ 150             | ≤ 30            | ≤ 1%                | Low (50-250 Kbps per user)  |
| **Office Productivity**      | **Moderate**         | ≤ 150             | ≤ 30            | ≤ 1%                | Medium (500 Kbps to 2 Mbps) |
| **Web Browsing**             | **Low to Moderate**  | ≤ 250             | ≤ 50            | ≤ 2%                | Low (100 Kbps to 512 Kbps) |
| **Cloud/SaaS Applications**  | **High**             | ≤ 150             | ≤ 30            | ≤ 1%                | Medium (500 Kbps to 2 Mbps) |
| **File Transfer and Backup** | **Moderate**         | ≤ 200             | ≤ 50            | ≤ 2%                | Low (500 Kbps to 2 Mbps)   |
| **Video Streaming**          | **Moderate**         | ≤ 200             | ≤ 50            | ≤ 2%                | Low to Medium (500 Kbps to 1.5 Mbps) |
| **ERP/CRM Systems**          | **High**             | ≤ 150             | ≤ 30            | ≤ 1%                | Medium to High (1–5 Mbps)   |
| **IT and Security Services** | **Low**              | ≤ 300+            | ≤ 100+          | ≤ 10%               | Very Low (< 100 Kbps)       |
---
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
```bash
config system sdwan
    config health-check
        edit "NAME"
            set probe-timeout 1000             # 1000ms timeout
            set probe-count 5                  # Average last 5 probes
            set dscp 46                        # DSCP EF (Expedited Forwarding)

            set sla-fail-log-period 60         # Log failure every 60 seconds
            set sla-pass-log-period 300        # Log success every 300 seconds

            set link-cost-factor latency       # Adjust link cost based on latency
            set initial-state enable           # Members start in "alive" state
        next
    end
end
```
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
```bash
# Spoke
set embed-measured-health enable
## Makes the spoke send SLA metrics (loss, latency, jitter) in its tunnel return packets to the hub.
# Hub
set detect-mode remote         # Trust remote SLA info
## The hub doesn’t probe itself — it reads embedded SLA metrics from the tunnel traffic.
# Optional route preference tweaking
set priority-in-sla 10         # Prefer if SLA is healthy
set priority-out-sla 50        # Use lower priority if out of SLA
```
*   **Link Cost and Tie-breaking**:
    *   In "Lowest Cost (SLA)" rules, if multiple members meet the SLA targets, the **member cost** (configured for each member) is used as a tiebreaker (lower cost is preferred).
    *   If members have the same SLA status and cost, the **configuration priority (interface preference order)** is used as the next tiebreaker.
    *   The `service-sla-tie-break` setting in the SD-WAN member configuration allows for different tie-breaking methods when multiple members meet the SLA in "Lowest Cost (SLA)" rules, such as `cfg-order` (configuration order - default), `fib-best-match`, and `input-device`.

*   **Troubleshooting Performance SLAs**:
    
```bash
diagnose sys sdwan health-check status
```
Get a real-time overview of SLA status and metrics.
```bash
diagnose sys link-monitor interface
```
Provides similar but more detailed information from the link monitor process.

+ Analyze SLA pass and fail logs in FortiAnalyzer if logging is enabled.
+ Check the `sla_map` value to understand which SLA targets are being met.

## **Example Configuration: Link State with SLA**

```bash
config system sdwan
    config health-check
        edit "NAME"

            set interval 5000                 # Send probe every 5 seconds
            set failtime 3                    # 3 consecutive failures to mark link dead
            set recoverytime 3                # 3 successful probes to mark it back alive
            set probe-timeout 1000
            set probe-count 5
            set initial-state enable          # Assume link is alive at boot
        next
    end
end
```

### **How This Works (Explained Step-by-Step)**

| Parameter             | Description |
|-----------------------|-------------|
| `interval 5000`       | Probe is sent every 5 seconds |
| `failtime 3`          | Link will be marked **dead** if 3 probes in a row fail (i.e., 15 seconds of failure) |
| `recoverytime 3`      | Link will be marked **alive** again after 3 successful probes in a row |
| `initial-state enable`| Link starts as alive at boot to avoid routing flaps |
| `probe-count 5`       | FortiGate calculates metrics like jitter/loss from the last 5 probes |
---

## **Quality Criteria** 
Refers to the **metric used by the "Best Quality" SD-WAN rule strategy to determine the preferred member for steering traffic**.

*   **Latency (default)**: FortiGate prefers the member with the **lowest latency**.
*   **Jitter**: FortiGate prefers the member with the **lowest jitter**.
*   **Packet Loss**: FortiGate prefers the member with the **lowest packet loss**.
*   **Bandwidth**: This option has three measurement types:
    *   **Inbandwidth (ingress)**: FortiGate prefers the member with the **most available ingress bandwidth**.
    *   **Outbandwidth (egress)**: FortiGate prefers the member with the **most available egress bandwidth**.
    *   **Bibandwidth (bidirectional)**: FortiGate prefers the member with the **most available combined ingress and egress bandwidth**. The available bandwidth is based on the interface settings (`estimated-upstream-bandwidth` and `estimated-downstream-bandwidth`) and current usage; if these settings are not defined, the physical interface speed is used.
*   **Custom-profile-1**: This option allows for a **weight-based calculation** of a **link quality index** using **latency, jitter, packet loss, and bibandwidth**. You can assign weights to each metric to influence the index, and the member with the **lowest link quality index** is preferred. You can assign a weight of 0 to ignore a specific metric in the calculation.