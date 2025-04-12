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
