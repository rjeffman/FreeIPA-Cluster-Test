FreeIPA-Cluster-Test Github Action
==================================

This actions creates a FreeIPA cluster using containers by executing [ipalab-config](https://pypi.org/project/ipalab-config) and run a set of playbook files.


Usage
=====

For the basic usage you must provide a cluster configuration file and a test playbook.

```yaml
- name: Test ipaserver
  uses: rjeffman/FreeIPA-Cluster-Test@v1.0.0
  with:
    cluster_configuration: tests/config/ipaserver_only.yml
    test_playbooks: tests/user/test_user.yml
```

The available input options are:

| Input parameter          | Description                            | Required |
| ----------------------- | --------------------------------------- | -------- |
| `cluster_configuration` | An ipalab-config cluster configuration. | yes      |
| `test_playbooks` | A space separated list of playbooks to be executed using the cluster. | yes |
| `distro`         | The default distro image to use. Defaults to `fedora-latest` | no |
| `ansible_vars`   | Path to a file with variables to be used when running the playbooks. | no |
| `ansible_requirements` | An Ansible requirements file for the test playbooks. | no |

An example usage in a workflow with a `distro` matrix and multiple test playbooks:

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
    matrix:
     test_distro:
       - fedora-latest
       - fedora-rawhide
       - c10s
    steps:
      - name: Clone the repository
        uses: actions/checkout@v4

      - name: Run FreeIPA tests
        uses: rjeffman/FreeIPA-Cluster-Test@v1.0.0
        with:
          cluster_configuration: tests/evironments/basic_cluster.yaml
          test_playbooks: >-
            tests/playbooks/test_hbac.yaml
            tests/playbooks/test_rbac.yaml
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
