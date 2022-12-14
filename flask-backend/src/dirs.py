import os
from os import listdir
from os.path import isfile, join
import hashlib

# Max length is 256 or 260, but it is on an escaped and decorated path
# Setting limit to 240 characters
MAX_LENGTH_WINDOWS = 240

def get_file_path(dir_path, filename, file_extension='.json'):
    # On Windows, semi-colons are restricted
    filename = filename.replace(':', '_')
    path = os.path.join(dir_path, filename + file_extension)
    
    if(is_path_too_long(path)):
        filename = get_filename_hash(filename)
        path = os.path.join(dir_path, filename + file_extension)
        
        if(is_path_too_long):
            raise OverflowError("Path exceeds maximum length (Windows protection)")
    
    return path

def get_filename_hash(filename):
    escaped_filename = filename.encode('unicode_escape')
    filename = str(int(hashlib.md5(escaped_filename).hexdigest(), 16))
    
    return filename

def is_path_too_long(path):
    escaped_path = path.encode('unicode_escape')
    return len(escaped_path) > MAX_LENGTH_WINDOWS

def get_data_dir():
    return prep_dir(
        os.path.join(
            os.getcwd(), '..', 'data'))


def get_tenant_list_dir():
    return prep_dir(
        os.path.join(
            get_data_dir(), 'tenant'))


def get_options_dir():
    return prep_dir(
        os.path.join(
            get_data_dir(), 'options'))


def get_tenant_data_dir():
    return prep_dir(
        os.path.join(
            get_data_dir(), 'tenant_data'))


def get_tenant_data_cache_dir(config):
    return prep_dir(
        os.path.join(
            get_tenant_data_dir(), config['tenant_key']))


def get_tenant_data_cache_sub_dir(config, sub_dir):
    return prep_dir(
        os.path.join(
            get_tenant_data_cache_dir(config), sub_dir))


def get_log_list_dir():
    return prep_dir(
        os.path.join(
            get_data_dir(), 'log_list'))


def get_log_data_dir(config):
    return prep_dir(
        os.path.join(
            get_log_list_dir(config), 'log_data'))


def prep_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def list_files_in_dir(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]

    return files
