# CLEMEA26-DEVNET-2619

This Ansible playbook check's a test organization and network for available firmware upgrades, compares those available versions against a defined policy for that product type and then schedules a designated test network for upgrade. It also runs pre-upgrade throughput tests and documents the results in a ticket that was created to track the firmware upgrade.

This is a small-scale example of firmware automation possible using the Meraki Ansible colletcion, but this can be extended to any number of networks or organizations.

# Getting Started

The playbook uses several environment variables, as well as some static variables used for development and testing.

You will need to configure your own env variables, such as:
*  `export MERAKI_DASHBOARD_API_KEY=yourKey`
*  `export MERAKI_ORG_ID=orgID`
*  `export FRESHDESK_API_KEY=yourKey`
*  `export FRESHDESK_DOMAIN=yourDomain`


Static variables for the iperf client / server will need to be replaced and interface IPs updated.

# How to build on this

* Uncomment the 'Gather Meraki Organizations' task and use its response to dynamically set the test_org_id variable.
* Modify the 'Get firmware versions for each network' task to loop over a list of organization IDs extracted from the 'Gather Meraki Organizations' task
* Replace the FreshDesk tasks with your own ticketing system
* Add additional throughput tests (e.g. inter-VLAN tests, reverse the direction of the tests, add UDP tests)
* Define acceptance criteria for the tests in a .yml file to read into the playbook
  * Define pass / fail / needs review thresholds to auto-close the firmware upgrade ticket
* Re-run the iperf tests after the scheduled firmware upgrade and document those in the ticket
* Add additional pre / post upgrade checks and post those to the ticket (e.g. wireless assurance data) to check for differences in user outcomes


# Resources
* [Meraki API documentation](https://developer.cisco.com/meraki/api-v1/)
* [Meraki Postman collections](https://www.postman.com/meraki-api?tab=collections)
* [Meraki Python SDK](https://github.com/meraki/dashboard-api-python) / [DevNet learning lab](https://developer.cisco.com/learning/modules/intro-meraki-python-sdk/)
* [Meraki Ansible collection](https://docs.ansible.com/ansible/latest/collections/cisco/meraki/index.html) / [DevNet learning lab](https://developer.cisco.com/learning/labs/meraki-dashboard-ansible/introduction/)
* [DevNet Code Exchange](https://developer.cisco.com/codeexchange/search/?products=Meraki)
