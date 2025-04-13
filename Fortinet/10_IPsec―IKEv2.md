# 10 - IPsec―IKEv2
## IKEv1 and IKEv2 Comparison
| Feature | IKEv1 | IKEv2 |
| ----- | ----- | ----- |
| Exchange Modes | Main (9 messages), Aggressive (6 messages) | One exchange procedure (4 messages for one child SA) |
| Authentication | Symmetric (initiator and responder use the same method) | Asymmetric (initiator and responder can use different methods) |
| NAT-T | Supported as an extension (RFC 3947, 3948\) | Built-in feature |
| Reliability | Unreliable (messages are not acknowledged) | Reliable (messages are acknowledged) |
| Phase 1 Matching | Peer ID, Peer ID \+ aggressive mode \+ PSK, Peer ID \+ main mode \+ certificate signature | Peer ID, Network ID |
| Traffic Selector | Less flexible | More flexible, supports dynamic updates |
| Security | Some algorithms are outdated, IKEv1 aggressive mode exposes peer IDs | Supports stronger encryption (AES-GCM, ChaCha20P) and DH groups (ECP), peer IDs are encrypted |
| Protocol Operation | More complex, multiple RFCs | Simpler, single main RFC (RFC 7296\) |
| Development Status | Development ceased | Actively being worked on |
| Negotiation Messages | More messages, more round trips | Fewer messages, fewer round trips, faster tunnel establishment |
## Reasons to Continue Using IKEv1

Despite being outdated, there are still reasons why IKEv1 might continue to be used. These include:

* **RADIUS or LDAP authentication for a FortiGate acting as a dial-up client**: FortiOS lacks a native EAP client, preventing it from directly authenticating against RADIUS or LDAP servers. In such scenarios, **IKEv1 must be used**.  
* **Multiple stages of authentication**: While IKEv2 can address this, it requires multiple authentication exchanges or EAP chaining with tunnel-based EAP (TEAP). IKEv1 offers a more established solution for this in certain dial-up user scenarios where both IPsec endpoints and the user need separate authentication.  
* **Long history in FortiOS**: With over 20 years of use in FortiOS, IKEv1 has benefited from numerous fixes and optimizations.  
* **Wide usage in multiple platforms**: IKEv1 is still prevalent across various platforms.
## IKEv2 Advantages

Transitioning to IKEv2 offers several advantages:

* **Actively developed**: IKEv2 is under active development by the IPsec Maintenance and Extensions (ipsecme) working group, ensuring ongoing improvements and security updates.  
* **Fewer messages for negotiation**: IKEv2 requires fewer messages (as few as four in the initial exchange), leading to **decreased latency** during tunnel establishment. It allows for a child SA to be set up within this initial exchange.  
* **Reliable protocol**: IKEv2 is a **reliable request and response protocol**, where the initiator retransmits requests until a response is received or the IKE SA is considered failed.  
* **Standardized fragmentation**: Fragmentation negotiation starts with the first message, and it has a **configurable MTU**.  
* **DoS protection**: IKEv2 includes built-in mechanisms for **denial-of-service (DoS) protection**.  
* **More accurate rekey logic**: The rekey logic for both IKE and IPsec SAs is more precisely defined in IKEv2 compared to IKEv1.  
* **Simplified cryptographic syntax**: The method for protecting IKE messages is based closely on ESP, simplifying implementation and security analysis.  
* **Standard EAP authentication**: IKEv2 uses **standard EAP authentication methods**.  
* **Asymmetric authentication**: IKEv2 supports **asymmetric authentication**, allowing the initiator and responder to use different methods.  
* **Traffic selector flexibility**: IKEv2 offers more flexibility in defining traffic selectors, allowing specification of the payload type for each selector. It also supports dynamic updates to traffic selectors.  
* **Matching dial-up phase 1 by ID**: IKEv2 allows matching dial-up phase 1 by ID, replacing the less secure method used in IKEv1's aggressive mode with pre-shared keys.  
* **IKE SA session resumption**: IKEv2 supports session resumption as defined in RFC 5723\.  
* **Quick crash detection**: IKEv2 includes a quick crash detection method (RFC 6290\) for interoperability with other vendors.  
* **Overlay network ID support**: IKEv2 supports setups with an overlay network ID.  
* **NAT-T as a built-in feature**: **NAT-T is natively supported in IKEv2**, unlike IKEv1 where it was added as an extension.
## Summary of Versions

Here's a summary of the key differences between IKEv1 and IKEv2 based on your source:

| Feature | IKEv1 | IKEv2 |
| ----- | ----- | ----- |
| **Exchange Modes** | Main (9 messages), Aggressive (6 messages) | One procedure only (4 messages for one child SA) |
| **Authentication Methods** | Symmetric | Asymmetric |
| **NAT-T** | Supported as extension (RFC 3947, RFC 3948\) | Built-in feature |
| **Reliability** | Unreliable—messages are not acknowledged | Reliable—messages are acknowledged |
| **Dial-up Phase 1 Matching by ID** | Peer ID, Peer ID \+ aggressive mode \+ PSK, Peer ID \+ main mode \+ certificate signature | Peer ID, Network ID |
| **Traffic Selector Flexibility** | Not supported | Supported |

## IKEv2 Exchange Process

The IKEv2 exchange process is used to negotiate an IPsec tunnel. Unlike IKEv1, IKEv2 is a **reliable "request and response" protocol**. The initiator will retransmit a request until it gets a response or determines the IKE SA has failed. While IKEv1 has distinct phase 1 (6 packets) and phase 2 (3 packets) exchanges, **IKEv2's exchange is more flexible**, ranging from as few as four packets to potentially 30, depending on the authentication complexity. After the initial exchange, subsequent traffic triggers the **CREATE\_CHILD\_SA exchange**, which is similar to IKEv1's phase 2\. **IKEv2 does not have aggressive or main modes**.

## IKEv2—A Request and Response Protocol

As mentioned, IKEv2 operates as a **request and response protocol**. It involves **two initial phases of negotiation**:

* **IKE\_SA\_INIT exchange**: This is the first round trip and negotiates the security settings for protecting subsequent IKE traffic and establishes initial keying material. It also enables DoS protection using a cookie mechanism. This exchange typically takes one round trip but can extend to two or three if the responder requests another key exchange or if DoS protection starts.  
* **IKE\_AUTH exchange**: This is the final stage of the initial exchange and occurs after IKE\_SA\_INIT. It is protected by the algorithms and keys established in the first phase. During this phase, the peers exchange their identities (IDi and IDr) and provide proof of their identity (AUTH). When EAP is not used, it's a single request and response. A **piggyback child (IPsec) SA is usually negotiated** along with the IKEv2 SA during this exchange.

Following these initial exchanges are later IKEv2 exchanges, including the **CREATE\_CHILD\_SA exchange** and the **Informational exchange**.

## IKEv2 Negotiation Steps

Although IKEv2 doesn't strictly use the terms "phase 1" and "phase 2," the FortiOS CLI and GUI often use this terminology for configuration. **Phase 1 settings configure the IKEv2 SA, while phase 2 settings configure the child (IPsec) SA**. The four main IKEv2 exchanges are:

* **IKE\_SA\_INIT**: Negotiates security settings for IKE traffic and enables DoS protection.  
* **IKE\_AUTH**: Performs mutual authentication, configures settings (like IP/mask, DNS), and can set up a piggyback child SA, negotiating IP flow and security settings for the IPsec SA.  
* **CREATE\_CHILD\_SA**: Creates new child SAs or rekeys existing ones, and can also rekey the IKE SA.  
* **INFORMATIONAL**: Conveys control messages, errors, or notifications between IKE endpoints after the initial exchanges.

# Monitor and Debug IKEv2

The commands used to **monitor, debug, and troubleshoot IKEv2 are the same as those used for IKEv1**.
```bash
diagnose vpn ike gateway list
```
Provides details about IKE gateways (tunnels).
⭕🔴
```bash
diagnose vpn ike gateway clear <name>
```
Closes a phase 1 connection (IKE SA), which can be used to force renegotiation during troubleshooting. Use with caution.  
```bash
diagnose vpn tunnel list
```
Displays current IPsec SA information for all active tunnels.  
```bash
diagnose vpn ike log filter
```
Allows filtering the IKE debug output based on various parameters like remote gateway IP address (`rem-addr4`). You can list the current filter using `diagnose vpn ike log filter list` and clear it with `diagnose vpn ike log filter clear`.  
```bash
diagnose debug application ike <bitmask>
```
Enables real-time IKE debug output. A bitmask of **\-1 enables all outputs**.  
```bash
diagnose debug enable
```
Must be enabled to see debug output.  
```bash
diagnose debug console timestamp enable
```
Enables timestamps in the debug output, useful for troubleshooting.  
```bash
diagnose debug disable
```
Disables debug output.  
```bash
diagnose debug reset
```
Disables all diagnose debug applications.
