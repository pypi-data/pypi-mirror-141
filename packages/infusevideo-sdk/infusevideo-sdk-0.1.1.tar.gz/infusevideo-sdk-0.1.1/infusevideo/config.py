import configparser
from pydantic import BaseSettings, ValidationError, validator
import os
from typing import Optional, Literal, Any

from .errors import ConfigurationError, ConfigAlreadyExists, ConfigNotFound, InvalidScopeError
from .scope import resolve_scope


class Profile(BaseSettings):
	name: str
	server: str = "api.infuse.video"
	auth: Literal["m2m", "human"] = "human"
	scope_type: Literal["account", "global"] = "account"
	organization: Optional[str] = None
	m2m_id: Optional[str] = None
	m2m_secret: Optional[str] = None
	scope: str
	auth_server: str = "infuse-video.eu.auth0.com"
	auth_client_id: str = "FZk0cmoF9orL9IJ9s3EQA5ZgT2IeOXRP"
	auth_audience: str = "infuse-api"

	@validator("scope_type")
	def global_no_m2m(cls, scope_type: str, values: dict[str, Any]) -> str:
		if scope_type == "global" and values.get("auth", None) == "m2m":
			raise AssertionError(
				"At this moment, scope_type = global is not compatible with auth = m2m. "
				"Use auth = human instead."
			)
		return scope_type

	@validator("organization")
	def organization_if_account(
			cls,
			organization: Optional[str],
			values: dict[str, Any],
	) -> Optional[str]:
		if values.get("scope_type", None) == "account" and organization is None:
			raise ValueError("This field must be defined")
		return organization

	@validator("m2m_id", "m2m_secret")
	def m2m_if_m2m(cls, m2m_cred: Optional[str], values: dict[str, Any]) -> Optional[str]:
		if values.get("auth", None) == "m2m" and m2m_cred is None:
			raise ValueError("This field must be defined when auth = m2m")
		return m2m_cred

	@validator("scope")
	def resolve_scope(cls, scope: str) -> str:
		try:
			resolved = resolve_scope(set(scope.split()))
			return " ".join(sorted(resolved))
		except InvalidScopeError as e:
			raise ValueError(str(e))


class Config:
	_configDir = os.path.join(os.path.expanduser("~"), ".infusevideo")
	_configFilename = "config"

	@classmethod
	def filename(cls, filename: str) -> str:
		return os.path.join(cls._configDir, filename)

	@classmethod
	def generate_sample_config(cls, organization: str) -> str:
		# Check if config does not exist
		configPath = cls.filename(cls._configFilename)
		if os.path.exists(configPath):
			raise ConfigAlreadyExists(configPath)

		# Create default config
		defaultConfig = [
			"[settings]",
			"defaultProfile = default",
			"",
			"[profile-default]",
			"# The organization to authenticate with. Looks like org_abcdef...",
			f"organization = {organization}",
			"# What scope to request. Can be multiple, space-separated.",
			"scope = read write",
			"# What type of authentication to use. Options: human, m2m",
			"#auth = human",
			"# When using m2m auth, specify the id and secret here",
			"#m2m_id = ",
			"#m2m_secret = ",
		]
		if not os.path.exists(cls._configDir):
			os.mkdir(cls._configDir)
		with open(configPath, "wt") as f:
			f.write("\n".join(defaultConfig))
			f.write("\n")
		return configPath

	def __init__(self, disableHumanAuth: bool = False):
		self._configPath = self.filename(self._configFilename)
		if not os.path.exists(self._configPath):
			raise ConfigNotFound(self._configPath)
		self._config = configparser.ConfigParser()
		self._config.read(self.configPath)
		self._disableHumanAuth = disableHumanAuth

	@property
	def configPath(self) -> str:
		return self._configPath

	@property
	def defaultProfile(self) -> str:
		try:
			return self._config["settings"]["defaultProfile"]
		except KeyError:
			return "default"

	def get_profile(self, name: str) -> Profile:
		try:
			profile = Profile(name=name, **self._config[f"profile-{name}"])
			if self._disableHumanAuth and profile.auth == "human":
				raise ConfigurationError(
					f"Requested human auth be disabled, but profile {name} has human auth set.",
				)
			return profile
		except KeyError:
			raise ConfigurationError(f"Profile {name!r} not defined in configuration file")
		except ValidationError as e:
			raise ConfigurationError(f"Invalid profile {name!r}: {e}")
