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