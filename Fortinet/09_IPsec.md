# 06 - IPsec
### Monitoring IPsec VPN Tunnels
```
get vpn ipsec tunnel summary
```
Provides summarized information about VPNs, including their status, selectors, and traffic statistics
```
get ipsec tunnel list
```
Shows a list of active IPsec tunnels with their remote gateway, proxy IDs, status, and timeout values

### IPsec SA Management
IKE negotiates two distinct SA types in two phases: Phase 1 negotiates the IKE SA, which sets up a secure channel, and Phase 2 negotiates the IPsec SA, which is used for encrypting and decrypting data. SAs have a lifetime and must be renegotiated.

```
diagnose vpn tunnel ?
```
Offers options to manage VPN tunnels, including ```down``` (shut down), ```up```(activate), ```list``` (list all tunnels), and ```flush``` (flush tunnel SAs).

### IPsec SA
```
diagnose vpn tunnel list
```
Displays the current IPsec Security Association (SA) information for all active tunnels.
```
diagnose vpn tunnel list name <tunnel name>
```
Shows SA information for a specific tunnel.<br />
The output includes details like <mark>the</mark> tunnel name, versions, serial numbers, local and remote gateways, bound interface, mode, encapsulation, options, proxy ID numbers, child SAs, reference counts, last sent and received timestamps, auto-discovery status, traffic statistics, DPD information, NAT-T status, and SA details such as SPIs, encryption and authentication algorithms, and key information. The npu_flag field indicates the hardware offloading status of the IPsec SAs.