import argparse
from typing import List, TextIO
import boto3
import json
import sys

from dataclasses import dataclass
from argparse import ArgumentParser


@dataclass
class SourceServer:
    id: str
    hostname: str
    os: str
    template: str


def listSourceServers(mgn) -> List[SourceServer]:
    resp = mgn.describe_source_servers(filters={"isArchived": False})

    servers = []
    for server in resp["items"]:
        sid = server["sourceServerID"]
        hostname = server["sourceProperties"]["identificationHints"][
            "hostname"]
        os = server["sourceProperties"]["os"]["fullString"]

        r = mgn.get_launch_configuration(sourceServerID=sid)
        template = r["ec2LaunchTemplateID"]

        servers.append(SourceServer(sid, hostname, os, template))
    return servers


def batchCreateLaunchTemplateVersion(mgn, ec2, sourceServers: TextIO,
                                     template: TextIO):
    tmpl = json.load(template)

    for s in sourceServers:
        s = s.strip()

        r = mgn.get_launch_configuration(sourceServerID=s)
        templateId = r["ec2LaunchTemplateID"]

        r = ec2.create_launch_template_version(LaunchTemplateId=templateId,
                                               LaunchTemplateData=tmpl)
        version = r["LaunchTemplateVersion"]["VersionNumber"]

        r = ec2.modify_launch_template(LaunchTemplateId=templateId,
                                       DefaultVersion=str(version))

        print(
            f"Set launch template {templateId} default version to {version} with template from {template.name}"
        )


if __name__ == "__main__":

    parser = ArgumentParser(description="""
        Migration Manager (MM) is a very small utility that can list source servers in a target account
        and apply mass launch template modifications.
    """)

    parser.add_argument("-l",
                        "--list",
                        help="list all source servers in account",
                        action="store_true")
    parser.add_argument(
        "-p",
        "--profile",
        help="AWS credential profile that targets a specific account")
    parser.add_argument(
        "-s",
        "--source-servers",
        type=argparse.FileType("r"),
        help="a newline separated file containing a list of source servers you want to apply a template too"
    )
    parser.add_argument(
        "-t",
        "--template",
        type=argparse.FileType("r"),
        help="a JSON template representing launch template data")

    args = parser.parse_args()

    boto3.setup_default_session(profile_name="default")
    if args.profile:
        boto3.setup_default_session(profile_name=args.profile)

    account = boto3.client("sts").get_caller_identity().get("Account")
    mgn = boto3.client("mgn")
    ec2 = boto3.client("ec2")

    if args.list:
        print("=== Listing Source Servers for:", account, "===")
        for server in listSourceServers(mgn):
            print(server.id, server.hostname, server.os, server.template)
        sys.exit()

    if args.source_servers and args.template:
        print("=== Batch applying template updates to:", account, "===")
        batchCreateLaunchTemplateVersion(mgn, ec2, args.source_servers,
                                         args.template)
        sys.exit()
