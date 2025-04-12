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

Let's delve into a comparison of IKEv1 and IKEv2 based on the information in your sources.

### **IKEv1 and IKEv2 Comparison**

IKEv1 and IKEv2 are **incompatible protocols** designed to achieve the same goal of key exchange and Security Association (SA) management for IPsec, but they do so in different ways. Although they can both run over the same UDP port due to some commonalities in their header format, they cannot interoperate. While the core functionalities of IKEv1 are spread across multiple RFC documents, **IKEv2 consolidates many of these functionalities**, including NAT-T, mode-cfg, EAP, and DPD, into a single main RFC.

### **IKEv1—An Outdated Version**

IKEv1 is considered an **outdated version**. Its **development ceased over a decade ago**, and it has been **deprecated and moved to historic status**. Several of its RFC specifications, such as RFC2409, RFC2408, and RFC2407, were made obsolete in December 2005\. Using unmaintained code like IKEv1 can lead to **security vulnerabilities** and potential use in packet amplification attacks. Furthermore, IKEv1 relies on **outdated algorithms** like RC5, IDEA, CAST, and Blowfish. Some widely used functionalities of IKEv1 never reached standard status and remained in draft state, and **IKEv1 lacks a standard RFC for fragmentation**.

### **Reasons to Continue Using IKEv1**

Despite being outdated, there are still reasons why IKEv1 might continue to be used. These include:

* **RADIUS or LDAP authentication for a FortiGate acting as a dial-up client**: FortiOS lacks a native EAP client, preventing it from directly authenticating against RADIUS or LDAP servers. In such scenarios, **IKEv1 must be used**.  
* **Multiple stages of authentication**: While IKEv2 can address this, it requires multiple authentication exchanges or EAP chaining with tunnel-based EAP (TEAP). IKEv1 offers a more established solution for this in certain dial-up user scenarios where both IPsec endpoints and the user need separate authentication.  
* **Long history in FortiOS**: With over 20 years of use in FortiOS, IKEv1 has benefited from numerous fixes and optimizations.  
* **Wide usage in multiple platforms**: IKEv1 is still prevalent across various platforms.

### **IKEv2 Overview**

IKEv2 is the **incompatible successor to IKEv1**. It was introduced over 15 years ago. Key specifications for IKEv2 are found in RFC 4306 (2005), RFC 5996 (2010), and RFC 7296 (2014). Unlike IKEv1, where core and additional functionalities are defined in separate RFCs, **IKEv2's main RFC covers many essential aspects in a single document**, simplifying implementation and understanding.

### **IKEv2 Advantages**

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

### **Summary of Versions**

Here's a summary of the key differences between IKEv1 and IKEv2 based on your source:

| Feature | IKEv1 | IKEv2 |
| ----- | ----- | ----- |
| **Exchange Modes** | Main (9 messages), Aggressive (6 messages) | One procedure only (4 messages for one child SA) |
| **Authentication Methods** | Symmetric | Asymmetric |
| **NAT-T** | Supported as extension (RFC 3947, RFC 3948\) | Built-in feature |
| **Reliability** | Unreliable—messages are not acknowledged | Reliable—messages are acknowledged |
| **Dial-up Phase 1 Matching by ID** | Peer ID, Peer ID \+ aggressive mode \+ PSK, Peer ID \+ main mode \+ certificate signature | Peer ID, Network ID |
| **Traffic Selector Flexibility** | Not supported | Supported |

### **IKEv2 Exchange Process**

The IKEv2 exchange process is used to negotiate an IPsec tunnel. Unlike IKEv1, IKEv2 is a **reliable "request and response" protocol**. The initiator will retransmit a request until it gets a response or determines the IKE SA has failed. While IKEv1 has distinct phase 1 (6 packets) and phase 2 (3 packets) exchanges, **IKEv2's exchange is more flexible**, ranging from as few as four packets to potentially 30, depending on the authentication complexity. After the initial exchange, subsequent traffic triggers the **CREATE\_CHILD\_SA exchange**, which is similar to IKEv1's phase 2\. **IKEv2 does not have aggressive or main modes**.

### **IKEv2—A Request and Response Protocol**

As mentioned, IKEv2 operates as a **request and response protocol**. It involves **two initial phases of negotiation**:

* **IKE\_SA\_INIT exchange**: This is the first round trip and negotiates the security settings for protecting subsequent IKE traffic and establishes initial keying material. It also enables DoS protection using a cookie mechanism. This exchange typically takes one round trip but can extend to two or three if the responder requests another key exchange or if DoS protection starts.  
* **IKE\_AUTH exchange**: This is the final stage of the initial exchange and occurs after IKE\_SA\_INIT. It is protected by the algorithms and keys established in the first phase. During this phase, the peers exchange their identities (IDi and IDr) and provide proof of their identity (AUTH). When EAP is not used, it's a single request and response. A **piggyback child (IPsec) SA is usually negotiated** along with the IKEv2 SA during this exchange.

Following these initial exchanges are later IKEv2 exchanges, including the **CREATE\_CHILD\_SA exchange** and the **Informational exchange**.

### **IKEv2 Negotiation Steps**

Although IKEv2 doesn't strictly use the terms "phase 1" and "phase 2," the FortiOS CLI and GUI often use this terminology for configuration. **Phase 1 settings configure the IKEv2 SA, while phase 2 settings configure the child (IPsec) SA**. The four main IKEv2 exchanges are:

* **IKE\_SA\_INIT**: Negotiates security settings for IKE traffic and enables DoS protection.  
* **IKE\_AUTH**: Performs mutual authentication, configures settings (like IP/mask, DNS), and can set up a piggyback child SA, negotiating IP flow and security settings for the IPsec SA.  
* **CREATE\_CHILD\_SA**: Creates new child SAs or rekeys existing ones, and can also rekey the IKE SA.  
* **INFORMATIONAL**: Conveys control messages, errors, or notifications between IKE endpoints after the initial exchanges.

### **IKEv2 Exchange Process—IKE\_SA\_INIT**

The **IKE\_SA\_INIT exchange** is the initial round trip in IKEv2 communication. The initiator formulates the first request, including its SPI (initiator security parameter index, which can act as a cookie for DoS protection), its proposed security protocols and algorithms, and a Diffie-Hellman public value along with a nonce. The responder then chooses a proposal, selects its Diffie-Hellman key pair, calculates the Diffie-Hellman shared secret and a nonce, and prepares its response, including its own SPI (responder SPI). This exchange establishes the initial IKE security association and the shared secret used to protect subsequent IKEv2 messages.

### **IKEv2 Exchange Process—IKE\_AUTH**

The **IKE\_AUTH exchange** follows the IKE\_SA\_INIT and completes the initial negotiation. It's protected by the cryptographic algorithms and keys agreed upon in the IKE\_SA\_INIT exchange. During this phase, the initiator sends its identity (IDi), authentication data (AUTH), and parameters for the initial child SA. The responder authenticates the initiator, accepts the child SA proposal, installs traffic protection based on the negotiated SAs, and sends its own identity (IDr), authentication data, and child SA parameters. If EAP is used, this exchange can involve multiple request and response rounds depending on the EAP method. By default, a child (IPsec) SA is negotiated during this phase.

### **IKEv2 Exchange Process—CREATE\_CHILD\_SA**

The **CREATE\_CHILD\_SA exchange** is used to establish new child SAs or to rekey existing ones after the initial IKE SA is established. Either endpoint can initiate this exchange. It involves a request to rekey an SPI, potentially a new Diffie-Hellman key exchange, and the exchange of new nonces and child SA parameters. Both sides then generate new keying material and install the new SAs, initiating IPsec SA protection with the new keys. In IKEv1, this was analogous to the phase 2 exchange.

### **IKEv2 Exchange Process—Informational**

The **Informational exchange** is used to convey control messages related to the IKE SA, such as errors or notifications of certain events. These exchanges occur only after the initial IKE\_SA\_INIT and IKE\_AUTH exchanges are complete and are **cryptographically protected** using the negotiated keys. Examples in the debug output show informational messages being sent and received, sometimes related to the deletion of an IKE SA.

### **Monitor and Debug IKEv2**

The commands used to **monitor, debug, and troubleshoot IKEv2 are the same as those used for IKEv1**.

* `diagnose vpn ike gateway list`: Provides details about IKE gateways (tunnels).  
* `diagnose vpn ike gateway clear <name>`: Closes a phase 1 connection (IKE SA), which can be used to force renegotiation during troubleshooting. Use with caution.  
* `diagnose vpn tunnel list`: Displays current IPsec SA information for all active tunnels.  
* `diagnose vpn ike log filter`: Allows filtering the IKE debug output based on various parameters like remote gateway IP address (`rem-addr4`). You can list the current filter using `diagnose vpn ike log filter list` and clear it with `diagnose vpn ike log filter clear`.  
* `diagnose debug application ike <bitmask>`: Enables real-time IKE debug output. A bitmask of **\-1 enables all outputs**.  
* `diagnose debug enable`: Must be enabled to see debug output.  
* `diagnose debug console timestamp enable`: Enables timestamps in the debug output, useful for troubleshooting.  
* `diagnose debug disable`: Disables debug output.  
* `diagnose debug reset`: Disables all diagnose debug applications.

### **IKEv2 Commands to Monitor, Debug, and Troubleshoot**

As listed above, the primary commands are `diagnose vpn ike gateway list`, `diagnose vpn ike gateway clear`, `diagnose vpn tunnel list`, `diagnose vpn ike log filter rem-addr4 <remote gateway IPv4>`, and `diagnose debug application ike -1` followed by `diagnose debug enable`.

### **IKEv2 Debug Output**

Analyzing the debug output after enabling it with `diagnose debug application ike -1` and `diagnose debug enable` allows you to follow the IKEv2 negotiation process.

* **IKE\_SA\_INIT exchange**: The debug shows the **SA\_INIT message being sent by the initiator** and the **SA\_INIT\_RESPONSE being received**. This includes the exchange of SPIs, proposed protocols, Diffie-Hellman values, and nonces. You can also observe notifications like NAT detection and fragmentation support. The establishment of the initial IKE SA and the generation of initial secret keys (SK\_ar) are also visible.  
* **IKE\_AUTH exchange**: After a successful SA\_INIT, the debug shows the initiator **preparing and sending the AUTH message**, which includes its identity and authentication data. It then shows the **AUTH\_RESPONSE being received** from the peer. The output includes decryption of the received message, verification of the peer's identity, successful authentication, and the establishment of the IKE SA. Notifications like MESSAGE\_ID\_SYNC\_SUPPORTED might also appear. The IKE SA operational status is set to "up".  
* **CREATE\_CHILD\_SA exchange**: Following the initial exchanges, if a child SA (IPsec SA) needs to be established or rekeyed (as often happens immediately), the debug output shows the negotiation of traffic selectors (TSi and TSr). It displays the **proposals for the child SA**, including protocol (ESP), encapsulation (TUNNEL), encryption algorithms (like 3DES\_CBC in the example), and authentication algorithms. The output indicates whether the proposals are matched and accepted. Finally, it shows the establishment of the IPsec SA with its SPIs and the configured source and destination traffic selectors. SNMP tunnel up traps might also be sent.

By examining these debug outputs, you can gain detailed insights into each step of the IKEv2 negotiation and identify potential issues by looking for mismatches in proposals, authentication failures, or errors during SA creation.