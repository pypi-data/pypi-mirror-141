> Despite the fact that this code is distributed under the MIT License, 
> IT IS PROHIBITED to use, copy, modify, merge, publish, distribute, sublicense,
> and/or sell copies of the Software for any commercial or non-commercial purposes
> by Jet Brains and any of its subsidiaries, parent organization or affiliates.

<p align="center">
    <img src="https://raw.githubusercontent.com/promisedio/promise/main/logo.svg" alt="PromisedIO" />
</p>
<p align="center">
    <b>PromisedIO</b>
</p>

###### PromisedIO is free and open source software released under the permissive MIT license.

You can read about promises [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise).

<!--- template:[promise] -->
# promise module
#### clearfreelists
```python
clearfreelists() -> None
```
Clear all freelists.

#### deferred
```python
deferred() -> Deferred
```
Create new [Deferred](#deferred) object.

#### exec_async
```python
exec_async(coro: Coroutine, context: Any = None) -> None
```
Start new coroutine and set the `context` for the new coroutine.

#### get_context
```python
get_context() -> Any
```
Get context of current corroutine.

#### process_promise_chain
```python
process_promise_chain() -> int
```
Process all scheduled (resolved or rejected) promises.

Returns active promise count.

#### run_forever
```python
run_forever() -> None
```
Start simple event loop.

#### setfreelistlimits
```python
setfreelistlimits(promise_limit: int = -1, promiseiter_limit: int = -1, deferred_limit: int = -1, coroutine_limit: int = -1) -> None
```
Update freelist limits. Default limit for each type is 1024.

### Deferred
#### Deferred.promise
```python
Deferred.promise() -> Promise
```
Get related [Promise](#promise) object.

#### Deferred.reject
```python
Deferred.reject(value: Exception) -> None
```
Reject related [Promise](#promise) object with the given exception `value`.

#### Deferred.resolve
```python
Deferred.resolve(value: Any) -> None
```
Resolve related [Promise](#promise) object with the given `value`.

### Lock
#### Lock.__new__
```python
Lock.__new__() -> Any
```
Create new [Lock](#lock) object.

#### Lock.acquire
```python
Lock.acquire() -> Promise
```
Acquire the lock.

#### Lock.release
```python
Lock.release() -> Promise
```
Release the lock.

### Promise
#### Promise.catch
```python
Promise.catch(rejected: Callable) -> Promise
```
The same as `.then(None, rejected)`

#### Promise.then
```python
Promise.then(fulfilled: Callable = None, rejected: Callable = None) -> Promise
```
Create new [Promise](#promise).

It takes up to two arguments: callback functions for the success and failure cases of the promise.


<!--- end:[promise] -->

<!--- template:[PROMISE_API] -->
<!--- end:[PROMISE_API] -->