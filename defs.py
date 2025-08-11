from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from dataclasses import field

@dataclass
class UserBasicInfo:
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    credentials: Optional['UserCredentials'] = None
    status: Optional['Status'] = None
    profile_picture: Optional[str] = None


@dataclass
class User(UserBasicInfo):
    role: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[Union[str, UserBasicInfo]] = None
    permissions: Optional[List[str]] = None


@dataclass
class UsersPage:
    users: List[User]
    total: int
    offset: int
    limit: int


@dataclass
class UserCredentials:
    username: Optional[str] = None
    secret: Optional[str] = None


@dataclass
class ClientCredentials:
    identity: Optional[str] = None
    secret: Optional[str] = None


@dataclass
class ClientBasicInfo:
    id: Optional[str] = None
    name: Optional[str] = None
    credentials: Optional[ClientCredentials] = None
    status: Optional['Status'] = None


QueryParamRoles = "roles"


@dataclass
class Client(ClientBasicInfo):
    tags: Optional[List[str]] = None
    domain_id: Optional[Union[str, 'DomainBasicInfo']] = None
    parent_group_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[Union[str, UserBasicInfo]] = None
    identity: Optional[str] = None
    parent_group_path: Optional[str] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    access_type: Optional[str] = None
    access_provider_id: Optional[str] = None
    access_provider_role_id: Optional[str] = None
    access_provider_role_name: Optional[str] = None
    access_provider_role_actions: Optional[List[str]] = None
    connection_types: Optional[List[str]] = None
    member_id: Optional[str] = None
    roles: Optional[List['MemberRoleActions']] = None


@dataclass
class ClientsPage:
    clients: List[Client]
    total: int
    offset: int
    limit: int


@dataclass
class GroupBasicInfo:
    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional['Status'] = None
    description: Optional[str] = None


@dataclass
class Group(GroupBasicInfo):
    domain_id: Optional[Union[str, 'DomainBasicInfo']] = None
    parent_id: Optional[Union[str, GroupBasicInfo]] = None
    metadata: Optional[Dict[str, Any]] = None
    level: Optional[int] = None
    path: Optional[str] = None
    children: Optional[List['Group']] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[Union[str, UserBasicInfo]] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    access_type: Optional[str] = None
    access_provider_id: Optional[str] = None
    access_provider_role_id: Optional[str] = None
    access_provider_role_name: Optional[str] = None
    access_provider_role_actions: Optional[List[str]] = None
    member_id: Optional[str] = None
    roles: Optional[List['MemberRoleActions']] = None


@dataclass
class GroupsPage:
    groups: List[Group]
    total: int
    offset: int
    limit: int


@dataclass
class HierarchyPageMeta:
    level: Optional[int] = None
    direction: Optional[int] = None  # ancestors (+1) or descendants (-1)
    # - `True`  - result is JSON tree representing groups hierarchy,
    # - `False` - result is JSON array of groups.
    tree: Optional[bool] = None


@dataclass
class HierarchyPage(HierarchyPageMeta):
    groups: List[Group] = field(default_factory=List)


@dataclass
class ChannelBasicInfo:
    id: Optional[str] = None
    name: Optional[str] = None
    status: Optional['Status'] = None


@dataclass
class Channel(ChannelBasicInfo):
    domain_id: Optional[Union[str, 'DomainBasicInfo']] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    parent_group_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    parent_group_path: Optional[str] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    access_type: Optional[str] = None
    access_provider_id: Optional[str] = None
    access_provider_role_id: Optional[str] = None
    access_provider_role_name: Optional[str] = None
    access_provider_role_actions: Optional[List[str]] = None
    connection_types: Optional[List[str]] = None
    member_id: Optional[str] = None
    roles: Optional[List['MemberRoleActions']] = None
    route: Optional[str] = None


@dataclass
class ChannelsPage:
    channels: List[Channel]
    total: int
    offset: int
    limit: int


@dataclass
class Login:
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class Token:
    access_token: str
    refresh_token: str
    access_type: Optional[str] = None


@dataclass
class DomainBasicInfo:
    id: Optional[str] = None
    name: Optional[str] = None
    route: Optional[str] = None
    status: Optional['Status'] = None


@dataclass
class Domain(DomainBasicInfo):
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    created_by: Optional[Union[str, UserBasicInfo]] = None
    updated_by: Optional[Union[str, UserBasicInfo]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    member_id: Optional[str] = None
    roles: Optional[List['MemberRoleActions']] = None


@dataclass
class DomainsPage:
    domains: List[Domain]
    total: int
    offset: int
    limit: int


@dataclass
class Permissions:
    permissions: List[str]


@dataclass
class Invitation:
    invited_by: Union[str, UserBasicInfo]
    invitee_user_id: Union[str, UserBasicInfo]
    domain_id: Union[str, DomainBasicInfo]
    domain_name: Optional[str] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None


@dataclass
class InvitationsPage:
    invitations: List[Invitation]
    total: int
    offset: int
    limit: int


@dataclass
class Response:
    status: int
    message: Optional[str] = None


class Status(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


@dataclass
class BasicPageMeta:
    total: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class PageMetadata(BasicPageMeta):
    order: Optional[str] = None
    dir: Optional[str] = None
    level: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    action: Optional[str] = None
    subject: Optional[str] = None
    object: Optional[str] = None
    tag: Optional[str] = None
    id: Optional[str] = None
    tree: Optional[bool] = None
    owner: Optional[str] = None
    shared_by: Optional[str] = None
    visibility: Optional[str] = None
    owner_id: Optional[str] = None
    topic: Optional[str] = None
    contact: Optional[str] = None
    state: Optional[str] = None
    list_perms: Optional[bool] = None
    invited_by: Optional[str] = None
    domain: Optional[str] = None
    user_id: Optional[str] = None
    relation: Optional[str] = None
    from_: Optional[int] = None  # 'from' is a Python keyword, so using 'from_'
    to: Optional[int] = None
    access_type: Optional[str] = None
    actions: Optional[List[str]] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    group: Optional[str] = None
    client: Optional[str] = None
    channel: Optional[str] = None
    connection_type: Optional[str] = None
    root_group: Optional[bool] = None


@dataclass
class MessagesPage:
    messages: List['SenMLMessage']
    total: int
    offset: int
    limit: int


@dataclass
class MessagesPageMetadata(PageMetadata):
    subtopic: Optional[str] = None
    publisher: Optional[Union[str, ClientBasicInfo]] = None
    protocol: Optional[str] = None
    comparator: Optional[str] = None
    vb: Optional[bool] = None
    vs: Optional[str] = None
    vd: Optional[str] = None
    aggregation: Optional[str] = None
    interval: Optional[str] = None
    v: Optional[int] = None


@dataclass
class SenMLMessage:
    channel: Optional[Union[str, ChannelBasicInfo]] = None
    subtopic: Optional[str] = None
    publisher: Optional[Union[str, ClientBasicInfo]] = None
    protocol: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    time: Optional[int] = None
    update_time: Optional[int] = None
    value: Optional[float] = None
    string_value: Optional[str] = None
    data_value: Optional[str] = None
    bool_value: Optional[bool] = None
    sum: Optional[float] = None


@dataclass
class Cert:
    client_id: Optional[str] = None
    cert_serial: Optional[str] = None
    client_key: Optional[str] = None
    client_cert: Optional[str] = None
    expiration: Optional[str] = None


@dataclass
class CertsPage:
    certs: List[Cert]
    total: int
    offset: int
    limit: int


@dataclass
class BootstrapConfig:
    channels: Optional[List[str]] = None
    external_id: Optional[str] = None
    external_key: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    name: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None
    ca_cert: Optional[str] = None
    content: Optional[str] = None
    state: Optional[int] = None
    encrypted_bootstrap: Optional[str] = None
    decrypted_key: Optional[str] = None
    encrypted_buffer: Optional[str] = None
    decrypted: Optional[str] = None


@dataclass
class BootstrapPage:
    configs: List[BootstrapConfig]
    total: int
    offset: int
    limit: int


@dataclass
class JournalsPageMetadata(PageMetadata):
    operation: Optional[str] = None
    with_metadata: Optional[bool] = None
    with_attributes: Optional[bool] = None


@dataclass
class Journal:
    id: Optional[str] = None
    operation: Optional[str] = None
    occurred_at: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


@dataclass
class JournalsPage:
    journals: List[Journal]
    total: int
    offset: int
    limit: int


@dataclass
class HealthInfo:
    status: str
    version: str
    commit: str
    description: str
    build_time: str
    instance_id: str


@dataclass
class Role:
    id: Optional[str] = None
    name: Optional[str] = None
    entity_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


@dataclass
class RoleProvision(Role):
    optional_actions: Optional[List[str]] = None
    optional_members: Optional[List[str]] = None


@dataclass
class RolePage:
    roles: List[Role]
    total: int
    offset: int
    limit: int


@dataclass
class MemberRoleActions:
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    access_provider_id: Optional[str] = None
    access_provider_path: Optional[str] = None
    access_type: Optional[str] = None


@dataclass
class MemberRoles:
    member_id: Optional[str] = None
    roles: Optional[List[MemberRoleActions]] = None


@dataclass
class MemberRolesPage:
    members: List[MemberRoles]
    total: int
    offset: int
    limit: int


@dataclass
class MembersRolePageQuery:
    total: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_by: Optional[str] = None
    dir: Optional[str] = None
    access_provider_id: Optional[str] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    actions: Optional[List[str]] = None
    access_type: Optional[str] = None


@dataclass
class EntityActionRole:
    entity_id: Optional[str] = None
    action: Optional[str] = None
    role_id: Optional[str] = None


@dataclass
class EntityMemberRole:
    entity_id: Optional[str] = None
    member_id: Optional[str] = None
    role_id: Optional[str] = None


@dataclass
class MembersPage:
    members: List[str]
    total: int
    offset: int
    limit: int


class OutputType(str, Enum):
    CHANNELS = "channels"
    SAVE_SENML = "save_senml"
    ALARMS = "alarms"
    EMAIL = "email"
    SAVE_REMOTE_PG = "save_remote_pg"


@dataclass
class Script:
    type: int
    value: str


class Recurring(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = "none"


@dataclass
class Schedule:
    start_datetime: str
    time: str
    recurring: Recurring
    recurring_period: int


class RuleStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    DELETED = "deleted"
    ALL = "all"
    UNKNOWN = "unknown"


@dataclass
class Rule:
    id: Optional[str] = None
    name: Optional[str] = None
    domain: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    input_channel: Optional[str] = None
    input_topic: Optional[str] = None
    logic: Optional[Script] = None
    outputs: Optional[List['Output']] = None
    schedule: Optional[Schedule] = None
    status: Optional[RuleStatus] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


@dataclass
class Output:
    type: OutputType


@dataclass
class ChannelOutput(Output):
    channel: Union[str, ChannelBasicInfo]
    topic: Optional[str] = None


@dataclass
class EmailOutput(Output):
    to: List[str]
    subject: Optional[str] = None
    content: Optional[str] = None


@dataclass
class PostgresDBOutput(Output):
    host: str
    port: int
    user: str
    password: str
    database: str
    table: str
    mapping: Optional[str] = None


@dataclass
class RulesPageMetadata:
    total: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    dir: Optional[str] = None
    name: Optional[str] = None
    input_channel: Optional[str] = None
    status: Optional[RuleStatus] = None
    tag: Optional[str] = None


@dataclass
class RulesPage(RulesPageMetadata):
    rules: List[Rule] = field(default_factory=List)


@dataclass
class ClientTelemetry:
    client_id: str
    domain_id: str
    subscriptions: int
    inbound_messages: int
    outbound_messages: int
    first_seen: datetime
    last_seen: datetime


@dataclass
class InvitationPageMeta(BasicPageMeta):
    invited_by: Optional[str] = None
    invitee_user_id: Optional[str] = None
    domain_id: Optional[str] = None
    role_id: Optional[str] = None
    invited_by_or_user_id: Optional[str] = None
    state: Optional[str] = None


class EntityType(str, Enum):
    GROUPS = "groups"
    CHANNELS = "channels"
    CLIENTS = "clients"
    DOMAINS = "domains"
    USERS = "users"
    DASHBOARDS = "dashboards"
    MESSAGES = "messages"


class Operation(str, Enum):
    CREATE = "create"
    READ = "read"
    LIST = "list"
    UPDATE = "update"
    DELETE = "delete"
    SHARE = "share"
    UNSHARE = "unshare"
    PUBLISH = "publish"
    SUBSCRIBE = "subscribe"


@dataclass
class Scope:
    id: Optional[str] = None
    pat_id: Optional[str] = None
    entity_type: Optional[EntityType] = None
    optional_domain_id: Optional[str] = None
    operation: Optional[Operation] = None
    entity_id: Optional[str] = None


class PatStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    ALL = "all"


@dataclass
class PAT:
    id: Optional[str] = None
    user: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    secret: Optional[str] = None
    scope: Optional[List[Scope]] = None
    status: Optional[PatStatus] = None
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    revoked: Optional[bool] = None
    revoked_at: Optional[datetime] = None


@dataclass
class PATsPage:
    pats: List[PAT]
    total: int
    offset: int
    limit: int


@dataclass
class ScopesPage:
    scopes: List[Scope]
    total: int
    offset: int
    limit: int


@dataclass
class PatPageMeta(BasicPageMeta):
    status: Optional[PatStatus] = None
    name: Optional[str] = None
    id: Optional[str] = None


@dataclass
class ScopesPageMeta(BasicPageMeta):
    pat_id: Optional[str] = None
    id: Optional[str] = None


class AlarmStatus(str, Enum):
    ACTIVE = "active"
    CLEARED = "cleared"
    ALL = "all"


@dataclass
class Alarm:
    id: Optional[str] = None
    rule_id: Optional[str] = None
    domain_id: Optional[str] = None
    channel_id: Optional[str] = None
    client_id: Optional[str] = None
    subtopic: Optional[str] = None
    measurement: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    threshold: Optional[str] = None
    cause: Optional[str] = None
    status: Optional[AlarmStatus] = None
    severity: Optional[int] = None
    assignee_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    assigned_at: Optional[datetime] = None
    assigned_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AlarmsPage:
    offset: int
    limit: int
    total: int
    alarms: List[Alarm]


@dataclass
class AlarmPageMeta(BasicPageMeta):
    domain_id: Optional[str] = None
    channel_id: Optional[str] = None
    client_id: Optional[str] = None
    subtopic: Optional[str] = None
    rule_id: Optional[str] = None
    status: Optional[AlarmStatus] = None
    assignee_id: Optional[str] = None
    severity: Optional[int] = None
    updated_by: Optional[str] = None
    assigned_by: Optional[str] = None
    acknowledged_by: Optional[str] = None
    resolved_by: Optional[str] = None


@dataclass
class Report:
    metric: 'Metric'
    messages: List[SenMLMessage]


@dataclass
class Metric:
    channel_id: Union[str, ChannelBasicInfo]
    client_id: Optional[Union[str, ClientBasicInfo]] = None
    name: Optional[str] = None
    subtopic: Optional[str] = None
    protocol: Optional[str] = None
    format: Optional[str] = None


@dataclass
class ReqMetric:
    channel_id: Union[str, ChannelBasicInfo]
    client_ids: Optional[List[Union[str, ClientBasicInfo]]] = None
    name: Optional[str] = None
    subtopic: Optional[str] = None
    protocol: Optional[str] = None
    format: Optional[str] = None


class Format(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    ALL = "AllFormats"


@dataclass
class ReportFile:
    name: Optional[str] = None
    data: Optional[List[int]] = None
    format: Optional[Format] = None


@dataclass
class ReportPage:
    total: int
    from_: Optional[datetime] = None  # 'from' is a Python keyword
    to: Optional[datetime] = None
    aggregation: Optional['AggConfig'] = None
    reports: List[Report] = field(default_factory=List)
    file: Optional[ReportFile] = None


class Aggregation(str, Enum):
    NONE = "none"
    MAX = "max"
    MIN = "min"
    SUM = "sum"
    COUNT = "count"
    AVG = "avg"


@dataclass
class AggConfig:
    agg_type: Optional[Aggregation] = None
    interval: Optional[str] = None


@dataclass
class MetricConfig:
    title: Optional[str] = None
    from_: Optional[str] = None  # 'from' is a Python keyword
    to: Optional[str] = None
    aggregation: Optional[AggConfig] = None
    file_format: Optional[Format] = None


@dataclass
class EmailSetting:
    to: Optional[List[str]] = None
    subject: Optional[str] = None
    content: Optional[str] = None


@dataclass
class ReportConfig:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    domain_id: Optional[str] = None
    schedule: Optional[Schedule] = None
    config: Optional[MetricConfig] = None
    email: Optional[EmailSetting] = None
    metrics: Optional[List[ReqMetric]] = None
    report_template: Optional[str] = None
    status: Optional[Status] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


@dataclass
class ReportConfigPage:
    offset: int
    limit: int
    total: int
    report_configs: List[ReportConfig]


@dataclass
class Template:
    html_template: str