import pytest

import tests.acceptance.cli_test

# FIXME Skipping all the acceptance tests when in `--conformity`
non_conformity_tests = [
    "test_build_failed",
    "test_build_failed_forcerm",
    "test_build_log_level",
    "test_build_memory_build_option",
    "test_build_no_cache",
    "test_build_no_cache_pull",
    "test_build_override_dir",
    "test_build_override_dir_invalid_path",
    "test_build_parallel",
    "test_build_plain",
    "test_build_pull",
    "test_build_rm",
    "test_build_shm_size_build_option",
    "test_build_with_buildarg_cli_override",
    "test_build_with_buildarg_from_compose_file",
    "test_build_with_buildarg_old_api_version",
    "test_config_compatibility_mode",
    "test_config_compatibility_mode_from_env",
    "test_config_compatibility_mode_from_env_and_option_precedence",
    "test_config_default",
    "test_config_external_network",
    "test_config_external_network_v3_5",
    "test_config_external_volume_v2",
    "test_config_external_volume_v2_x",
    "test_config_external_volume_v3_4",
    "test_config_external_volume_v3_x",
    "test_config_list_services",
    "test_config_list_volumes",
    "test_config_quiet",
    "test_config_quiet_with_error",
    "test_config_restart",
    "test_config_stdin",
    "test_config_v1",
    "test_config_v3",
    "test_config_with_dot_env",
    "test_config_with_dot_env_and_override_dir",
    "test_config_with_env_file",
    "test_config_with_hash_option",
    "test_create",
    "test_create_with_force_recreate",
    "test_create_with_force_recreate_and_no_recreate",
    "test_create_with_no_recreate",
    "test_down",
    "test_down_invalid_rmi_flag",
    "test_down_signal",
    "test_down_timeout",
    "test_env_file_relative_to_compose_file",
    "test_events_human_readable",
    "test_events_json",
    "test_exec_custom_user",
    "test_exec_detach_long_form",
    "test_exec_novalue_var_dotenv_file",
    "test_exec_service_with_environment_overridden",
    "test_exec_without_tty",
    "test_exec_workdir",
    "test_exit_code_from_signal_stop",
    "test_expanded_port",
    "test_forward_exitval",
    "test_help",
    "test_help_nonexistent",
    "test_home_and_env_var_in_volume_path",
    "test_host_not_reachable",
    "test_host_not_reachable_volumes_from_container",
    "test_host_not_reachable_volumes_from_container",
    "test_images",
    "test_images_default_composefile",
    "test_images_tagless_image",
    "test_images_use_service_tag",
    "test_kill",
    "test_kill_signal_sigstop",
    "test_kill_stopped_service",
    "test_logs_default",
    "test_logs_follow",
    "test_logs_follow_logs_from_new_containers",
    "test_logs_follow_logs_from_restarted_containers",
    "test_logs_invalid_service_name",
    "test_logs_on_stopped_containers_exits",
    "test_logs_tail",
    "test_logs_timestamps",
    "test_pause_no_containers",
    "test_pause_unpause",
    "test_port",
    "test_port_with_scale",
    "test_ps",
    "test_ps_all",
    "test_ps_alternate_composefile",
    "test_ps_default_composefile",
    "test_ps_services_filter_option",
    "test_ps_services_filter_status",
    "test_pull",
    "test_pull_can_build",
    "test_pull_with_digest",
    "test_pull_with_ignore_pull_failures",
    "test_pull_with_include_deps",
    "test_pull_with_no_deps",
    "test_pull_with_parallel_failure",
    "test_pull_with_quiet",
    "test_quiet_build",
    "test_restart",
    "test_restart_no_containers",
    "test_restart_stopped_container",
    "test_rm",
    "test_rm_all",
    "test_rm_stop",
    "test_run_detached_connects_to_network",
    "test_run_does_not_recreate_linked_containers",
    "test_run_env_values_from_system",
    "test_run_handles_sighup",
    "test_run_handles_sigint",
    "test_run_handles_sigterm",
    "test_run_interactive_connects_to_network",
    "test_run_label_flag",
    "test_run_one_off_with_multiple_volumes",
    "test_run_one_off_with_volume",
    "test_run_one_off_with_volume_merge",
    "test_run_rm",
    "test_run_service_with_compose_file_entrypoint",
    "test_run_service_with_compose_file_entrypoint_and_command_overridden",
    "test_run_service_with_compose_file_entrypoint_and_empty_string_command",
    "test_run_service_with_compose_file_entrypoint_overridden",
    "test_run_service_with_dependencies",
    "test_run_service_with_dockerfile_entrypoint",
    "test_run_service_with_dockerfile_entrypoint_and_command_overridden",
    "test_run_service_with_dockerfile_entrypoint_overridden",
    "test_run_service_with_environment_overridden",
    "test_run_service_with_explicitly_mapped_ip_ports",
    "test_run_service_with_explicitly_mapped_ports",
    "test_run_service_with_links",
    "test_run_service_with_map_ports",
    "test_run_service_with_scaled_dependencies",
    "test_run_service_with_unset_entrypoint",
    "test_run_service_with_use_aliases",
    "test_run_service_with_user_overridden",
    "test_run_service_with_user_overridden_short_form",
    "test_run_service_with_workdir_overridden",
    "test_run_service_with_workdir_overridden_short_form",
    "test_run_service_without_links",
    "test_run_service_without_map_ports",
    "test_run_unicode_env_values_from_system",
    "test_run_with_custom_name",
    "test_run_with_expose_ports",
    "test_run_with_no_deps",
    "test_run_without_command",
    "test_scale",
    "test_scale_v2_2",
    "test_shorthand_host_opt",
    "test_shorthand_host_opt_interactive",
    "test_start_no_containers",
    "test_stop",
    "test_stop_signal",
    "test_top_processes_running",
    "test_top_services_not_running",
    "test_top_services_running",
    "test_unpause_no_containers",
    "test_up",
    "test_up_attached",
    "test_up_detached",
    "test_up_detached_long_form",
    "test_up_external_networks",
    "test_up_handles_abort_on_container_exit",
    "test_up_handles_abort_on_container_exit_code",
    "test_up_handles_aborted_dependencies",
    "test_up_handles_force_shutdown",
    "test_up_handles_sigint",
    "test_up_handles_sigterm",
    "test_up_logging",
    "test_up_logging_legacy",
    "test_up_missing_network",
    "test_up_no_ansi",
    "test_up_no_services",
    "test_up_no_start",
    "test_up_no_start_remove_orphans",
    "test_up_scale_reset",
    "test_up_scale_scale_down",
    "test_up_scale_scale_up",
    "test_up_scale_to_zero",
    "test_up_with_attach_dependencies",
    "test_up_with_default_network_config",
    "test_up_with_default_override_file",
    "test_up_with_duplicate_override_yaml_files",
    "test_up_with_extends",
    "test_up_with_external_default_network",
    "test_up_with_force_recreate",
    "test_up_with_force_recreate_and_no_recreate",
    "test_up_with_healthcheck",
    "test_up_with_ignore_remove_orphans",
    "test_up_with_links_v1",
    "test_up_with_multiple_files",
    "test_up_with_net_is_invalid",
    "test_up_with_net_v1",
    "test_up_with_network_aliases",
    "test_up_with_network_internal",
    "test_up_with_network_labels",
    "test_up_with_network_mode",
    "test_up_with_network_static_addresses",
    "test_up_with_networks",
    "test_up_with_no_deps",
    "test_up_with_no_recreate",
    "test_up_with_override_yaml",
    "test_up_with_pid_mode",
    "test_up_with_timeout",
    "test_up_with_volume_labels",
    "test_fail_on_both_host_and_context_opt",
    "test_fail_run_on_inexistent_context",
    "test_events_with_stop_process_flag",
]


def pytest_addoption(parser):
    parser.addoption(
        "--conformity",
        action="store_true",
        default=False,
        help="Only runs tests that are not black listed as non conformity test. "
             "The conformity tests check for compatibility with the Compose spec."
    )
    parser.addoption(
        "--binary",
        default=tests.acceptance.cli_test.DOCKER_COMPOSE_EXECUTABLE,
        help="Forces the execution of a binary in the PATH. Default is `docker-compose`."
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--conformity"):
        return
    if config.getoption("--binary"):
        tests.acceptance.cli_test.DOCKER_COMPOSE_EXECUTABLE = config.getoption("--binary")

    print("Binary -> {}".format(tests.acceptance.cli_test.DOCKER_COMPOSE_EXECUTABLE))
    skip_non_conformity = pytest.mark.skip(reason="skipping because that's not a conformity test")
    for item in items:
        if item.name in non_conformity_tests:
            # print("Skipping '{}' when running in compatibility mode".format(item.name))
            item.add_marker(skip_non_conformity)
