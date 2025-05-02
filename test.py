    try:
        with open(queue_mapping_path, 'r') as file:
            queue_mapping = yaml.safe_load(file)
        if not queue_mapping:
             print(f"  WARNING: Queue mapping file '{queue_mapping_path}' is empty or invalid. Skipping queue update.")
             queue_mapping = {} # Ensure it's an empty dict if loading fails partially
    except FileNotFoundError:
        print(f"  ERROR: Queue mapping file not found at '{queue_mapping_path}'. Skipping queue update.")
        queue_mapping = {}
    except yaml.YAMLError as e:
        print(f"  ERROR: Could not parse YAML from '{queue_mapping_path}': {e}. Skipping queue update.")
        queue_mapping = {}


if not queue_mapping:
         print("  Skipping queue configuration update because queue mapping could not be loaded.")
    else:
        try:
            with open(queue_config_path, 'r') as file:
                queue_data = yaml.safe_load(file)

            if not queue_data or 'Queues' not in queue_data:
                 print(f"  WARNING: No 'Queues' list found in '{queue_config_path}'. Skipping queue update.")
                 return

            queues_updated = 0
            for queue in queue_data.get('Queues', []):
                queue_name = queue.get('Name')
                if not queue_name:
                    print("  WARNING: Skipping queue entry with missing 'Name'.")
                    continue

                current_hoo_id = queue.get('HoursOfOperationId')

                for hoo_name, target_queues in queue_mapping.items():
                    if isinstance(target_queues, list) and queue_name in target_queues:
                        if hoo_name in processed_arns:
                            try:
                                new_hoo_id = processed_arns[hoo_name].split('/')[-1]
                                if current_hoo_id != new_hoo_id:
                                    print(f"  Updating HoO ID for Queue '{queue_name}' to '{new_hoo_id}' (from HoO '{hoo_name}')")
                                    queue['HoursOfOperationId'] = new_hoo_id
                                    queues_updated += 1
                            except IndexError:
                                 print(f"  ERROR: Could not extract ID from ARN '{processed_arns[hoo_name]}' for HoO '{hoo_name}'.")
                        else:
                            print(f"  WARNING: Cannot update Queue '{queue_name}'. Required HoO '{hoo_name}' (from mapping file) was not processed or failed.")
                        break

            if queues_updated > 0:
                print(f"Saving updated queue configuration to '{queue_config_path}'...")
                with open(queue_config_path, 'w') as file:
                    yaml.dump(queue_data, file, default_flow_style=False, sort_keys=False)
            else:
                print("  No changes required in queue configuration file.")

        except FileNotFoundError:
            print(f"  WARNING: Queue configuration file not found at '{queue_config_path}'. Skipping update.")
        except yaml.YAMLError as e:
            print(f"  ERROR: Could not parse YAML from '{queue_config_path}': {e}")
        except Exception as e:
            print(f"  ERROR updating queue configuration '{queue_config_path}': {e}")
