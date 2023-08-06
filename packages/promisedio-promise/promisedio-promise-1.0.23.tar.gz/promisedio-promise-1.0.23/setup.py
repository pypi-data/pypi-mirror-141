# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promisedio', 'promisedio.promise']

package_data = \
{'': ['*'], 'promisedio.promise': ['capsule/promisedio/*', 'clinic/*']}

setup_kwargs = {
    'name': 'promisedio-promise',
    'version': '1.0.23',
    'description': 'High-performance promise implementation for Python',
    'long_description': '> Despite the fact that this code is distributed under the MIT License, \n> IT IS PROHIBITED to use, copy, modify, merge, publish, distribute, sublicense,\n> and/or sell copies of the Software for any commercial or non-commercial purposes\n> by Jet Brains and any of its subsidiaries, parent organization or affiliates.\n\n<p align="center">\n    <img src="https://raw.githubusercontent.com/promisedio/promise/main/logo.svg" alt="PromisedIO" />\n</p>\n<p align="center">\n    <b>PromisedIO</b>\n</p>\n\n###### PromisedIO is free and open source software released under the permissive MIT license.\n\nYou can read about promises [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise).\n\n<!--- template:[promise] -->\n# promise module\n#### clearfreelists\n```python\nclearfreelists() -> None\n```\nClear all freelists.\n\n#### deferred\n```python\ndeferred() -> Deferred\n```\nCreate new [Deferred](#deferred) object.\n\n#### exec_async\n```python\nexec_async(coro: Coroutine, context: Any = None) -> None\n```\nStart new coroutine and set the `context` for the new coroutine.\n\n#### get_context\n```python\nget_context() -> Any\n```\nGet context of current corroutine.\n\n#### process_promise_chain\n```python\nprocess_promise_chain() -> int\n```\nProcess all scheduled (resolved or rejected) promises.\n\nReturns active promise count.\n\n#### run_forever\n```python\nrun_forever() -> None\n```\nStart simple event loop.\n\n#### setfreelistlimits\n```python\nsetfreelistlimits(promise_limit: int = -1, promiseiter_limit: int = -1, deferred_limit: int = -1, coroutine_limit: int = -1) -> None\n```\nUpdate freelist limits. Default limit for each type is 1024.\n\n### Deferred\n#### Deferred.promise\n```python\nDeferred.promise() -> Promise\n```\nGet related [Promise](#promise) object.\n\n#### Deferred.reject\n```python\nDeferred.reject(value: Exception) -> None\n```\nReject related [Promise](#promise) object with the given exception `value`.\n\n#### Deferred.resolve\n```python\nDeferred.resolve(value: Any) -> None\n```\nResolve related [Promise](#promise) object with the given `value`.\n\n### Lock\n#### Lock.__new__\n```python\nLock.__new__() -> Any\n```\nCreate new [Lock](#lock) object.\n\n#### Lock.acquire\n```python\nLock.acquire() -> Promise\n```\nAcquire the lock.\n\n#### Lock.release\n```python\nLock.release() -> Promise\n```\nRelease the lock.\n\n### Promise\n#### Promise.catch\n```python\nPromise.catch(rejected: Callable) -> Promise\n```\nThe same as `.then(None, rejected)`\n\n#### Promise.then\n```python\nPromise.then(fulfilled: Callable = None, rejected: Callable = None) -> Promise\n```\nCreate new [Promise](#promise).\n\nIt takes up to two arguments: callback functions for the success and failure cases of the promise.\n\n\n<!--- end:[promise] -->\n\n<!--- template:[PROMISE_API] -->\n<!--- end:[PROMISE_API] -->',
    'author': 'aachurin',
    'author_email': 'aachurin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/promisedio/promise',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
