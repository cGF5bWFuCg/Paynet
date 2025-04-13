## BGP Overview
**BGP (Border Gateway Protocol) is the protocol <ins>underlying</ins> the global routing system of the internet**

By default, **FortiGate BGP does not advertise any prefixes**. You need to explicitly configure FortiGate to advertise prefixes using either the **redistribution command** or the **network command**.
## Protocol Redistribution
Protocol redistribution allows you to advertise routes learned from non-BGP routing protocols (like connected, static, OSPF, RIP, IS-IS) into BGP.<br />
By default, FortiGate BGP doesn't advertise prefixes from other protocols.
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
*   **Access lists** for BGP are **simple** and filter based on prefixes. Similar to OSPF, `ge` and `le` parameters are available for more granular prefix matching. They can prevent injecting routes into the routing table using `distribute-list-in` or advertising routes to neighbors using `distribute-list-out`.
*   **Prefix lists** for BGP are also **simple** and filter based on prefixes with logical operators. They can prevent injecting routes using `prefix-list-in` or advertising routes using `prefix-list-out`. Additionally, they can filter routes redistributed by other protocols and can modify BGP attributes.
*   **Route Maps** for BGP are **advanced**, capable of modifying BGP attributes and providing more granularity than access and prefix lists. They can filter both injecting and advertising routes using `route-map-in` and `route-map-out` parameters. Access and prefix lists can be used as objects within route maps.