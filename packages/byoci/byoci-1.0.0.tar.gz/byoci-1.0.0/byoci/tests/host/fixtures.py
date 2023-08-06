# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import shutil


from byoci.host import config
from byoci.tests import fixtures
from byoci.tests.host import (
    assertions,
    features,
)
from byov import (
    config as vms_config,
    subprocesses,
)


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


# Make sure user (or system) defined environment variables do not leak in the
# test environment.
isolated_environ = {
    'HOME': None,
}


def isolate_from_disk_for_host(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup so tests can setup arbitrary files including
    config ones.
    """
    # Preserve some options from the outer environment
    outer = config.VmStack(None)
    # FIXME: One place to fix to better handle sso/ldap launchpad/gitlab
    # -- vila 2018-08-08
    lp_login = outer.get('launchpad.login')
    gl_login = outer.get('gitlab.login')
    # If there is a gitlab test server
    # FIXME: hard-coded vm name -- vila 2018-09-19
    gitlab_conf = config.VmStack('gitlab')
    if features.gitlab_test_server.available():
        gitlab_api_url = gitlab_conf.get('gitlab.api.url')
    else:
        gitlab_api_url = ''
    # FIXME: These options are badly named (not precise enough) and not stored
    # in the right place -- vila 2018-08-07
    ldap_user = outer.get('ldap.user')
    ldap_password = outer.get('ldap.password')
    ssh_key = outer.get('ssh.key')
    fixtures.set_uniq_cwd(test)
    # Share the lxd certificate. We could generate one on the fly but assume
    # instead that one is already available since we require the lxc client
    # already.
    lxd_conf_dir = os.path.expanduser('~/.config/lxc')
    # Isolate tests from the user environment
    fixtures.isolate_from_env(test, isolated_environ)
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    fixtures.override_env(test, 'BZR_HOME', test.home_dir)
    fixtures.override_env(test, 'LXD_CONF', lxd_conf_dir)
    fixtures.set_bzr_identity(test)
    inner = config.VmStack(None)
    inner.set('byoci', 'selftest')
    # Inject preserved options
    inner.set('launchpad.login', lp_login)
    inner.set('gitlab.login', gl_login)
    inner.set('gitlab.api.url', gitlab_api_url)
    # FIXME: Make sure those are truly optional -- vila 2018-11-23
    if ldap_user:
        inner.set('ldap.user', ldap_user)
    if ldap_password:
        inner.set('ldap.password', ldap_password)
    inner.set('ssh.key', ssh_key)
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir,
                                vms_config.system_config_dir()[1:])
    os.makedirs(test.etc_dir)
    fixtures.patch(test, vms_config, 'system_config_dir',
                   lambda: test.etc_dir)
    # Pre-define some vm names to be unique
    test.master_name = 'brz-master-selftest-{}'.format(os.getpid())
    inner.set('selftest.master', test.master_name)
    test.monitor_name = 'brz-monitor-selftest-{}'.format(os.getpid())
    inner.set('selftest.monitor', test.monitor_name)
    test.slave_name = 'brz-slave-selftest-{}'.format(os.getpid())
    # A single slave will do
    inner.set('selftest.slaves', test.slave_name)
    # Source access
    inner.set('selftest.host.definition', BRANCH_ROOT)
    # Saving the config creates the missing dirs (~/.config/byov) in the tmp
    # test dir
    inner.store.save()
    inner.store.unload()
    return outer, inner


def setup_byoci_conf(test):
    """Setup byoci selftest config files.

    This allows tests to get access to all vm definitions composing a byoci
    setup.
    """
    features.test_requires(test, features.tests_config)
    os.symlink(os.path.join(BRANCH_ROOT, 'byov.conf'), 'byov.conf')
    etc_confd_dir = os.path.join(test.etc_dir, 'conf.d')
    os.mkdir(etc_confd_dir)
    os.mkdir('byov.conf.d')
    os.symlink(os.path.join(BRANCH_ROOT,
                            'byov.conf.d/selftest.conf-tests'),
               os.path.join('byov.conf.d', 'selftest.conf'))
    os.symlink(os.path.join(BRANCH_ROOT,
                            'byov.conf.d/byov.py'),
               os.path.join('byov.conf.d', 'byov.py'))

    # Make user provided test config files visible to tests by installing them
    # under self.home_dir/.config/byov/conf.d
    user_confd_dir = os.path.join(test.home_dir, '.config', 'byov', 'conf.d')
    os.makedirs(user_confd_dir)

    def install(src, dst):
        with open(src) as s, open(dst, 'w') as d:
            d.write(s.read())
    # Since ~/.config/byov/byov.conf is easier to use for test themselves, it
    # makes sense to divert the outer ~/.config/byov/byov.conf to
    # /etc/byov/byov.conf
    install(features.tests_config.user_path,
            os.path.join(etc_confd_dir, config.config_file_basename()))
    if features.tests_config.more_paths:
        for p in features.tests_config.more_paths:
            _, bname = os.path.split(p)
            # Drop the -tests suffix from the basename
            install(p, os.path.join(user_confd_dir, bname[:-len('-tests')]))

    # FIXME: Relative paths for scripts are still a blurry area in byov,
    # here the setup scripts needs to be available from the current directory
    # (rather than relative to the configuration file), so a symlink will do
    # -- vila 2017-12-18
    os.symlink(os.path.join(BRANCH_ROOT, 'setup'), 'setup')
    # Same for testing scripts
    os.symlink(os.path.join(BRANCH_ROOT, 'testing'), 'testing')
    # byov.py want to import from byoci
    os.symlink(os.path.join(BRANCH_ROOT, 'byoci'), 'byoci')


def setup_secrets(test):
    """Duplicate existing secrets so tests can delete/create them."""
    conf = config.VmStack(None)
    orig = conf.get('selftest.host.secrets')
    shutil.copytree(orig, 'secrets')
    conf.set('selftest.host.secrets', os.path.join(test.uniq_dir, 'secrets'))
    conf.store.save()
    conf.store.unload()


def setup_vm(test, vm_name):
    test.addCleanup(teardown_vm, test, vm_name)
    cmd = ['byovm', 'setup', vm_name]
    ret, out, err = subprocesses.run(cmd)
    assertions.assertShellSuccess(test, cmd, ret, out, err)
    return ret


def teardown_vm(test, vm_name):
    cmd = ['byovm', 'teardown', '--force', vm_name]
    ret, out, err = subprocesses.run(cmd)
    test.out.write(out)
    test.err.write(err)
    return ret


# FIXME: Hiding the dependency on the vm names doesn't sound like a good idea,
# better to call setup_vm in the tests themselves -- vila 2018-10-20
def setup_master(test):
    return setup_vm(test, test.master_name)


def teardown_master(test):
    return teardown_vm(test, test.master_name)


def setup_monitor(test):
    return setup_vm(test, test.monitor_name)


def teardown_monitor(test):
    return teardown_vm(test, test.monitor_name)


def setup_slave(test):
    return setup_vm(test, test.slave_name)


def teardown_slave(test):
    return teardown_vm(test, test.slave_name)


# Useful shortcuts to export
override_logging = fixtures.override_logging
