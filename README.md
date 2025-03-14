FreeIPA-Cluster-Test Github Action
==================================

This actions creates a FreeIPA cluster using containers by executing [ipalab-config](https://pypi.org/project/ipalab-config) and run a set of playbook files.


Usage
-----

For the basic usage you must provide a cluster configuration file and a test playbook.

```yaml
- name: Test ipaserver deployment
  uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
  with:
    cluster_configuration: tests/config/ipaserver_only.yml
    test_playbooks: tests/user/test_user.yml
```

The available input options are:

| Input parameter          | Description                            | Required |
| ----------------------- | --------------------------------------- | -------- |
| `cluster_configuration` | An ipalab-config cluster configuration. | yes      |
| `test_playbooks` | A space separated list of playbooks to be executed using the cluster. | yes |
| `distro`         | The default distro image to use. Defaults to `fedora`. | no |
| `ansible_vars`   | Path to a file with variables to be used when running the playbooks. | no |
| `ansible_requirements` | An Ansible requirements file for the test playbooks. | no |
| `shutdown` | Shutdown the compose after tests are executed. Default is `false` to keep original behavior. | no |
| `ipalab_config_version` | The `ipalab-config` version to install. | no |
| `debug` | Run ipalab-config in debug mode. | no |

An example usage in a workflow with a `distro` matrix and multiple test playbooks:

```yaml
---
name: test-freeipa-matrix
run-name: Test FreeIPA using a Github Action and a Distro Matrix
on:
  - push
  - pull_request

jobs:
  test-freeipa-distros:
    name: Test distro matrix
    runs-on: ubuntu-24.04
    strategy:
      matrix:
       test_distro:
         - fedora-latest
         - fedora-rawhide
         - c10s
    steps:
      - name: Clone the repository
        uses: actions/checkout@v4

      - name: Run FreeIPA tests
        uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
        with:
          cluster_configuration: tests/environments/basic_cluster.yaml
          distro: ${{ matrix.test_distro }}
          test_playbooks: >-
            tests/playbooks/test_hbac.yaml
            tests/playbooks/test_rbac.yaml
          shutdown: true
```

Note that in the previous example it was used the folded strip block scalar `>-` that will produce a single line, space separated list of files.

A cluster configuration example (the file `tests/evironments/basic_cluster.yaml`) could be created as:

```yaml
ipa_deployments:
  - name: ipacluster
    domain: ipa.test
    admin_password: SomeADMINpassword
    dm_password: SomeDMpassword
    cluster:
      servers:
        - name: server
          capabilities: ["CA", "DNS", "KRA"]
        - name: replica
          capabilities: ["CA"]
      clients:
        - name: cli-01
```

**Using a custom ipalab-config version**

It is possible to use a specific `ipalab-config` version using a version specifier or a specific archive by setting the `ipalab_config_version`.

To pin `ipalab_config` version use:

```
  - name: Run FreeIPA tests
    uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
    with:
      cluster_configuration: tests/environments/basic_cluster.yaml
      test_playbooks: tests/playbooks/mytests.yaml
      ipalab_config_version: "ipalab-config==0.10.2"
```

To use a custom `ipalab_config` repository or development branch:

```
  - name: Run FreeIPA tests
    uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
    with:
      cluster_configuration: tests/environments/basic_cluster.yaml
      test_playbooks: tests/playbooks/mytests.yaml
      ipalab_config_version: "git+https://github.com/rjeffman/ipalab-config.git@main"
```

Testing without Ansible
-----------------------

The original goal of this action was to run Ansible playbooks to test software (mostly Ansible roles and modules), and this section shows an exampel on how to use this action with other testing frameworks.

```yaml
---
name: test-freeipa-action
run-name: Test FreeIPA using a Github Action
on:
  - push
  - pull_request

jobs:
  test-freeipa-hbac
    runs-on: ubuntu-24.04
    steps:
      - name: Clone the repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4

      - name: Install test dependencies
        run: |
          pip install coverage pytest

      - name: Run FreeIPA tests
        uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
        with:
          cluster_configuration: tests/evironments/basic_cluster.yaml

      - name: Test with pytest
        run: |
          podman unshare --rootless-netns coverage run -m pytest

      - name: Generate Coverage report
        run: |
          coverage report -m

      - name: Shutdown FreeIPA environment
        uses: rjeffman/FreeIPA-Cluster-Test@v1.3.0
        with:
          cluster_configuration: tests/evironments/basic_cluster.yaml
          shutdown: true
```

Note the use of `podman unshare --rootless-netns` to access the node namespace.
