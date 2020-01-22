def one_param_to_int(x=None):
    if x:
        return int(x[0])
    return


def one_param_to_vlan_dict(x=None):
    if x:
        return {"vlan_id": int(x[0]), "admin_state": "up", "vlan_name": "VLAN%s" % x[0]}
    return


def bgp_rid_to_list(x=None):
    if x:
        return {'status': 'enable', 'as_number': int(x[0])}
    return
