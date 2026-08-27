"""
NetSage AI - Deterministic Rule Checker
Runs config sanity checks that do NOT rely on AI: duplicate IPs, wrong masks,
gateway mismatch, interface down, missing VLAN, missing routes.

Expects a devices list where each device is a dict, e.g.:
{
    "name": "PC1",
    "ip": "192.168.10.10",
    "mask": "255.255.255.0",
    "gateway": "192.168.10.1",
    "vlan": "10",
    "status": "up"
}
"""

import ipaddress


def check_duplicate_ips(devices):
    seen = {}
    duplicates = []
    for d in devices:
        ip = d.get("ip")
        if not ip:
            continue
        if ip in seen:
            duplicates.append((d["name"], seen[ip], ip))
        else:
            seen[ip] = d["name"]
    return duplicates


def check_wrong_mask(devices, expected_mask="255.255.255.0"):
    issues = []
    for d in devices:
        if d.get("mask") and d["mask"] != expected_mask:
            issues.append((d["name"], d["mask"], expected_mask))
    return issues


def check_gateway_mismatch(devices):
    issues = []
    for d in devices:
        try:
            if not d.get("ip") or not d.get("mask") or not d.get("gateway"):
                continue
            net = ipaddress.ip_network(f"{d['ip']}/{d['mask']}", strict=False)
            if ipaddress.ip_address(d["gateway"]) not in net:
                issues.append(d["name"])
        except ValueError as e:
            issues.append(f"{d['name']} (parse error: {e})")
    return issues


def check_interface_down(devices):
    return [d["name"] for d in devices if d.get("status", "").lower() in ("down", "administratively down")]


def check_missing_vlan(devices, valid_vlans):
    return [d["name"] for d in devices if d.get("vlan") not in valid_vlans]


def check_missing_routes(routes, required_subnets):
    """routes: list of subnet strings currently in the routing table.
    required_subnets: list of subnet strings that should be reachable."""
    missing = [s for s in required_subnets if s not in routes]
    return missing


def run_all_checks(devices, valid_vlans, routes, required_subnets):
    results = {
        "duplicate_ips": check_duplicate_ips(devices),
        "wrong_mask": check_wrong_mask(devices),
        "gateway_mismatch": check_gateway_mismatch(devices),
        "interface_down": check_interface_down(devices),
        "missing_vlan": check_missing_vlan(devices, valid_vlans),
        "missing_routes": check_missing_routes(routes, required_subnets),
    }
    return results


if __name__ == "__main__":
    # Sample test data — replace with real parsed data from your lab cases
    sample_devices = [
        {"name": "PC1", "ip": "192.168.10.10", "mask": "255.255.255.0", "gateway": "192.168.10.1", "vlan": "10", "status": "up"},
        {"name": "PC2", "ip": "192.168.10.10", "mask": "255.255.255.0", "gateway": "192.168.10.1", "vlan": "10", "status": "up"},
        {"name": "PC3", "ip": "192.168.20.5", "mask": "255.255.255.0", "gateway": "192.168.30.1", "vlan": "20", "status": "up"},
        {"name": "PC4", "ip": "192.168.40.5", "mask": "255.255.255.0", "gateway": "192.168.40.1", "vlan": "99", "status": "down"},
    ]
    valid_vlans = ["10", "20", "30", "40"]
    routes = ["192.168.10.0", "192.168.20.0"]
    required_subnets = ["192.168.10.0", "192.168.20.0", "192.168.30.0"]

    results = run_all_checks(sample_devices, valid_vlans, routes, required_subnets)

    print("=== NetSage AI Rule Checker Results ===")
    for check_name, findings in results.items():
        status = "FAIL" if findings else "PASS"
        print(f"[{status}] {check_name}: {findings if findings else 'no issues found'}")
