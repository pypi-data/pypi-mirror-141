"""Provides base classes and implementations for `processors`.

Processor has the following three features based on AWS API access:
1. Retrieves AWS resource types supported by the processor
2. Retrieves configuration of all AWS resources belonging the above types, for CLI auto-completion.
3. Describes configuration of specific AWS resources searched by the given key-value query.

Processor is created per AWS API endpoint (e.g. describe_vpcs of ec2).
To create such processors, inherit ResourceTypeProcessor and implement abstract methods in it.
"""

import collections.abc
import contextlib
import json
import urllib.parse
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union, overload

import boto3
import boto3.session

from awsdsc.exception import AwsdscException


def AWS_access(f):
    """Decorator function for AWS access methods of ResourceTypeProcessor."""

    def _(self, *args, **kwargs):
        if not hasattr(self, "_initialized"):
            self._initialized = False
        if not self._initialized:
            try:
                self._init_client()
            except Exception as e:
                raise AwsdscException(
                    f"""The below exception occurs while initializing AWS clients.
Make sure your AWS credentials are properly setup.

{str(e)}"""
                )
            self._initialized = True
        return f(self, *args, **kwargs)

    return _


class ResourceTypeProcessor(ABC):
    @abstractmethod
    def __init__(self, session: boto3.session.Session = None):
        self.session = session

    @abstractmethod
    def _init_client(self):
        pass

    def _create_client(self, name: str):
        if self.session:
            return self.session.client(name)
        else:
            return boto3.client(name)

    @AWS_access
    def describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """Retrieves configuration of AWS resources searched by query composed by the given key-value pairs

        Args:
            key_vaules: key-value pairs for composing query
              For example, query is like "k1 == v1 and k2 == v2"
              where key_values = {"k1": "v1", "k2": "v2"}
        Returns:
            Configuration object of the searched AWS resources.
            It is a list if multiple resources found and otherwise dictionary.
        """
        return self._describe(key_values)

    @abstractmethod
    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """Almost same as describe method."""
        pass

    @AWS_access
    def list_candidates(self, typ: str) -> list[dict[str, str]]:
        """Retrieves all completion candidates of the given AWS resource type.

        Args:
            typ: AWS resource type (e.g. AWS::EC2::Instance)
        Returns:
            Completion candidate list.
            Each element of the list has a subset of fields of one AWS resource.
            For example:

            [
                {"name": "foo", "id": "foo_id"},
                {"name": "bar", "id": "bar_id"},
            ]

            Each key name, like name and id in the above example,
            is used for describe method parameters as it is.
        """
        return self._list_candidates(typ)

    @abstractmethod
    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        """Almost same as list_candidates method."""
        pass

    @AWS_access
    def list_types(self) -> list[str]:
        """List types supported by this processor."""
        result = self._list_types()
        if isinstance(result, str):
            return [result]
        return result

    @abstractmethod
    def _list_types(self) -> Union[str, list[str]]:
        """Almost same as list_types method."""
        pass

    def _application_order(self):
        return 0

    def __lt__(self, other):
        return self._application_order() < other._application_order()

    def _exec_with_next_token(  # nosec
        self,
        params: dict[str, Any],
        func: Callable[..., dict[str, Any]],
        postfunc: Callable[[dict[str, Any]], list],
        next_token_key: str = "NextToken",
        filter_func: Callable[[dict[str, Any]], bool] = None,
        next_token: str = None,
    ) -> list[dict[str, Any]]:
        """Call AWS API function with next_token.

        Args:
            params: Parameters for func
            func: AWS API function to execute
            postfunc: post-processing function for return value of func
            next_token_key: key name of next_token in return value of func
        Returns:
            A list of func results of multiple API calls.
        """
        if next_token:
            params[next_token_key] = next_token

        res = func(**params)
        results = postfunc(res)
        if filter_func:
            results = list(filter(filter_func, results))

        if next_token_key in res and res[next_token_key]:
            rs = self._exec_with_next_token(
                params,
                func,
                postfunc,
                next_token_key,
                filter_func,
                res[next_token_key],
            )
            results.extend(rs)

        return results

    @overload
    def _json_loads_recursively(self, obj: dict[str, Any]) -> dict[str, Any]:
        ...

    @overload
    def _json_loads_recursively(self, obj: list) -> list:
        ...

    def _json_loads_recursively(
        self,
        obj: Union[list, dict[str, Any]],
    ) -> Union[list, dict[str, Any]]:
        """Converts JSON string field to object recursively."""
        return self._map_nested_dicts(obj, self._json_loads_without_error)

    def _map_nested_dicts(self, obj: Any, func) -> Any:
        """Apply func to all fields of obj recursively."""
        if isinstance(obj, collections.abc.Mapping):
            return {k: self._map_nested_dicts(v, func) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._map_nested_dicts(e, func) for e in obj]
        return func(obj)

    def _json_loads_without_error(self, s):
        if isinstance(s, str):
            with contextlib.suppress(ValueError):
                return json.loads(urllib.parse.unquote(s))
        return s


class EventsRuleProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("events")

    def _describe(
        self, key_values: dict[str, str]
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        rule = self.client.describe_rule(**key_values)
        rule["EventPattern"] = json.loads(rule["EventPattern"])
        targets = self._describe_events_rule_targets(rule["Name"])
        return dict(rule, Targets=targets)

    def _describe_events_rule_targets(self, name: str):
        return self._exec_with_next_token(
            {"Rule": name},
            self.client.list_targets_by_rule,
            lambda r: r["Targets"],
        )

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {},
            self.client.list_rules,
            lambda r: [{"Name": d["Name"]} for d in r["Rules"]],
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::Events::Rule"


class Ec2Processor(ResourceTypeProcessor):
    def __init__(
        self,
        session: Optional[boto3.session.Session],
        data_label: str,
        key_value_labels: dict[str, str],
        describe_func: str,
        resource_type: str,
    ):
        super().__init__(session)
        self._data_label = data_label
        self._key_value_labels = key_value_labels
        self._describe_func = describe_func
        self._resource_type = resource_type

    def _init_client(self, session: boto3.session.Session = None):
        self.client = self._create_client("ec2")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        filters = [{"Name": k, "Values": [v]} for k, v in key_values.items()]
        return self._exec_with_next_token(
            {
                "Filters": filters,
                "MaxResults": 100,
            },
            getattr(self.client, self._describe_func),
            lambda r: r[self._data_label],
        )

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"MaxResults": 100},
            getattr(self.client, self._describe_func),
            self._post_process_list_candidates,
        )

    def _post_process_list_candidates(self, result: dict[str, Any]):
        cands = []
        for d in result[self._data_label]:
            cand = dict()
            for k, v in self._key_value_labels.items():
                if v in d:
                    cand[k] = d[v]
            if "Tags" in d:
                for t in d["Tags"]:
                    cand[f"tag:{t['Key']}"] = t["Value"]
            cands.append(cand)
        return cands

    def _list_types(self) -> Union[str, list[str]]:
        return self._resource_type


class Ec2VpcProcessor(Ec2Processor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(
            session,
            "Vpcs",
            {
                "cidr": "CidrBlock",
                "dhcp-options-id": "DhcpOptionsId",
                "owner-id": "OwnerId",
                "state": "State",
                "vpc-id": "VpcId",
            },
            "describe_vpcs",
            "AWS::EC2::VPC",
        )


class Ec2SubnetProcessor(Ec2Processor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(
            session,
            "Subnets",
            {
                "availability-zone": "AvailabilityZone",
                "availability-zone-id": "AvailabilityZoneId",
                "cidr-block": "CidrBlock",
                "outpost-arn": "OutpostArn",
                "owner-id": "OwnerId",
                "state": "State",
                "subnet-arn": "SubnetArn",
                "subnet-id": "SubnetId",
                "vpc-id": "VpcId",
            },
            "describe_subnets",
            "AWS::EC2::Subnet",
        )


class Ec2NetworkInterfacesProcessor(Ec2Processor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(
            session,
            "NetworkInterfaces",
            {
                "availability-zone": "AvailabilityZone",
                "group-id": "GroupId",
                "group-name": "GroupName",
                "mac-address": "MacAddress",
                "network-interface-id": "NetworkInterfaceId",
                "owner-id": "OwnerId",
                "private-ip-address": "PrivateIpAddress",
                "private-dns-name": "PrivateDnsName",
                "requester-id": "RequesterId",
                "status": "Status",
                "subnet-id": "SubnetId",
                "vpc-id": "VpcId",
            },
            "describe_network_interfaces",
            "AWS::EC2::NetworkInterface",
        )


class EcsClusterProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("ecs")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        return self.client.describe_clusters(clusters=[key_values["name"]])["clusters"]

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"maxResults": 100},
            self.client.list_clusters,
            lambda r: [
                {"name": d[d.rfind("/") + 1 :]} for d in r["clusterArns"]  # noqa: E203
            ],
            "nextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::ECS::Cluster"


class CodeArtifactDomainProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("codeartifact")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        return self.client.describe_domain(**key_values)["domain"]

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"maxResults": 100},
            self.client.list_domains,
            lambda r: [{"domain": d["name"]} for d in r["domains"]],
            "nextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::CodeArtifact::Domain"


class CodeArtifactRepositoryProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("codeartifact")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        return self.client.describe_repository(**key_values)["repository"]

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"maxResults": 100},
            self.client.list_repositories,
            lambda r: [
                {
                    "repository": d["name"],
                    "domain": d["domainName"],
                    "domainOwner": d["domainOwner"],
                }
                for d in r["repositories"]
            ],
            "nextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::CodeArtifact::Repository"


class CodeCommitRepositoryProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("codecommit")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        return self.client.get_repository(**key_values)

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {},
            self.client.list_repositories,
            lambda r: [
                {
                    "repositoryName": d["repositoryName"],
                }
                for d in r["repositories"]
            ],
            "nextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::CodeCommit::Repository"


class ApiGatewayV2DomainNameProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("apigatewayv2")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        return self.client.get_domain_name(**key_values)

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"MaxResults": "100"},
            self.client.get_domain_names,
            lambda r: [
                {
                    "DomainName": d["DomainName"],
                }
                for d in r["Items"]
            ],
            "NextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::ApiGatewayV2::DomainName"


class ApiGatewayV2VpcLinkProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("apigatewayv2")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        def _filter_func(d: dict[str, Any]) -> bool:
            for k, v in key_values.items():
                if k.startswith("tag:"):
                    name = k[4:]
                    if d["Tags"][name] != v:
                        return False
                else:
                    if d[k] != v:
                        return False
            return True

        return self._exec_with_next_token(
            {"MaxResults": "100"},
            self.client.get_vpc_links,
            lambda r: r["Items"],
            "NextToken",
            _filter_func,
        )

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        return self._exec_with_next_token(
            {"MaxResults": "100"},
            self.client.get_vpc_links,
            lambda r: [
                {
                    "Name": d["Name"],
                    **{f"tag:{t}": d["Tags"][t] for t in d["Tags"].keys()},
                }
                for d in r["Items"]
            ],
            "NextToken",
        )

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::ApiGatewayV2::VpcLink"


class ConfigConfigurationRecorderProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("config")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        params = {
            "ConfigurationRecorderNames": [key_values["name"]],
        }
        return self.client.describe_configuration_recorders(**params)[
            "ConfigurationRecorders"
        ]

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        res = self.client.describe_configuration_recorders()
        return [{"name": d["name"]} for d in res["ConfigurationRecorders"]]

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::Config::ConfigurationRecorder"


class ConfigDeliveryChannelProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session = None):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("config")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        params = {
            "DeliveryChannelNames": [key_values["name"]],
        }
        return self.client.describe_delivery_channels(**params)

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        res = self.client.describe_delivery_channels()
        return [{"name": d["name"]} for d in res["DeliveryChannels"]]

    def _list_types(self) -> Union[str, list[str]]:
        return "AWS::Config::DeliveryChannel"


class ConfigProcessor(ResourceTypeProcessor):
    def __init__(self, session: boto3.session.Session):
        super().__init__(session)

    def _init_client(self):
        self.client = self._create_client("config")

    def _describe(
        self,
        key_values: dict[str, str],
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        query_fields = [
            "tags",
            "configuration",
            "supplementaryConfiguration",
            "resourceType",
        ]

        where_statements = [
            f"{k} = '{v}'" for k, v in key_values.items() if not k.startswith("tag:")
        ]
        for k, v in key_values.items():
            if k.startswith("tag:"):
                where_statements.append(f"tags.tag = '{k[4:]}={v}'")
        where_statement = " AND ".join(where_statements)

        params = {
            "Expression": f"SELECT {', '.join(query_fields)} WHERE {where_statement}",
            "Limit": 100,
        }
        return self._exec_with_next_token(
            params,
            self.client.select_resource_config,
            self._post_process_describe,
        )

    def _post_process_describe(self, res: dict[str, Any]) -> list:
        results = res["Results"]
        results = [json.loads(r) for r in results]
        results = self._json_loads_recursively(results)
        for i, r in enumerate(results):
            del r["resourceType"]
            del r["tags"]
            result = r["configuration"]
            result.update(r["supplementaryConfiguration"])
            results[i] = result
        return results

    def _list_candidates(self, typ: str) -> list[dict[str, str]]:
        params = {
            "Expression": f"SELECT resourceName, resourceId, tags WHERE resourceType = '{typ}'",
            "Limit": 100,
        }
        return self._exec_with_next_token(
            params,
            self.client.select_resource_config,
            self._post_process_list_candidates,
        )

    def _post_process_list_candidates(self, res: dict[str, Any]):
        results = [json.loads(s) for s in res["Results"]]
        return [
            {
                "resourceName": d.get("resourceName"),
                "resourceId": d["resourceId"],
                **{f"tag:{t['key']}": t["value"] for t in d["tags"]},
            }
            for d in results
        ]

    def _list_types(self) -> Union[str, list[str]]:
        results = self.client.describe_configuration_recorders()

        types = []
        for recorder in results["ConfigurationRecorders"]:
            types.extend(recorder["recordingGroup"]["resourceTypes"])
        types = list(set(types))

        return types

    def _application_order(self):
        return 99
