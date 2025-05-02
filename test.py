    config = load_environment_config(env, country)

    try:
        config_dir = os.path.dirname(config['queue_config_path'])
        queue_mapping_file_path = os.path.join(config_dir, 'queue_hoo_mapping.yaml')
        print(f"Derived queue mapping file path: {queue_mapping_file_path}")
    except KeyError:
        print("ERROR: Could not determine queue_config_path from environment configuration. Cannot derive queue mapping path.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to construct queue mapping file path: {e}")
        sys.exit(1)

    # 2. Initialize AWS Client
    connect_client = initialize_aws_client(env, config['region'])
