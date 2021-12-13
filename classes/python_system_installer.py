# coding: utf-8
# encoding: utf-8

"""
    Python class to create directory for Python Project
    Architecture should be:
        - /home/<account>/workspace/
    Python directory should be : .../workspace/python
    Odoo directories should be :
        - .../workspace/python/odoo
            - v8
                - community
                - common
                - odoo8
            - v9
            - ...
"""
import os
import subprocess

MAX_VERSION = 16


class PythonSystemInstaller:
    _install_dir = False
    _python_dir = 'Python'
    _workspace_dir = 'workspace'
    _odoo_dir = 'Odoo'

    def __init__(self, install_directory):
        self._install_dir = install_directory

    """
        Function to create workspace directory.
    """
    def _create_workspace_dir(self):
        workspace_dir = os.path.join(self._install_dir, '') + self._workspace_dir
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)

    """
        Function to create python directory.
    """
    def _create_python_dir(self):
        python_dir = os.path.join(self._install_dir, '') + \
                     os.path.join(self._workspace_dir, '') + \
                     self._python_dir
        if not os.path.exists(python_dir):
            os.makedirs(python_dir)

    """
        Function to create Odoo directory + each version of Odoo.
    """
    def _create_odoo_dir(self):
        odoo_dir = os.path.join(self._install_dir, '') + \
                   os.path.join(self._workspace_dir, '') + \
                   os.path.join(self._python_dir, '') + \
                   os.path.join(self._odoo_dir)

        if not os.path.exists(odoo_dir):
            os.makedirs(odoo_dir)

        # Create directory for each version of Odoo.
        i = 8
        for i in range(i, MAX_VERSION):
            odoo_version = os.path.join(odoo_dir, '') + 'v' + str(i)
            if not os.path.exists(odoo_version):
                os.makedirs(odoo_version)
            i += 1

    def _get_odoo_dir(self):
        return os.path.join(self._install_dir, '') + \
            os.path.join(self._workspace_dir, '') + \
            os.path.join(self._python_dir, '') + \
            os.path.join(self._odoo_dir, '')

    def _get_version_odoo_dir(self):
        odoo_dir = self._get_odoo_dir()

    """
        Function to clone repository
    """
    @staticmethod
    def _git_cloning_repo(git_repo, name_directory=False, branch=False):
        command = 'git clone %s' % git_repo
        command += ' --depth=1'
        command += ' --single-branch'
        if branch:
            command += ' --branch %s' % str(branch)
        command += ' ' + name_directory
        subprocess.call(command, shell=True)

    """
        Function to prepare the clone repository of common
    """
    def _git_cloning_common(self, odoo_version):
        repo = 'git@gitlab.ndp-systemes.fr:odoo-addons/common-modules.git'
        dir_to_use = self._get_odoo_dir() + \
            os.path.join('v%s' % odoo_version, '') + \
            'common%s' % odoo_version
        if not os.path.exists(dir_to_use):
            self._git_cloning_repo(repo, dir_to_use, float(odoo_version))
        else:
            print('Directory exists : %s.' % dir_to_use)

    """
        Function to prepare the clone repository of community
    """
    def _git_cloning_community(self, odoo_version):
        repo = 'git@gitlab.ndp-systemes.fr:odoo-addons/community-addons.git'
        dir_to_use = self._get_odoo_dir() + \
            os.path.join('v%s' % odoo_version, '') + \
            'community%s' % odoo_version
        if not os.path.exists(dir_to_use):
            self._git_cloning_repo(repo, dir_to_use, float(odoo_version))
        else:
            print('Directory exists : %s.' % dir_to_use)

    """
        Function to install System.
    """
    def install_system(self):
        self._create_workspace_dir()
        self._create_python_dir()
        self._create_odoo_dir()

        # cloning common + community
        for i in range(8, MAX_VERSION):
            self._git_cloning_common(i)
            self._git_cloning_community(i)
