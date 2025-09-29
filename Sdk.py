from .users import Users
from .domains import Domains
from .certs import Certs
from .groups import Groups
from .channels import Channels
from .messages import Messages
from .bootstrap import Bootstrap
from .journals import Journals
from .health import Health
from .clients import Clients
from .rules import Rules
from .pats import PATs
from .alarms import Alarms
from .reports import Reports

# Import all type definitions
from .defs import *

DEFAULT_URL = "http://localhost"


class SDK:
    """Main SDK class that provides access to all Magistrala services."""
    
    def __init__(
        self,
        users_url: str = DEFAULT_URL,
        channels_url: str = DEFAULT_URL,
        domains_url: str = DEFAULT_URL,
        clients_url: str = DEFAULT_URL,
        groups_url: str = DEFAULT_URL,
        certs_url: str = DEFAULT_URL,
        readers_url: str = DEFAULT_URL,
        http_adapter_url: str = DEFAULT_URL,
        bootstrap_url: str = DEFAULT_URL,
        journal_url: str = DEFAULT_URL,
        rules_url: str = DEFAULT_URL,
        reports_url: str = DEFAULT_URL,
        auth_url: str = DEFAULT_URL,
        alarms_url: str = DEFAULT_URL,
    ):
        """
        Initializes the SDK with the provided URLs for various services.
        Args:
            users_url: URL for user-related operations.
            channels_url: URL for channel-related operations.
            domains_url: URL for domain-related operations.
            clients_url: URL for client-related operations.
            groups_url: URL for group-related operations.
            certs_url: URL for certificate-related operations.
            readers_url: URL for message readers.
            http_adapter_url: URL for HTTP adapter operations.
            bootstrap_url: URL for bootstrap operations.
            journal_url: URL for journal operations.
            rules_url: URL for rules management.
            reports_url: URL for report generation.
            auth_url: URL for authentication services.
            alarms_url: URL for alarm management.
        """
        self.users_url = users_url
        self.channels_url = channels_url
        self.domains_url = domains_url
        self.clients_url = clients_url
        self.groups_url = groups_url
        self.certs_url = certs_url
        self.readers_url = readers_url
        self.http_adapter_url = http_adapter_url
        self.bootstrap_url = bootstrap_url
        self.journal_url = journal_url
        self.rules_url = rules_url
        self.reports_url = reports_url
        self.auth_url = auth_url
        self.alarms_url = alarms_url


        self.users = Users(users_url=self.users_url, clients_url=self.clients_url)
        self.domains = Domains(domains_url=self.domains_url)
        self.clients = Clients(clients_url=self.clients_url)
        self.certs = Certs(certs_url=self.certs_url)
        self.groups = Groups(groups_url=self.groups_url)
        self.channels = Channels(channels_url=self.channels_url)
        self.messages = Messages(
            readers_url=self.readers_url,
            http_adapter_url=self.http_adapter_url
        )
        self.bootstrap = Bootstrap(bootstrap_url=self.bootstrap_url)
        self.journals = Journals(journal_url=self.journal_url)
        self.health = Health(
            users_url=self.users_url,
            clients_url=self.clients_url,
            channels_url=self.channels_url,
            bootstrap_url=self.bootstrap_url,
            certs_url=self.certs_url,
            readers_url=self.readers_url,
            http_adapter_url=self.http_adapter_url,
            journal_url=self.journal_url,
            domains_url=self.domains_url,
            groups_url=self.groups_url,
            auth_url=self.auth_url,
        )
        self.rules = Rules(rules_url=self.rules_url)
        self.reports = Reports(reports_url=self.reports_url)
        self.pats = PATs(auth_url=self.auth_url)
        self.alarms = Alarms(alarms_url=self.alarms_url)