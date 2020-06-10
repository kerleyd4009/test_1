# A file to test list with dict

test = {'error': None,
        'result': [
            {'id': 435227, 'labels': [], 'tb_capacity': None, 'system_serial': 1164, 'index': 19, 'parent_index': 4,
             'vendor': 'HGST', 'model': 'HUS724030ALS641',
             'serial_number': 'P9J0GNRW', 'firmware': 'B280', 'part_number': None,
             'state_description': 'Drive is not ACTIVE', 'created': '2015-08-29T11:06:36Z',
             'updated': '2020-05-05T12:16:58Z', 'sku': 'DSK-00012', 'connected_to_node_1': False,
             'connected_to_node_2': False, 'connected_to_node_3': False,
             'state': 'MISSING', 'product_rev': 'B280', 'bytes_capacity': 0, 'bg_scan_hardware_errors': 0,
             'bg_scan_recovered_errors': 0, 'bg_scan_status': 0,
             'bg_scan_total_errors': 0, 'bg_scans_performed': 0, 'non_medium_errors': 0, 'pending_reallocations': 0,
             'power_on_hours': 0, 'reallocations': 0,
             'temperature': 0, 'total_read_bytes_processed': 0, 'total_read_uncorrected': 0,
             'total_verify_bytes_processed': 0, 'total_verify_uncorrected': 0,
             'total_write_bytes_processed': 0, 'fail_reason': 'drive lost during boot', 'smart_health_status': 'OK',
             'parent': 7257},

            {'id': 434936, 'labels': [], 'tb_capacity': None, 'system_serial': 1164, 'index': 49, 'parent_index': 5,
             'vendor': 'HGST',
             'model': 'HUS724030ALS641', 'serial_number': 'P9J0EHYW', 'firmware': 'B280', 'part_number': None,
             'state_description': 'Drive is not ACTIVE', 'created': '2015-08-29T11:06:36Z',
             'updated': '2020-05-05T12:16:58Z', 'sku': 'DSK-00012',
             'connected_to_node_1': False, 'connected_to_node_2': False, 'connected_to_node_3': False,
             'state': 'MISSING', 'product_rev': 'B280',
             'bytes_capacity': 0, 'bg_scan_hardware_errors': 0, 'bg_scan_recovered_errors': 0, 'bg_scan_status': 0,
             'bg_scan_total_errors': 0,
             'bg_scans_performed': 0, 'non_medium_errors': 0, 'pending_reallocations': 0, 'power_on_hours': 0,
             'reallocations': 0, 'temperature': 0,
             'total_read_bytes_processed': 0, 'total_read_uncorrected': 0, 'total_verify_bytes_processed': 0,
             'total_verify_uncorrected': 0,
             'total_write_bytes_processed': 0, 'fail_reason': 'slow response', 'smart_health_status': 'OK',
             'parent': 7258},

            {'id': 434932, 'labels': [], 'tb_capacity': 3, 'system_serial': 1164, 'index': 13, 'parent_index': 6,
             'vendor': 'HGST', 'model': 'HUS724030ALS641',
             'serial_number': 'P9J0EZ0W', 'firmware': 'B280', 'part_number': None,
             'state_description': 'Drive is not ACTIVE', 'created': '2015-08-29T11:06:36Z',
             'updated': '2020-05-05T12:16:58Z', 'sku': 'DSK-00012', 'connected_to_node_1': True,
             'connected_to_node_2': True, 'connected_to_node_3': True,
             'state': 'READY', 'product_rev': 'B280', 'bytes_capacity': 3000592981504, 'bg_scan_hardware_errors': 0,
             'bg_scan_recovered_errors': 0, 'bg_scan_status': 1,
             'bg_scan_total_errors': 0, 'bg_scans_performed': 179, 'non_medium_errors': 0, 'pending_reallocations': 0,
             'power_on_hours': 37887, 'reallocations': 0,
             'temperature': 28, 'total_read_bytes_processed': 6175193842176, 'total_read_uncorrected': 0,
             'total_verify_bytes_processed': 71607693524992,
             'total_verify_uncorrected': 0, 'total_write_bytes_processed': 14180829163520,
             'fail_reason': 'slow response', 'smart_health_status': 'OK', 'parent': 7259}],
        'metadata': {'pages_total': 1, 'page_size': 50, 'next': None, 'ready': True, 'number_of_objects': 3, 'page': 1,
                     'previous': None}}

# print("E" + str(test['result'][1]['parent_index']) + "D" + str(test['result'][1]['index']))
ecomp = []
for item in test['result']:
  ecomp = ("E" + str(item['parent_index']) + "D" + str(item['index']))


print(str(ecomp))
#for item, item_dict in test.items():
#    for results in item_dict or ():
#        for k, v in results.items() or ():
#            print(k, v)