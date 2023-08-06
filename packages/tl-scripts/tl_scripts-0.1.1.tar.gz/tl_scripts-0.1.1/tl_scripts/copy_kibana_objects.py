import os
import tempfile
from typing import List, Optional

import ndjson
import pexpect
import requests


def copy_kibana_objects(origin_env: Optional[str] = None, destination_env: Optional[str] = None, origin_space_id: Optional[str] = None,
                        destination_space_id: Optional[str] = None, dashboard_id: Optional[str] = None,
                        new_index_pattern: Optional[str] = None):
    try:
        if origin_env:
            p = pexpect.spawn(f'kubectx {origin_env}')
            p.close()
        else:
            print("Select base environment to copy objects from")
            p = pexpect.spawn('kubectx')
            p.interact()

        base_kibana_port_forward = pexpect.spawn('kubectl -n data port-forward svc/kibana 5601')
        base_kibana_port_forward.expect("Forwarding from 127.0.0.1:5601 -> 5601")

        if origin_space_id is None or not origin_space_id:
            origin_space_id = get_space()

        if dashboard_id is None or not dashboard_id:
            dashboard_id = get_dashboard_id(origin_space_id)

        print("Exporting dashboard and all connected objects")
        list_of_saved_objects = get_list_of_saved_objects(dashboard_id, origin_space_id)

        base_kibana_port_forward.close(force=True)
        if destination_env:
            p = pexpect.spawn(f'kubectx {destination_env}')
            p.close()
        else:
            print("Select destination environment to move objects to")
            p = pexpect.spawn('kubectx')
            p.interact()

        destination_kibana_port_forward = pexpect.spawn('kubectl -n data port-forward svc/kibana 5601')
        destination_kibana_port_forward.expect("Forwarding from 127.0.0.1:5601 -> 5601")

        if destination_space_id is None or not destination_space_id:
            destination_space_id = get_space()

        if new_index_pattern is None or not new_index_pattern:
            new_index_pattern = get_new_index_pattern(destination_space_id)

        replace_old_to_new_index_pattern(list_of_saved_objects, new_index_pattern)

        import_objects_to_kibana(list_of_saved_objects, destination_space_id)
    finally:
        if 'base_kibana_port_forward' in vars() or 'base_kibana_port_forward' in globals():
            base_kibana_port_forward.close(force=True)
        if 'destination_kibana_port_forward' in vars() or 'destination_kibana_port_forward' in globals():
            destination_kibana_port_forward.close(force=True)


def import_objects_to_kibana(list_of_saved_objects, space_id):
    url = f'http://localhost:5601/kibana/s/{space_id}/api/saved_objects/_import?overwrite=true'
    headers = {'kbn-xsrf': "true"}
    fd, path = tempfile.mkstemp(suffix=".ndjson")
    try:
        with os.fdopen(fd, 'w') as tmp:
            ndjson.dump(list_of_saved_objects, tmp)

        r = requests.post(url, files={"file": open(path, 'rb')}, headers=headers)
        print(r.text)
    finally:
        os.remove(path)


def replace_old_to_new_index_pattern(list_of_saved_objects, new_index_pattern):
    for obj in list_of_saved_objects:
        for ref in obj["references"]:
            if ref["type"] == 'index-pattern':
                ref["id"] = new_index_pattern


def get_list_of_saved_objects(dashboard_id, origin_space_id):
    url = f'http://localhost:5601/kibana/s/{origin_space_id}/api/saved_objects/_export'
    headers = {'content-type': 'application/json',
               'kbn-xsrf': "true"}
    json_body = {
        "objects": [
            {
                "type": "dashboard",
                "id": f"{dashboard_id}"
            }
        ],
        "excludeExportDetails": "true",
        "includeReferencesDeep": "true"
    }
    r = requests.post(url, json=json_body, headers=headers)
    list_of_objects = r.json(cls=ndjson.Decoder)
    list_of_objects = [obj for obj in list_of_objects if
                       "type" in obj and obj["type"] in ["visualization", "dashboard"]]
    return list_of_objects


def get_space():
    r = requests.get('http://localhost:5601/kibana/api/spaces/space')
    list_of_spaces = r.json()
    space_names = [space["name"] for space in list_of_spaces]
    space_selected = user_select_from_list(space_names, "space")
    selected_space = list_of_spaces[space_selected]
    space_id = selected_space["id"]
    return space_id


def get_dashboard_id(origin_space_id):
    url = f'http://localhost:5601/kibana/s/{origin_space_id}/api/saved_objects/_export'
    json_body = {
        "type": "dashboard",
        "excludeExportDetails": "true"
    }
    headers = {'content-type': 'application/json',
               'kbn-xsrf': "true"}
    r = requests.post(url, json=json_body, headers=headers)
    list_of_dashboards = r.json(cls=ndjson.Decoder)
    list_of_dashboards = [dash for dash in list_of_dashboards if "id" in dash]
    dashboard_names = [dash["attributes"]["title"] for dash in list_of_dashboards]
    dashboard_selected = user_select_from_list(dashboard_names, "dashboard")
    selected_dashboard = list_of_dashboards[dashboard_selected]
    dashboard_id = selected_dashboard['id']
    return dashboard_id


def get_new_index_pattern(space_id):
    url = f'http://localhost:5601/kibana/s/{space_id}/api/saved_objects/_export'
    json_body = {
        "type": "index-pattern",
        "excludeExportDetails": "true"
    }
    headers = {'content-type': 'application/json',
               'kbn-xsrf': "true"}
    r = requests.post(url, json=json_body, headers=headers)
    list_of_idx_ptrn = r.json(cls=ndjson.Decoder)
    list_of_idx_ptrn = [dash for dash in list_of_idx_ptrn if "id" in dash]
    ptrn_names = [ptrn["attributes"]["title"] for ptrn in list_of_idx_ptrn]
    ptrn_selected = user_select_from_list(ptrn_names, "new index pattern")
    selected_ptrn = list_of_idx_ptrn[ptrn_selected]
    new_index_pattern = selected_ptrn['id']
    return new_index_pattern


def user_select_from_list(list_options: List[str], resource_name: str) -> int:
    print(f"select a {resource_name}")
    for idx, name in enumerate(list_options):
        print(f"({idx}) {name}")
    index_selected = input()
    last_valid_idx = len(list_options) - 1
    try:
        int_selected = int(index_selected)
    except:
        print(f"input not valid. Selected was : {index_selected}, valid values are: 0 - {last_valid_idx}")
        exit(-1)

    if int_selected < 0 or int_selected > last_valid_idx:
        print(
            f"Wrong index selected. Selected was : {index_selected}, valid values are: 0 - {last_valid_idx}")
        exit(-1)
    print(f"Selected {resource_name}: {list_options[int_selected]}")
    return int_selected
