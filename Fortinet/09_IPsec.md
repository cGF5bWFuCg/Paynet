# 09 - IPsec
## Monitor IPsec VPN Tunnels
```bash
get vpn ipsec tunnel summary
```
Provides summarized information about VPNs, including their status, selectors, and traffic statistics
```bash
get ipsec tunnel list
```
Shows a list of active IPsec tunnels with their remote gateway, proxy IDs, status, and timeout values
### IPsec SA Management
IKE negotiates two distinct SA types in two phases: Phase 1 negotiates the IKE SA, which sets up a secure channel, and Phase 2 negotiates the IPsec SA, which is used for encrypting and decrypting data. SAs have a lifetime and must be renegotiated.
```bash
diagnose vpn tunnel ?
```
Offers options to manage VPN tunnels, including ```down``` (shut down), ```up```(activate), ```list``` (list all tunnels), and ```flush``` (flush tunnel SAs).
### IPsec SA
```bash
diagnose vpn tunnel list
```
Displays the current IPsec Security Association (SA) information for all active tunnels.
```bash
diagnose vpn tunnel list name <tunnel name>
```
Shows SA information for a specific tunnel.<br />
The output includes details like the tunnel name, versions, serial numbers, local and remote gateways, bound interface, mode, encapsulation, options, proxy ID numbers, child SAs, reference counts, last sent and received timestamps, auto-discovery status, traffic statistics, DPD information, NAT-T status, and SA details such as SPIs, encryption and authentication algorithms, and key information. The ```npu_flag``` field indicates the hardware offloading status of the IPsec SAs.
### IPsec Tunnel Details
```bash
get vpn ipsec tunnel details
```
Provides detailed information about active IPsec tunnels. <br />The output includes the tunnel name, type, local and remote gateways, mode (IKE version), interface, traffic counters (packets and bytes sent/received, errors), DPD status, phase 2 selectors (source and destination addresses/ports/protocols), SA lifetime/rekey values, MTU, replay status, and the negotiated encryption, authentication, and keys for both inbound and outbound SAs.
### IKE Gateway List
```bash
diagnose vpn ike gateway list
```
Provides details about IKE gateways (phase 1 of the VPN connection). 
```bash
diagnose vpn ike gateway list name <tunnel name> 
```
Shows information for a specific tunnel, including the virtual domain, name, version, interface, local and remote addresses and ports, creation time, auto-discovery status, IKE and IPsec SA creation and establishment times, IDs/SPIs, direction (initiator/responder), status, negotiated proposal, key, lifetime/rekey values, and DPD statistics. 
```bash
diagnose vpn ike gateway clear <name>
``` 
Closes a phase 1 connection and should be used with caution as clearing without a name affects all VDOMs.
### Additional IPsec Debug Commands
```bash
get vpn ipsec stats tunnel
```
Provides global counters related to all active VPNs, including the total number of tunnels (static/DDNS, dynamic, manual), errors, and the total and up counts of selectors.
## Debug an IPsec VPN Connection
```bash
diagnose debug application ike <bitmask> 
diagnose debug enable
```
The IKE daemon handles all IPsec connections. To enable real-time debug for IKE.
A bitmask of -1 is recommended to enable all outputs, which includes DPD packets and negotiation information. 
```bash
diagnose debug console timestamp enable
```
Enabling timestamps is also helpful. 
```bash
diagnose debug application ike 0
diagnose debug disable
diagnose debug reset
```
Remember to disable all debug applications after troubleshooting.
### IKE Filter Options
```bash
diagnose vpn ike log filter
```
Allows you to set filters for the IKE real-time debug output to focus on relevant information. Common filter options include ```rem-addr4``` (filter by remote gateway IPv4 address), ```mdst-addr6``` (multiple IPv6 remote gateway addresses), ```dst-port```, vd (virtual domain), ```interface```, and negate. 
```bash
diagnose vpn ike log filter clear
```
Remove any set filters.
### IKE Real-Time Debug
```bash
diagnose debug enable
diagnose debug disable
diagnose debug application ike -1
diagnose debug console timestamp enable
.
.
.
diagnose debug disable
```
It displays messages exchanged between peers, negotiated settings, and any errors encountered. The bitmask in the # diagnose debug application ike <bitmask> command controls the level of detail in the output, with -1 enabling the most verbose logging, including major errors (1), configuration changes (2), connection attempts (4), negotiation messages (8), NAT-T messages (16), DPD messages (32), encryption and decryption keys (64), and encrypted traffic payload (128).
## IPsec Traffic and Hardware Offload
```bash
config vpn ipsec phase1-interface
  edit <tunnel_name>
    set npu-offload enable | disable
  next
end
```
You can enable or disable NPU offload for a specific IPsec tunnel interface using the CLI command.
```bash
diagnose vpn tunnel list name <tunnel name>
```
Each IPsec SA has an `npu_flag` field indicating its offloading status. The npu_flag values can indicate if <ins>both inbound and outbound SAs</ins> are loaded to the <ins>kernel</ins> `(00)`, if only the <ins>outbound SA</ins> is copied to the <ins>NPU</ins> `(01)`, if only the <ins>inbound SA</ins> is copied to the <ins>NPU</ins> `(02)`, or if <ins>both</ins> are copied to the <ins>NPU</ins> `(03)`. The session table also includes this field for IPsec traffic.
## Hardware Offloading Statistics
```bash
diagnose vpn ipsec status
```
## IPsec Troubleshooting
Troubleshooting IPsec involves a systematic approach to identify where the connection process fails. Key steps include: 
 + Verifying <ins>configurations</ins> on both peers, 
 + Checking the <ins>internet</ins> connection, 
 + Examining <ins>debug outputs</ins>,
 + Ensuring traffic matches the defined selectors and <ins>firewall policies</ins>.<br /> 

Common problems include:
 + <ins>Encryption mismatches</ins>, 
 + <ins>Authentication failures</ins> (e.g., <ins>pre-shared</ins> key mismatch), 
 + Incorrect phase 1 or 2 <ins>settings</ins>, 
 + <ins>NAT</ins> interference, 
 + <ins>Blocked ESP</ins> packets by intermediate devices, 
 + <ins>Quick mode</ins> selector mismatches, 
 + <ins>Routing</ins> issues, 
 + Firewall <ins>policy</ins> misconfigurations.

### Debug Flow of Tunnel Traffic
```bash
diagnose debug flow
```
The debug flow tool is crucial for troubleshooting traffic that is not passing through an <ins>established</ins> VPN tunne
```bash
diagnose debug flow trace start <number_of_packets>
diagnose debug enable
```
The output shows the packet details, <ins>route lookups</ins>, <ins>firewall policy</ins> checks, and whether the <ins>traffic enters the IPsec interface for encryption</ins> or if it is dropped. You can filter the debug flow by <ins>source/destination IP addresses, protocols,</ins> and <ins>ports</ins>.
### Capturing IKE Traffic
```bash
diagnose sniffer packet <interface> 'host <remote-gw> and udp port 500'
```
To capture IKE traffic (UDP port 500)
```bash
diagnose sniffer packet any 'host <remote-gw> and (udp port 500 or udp port 4500)'
```
If <ins>NAT-T</ins> is involved (using UDP port 4500)

```bash
diagnose sniffer packet any 'host <remote-gw> and esp'
```
To capture ESP traffic (IP protocol 50)
### Common IPsec Problems
| Problem                                      | Output of IKE debug                                               | Common causes                                | Common solutions                                              |
|----------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------|----------------------------------------------------------------|
| Tunnel is not coming up                      | Error: negotiation failure                                        | IPsec configuration mismatch                  | Verify phase 1 and phase 2 configurations between both peers   |
|                                              | Error: no SA proposal chosen                                      | IPsec configuration mismatch                  | Verify phase 1 and phase 2 configurations between both peers   |
| Tunnel is unstable                           | DPD packet lost                                                   | ISP issue                                     | Check internet connection                                     |
| Tunnel is up but traffic doesn’t pass through it | Error in debug flow: no matching IPsec selector, drop             | Quick mode selectors mismatch                 | Verify quick mode selectors are correct                        |
|                                              |                                                                   | NAT is enabled                                | Disable NAT on the VPN firewall policy                         |
|                                              | Routing issue                                                     | Route missing or pointing to wrong device     | Verify route is correctly defined                              |