def update_local_configs(processed_arns, main_config_path, queue_config_path, queue_mapping_path):
print(f"\nProcessing Queue configuration: '{queue_config_path}' using mapping '{queue_mapping_path}'")
# Load the queue mapping from the hoo-quue_mapping file
    queue_mapping = {}
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
