import glob
import re
import shutil

from freehub import git_ops
from freehub.utils import *
import logging
import json
import os
import sys
import fnmatch
# _BRANCH_DICT='branch_dict'
# _FAKE2TRUE: str='fake2true'
# _TRUE2FAKE='true2fake'
# _BRANCH_LIST='remote_branch_list'
USER_HOME=os.path.expanduser('~')
STORE_HOME=USER_HOME+'/.store'
STORE_TMP_DIR='/.store/.tmp'
# SCRIPTS_PATH='/.freehub-scripts'
# BRANCH_LIST_DIR=STORE_HOME+'/BranchLists'
# SHADOW_STORE_HOME=STORE_HOME+'/ShadowStores'
# STORE_TMP_DIR=STORE_HOME+'/tmp'
# STORE_CLASS_DIR=STORE_HOME+'/Store.Class'
STORE_CONFIG_FILE=STORE_HOME+'/config.json'
# FREEHUB_LOCATION='https://OpenGitspace:Gitspace@123456@gitee.com/OpenGitspace/meta'
DEFAULT_HOST='gitee.com'

# DEFAULT_USERNAME='OpenGitspace'
DEFAULT_USERNAME='peiiii'
DEFAULT_REPO='gitspace'

# DEFAULT_PASSWORD='Gitspace@123456'

def _read_config():
    if not os.path.exists(STORE_CONFIG_FILE):
        return None
    with open(STORE_CONFIG_FILE,'r',encoding='utf-8') as f:
        return json.load(f)
def _write_config(data):
    with open(STORE_CONFIG_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f)

def get_default_repo_address():
    cfg:dict=_read_config()
    username=DEFAULT_USERNAME
    repo=DEFAULT_REPO
    host=DEFAULT_HOST
    # if cfg:
    #     username=cfg.get('username',username)
    #     host=cfg.get('default_host',host)
    #     repo=cfg.get('default_repo',repo)
    return '%s/%s/%s'%(host,username,repo)
class Address:
    def __init__(self,protocol,host,username,repo_name,branch_name,rel_path):
        self.protocol=protocol
        self.host=host
        self.username=username
        self.repo_name=repo_name
        self.branch_name=branch_name
        self.rel_path=rel_path
    def to_url(self):
        return '%s://%s/%s/%s:'%(self.protocol,self.host,self.username,self.repo_name)+join_path(self.branch_name,self.rel_path)
    @classmethod
    def from_url(cls,url):

        protocol,repo_address,branch_name,rel_path=cls.parse_address(url)
        host,username,repo_name=repo_address.split('/')
        return cls(protocol,host,username,repo_name,branch_name,rel_path)
    @classmethod
    def parse_address(cls,address):
        '''
           address: [[[{host}/]{username}/]{repo_name}:]{branch_name}[/{relative_path}]
           '''

        def parse_rest(rest: str):
            rest = rest.strip('/')
            if '/' in rest:
                branch_name, relative_path = rest.split('/', maxsplit=1)
            else:
                branch_name = rest
                relative_path = '/'
            return branch_name, relative_path

        repo_address, rest = address.rsplit(':', maxsplit=1)
        protocol = "freehub"
        if "://" in repo_address:
            protocol, repo_address = repo_address.split('://', maxsplit=1)
        branch_name, relative_path = parse_rest(rest)
        return protocol, repo_address, branch_name, relative_path
    @classmethod
    def get_complete_address(cls,address:str):
        address = address.replace('\\', '/')
        protocol="freehub"
        if "://" in address:
            protocol,address=address.split('://',maxsplit=1)
        if ':' in address:
            assert address.count(':') == 1
            repo_address, rest = address.split(':')
            parts = repo_address.split('/')
            assert len(parts) >= 1
            assert len(parts) <= 3
            default_parts = get_default_repo_address().split('/')
            default_parts[-1] = parts[-1]
            if len(parts) >= 2:
                default_parts[-2] = parts[-2]
            if len(parts) >= 3:
                default_parts[-3] = parts[-3]
            repo_address = '/'.join(default_parts)
        else:
            repo_address = get_default_repo_address()
            rest = address
        addr = protocol+"://"+':'.join([repo_address, rest])
        return addr
    def get_repo_url(self):
        host, username_, repo = self.host,self.username,self.repo_name
        cfg = _read_config()

        if cfg and 'password' in cfg and 'username' in cfg:
            username = cfg.get('username')
            password = cfg.get('password')
            repo_url = 'https://%s:%s@%s/%s/%s' % (username, password, host, username_, repo)
            # print("repo_url:", 'https://%s:******@%s/%s/%s' % (username, host, username_, repo))
        else:
            # username=DEFAULT_USERNAME
            # password=DEFAULT_PASSWORD
            repo_url = 'https://%s/%s/%s' % (host, username_, repo)
            # print("repo_url:",repo_url)
        return repo_url



def get_complete_address(address):
    return Address.get_complete_address(address)
def parse_address(address):
    '''
       address: [[[{host}/]{username}/]{repo_name}:]{branch_name}[/{relative_path}]
       '''
    return Address.parse_address(address)





def download_branch(remote_location,branch,dst,overwrite=False,quiet=True):
    check_and_make_empty_dir(dst,overwrite)
    repo=git_ops.git_init(dst)
    git_ops.create_head(repo)
    git_ops.pull_remote_branch(repo,remote_location,branch,quiet=quiet)

def upload_branch(repo,remote_location,branch,overwrite=False,quiet=True):
    if git_ops.exists_remote_branch(remote_location,branch):
        if not overwrite:
            raise Exception('Remote branch %s already exists at %s .'%(branch,remote_location))
        else:
            logging.warning('Will overwrite remote branch %s at %s .'%(branch,remote_location))
    else:
        logging.info('Will upload to a new branch %s at %s .'%(branch,remote_location))
    branches=git_ops.list_branch(repo)
    if not branch in branches:
        raise Exception('Local branch %s does not exist.'%(branch))
    git_ops.push_local_branch(repo, branch, remote_location,quiet=quiet)


def download_branch_to_cache(remote_location,branch,cache_dir=None,overwrite=True,**kwargs):
    cache_dir=cache_dir or os.path.join(STORE_HOME,branch)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    download_branch(remote_location,branch,dst=cache_dir,overwrite=overwrite,**kwargs)
    return cache_dir
def download_branch_to_dir(remote_location,branch,dst,cache_dir=None,overwrite=True,**kwargs):
    cache_dir=cache_dir or os.path.join(STORE_HOME,branch)
    download_branch_to_cache(remote_location,branch,cache_dir,overwrite=overwrite,**kwargs)
    copy_repo_files_to_dir(cache_dir,dst)

def upload_to_remote(remote_location,branch_name,relative_path,src_path,cache_dir=None,overwrite=True,**kwargs):
    ''''''
    cache_dir = cache_dir or os.path.join(STORE_HOME, branch_name)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    if git_ops.exists_remote_branch(remote_location, branch_name):
        download_branch_to_cache(remote_location, branch_name, cache_dir)
        repo = git_ops.Repo(cache_dir)
        git_ops.pull_remote_branch(repo, remote_location, branch_name)
    else:
        repo = git_ops.git_init(cache_dir)
    copy_to_repo(src_path,cache_dir,relative_path,overwrite=overwrite)

    #############################

    git_ops.create_head(repo)
    git_ops.create_branch(repo,branch_name,force=True)
    git_ops.switch_branch(repo,branch_name,recover=False)
    git_ops.stage_all_changes(repo)
    git_ops.commit_current_branch(repo)
    try:
        upload_branch(repo,remote_location,branch_name,overwrite=overwrite,**kwargs)
    except GitProtocolError as e:
        logging.error('Error occurred. Might be the permission problem, please check if you have the permission.')
        raise e



def freehub_download(address,dst_path,overwrite=False,inplace=False,**kwargs):
    '''
    {cache_dir}/{relative_path}
    relative_path: can be a path pattern, e.g. *.txt
    '''
    a=Address.from_url(address)
    cache_dir=download_branch_to_cache(a.get_repo_url(),a.branch_name,overwrite=overwrite,**kwargs)
    print(cache_dir)
    copy_repo_files_to(cache_dir,a.rel_path,dst_path,a.branch_name,inplace=inplace)


def freehub_upload(src_path,address,overwrite=False,**kwargs):
    addr=Address.from_url(address)
    upload_to_remote(addr.get_repo_url(),addr.branch_name,addr.rel_path,src_path,overwrite=overwrite,**kwargs)
def fetch(address,**kwargs):
    addr = Address.from_url(address)
    cache_dir = download_branch_to_cache(addr.get_repo_url(), addr.branch_name, overwrite=True,**kwargs)
    path = join_path(cache_dir, addr.rel_path)
    return path
def freehub_run(address,**kwargs):
    ''''''
    addr = Address.from_url(address)
    cache_dir = download_branch_to_cache(addr.get_repo_url(), addr.branch_name, overwrite=True,**kwargs)
    script_path=join_path(cache_dir,addr.rel_path)
    os.system(script_path)
def freehub_cat(address:str,**kwargs):
    addr = Address.from_url(address)
    cache_dir = download_branch_to_cache(addr.get_repo_url(), addr.branch_name, overwrite=True,**kwargs)
    file_path = join_path(cache_dir, addr.rel_path)
    with open(file_path,'r') as f:
        print(f.read())
def freehub_update():
    cache_dir=join_path(STORE_HOME,'freehub')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        time.sleep(1e-10)
    freehub_download('gitee.com/peiiii/gitspace:freehub',cache_dir)
    dist_dir=join_path(cache_dir,'dist')
    files=glob.glob(dist_dir+'/*.whl')
    print('Files to install:',files)
    for f in files:
        if f.endswith('.whl'):
            os.system('pip3 install %s --user'%(f))
    if not files:
        logging.warning('Noting to install')

    # cache_dir=freehub_download('gitee.com/')
def freehub_search(pattern: str,**kwargs):
    '''
    :param reg_str: [[{host}/]{username}/]{repo_name}[:{branch_name}]
    :return:
    '''
    # convert repo_address into repo_url
    addr = Address.from_url(pattern)
    assert addr.rel_path != '/'
    cache_dir = download_branch_to_cache(addr.get_repo_url(), addr.branch_name, overwrite=True,**kwargs)
    fs = glob.glob(join_path(cache_dir, addr.rel_path), recursive=True)
    for f in fs:
        rel_path = get_relative_path(cache_dir, f)
        print(rel_path)

def freehub_branch_search(pattern: str):
    addr=Address.from_url(pattern)
    assert addr.rel_path=='/'
    branches = git_ops.list_remote_branch(addr.get_repo_url())
    for b in branches:
        if addr.branch_name:
            if fnmatch.fnmatch(b, addr.branch_name):
                print(b)
        else:
            print(b)



def freehub_login():
    user_name=input('Username:')
    password=input('Password:')
    host=input('Default Host(default host is gitee.com):') or 'gitee.com'
    repo=input('Default Repository:')
    _write_config(dict(
        username=user_name,
        password=password,
        default_repo=repo,
        default_host=host,
    ))
    print('Login successfully.')
def freehub_logout():
    os.remove(STORE_CONFIG_FILE)
    print('Logout successfully.')


def test():
    default_remote_location = ''
    repo_path = '../data/OpenGitspace'
    import wk
    wk.remake(repo_path)

    # repo_path = './data/'
    # download_branch(default_remote_location,'test',repo_path)
    # upload_branch(default_remote_location,'test2',repo_path,overwrite=True)
    # download_to_dir(default_remote_location,'test',repo_path)
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')

    wk.Folder(repo_path).open('readme.txt','w').write('yes')
    #freehub
    freehub_upload(repo_path,get_complete_address('0'),overwrite=True)
    shutil.rmtree(repo_path)
    freehub_download('0',os.path.dirname(repo_path))
if __name__ == '__main__':
    test()







