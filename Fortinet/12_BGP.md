## BGP Overview
**BGP (Border Gateway Protocol) is the protocol <ins>underlying</ins> the global routing system of the internet**

By default, **FortiGate BGP does not advertise any prefixes**. You need to explicitly configure FortiGate to advertise prefixes using either the **redistribution command** or the **network command**.
## Protocol Redistribution
Protocol redistribution allows you to advertise routes learned from non-BGP routing protocols (like connected, static, OSPF, RIP, IS-IS) into BGP
```bash
config router bgp
    config redistribute "ospf"
        set status enable
        set route-map "ospf-to-bgp"
    end
end
```
To verify redistribution
```bash
get router info bgp network
get router info bgp neighbors
```