# Migration Manager

Migration Manager (MM) is a very small utility that can list source servers in a target account
and apply mass launch template modifications.

## Usage

```bash
python3 mm.py -h 

usage: mm.py [-h] [-l] [-p PROFILE] [-s SOURCE_SERVERS] [-t TEMPLATE]

Migration Manager (MM) is a very small utility that can list source servers in a target account and apply mass
launch template modifications.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all source servers in account
  -p PROFILE, --profile PROFILE
                        AWS credential profile that targets a specific account
  -s SOURCE_SERVERS, --source-servers SOURCE_SERVERS
                        a newline separated file containing a list of source servers you want to apply a
                        template too
  -t TEMPLATE, --template TEMPLATE
                        a JSON template representing launch template data
```

List every source server in a staging account

```bash
python3 mm.py -l -p stage    

=== Listing Source Servers for: 662658670280 ===
s-36d8ff026f4727e24 ip-172-32-1-51 Linux_4.14.238-125.422.amzn1.x86_64 lt-047f04e87280e54a0
s-36e084716e5019998 EC2AMAZ-5T1JQQG Windows_64bit_version10.0 lt-0b2234ba79619d365
s-366b18033ca4a6e4e EC2AMAZ-895QHLB Windows_64bit_version10.0 lt-019ef4f6ded6dba5d
```

Apply a common launch configuration template to multiple source servers in a staging account

```bash
python3 mm.py -s c5-pool.txt -t c5-blueprint.json -p stage

=== Batch applying template updates to: 662658670280 ===
Set launch template lt-047f04e87280e54a0 default version to 25 with template from c5-blueprint.json
Set launch template lt-0b2234ba79619d365 default version to 15 with template from c5-blueprint.json
Set launch template lt-019ef4f6ded6dba5d default version to 15 with template from c5-blueprint.json
```