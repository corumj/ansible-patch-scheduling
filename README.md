# ansible-advanced-scheduling
An advanced scheduling lookup to allow patching an arbitrary number of days after patch tuesday

## Instructions for using this lookup plugin

You'll need to either copy the patch_day.py file into your own lookup_plugins folder in your ansible workspace or clone this and modify the test.yml to your particular task.

Set the variable for the lookup:
```
vars:
  offset: 18
  patch_day: "{{ lookup('patch_day', '{{ offset }}') }}"
```
You can change the offset days to any number or '0' if you want to run the block on Patch Tuesday.

In your playbook, use a block to set a conditional for a range of tasks.
```
  tasks:
    - name: Run tasks if it's time 
      block:
        - debug: 
            msg: "Hello World"
      when: ansible_date_time['date'] == patch_day
```
