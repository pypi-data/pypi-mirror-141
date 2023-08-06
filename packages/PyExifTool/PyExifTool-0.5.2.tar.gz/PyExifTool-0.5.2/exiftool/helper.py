# -*- coding: utf-8 -*-
# PyExifTool <http://github.com/sylikc/pyexiftool>
# Copyright 2021 Kevin M (sylikc)

# More contributors in the CHANGELOG for the pull requests

# This file is part of PyExifTool.
#
# PyExifTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the licence, or
# (at your option) any later version, or the BSD licence.
#
# PyExifTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING.GPL or COPYING.BSD for more details.

"""

This contains a helper class, which makes it easier to use the low-level ExifTool class

.. note::
	:py:class:`exiftool.helper.ExifToolHelper` class of this submodule is available in the ``exiftool`` namespace as :py:class:`exiftool.ExifToolHelper`

"""

import logging

from .exiftool import ExifTool
from .exceptions import OutputEmpty, OutputNotJSON, ExifToolExecuteError

try:        # Py3k compatibility
	basestring
except NameError:
	basestring = (bytes, str)


#from pathlib import PurePath  # Python 3.4 required

from typing import Any, Union, Optional, List, Dict




# ======================================================================================================================


def _is_iterable(in_param: Any) -> bool:
	"""
	Checks if this item is iterable, instead of using isinstance(list), anything iterable can be ok

	NOTE: STRINGS ARE CONSIDERED ITERABLE by Python

	if you need to consider a code path for strings first, check that before checking if a parameter is iterable via this function
	"""
	# a different type of test of iterability, instead of using isinstance(list)
	# https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
	try:
		iterator = iter(in_param)
	except TypeError:
		return False

	return True



# ======================================================================================================================

class ExifToolHelper(ExifTool):
	"""
	This class extends the low-level :py:class:`exiftool.ExifTool` class with 'wrapper'/'helper' functionality

	It keeps low-level core functionality with the base class but extends helper functions in a separate class
	"""

	##########################################################################################
	#################################### OVERRIDE METHODS ####################################
	##########################################################################################

	# ----------------------------------------------------------------------------------------------------------------------
	def __init__(self, auto_start: bool = True, check_execute: bool = True, **kwargs) -> None:
		"""
		:param bool auto_start: Will automatically start the exiftool process on first command run, defaults to True
		:param bool check_execute: Will check the exit status (return code) of all commands.  This catches some invalid commands passed to exiftool subprocess, defaults to True

		all other parameters are passed directly to super-class' constructor: :py:meth:`exiftool.ExifTool.__init__()`
		"""
		# call parent's constructor
		super().__init__(**kwargs)

		self._auto_start: bool = auto_start
		self._check_execute: bool = check_execute


	# ----------------------------------------------------------------------------------------------------------------------
	def execute(self, *params) -> str:
		"""
		Override the :py:meth:`exiftool.ExifTool.execute()` method

		Adds logic to auto-start if not running, if auto_start == True

		:raises ExifToolExecuteError: If :py:attr:`check_execute` == True, and exit status was non-zero
		"""
		if self._auto_start and not self.running:
			self.run()

		result: str = super().execute(*params)

		# imitate the subprocess.run() signature.  check=True will check non-zero exit status
		if self._check_execute and self._last_status:
			raise ExifToolExecuteError(self._last_status, self._last_stdout, self._last_stderr, params)

		return result

	# ----------------------------------------------------------------------------------------------------------------------
	def run(self) -> None:
		"""
		override the :py:meth:`exiftool.ExifTool.run()` method

		Adds logic to check if already running.  Will not attempt to run if already running (so no warning about 'ExifTool already running' will trigger) """
		if self.running:
			return

		super().run()


	# ----------------------------------------------------------------------------------------------------------------------
	def terminate(self, **opts) -> None:
		"""
		override the :py:meth:`exiftool.ExifTool.terminate()` method

		Adds logic to check if not running (so no warning about 'ExifTool not running' will trigger)

		opts are passed directly to the parent verbatim
		"""
		if not self.running:
			return

		super().terminate(**opts)


	########################################################################################
	#################################### NEW PROPERTIES ####################################
	########################################################################################

	# ----------------------------------------------------------------------------------------------------------------------
	@property
	def check_execute(self) -> bool:
		"""
		Flag to enable/disable checking exit status (return code) on execute

		If enabled, will raise :py:exc:`exiftool.exceptions.ExifToolExecuteError` if a non-zero exit status is returned during :py:meth:`execute()`

		.. warning::
			While this property is provided to give callers an option to enable/disable error checking, it is generally **NOT** recommended to disable ``check_execute``.

			**If disabled, exiftool will fail silently, and hard-to-catch bugs may arise.**

			That said, there may be some use cases where continue-on-error behavior is desired.

		:getter: Returns current setting
		:setter: Enable or Disable the check

			.. note::
				This settings can be changed any time and will only affect subsequent calls

		:type: bool
		"""
		return self._check_execute

	@check_execute.setter
	def check_execute(self, new_setting: bool) -> None:
		self._check_execute = new_setting



	# ----------------------------------------------------------------------------------------------------------------------



	#####################################################################################
	#################################### NEW METHODS ####################################
	#####################################################################################


	# all generic helper functions will follow a convention of
	# function(files to be worked on, ... , params=)


	# ----------------------------------------------------------------------------------------------------------------------
	def get_metadata(self, files: Union[str, List], params: Optional[Union[str, List]] = None) -> List:
		"""
		Return all metadata for the given files.

		:param files: Files parameter matches :py:meth:`get_tags()`

		:param params: Optional parameters to send to *exiftool*
		:type params: list or None

		:return: The return value will have the format described in the documentation of :py:meth:`get_tags()`.
		"""
		return self.get_tags(files, None, params=params)


	# ----------------------------------------------------------------------------------------------------------------------
	def get_tags(self, files: Union[str, List], tags: Optional[Union[str, List]], params: Optional[Union[str, List]] = None) -> List:
		"""
		Return only specified tags for the given files.

		:param files: File(s) to be worked on.

			If a ``str`` is provided, it will get tags for a single file

			If an interable is provided, the list is copied and any non-basestring elements are converted to str (to support ``PurePath`` and other similar objects)

			.. warning::
				Currently, filenames are NOT checked for existence, that is left up to the caller.

				Wildcard strings are valid and passed verbatim to exiftool.

				However, exiftool's globbing is different than Python's globbing.  Read `ExifTool Common Mistakes - Over-use of Wildcards in File Names`_ for more info

		:type files: str or list


		:param tags: Tag(s) to read.  If tags is None, or [], method will returns all tags

			.. note::
				The tag names may include group names, as usual in the format ``<group>:<tag>``.

		:type tags: str, list, or None


		:param params: Optional parameter(s) to send to *exiftool*
		:type params: str, list, or None


		:return: The format of the return value is the same as for :py:meth:`exiftool.ExifTool.execute_json()`.


		:raises ValueError: Invalid Parameter
		:raises TypeError: Invalid Parameter
		:raises ExifToolExecuteError: If :py:attr:`check_execute` == True, and exit status was non-zero


		.. _ExifTool Common Mistakes - Over-use of Wildcards in File Names: https://exiftool.org/mistakes.html#M2

		"""

		final_tags:  Optional[List] = None
		final_files: Optional[List] = None

		if tags is None:
			# all tags
			final_tags = []
		elif isinstance(tags, basestring):
			final_tags = [tags]
		elif _is_iterable(tags):
			final_tags = tags
		else:
			raise TypeError(f"{self.__class__.__name__}.get_tags: argument 'tags' must be a str/bytes or a list")

		if not files:
			# Exiftool process would return None anyways
			raise ValueError(f"{self.__class__.__name__}.get_tags: argument 'files' cannot be empty")
		elif isinstance(files, basestring):
			final_files = [files]
		elif not _is_iterable(files):
			final_files = [str(files)]
		else:
			# duck-type any iterable given, and str() it
			# this was originally to support Path() but it's now generic to support any object that str() to something useful

			# Thanks @jangop for the single line contribution!
			final_files = [x if isinstance(x, basestring) else str(x) for x in files]

			# TODO: this list copy could be expensive if the input is a very huge list.  Perhaps in the future have a flag that takes the lists in verbatim without any processing?

		exec_params: List = []

		if params:
			if isinstance(params, basestring):
				# if params is a string, append it as is
				exec_params.append(params)
			elif _is_iterable(params):
				# this is done to avoid accidentally modifying the reference object params
				exec_params.extend(params)
			else:
				raise TypeError(f"{self.__class__.__name__}.get_tags: argument 'params' must be a str or a list")

		# tags is always a list by this point.  It will always be iterable... don't have to check for None
		exec_params.extend([f"-{t}" for t in final_tags])

		exec_params.extend(final_files)

		try:
			ret = self.execute_json(*exec_params)
		except OutputEmpty:
			raise
			#raise RuntimeError(f"{self.__class__.__name__}.get_tags: exiftool returned no data")
		except OutputNotJSON:
			raise
		except ExifToolExecuteError:
			# if last_status is <> 0, raise an error that one or more files failed?
			raise

		return ret


	# ----------------------------------------------------------------------------------------------------------------------
	def set_tags(self, files: Union[str, List], tags: Dict, params: Optional[Union[str, List]] = None):
		"""
		Writes the values of the specified tags for the given file(s).

		:param files: File(s) to be worked on.

			If a ``str`` is provided, it will set tags for a single file

			If an interable is provided, the list is copied and any non-basestring elements are converted to str (to support ``PurePath`` and other similar objects)

			.. warning::
				Currently, filenames are NOT checked for existence, that is left up to the caller.

				Wildcard strings are valid and passed verbatim to exiftool.

				However, exiftool's globbing is different than Python's globbing.  Read `ExifTool Common Mistakes - Over-use of Wildcards in File Names`_ for more info

		:type files: str or list


		:param tags: Tag(s) to write.

			Dictionary keys = tags, values = str or list

			If a value is a str, will set key=value
			If a value is a list, will iterate over list and set each individual value to the same tag (

			.. note::
				The tag names may include group names, as usual in the format ``<group>:<tag>``.

			.. note::
				Value of the dict can be a list, in which case, the tag will be passed with each item in the list, in the order given

				This allows setting things like ``-Keywords=a -Keywords=b -Keywords=c`` by passing in ``tags={"Keywords": ['a', 'b', 'c']}``

		:type tags: dict


		:param params: Optional parameter(s) to send to *exiftool*
		:type params: str, list, or None


		:return: The format of the return value is the same as for :py:meth:`execute()`.


		:raises ValueError: Invalid Parameter
		:raises TypeError: Invalid Parameter
		:raises ExifToolExecuteError: If :py:attr:`check_execute` == True, and exit status was non-zero


		.. _ExifTool Common Mistakes - Over-use of Wildcards in File Names: https://exiftool.org/mistakes.html#M2

		"""
		final_files: Optional[List] = None

		if not files:
			# Exiftool process would return None anyways
			raise ValueError(f"{self.__class__.__name__}.set_tags: argument 'files' cannot be empty")
		elif isinstance(files, basestring):
			final_files = [files]
		elif not _is_iterable(files):
			final_files = [str(files)]
		else:
			# duck-type any iterable given, and str() it
			# this was originally to support Path() but it's now generic to support any object that str() to something useful
			final_files = [x if isinstance(x, basestring) else str(x) for x in files]
			# TODO: this list copy could be expensive if the input is a very huge list.  Perhaps in the future have a flag that takes the lists in verbatim without any processing?

		if not tags:
			raise ValueError(f"{self.__class__.__name__}.set_tags: argument 'tags' cannot be empty")
		elif not isinstance(tags, dict):
			raise TypeError(f"{self.__class__.__name__}.set_tags: argument 'tags' must be a dict")


		exec_params: List = []

		if params:
			if isinstance(params, basestring):
				# if params is a string, append it as is
				exec_params.append(params)
			elif _is_iterable(params):
				# this is done to avoid accidentally modifying the reference object params
				exec_params.extend(params)
			else:
				raise TypeError(f"{self.__class__.__name__}.get_tags: argument 'params' must be a str or a list")


		for tag, value in tags.items():
			# contributed by @daviddorme in https://github.com/sylikc/pyexiftool/issues/12#issuecomment-821879234
			# allows setting things like Keywords which require separate directives
			# > exiftool -Keywords=keyword1 -Keywords=keyword2 -Keywords=keyword3 file.jpg
			# which are not supported as duplicate keys in a dictionary
			if isinstance(value, list):
				for item in value:
					exec_params.append(f"-{tag}={item}")
			else:
				exec_params.append(f"-{tag}={value}")

		exec_params.extend(final_files)

		try:
			return self.execute(*exec_params)
			#TODO if execute returns data, then error?
		except ExifToolExecuteError:
			# last status non-zero
			raise


	# ----------------------------------------------------------------------------------------------------------------------
