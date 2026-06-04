# CLUS26-DEVNET-2619

Modular Ansible playbooks for Meraki firmware test automation: discover eligible upgrades,
schedule upgrades, create ServiceNow change requests, run pre-upgrade iperf3 tests, and
document results.

## Playbooks

| Playbook | Purpose |
|----------|---------|
| `playbooks/discover_firmware.yml` | Find network, apply release policy, pick next firmware upgrade |
| `playbooks/schedule_upgrade.yml` | Schedule Meraki upgrade (requires workflow state) |
| `playbooks/fetch_changelog.yml` | Match target version to Meraki Community RSS link |
| `playbooks/create_servicenow_change.yml` | CHG + CTASK creation |
| `playbooks/iperf_pre_upgrade.yml` | Run all iperf3 scenarios |
| `playbooks/post_iperf_to_change.yml` | Post iperf results to ServiceNow change task work notes |
| `playbooks/cancel_scheduled_upgrade.yml` | Revert scheduled upgrade |
| `playbooks/site.yml` | Full workflow (imports all playbooks in order) |

## Workflow state

Each step reads/writes `{{ workflow_state_dir }}/{{ workflow_run_id }}.json` so playbooks
can run standalone in Semaphore or chained via `site.yml`.

- Default local dir: `.workflow_state/` (gitignored)
- Semaphore: set `workflow_state_dir` to a persistent mount (e.g. `/var/semaphore/workflow_state`)

**Discover** generates `workflow_run_id` if omitted. Downstream playbooks require `-e workflow_run_id=...`.

## Getting started

```bash
ansible-galaxy collection install -r collections/requirements.yml

export MERAKI_DASHBOARD_API_KEY=yourKey
export MERAKI_ORG_ID=yourOrgId
export TEST_NETWORK_ID=L_655836695735845620
export SN_HOST=https://yourinstance.service-now.com
export SN_USERNAME=yourUser
export SN_PASSWORD=yourPassword
```

```bash
# Step 1 — discover (provide network id or tag)
ansible-playbook playbooks/discover_firmware.yml \
  -e test_org_id=$MERAKI_ORG_ID \
  -e test_product=wireless \
  -e test_network_id=YOUR_NETWORK_ID

# Step 2 — schedule (use workflow_run_id from discover output)
ansible-playbook playbooks/schedule_upgrade.yml \
  -e workflow_run_id=20250604T153045Z
```

## Survey / extra-vars (Discover)

| Variable | Required | Notes |
|----------|----------|-------|
| `test_org_id` | yes | Meraki organization ID |
| `test_product` | yes | `wireless`, `switch`, `appliance`, etc. |
| `test_network_id` | optional | Explicit network (highest priority); or set env `TEST_NETWORK_ID` |
| `test_network_tag` | optional | Filter by tag; or set env `TEST_NETWORK_TAG`; channel tags `stable`/`candidate`/`beta` |
| `test_network_type` | optional | `production` or `test` — fallback policy via `version_policies.yml` |
| `release_policy_override` | optional | Force `stable`, `candidate`, or `beta` channel |
| `workflow_run_id` | optional | Auto-generated on discover |

## Version comparison

Upgrades are filtered using the Meraki **`firmware`** slug (e.g. `wireless-32-1-5` → `32.1.5`),
not `id` or `shortName` alone. See plan docs for edge cases (downgrades in available list,
same-id duplicates, etc.).

## Semaphore

- **Variable Group secrets:** `MERAKI_DASHBOARD_API_KEY`, `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD`
- **Variable Group JSON:** `workflow_state_dir`, `snow_ci_class`, `test_network_id`, `pi_interfaces`, etc.
- **Or env vars:** `TEST_NETWORK_ID`, `MERAKI_ORG_ID`, `SN_*` (Semaphore forwards these to the Ansible process if configured on the template/runner)
- One task template per playbook; downstream templates only need `workflow_run_id` survey var
- Mount persistent storage at `workflow_state_dir` on the runner

## Inventory

Update `hosts` and `group_vars/all.yml` `pi_interfaces` for iperf3 tests.

## Resources

* [Meraki Ansible collection](https://docs.ansible.com/ansible/latest/collections/cisco/meraki/index.html)
* [ServiceNow ITSM collection](https://galaxy.ansible.com/ui/repo/published/servicenow/itsm/)
* [Semaphore survey variables](https://semaphoreui.com/docs/user-guide/task-templates/survey-vars)
