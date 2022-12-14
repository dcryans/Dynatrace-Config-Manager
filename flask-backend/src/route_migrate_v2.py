from flask import Flask, Blueprint
from flask_cors import cross_origin
import json
import flask_utils
import process_migrate_config
import ui_api_entity_config
import process_utils
import response_utils

blueprint_route_migrate_v2 = Blueprint('blueprint_route_migrate_v2', __name__)


@blueprint_route_migrate_v2.route('/migrate_settings_2_0', methods=['POST'])
@cross_origin(origin='*')
def migrate_settings_2_0():
    tenant_key_main = flask_utils.get_arg('tenant_key_main', '0')
    tenant_key_target = flask_utils.get_arg('tenant_key_target', '0')
    entity_filter = flask_utils.get_arg_json('entity_filter',
                                             process_utils.ALL_BASIC_ENTITY_LIST)
    active_rules = flask_utils.get_arg_json('active_rules')
    forced_schema_id = flask_utils.get_arg('forced_schema_id')
    forced_key_id = flask_utils.get_arg('forced_key_id')
    forced_keep_action_only = flask_utils.get_arg_json('forced_keep_action_only')
    context_params = flask_utils.get_arg_json('context_params')
    use_environment_cache = flask_utils.get_arg_bool(
        'use_environment_cache', False)
    preemptive_config_copy = flask_utils.get_arg_bool('preemptive_config_copy', False)
    pre_migration = flask_utils.get_arg_bool('pre_migration', True)

    run_info = process_utils.get_run_info(
        tenant_key_main, tenant_key_target, context_params, entity_filter, use_environment_cache=use_environment_cache,
        forced_schema_id=forced_schema_id, forced_key_id=forced_key_id, forced_keep_action_only=forced_keep_action_only, 
        preemptive_config_copy=preemptive_config_copy)

    def call_process():
        result = process_migrate_config.migrate_config(
            run_info,
            tenant_key_main, tenant_key_target, active_rules, context_params, pre_migration)
        return result

    return response_utils.call_and_get_response(call_process, run_info)


@blueprint_route_migrate_v2.route('/migrate_ui_api_entity', methods=['POST'])
@cross_origin(origin='*')
def migrate_ui_api_entity():
    tenant_key_main = flask_utils.get_arg('tenant_key_main', '0')
    tenant_key_target = flask_utils.get_arg('tenant_key_target', '0')
    entity_filter = flask_utils.get_arg_json('entity_filter',
                                             process_utils.ALL_BASIC_ENTITY_LIST)
    active_rules = flask_utils.get_arg_json('active_rules')
    context_params = flask_utils.get_arg_json('context_params')
    use_environment_cache = flask_utils.get_arg_bool(
        'use_environment_cache', False)
    pre_migration = flask_utils.get_arg_bool('pre_migration', True)

    run_info = process_utils.get_run_info(
        tenant_key_main, tenant_key_target, context_params, entity_filter, use_environment_cache=use_environment_cache)

    def call_process():
        done = ui_api_entity_config.copy_entity(run_info)
        return done

    return response_utils.call_and_get_response(call_process, run_info)
