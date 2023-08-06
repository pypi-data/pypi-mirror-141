import json
import os.path
import requests
from typing import Union, Optional, Any, BinaryIO

from .auth import Auth
from .config import Profile
from .errors import AuthorizationError, UnrequestedScopeError, RequestedScopeError


class Client:
	def __init__(self, profile: Profile) -> None:
		self._baseUrl = f"https://{profile.server}"
		self._profile = profile
		self._auth = Auth(profile)

	@property
	def auth(self) -> Auth:
		return self._auth

	@property
	def profile(self) -> Profile:
		return self._profile

	def request(
			self,
			method: str,
			route: str,
			*,
			params: Optional[list[tuple[str, str]]] = None,
			data: Optional[str] = None,
			content_type: str = "application/json",
			fileName: Optional[str] = None,
			fileField: str = "file",
	) -> Union[list[Any], dict[str, Any], str]:
		"""Do the actual request

		Args:
			...

		Returns:
			...
		"""
		for tries in range(2):
			files: Optional[dict[str, tuple[str, str]]] = None
			fileObj: Optional[BinaryIO] = None

			headers: dict[str, str] = {
				"Content-Type": content_type,
				"Authorization": f"Bearer {self._auth.token}",
			}

			try:
				if fileName is not None:
					del headers["Content-Type"] # Automatically supplied by requests in this case
					fileObj = open(fileName, "rb")
					files = {
						fileField: (
							os.path.basename(fileName),
							fileObj,
						),
					}

				# Request with auth
				response = requests.request(
					method,
					f"{self._baseUrl}{route}",
					params=params,
					data=data,
					headers=headers,
					files=files,
				)
			finally:
				if fileObj is not None:
					fileObj.close()

			# if 401 auth
			if response.status_code == 401:
				try:
					error = response.json()
					if error["type"] == "InvalidSignature":
						# We should be able to automatically recover from this
						self._auth.refresh()
						continue
					if error["type"] == "MissingScope":
						# We can also recover from this, if that scope is in the profile but hasn't
						# been requested yet.
						if error["required"] not in self._auth.profileScope:
							# Cannot happen, config change required
							raise UnrequestedScopeError(error["required"], self._profile)
						elif error["required"] in self._auth.requestedScope:
							# Requested but apparently not granted, not going to happen either
							raise RequestedScopeError(error["required"], self._profile)
						else:
							# It is in the profile, not in requested, just refresh the token
							self._auth.refresh()
							continue
					raise AuthorizationError(json.dumps(error, indent=4))
				except (requests.JSONDecodeError, KeyError):
					raise AuthorizationError(response.text)

			# else return json/str
			try:
				return response.json()
			except requests.JSONDecodeError:
				return response.text
