// Copyright (c) 2021-2022 Andrey Churin <aachurin@gmail.com> Promisedio

/*[capsule:name PROMISE_API]*/
/*[capsule:output capsule/promisedio/]*/

/*[capsule:copy]*/
#include <promisedio.h>

typedef PyObject *(*promisecb)(PyObject *value, PyObject *promise);
typedef void (*unlockloop)(void* ctx);

enum {
    PROMISE_INITIAL = 0x0000,
    PROMISE_FULFILLED = 0x0001,
    PROMISE_REJECTED = 0x0002,
    PROMISE_RESOLVING = 0x0004,
    PROMISE_RESOLVED = 0x0008,
    PROMISE_INTERIM = 0x0010,
    PROMISE_C_CALLBACK = 0x0020,
    PROMISE_PY_CALLBACK = 0x0040,
    PROMISE_VALUABLE = 0x0100
};

enum {
    PROMISE_HAS_CALLBACK = (PROMISE_C_CALLBACK | PROMISE_PY_CALLBACK),
    PROMISE_SCHEDULED = (PROMISE_FULFILLED | PROMISE_REJECTED),
    PROMISE_FREEZED = (PROMISE_RESOLVING | PROMISE_RESOLVED)
};

#define PROMISE_PUBLIC_FIELDS   \
    PyObject_HEAD               \
    Chain_NODE(Promise);        \
    PyObject *ctx;              \
    void *timer;                \
    char data[24];              \
    int flags;

typedef struct promise_s Promise;

Py_LOCAL_INLINE(PyObject *)
Py_NewError(PyObject *exception, const char *msg)
{
    PyObject *value = PyUnicode_FromString(msg);
    if (!value)
        return NULL;
    PyObject *exc = PyObject_CallOneArg(exception, value);
    Py_DECREF(value);
    return exc;
}

Py_LOCAL_INLINE(PyObject *)
Py_FetchError()
{
    PyObject *exc, *val, *tb;
    PyErr_Fetch(&exc, &val, &tb);
    if (exc == NULL)
        return NULL;
    PyErr_NormalizeException(&exc, &val, &tb);
    if (tb != NULL) {
        PyException_SetTraceback(val, tb);
        Py_DECREF(tb);
    }
    Py_DECREF(exc);
    return val;
}

/*[capsule:endcopy]*/

typedef struct {
    Chain_ROOT(Promise)
} Promisechain;

typedef struct coroutine_s Coroutine;

typedef struct {
    /* Promise chain */
    Promisechain promisechain;
    /* Types */
    PyTypeObject *PromiseType;
    PyTypeObject *DeferredType;
    PyTypeObject *PromiseiterType;
    PyTypeObject *CoroutineType;
    PyTypeObject *LockType;
    PyTypeObject *QueueType;
    PyObject *EventType;
    PyObject *NoArgs;
    PyObject *print_stack;
    /* Current coroutine */
    Coroutine *current_coro;
    /* Callback */
    int in_chain_routine;
    unlockloop unlockloop_func;
    void *unlockloop_ctx;
    /* State */
    PyObject *await_event;
    Py_ssize_t promise_count;
    /* Freelists */
    Freelist_GC_HEAD(PromiseType)
    Freelist_GC_HEAD(DeferredType)
    Freelist_GC_HEAD(PromiseiterType)
    Freelist_GC_HEAD(CoroutineType)
} _modulestate;

struct promise_s {
    PROMISE_PUBLIC_FIELDS
    PyObject *fulfilled;
    PyObject *rejected;
    Coroutine *coro;
    PyObject *value;
    _ctx_var;
    Chain_ROOT(Promise)
};

/*[capsule:copy]*/
#ifdef CAPSULE_PROMISE_API
struct promise_s {
    PROMISE_PUBLIC_FIELDS
};

Py_LOCAL_INLINE(int)
Promise_WasScheduled(Promise *promise)
{
    return (promise->flags & PROMISE_SCHEDULED) != 0;
}

Py_LOCAL_INLINE(void *)
Promise_Data(Promise *promise)
{
    return &(promise->data);
}

#define Promise_DATA(promise, type) \
    ((type *) Promise_Data(promise))


Py_LOCAL_INLINE(PyObject *)
Promise_GetCtx(Promise *promise)
{
    return promise->ctx;
}

Py_LOCAL_INLINE(PyObject *)
Promise_SetCtx(Promise *promise, PyObject *ctx)
{
    PyObject *ret = promise->ctx;
    promise->ctx = ctx;
    return ret;
}
#endif
/*[capsule:endcopy]*/

typedef struct {
    PyObject_HEAD
    Promise *promise;
    _ctx_var;
} Deferred;

typedef struct {
    PyObject_HEAD
    Promise *promise;
    _ctx_var;
} Promiseiter;

typedef struct coroutine_s {
    PyObject_HEAD
    PyObject *coro;
    PyObject *context;
    Promise *promise;
    _ctx_var;
} Coroutine;

typedef struct {
    PyObject_HEAD
    PyObject *ctx;
    int locked;
    _ctx_var;
    Chain_ROOT(Promise)
} Lock;

typedef struct {
    PyObject_HEAD
} NoArgs;

#include "clinic/promise.c.h"

/*[clinic input]
module promise
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=c425861e022a97bb]*/

/*[clinic input]
promise.clearfreelists -> object(typed="None")

Clear all freelists.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_clearfreelists_impl(PyObject *module)
/*[clinic end generated code: output=3376cbbe518b4304 input=c1d768a2525f8a4b]*/
{
    _CTX_set_module(module);
    Freelist_GC_Clear(PromiseType);
    Freelist_GC_Clear(DeferredType);
    Freelist_GC_Clear(PromiseiterType);
    Freelist_GC_Clear(CoroutineType);
    Py_RETURN_NONE;
}

/*[clinic input]
promise.setfreelistlimits -> object(typed="None")
    promise_limit: Py_ssize_t = -1
    promiseiter_limit: Py_ssize_t = -1
    deferred_limit: Py_ssize_t = -1
    coroutine_limit: Py_ssize_t = -1

Update freelist limits. Default limit for each type is 1024.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_setfreelistlimits_impl(PyObject *module, Py_ssize_t promise_limit,
                               Py_ssize_t promiseiter_limit,
                               Py_ssize_t deferred_limit,
                               Py_ssize_t coroutine_limit)
/*[clinic end generated code: output=5b0fc0bd4a92ef56 input=f60e0abc9fbfd39a]*/
{
    _CTX_set_module(module);
    if (promise_limit >= 0) {
        Freelist_GC_Limit(PromiseType, promise_limit);
    }
    if (promiseiter_limit >= 0) {
        Freelist_GC_Limit(PromiseiterType, promiseiter_limit);
    }
    if (deferred_limit >= 0) {
        Freelist_GC_Limit(DeferredType, deferred_limit);
    }
    if (coroutine_limit >= 0) {
        Freelist_GC_Limit(CoroutineType, coroutine_limit);
    }
    Py_RETURN_NONE;
}

Py_LOCAL(void)
print_unhandled_exception_from_dealloc(PyObject *value)
{
    PySys_WriteStderr("Unhandled promise rejection:\n");
    if (value) {
        PyObject *error_type, *error_value, *error_traceback;
        PyErr_Fetch(&error_type, &error_value, &error_traceback);
        PyObject *exc = PyExceptionInstance_Class(value);
        PyObject *tb = PyException_GetTraceback(value);
        if (!tb)
            tb = Py_NewRef(Py_None);
        PyErr_Display(exc, value, tb);
        PySys_WriteStderr("\n");
        PyException_SetTraceback(value, Py_None);
        Py_DECREF(tb);
        PyErr_Restore(error_type, error_value, error_traceback);
    } else {
        PySys_WriteStderr("lost exception value\n");
    }
}

/* Start loop and set scheduler hook and ctx*/
CAPSULE_API(int)
Promise_StartLoop(_ctx_var, unlockloop unlock_func, void *ctx)
{
    if (S(unlockloop_func)) {
        PyErr_SetString(PyExc_RuntimeError, "The loop is already running.");
        return -1;
    }
    S(unlockloop_func) = unlock_func;
    S(unlockloop_ctx) = ctx;
    return 0;
}

/* Set scheduler loop release hook */
CAPSULE_API(int)
Promise_StopLoop(_ctx_var, unlockloop unlock_func, void *ctx)
{
    if (S(unlockloop_func) || S(unlockloop_ctx)) {
        if (unlock_func != S(unlockloop_func) || ctx != S(unlockloop_ctx))
            return -1;
        S(unlockloop_func) = NULL;
        S(unlockloop_ctx) = NULL;
        return 0;
    }
    return -1;
}

/* Create new Promise object */
CAPSULE_API(Promise *)
Promise_New(_ctx_var)
{
    Promise *self = (Promise *) Freelist_GC_New(PromiseType);
    if (!self)
        return NULL;
    Chain_INIT(self);
    Chain_NODEINIT(self);
    self->value = NULL;
    self->coro = NULL;
    self->flags = PROMISE_INITIAL;
    self->fulfilled = NULL;
    self->rejected = NULL;
    self->ctx = NULL;
    self->timer = NULL;
    _CTX_save(self);
    PyTrack_MarkAllocated(self);
    PyObject_GC_Track(self);
    S(promise_count)++;
    LOG("promise_count=%zd", S(promise_count));
    return self;
}

/* Internal method for future use. */
CAPSULE_API(void)
Promise_Callback(Promise *self, promisecb fulfilled, promisecb rejected)
{
    assert(!(self->flags & (PROMISE_HAS_CALLBACK | PROMISE_FREEZED)));
    self->flags |= PROMISE_C_CALLBACK;
    self->fulfilled = (PyObject *) fulfilled;
    self->rejected = (PyObject *) rejected;
}

CAPSULE_API(void)
Promise_PyCallback(Promise *self, PyObject *fulfilled, PyObject *rejected)
{
    assert(!(self->flags & (PROMISE_HAS_CALLBACK | PROMISE_FREEZED)));
    self->flags |= PROMISE_PY_CALLBACK;
    PyTrack_XINCREF(fulfilled);
    PyTrack_XINCREF(rejected);
    self->fulfilled = fulfilled;
    self->rejected = rejected;
}

#define schedule_promise(self, val, flag, invoke_callback)                      \
do {                                                                            \
    PyTrack_INCREF(val);                                                        \
    (self)->value = val;                                                        \
    (self)->flags |= (flag);                                                    \
    Py_INCREF(self);                                                            \
    Chain_APPEND(&S(promisechain), self);                                       \
    if ((invoke_callback) && (!(S(in_chain_routine))) && S(unlockloop_func)) {  \
        S(unlockloop_func)(S(unlockloop_ctx));                                  \
    }                                                                           \
    S(promise_count)--;                                                         \
    LOG("schedule_promise(%p, invoke_callback=%d): promise_count=%zd",          \
        self, invoke_callback, S(promise_count));                               \
} while (0)

/* Create a new resolved promise, steals value reference */
CAPSULE_API(Promise *)
Promise_NewResolved(_ctx_var, PyObject *value, PyObject *func)
{
    Promise *promise = Promise_New(_ctx);
    if (promise) {
        if (value == NULL) {
            schedule_promise(promise, S(NoArgs), PROMISE_FULFILLED, 0);
        } else if (Py_IsNone(value)) {
            schedule_promise(promise, Py_None, PROMISE_FULFILLED, 0);
        } else {
            schedule_promise(promise, value, PROMISE_FULFILLED, 0);
            Py_DECREF(value);
        }
        if (func) {
            Promise_PyCallback(promise, func, NULL);
        }
        return promise;
    }
    return NULL;
}

/* Create a new promise derived from the given. */
CAPSULE_API(Promise *)
Promise_Then(Promise *self)
{
    _CTX_set(self);
    Promise *promise = Promise_New(_ctx);
    if (!promise)
        return NULL;
    self->flags |= PROMISE_VALUABLE;
    if (self->flags & PROMISE_RESOLVED) {
        schedule_promise(promise, self->value, (self->flags & PROMISE_SCHEDULED) | PROMISE_INTERIM, 0);
    } else {
        Py_INCREF(promise);
        promise->flags |= PROMISE_INTERIM;
        Chain_APPEND(self, promise);
    }
    return promise;
}

/* Resolve promise. */
CAPSULE_API(void)
_Promise_ResolveEx(Promise *self, PyObject *value, int invoke_callback)
{
    assert(!(self->flags & PROMISE_INTERIM));
    assert(!(self->flags & PROMISE_SCHEDULED));
    _CTX_set(self);
    schedule_promise(self, value, PROMISE_FULFILLED, invoke_callback);
}

/*[capsule:copy]*/
#ifdef CAPSULE_PROMISE_API

#define Promise_Resolve(self, value) Promise_ResolveEx(self, value, 0)
#define Promise_ResolveEx(self, value, invoke_callback)     \
    if (!((self)->flags & PROMISE_SCHEDULED))               \
        _Promise_ResolveEx(self, value, invoke_callback)

#endif
/*[capsule:endcopy]*/

/* Reject promise */
CAPSULE_API(void)
_Promise_RejectEx(Promise *self, PyObject *value, int invoke_callback)
{
    assert(!(self->flags & PROMISE_INTERIM));
    assert(!(self->flags & PROMISE_SCHEDULED));
    _CTX_set(self);
    if (!value) {
        value = Py_FetchError();
        schedule_promise(self, value, PROMISE_REJECTED, invoke_callback);
        Py_DECREF(value);
    } else {
        schedule_promise(self, value, PROMISE_REJECTED, invoke_callback);
    }
}

/*[capsule:copy]*/
#ifdef CAPSULE_PROMISE_API

#define Promise_Reject(self, value) Promise_RejectEx(self, value, 0)
#define Promise_RejectEx(self, value, invoke_callback)      \
    if (!(self->flags & PROMISE_SCHEDULED))                 \
        _Promise_RejectEx(self, value, invoke_callback)

#endif
/*[capsule:endcopy]*/

CAPSULE_API (void)
_Promise_RejectArgsEx(Promise *self, PyObject *exc, PyObject *args, int invoke_callback)
{
    PyObject *value = PyObject_Call(exc, args, NULL);
    _Promise_RejectEx(self, value, invoke_callback);
    Py_XDECREF(value);
}

/*[capsule:copy]*/
#ifdef CAPSULE_PROMISE_API

#define Promise_RejectArgs(self, exc, args) Promise_RejectArgsEx(self, exc, args, 0)
#define Promise_RejectArgsEx(self, exc, args, invoke_callback)  \
    if (!(self->flags & PROMISE_SCHEDULED))                     \
        _Promise_RejectArgsEx(self, exc, args, invoke_callback)

#endif
/*[capsule:endcopy]*/

CAPSULE_API(void)
_Promise_RejectStringEx(Promise *self, PyObject *exc, const char *msg, int invoke_callback)
{
    PyObject *value = Py_NewError(exc, msg);
    _Promise_RejectEx(self, value, invoke_callback);
    Py_XDECREF(value);
}

/*[capsule:copy]*/
#ifdef CAPSULE_PROMISE_API

#define Promise_RejectString(self, exc, msg) Promise_RejectStringEx(self, exc, msg, 0)
#define Promise_RejectStringEx(self, exc, msg, invoke_callback)     \
    if (!(self->flags & PROMISE_SCHEDULED))                         \
        _Promise_RejectStringEx(self, exc, msg, invoke_callback)

#endif
/*[capsule:endcopy]*/

Py_LOCAL_INLINE(Coroutine *) coroutine_new(PyObject *coro, Promise *promise, PyObject *context);

Py_LOCAL_INLINE(int)
promise_exec_async(_ctx_var, PyObject *coro, PyObject *context)
{
    assert (coro != NULL);
    Promise *promise = Promise_New(_ctx);
    if (!promise)
        return -1;
    Coroutine *coroutine = coroutine_new(coro, NULL, context);
    if (!coroutine) {
        Py_DECREF(promise);
        return -1;
    }
    schedule_promise(promise, Py_None, PROMISE_FULFILLED | PROMISE_VALUABLE, 1);
    Py_INCREF(coro);
    promise->coro = coroutine;
    Py_DECREF(promise);
    return 0;
}

/*[clinic input]
promise.exec_async as promise_execasync -> object(typed="None")
    coro: object(subclass_of='&PyCoro_Type', typed='Coroutine')
    context: object(typed='Any') = None

Start new coroutine and set the `context` for the new coroutine.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_execasync_impl(PyObject *module, PyObject *coro, PyObject *context)
/*[clinic end generated code: output=cfd479a9a3dcd210 input=0105fdd1ce32874a]*/
{
    _CTX_set_module(module);
    if (Py_IsNone(context)) {
        context = NULL;
    }
    promise_exec_async(_ctx, coro, context);
    Py_RETURN_NONE;
}

Py_LOCAL_INLINE(int)
resume_coroutine(_ctx_var, Coroutine *coro, PyObject *value, int reject)
{
    _Py_IDENTIFIER(throw);

    PyObject *result;
    Py_INCREF(value);

    Py_INCREF(coro);
    S(current_coro) = coro;
    int ret = 0;

    while (1) {
        // value leaving circuit
        if (reject) {
            result = _PyObject_CallMethodIdOneArg(coro->coro, &PyId_throw, value);
        } else {
            PySendResult send_result = PyIter_Send(coro->coro, value, &result);
            if (send_result == PYGEN_RETURN) {
                Py_DECREF(value);
                if (coro->promise) {
                    schedule_promise(coro->promise, result, PROMISE_FULFILLED, 1);
                    Py_CLEAR(coro->promise);
                }
                Py_DECREF(result);
                goto finally;
            }
        }
        Py_DECREF(value);
        if (!result) {
            if (PyErr_ExceptionMatches(PyExc_KeyboardInterrupt)
                || PyErr_ExceptionMatches(PyExc_SystemExit)) {
                ret = -1;
                goto finally;
            }
            if (coro->promise) {
                value = Py_FetchError();
                schedule_promise(coro->promise, value, PROMISE_REJECTED, 1);
                Py_CLEAR(coro->promise);
                Py_DECREF(value);
            } else {
                PyErr_WriteUnraisable(coro->coro);
            }
            goto finally;
        }
        if (Py_TYPE(result) != S(PromiseType)) {
            Py_DECREF(result);
            value = Py_NewError(PyExc_RuntimeError, "`await` argument expected to be a promise.");
            if (!value) {
                value = Py_FetchError();
            }
            reject = 1;
            continue;
        }
        Promise *promise = (Promise *) result;
        promise->flags |= PROMISE_VALUABLE;
        Py_INCREF(coro);
        promise->coro = coro;
        Py_DECREF(promise);
        break;
    }

finally:
    Py_CLEAR(S(current_coro));
    return ret;
}

Py_LOCAL_INLINE(int)
handle_scheduled_promise(_ctx_var, Promise *promise)
{
    // It's a heart of an engine
    assert(!(promise->flags & PROMISE_RESOLVED) && (promise->flags & PROMISE_SCHEDULED));

    LOG("(%p)", promise);

    int exec_status = promise->flags & PROMISE_SCHEDULED;
    promise->flags |= PROMISE_RESOLVING;

    if (promise->flags & PROMISE_HAS_CALLBACK) {
        PyObject *value = NULL;
        PyObject *handler = (promise->flags & PROMISE_FULFILLED) ? promise->fulfilled : promise->rejected;
        if (handler) {
            if (promise->flags & PROMISE_C_CALLBACK) {
                value = ((promisecb) handler)(promise->value, (PyObject *) promise);
            } else if (promise->value == S(NoArgs)) {
                value = PyObject_CallNoArgs(handler);
            } else {
                value = PyObject_CallOneArg(handler, promise->value);
            }
            if (!value) {
                if (PyErr_ExceptionMatches(PyExc_KeyboardInterrupt)
                    || PyErr_ExceptionMatches(PyExc_SystemExit)) {
                    return -1;
                }
                exec_status = PROMISE_REJECTED;
                value = Py_FetchError();
            } else {
                exec_status = PROMISE_FULFILLED;
            }
        }
        if (promise->flags & PROMISE_PY_CALLBACK) {
            PyTrack_CLEAR(promise->fulfilled);
            PyTrack_CLEAR(promise->rejected);
        }
        promise->flags ^= promise->flags & PROMISE_HAS_CALLBACK;

        if (value != NULL) {
            if (Py_TYPE(value) == S(PromiseType)) {
                Promise *new_promise = (Promise *) value;
                if (new_promise == promise) {
                    // The same promise. It's bad but not fatal.
                    Py_DECREF(new_promise);
                } else if (new_promise->flags & PROMISE_RESOLVED) {
                    // Easy-peasy. Just copy exec_status and value.
                    exec_status = new_promise->flags & PROMISE_SCHEDULED;
                    PyTrack_INCREF(new_promise->value);
                    PyTrack_XSETREF(promise->value, new_promise->value);
                    Py_DECREF(new_promise);
                } else {
                    if (new_promise->coro || Py_REFCNT(new_promise) > 2) {
                        LOG("(%p) replace promise", new_promise);
                        Py_XSETREF(new_promise, Promise_Then(new_promise));
                    }
                    if (promise->coro || Py_REFCNT(promise) > 1) {
                        LOG("(%p) re-schedule promise: %p", new_promise, promise);
                        // We must re-schedule promise
                        Py_INCREF(promise);
                        S(promise_count)++;
                        LOG("promise_count=%zd", S(promise_count));
                        // Must clear the promise value as it was already set
                        PyTrack_CLEAR(promise->value);
                        Chain_APPEND(new_promise, promise);
                    } else {
                        LOG("(%p) move chain: %p", new_promise, promise);
                        // We can replace the current promise with a new one by moving the child promises only
                        Chain_MOVE(new_promise, promise);
                    }
                    Py_DECREF(new_promise);
                    return 0;
                }
            } else {
                PyTrack_XSETREF(promise->value, value);
                PyTrack_MarkEnter(value);
            }
        }
    }

    PyTrack_CLEAR(promise->ctx);

    promise->flags ^= promise->flags & PROMISE_SCHEDULED;
    promise->flags |= exec_status | PROMISE_RESOLVED;

    if (Chain_HEAD(promise)) {
        Promise *it;
        PyObject *value = promise->value;
        Chain_PULLALL(it, promise) {
            schedule_promise(it, value, exec_status, 0);
            Py_DECREF(it);
        }
    }

    if (promise->coro) {
        int ret = resume_coroutine(_ctx, promise->coro, promise->value,
                                   exec_status & PROMISE_REJECTED);
        // release coro ASAP
        Py_CLEAR(promise->coro);
        return ret;
    }

    return 0;
}

CAPSULE_API(void)
Promise_ClearChain(_ctx_var)
{
    Promise *it;
    Chain_PULLALL(it, &S(promisechain)) {
        Py_DECREF(it);
    }
}

CAPSULE_API(int)
Promise_ProcessChain(_ctx_var)
{
    int ret = 0;
    if (Chain_HEAD(&S(promisechain))) {
        Promise *it;
        S(in_chain_routine) = 1;
        Chain_PULLALL(it, &S(promisechain)) {
            int err = handle_scheduled_promise(_ctx, it);
            Py_DECREF(it);
            if (err) {
                S(in_chain_routine) = 0;
                return -1;
            }
        }
        S(in_chain_routine) = 0;
        ret = 1;
    }
    if (S(promise_count)) {
        ret += 2;
    }
    return ret;
}

CAPSULE_API(int)
Promise_GetStats(_ctx_var, Py_ssize_t *active_promises)
{
    *active_promises = S(promise_count);
    return Chain_HEAD(&S(promisechain)) != NULL;
}


/*[clinic input]
promise.process_promise_chain -> object(typed="int")

Process all scheduled (resolved or rejected) promises.

Returns active promise count.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_process_promise_chain_impl(PyObject *module)
/*[clinic end generated code: output=0587509f3b9441b4 input=bfb420ad4e54c1dc]*/
{
    _CTX_set_module(module);
    int ret = Promise_ProcessChain(_ctx);
    if (ret < 0) {
        return NULL;
    }
    return PyLong_FromSsize_t(S(promise_count));
}

static void
promise_unlockloop(_ctx_var)
{
    _Py_IDENTIFIER(set);
    PyObject *ret = _PyObject_CallMethodIdNoArgs(S(await_event), &PyId_set);
    if (!ret) {
        PyErr_WriteUnraisable(S(await_event));
    } else {
        Py_DECREF(ret);
    }
}

/*[clinic input]
promise.run_forever -> object(typed="None")

Start simple event loop.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_run_forever_impl(PyObject *module)
/*[clinic end generated code: output=dbc5007e1e267e20 input=1dae6841a1c8c431]*/
{
    _CTX_set_module(module);
    PyObject *event = PyObject_CallNoArgs(S(EventType));
    if (!event)
        return NULL;
    if (Promise_StartLoop(_ctx, (unlockloop) promise_unlockloop, _ctx)) {
        Py_DECREF(event);
        return NULL;
    }
    S(await_event) = event;
    _Py_IDENTIFIER(wait);
    _Py_IDENTIFIER(clear);
    while (1) {
        if (Promise_ProcessChain(_ctx) <= 1)
            // no more promises to resolve or error
            break;
        PyObject *ret = _PyObject_CallMethodIdNoArgs(event, &PyId_wait);
        if (!ret)
            break;
        Py_DECREF(ret);
        ret = _PyObject_CallMethodIdNoArgs(event, &PyId_clear);
        if (!ret)
            break;
        Py_DECREF(ret);
    }
    Py_CLEAR(S(await_event));
    Promise_ClearChain(_ctx);   // TODO: maybe I should not clear the chain?
    Promise_StopLoop(_ctx, (unlockloop) promise_unlockloop, _ctx);
    if (PyErr_Occurred())
        return NULL;

    Py_RETURN_NONE;
}

/*[clinic input]
promise.get_context -> object(typed="Any")

Get context of current corroutine.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_get_context_impl(PyObject *module)
/*[clinic end generated code: output=7587612ed5fc5f8b input=dbe598a5fb87dab2]*/
{
    _CTX_set_module(module);
    if (!S(current_coro)) {
        PyErr_SetString(PyExc_ValueError, "No context");
    }
    Coroutine *coro = S(current_coro);
    if (coro->context) {
        Py_INCREF(coro->context);
        return coro->context;
    }
    Py_RETURN_NONE;
}

static PyObject *
forbidden_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyErr_SetString(PyExc_TypeError, "You should not create this object directly");
    return NULL;
}

PyDoc_STRVAR(coroutine_doc, "Coroutine wrapper which holds context and result promise");

Py_LOCAL_INLINE(Coroutine *)
coroutine_new(PyObject *coro, Promise *promise, PyObject *context)
{
    _CTX_set(promise);
    Coroutine *wrapper = (Coroutine *) Freelist_GC_New(CoroutineType);
    if (!wrapper)
        return NULL;
    PyTrack_MarkAllocated(wrapper);
    PyObject_GC_Track(wrapper);
    _CTX_save(wrapper);
    Py_INCREF(coro);
    wrapper->coro = coro;
    Py_XINCREF(promise);
    wrapper->promise = promise;
    Py_XINCREF(context);
    wrapper->context = context;
    return wrapper;
}

static int
coroutine_traverse(Coroutine *self, visitproc visit, void *arg)
{
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->coro);
    Py_VISIT(self->promise);
    Py_VISIT(self->context);
    return 0;
}

static int
coroutine_clear(Coroutine *self)
{
    Py_CLEAR(self->coro);
    Py_CLEAR(self->promise);
    Py_CLEAR(self->context);
    return 0;
}

static void
coroutine_dealloc(Coroutine *self)
{
    _CTX_set(self);
    PyTrack_MarkDeleted(self);
    PyObject_GC_UnTrack(self);
    coroutine_clear(self);
    Freelist_GC_Delete(CoroutineType, self);
}

static PyObject *
coroutine_repr(PyObject *self)
{
    return PyUnicode_FromFormat("<Coroutine object at %p>", self);
}

static PyType_Slot coroutine_slots[] = {
    {Py_tp_doc, (char *) coroutine_doc},
    {Py_tp_new, forbidden_new},
    {Py_tp_dealloc, coroutine_dealloc},
    {Py_tp_traverse, coroutine_traverse},
    {Py_tp_clear, coroutine_clear},
    {Py_tp_repr, coroutine_repr},
    {0, 0},
};

static PyType_Spec coroutine_spec = {
    "promisedio.promise.Coroutine",
    sizeof(Coroutine),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE,
    coroutine_slots,
};

PyDoc_STRVAR(promiseiter_doc, "Iterator for async magic");

static PyObject *
promiseiter_new(Promise *promise)
{
    _CTX_set(promise);
    Promiseiter *it = (Promiseiter *) Freelist_GC_New(PromiseiterType);
    if (!it)
        return NULL;
    PyTrack_MarkAllocated(it);
    PyObject_GC_Track(it);
    _CTX_save(it);
    if (promise->coro || promise->flags & PROMISE_RESOLVED) {
        it->promise = Promise_Then(promise);
        if (it->promise == NULL) {
            Py_DECREF(it);
            return NULL;
        }
    } else {
        Py_INCREF(promise);
        it->promise = promise;
    }
    return (PyObject *) it;
}

static int
promiseiter_traverse(Promiseiter *self, visitproc visit, void *arg)
{
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->promise);
    return 0;
}

static int
promiseiter_clear(Promiseiter *self)
{
    Py_CLEAR(self->promise);
    return 0;
}

static void
promiseiter_dealloc(Promiseiter *self)
{
    _CTX_set(self);
    PyTrack_MarkDeleted(self);
    PyObject_GC_UnTrack(self);
    promiseiter_clear(self);
    Freelist_GC_Delete(PromiseiterType, self);
}

static PyObject *
promiseiter_repr(PyObject *self)
{
    return PyUnicode_FromFormat("<promiseiter object at %p>", self);
}

static PyObject *
promiseiter_iternext(Promiseiter *self)
{
    PyObject *res = (PyObject *) (self->promise);
    self->promise = NULL;
    return res;
}

static PyObject *
promiseiter_send(Promiseiter *self, PyObject *value)
{
    _PyGen_SetStopIterationValue(value);
    return NULL;
}

static PyMethodDef promiseiter_methods[] = {
    {"send", (PyCFunction) promiseiter_send, METH_O, NULL},
    {NULL, NULL},
};

static PyType_Slot promiseiter_slots[] = {
    {Py_tp_doc, (char *) promiseiter_doc},
    {Py_tp_new, forbidden_new},
    {Py_tp_methods, promiseiter_methods},
    {Py_tp_dealloc, promiseiter_dealloc},
    {Py_tp_traverse, promiseiter_traverse},
    {Py_tp_clear, promiseiter_clear},
    {Py_tp_repr, promiseiter_repr},
    {Py_tp_iter, PyObject_SelfIter},
    {Py_tp_iternext, promiseiter_iternext},
    {0, 0},
};

static PyType_Spec promiseiter_spec = {
    "promisedio.promise.Promiseiter",
    sizeof(Promiseiter),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE,
    promiseiter_slots,
};

PyDoc_STRVAR(promise_doc, "The Promise object represents the eventual completion (or failure) of "
                          "an asynchronous operation and its resulting value.\n");

static PyMethodDef promise_methods[] = {
    PROMISE_PROMISE_THEN_METHODDEF
    PROMISE_PROMISE_CATCH_METHODDEF
    {NULL} /* Sentinel */
};

/*[clinic input]
class promise.Promise "Promise *" "&PromiseType"
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=1cf6b3558b6d3efd]*/

/*[clinic input]
promise.Promise.then -> object(typed="Promise")
    fulfilled: object(typed='Callable') = None
    rejected: object(typed='Callable') = None

Create new `Promise`.

It takes up to two arguments: callback functions for the success and failure cases of the promise.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Promise_then_impl(Promise *self, PyObject *fulfilled,
                          PyObject *rejected)
/*[clinic end generated code: output=9573450632b756bf input=c717bcd7b3415de6]*/
{
    if (Py_IsNone(fulfilled)) {
        fulfilled = NULL;
    }
    if (fulfilled && !PyCallable_Check(fulfilled)) {
        PyErr_SetString(PyExc_TypeError, "`fulfilled` argument must be a callable");
        return NULL;
    }
    if (Py_IsNone(rejected)) {
        rejected = NULL;
    }
    if (rejected && !PyCallable_Check(rejected)) {
        PyErr_SetString(PyExc_TypeError, "`rejected` argument must be a callable");
        return NULL;
    }
    Promise *promise = Promise_Then(self);
    if (promise) {
        promise->flags |= PROMISE_PY_CALLBACK;
        PyTrack_XINCREF(fulfilled);
        PyTrack_XINCREF(rejected);
        promise->fulfilled = fulfilled;
        promise->rejected = rejected;
    }
    return (PyObject *) promise;
}

/*[clinic input]
promise.Promise.catch -> object(typed="Promise")
    rejected: object(typed='Callable')

The same as `.then(None, rejected)`
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Promise_catch_impl(Promise *self, PyObject *rejected)
/*[clinic end generated code: output=10c9938cc577180f input=b28e3d27c63a73f8]*/
{
    if (!PyCallable_Check(rejected)) {
        PyErr_SetString(PyExc_TypeError, "`rejected` argument must be a callable");
        return NULL;
    }
    Promise *promise = Promise_Then(self);
    if (promise) {
        promise->flags |= PROMISE_PY_CALLBACK;
        PyTrack_INCREF(rejected);
        promise->rejected = rejected;
    }
    return (PyObject *) promise;
}

static int
promise_traverse(Promise *self, visitproc visit, void *arg)
{
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(Chain_HEAD(self));
    Py_VISIT(Chain_NEXT(self));
    Py_VISIT(self->value);
    Py_VISIT(self->ctx);
    // coro, fulfilled and rejected normally should be NULL
    Py_VISIT(self->coro);
    if (self->flags & PROMISE_PY_CALLBACK) {
        Py_VISIT(self->fulfilled);
        Py_VISIT(self->rejected);
    }
    return 0;
}

static int
promise_clear(Promise *self)
{
    Py_CLEAR(Chain_HEAD(self));
    Py_CLEAR(Chain_NEXT(self));
    PyTrack_CLEAR(self->value);
    PyTrack_CLEAR(self->ctx);
    // coro, context, fulfilled and rejected normally should be NULL
    Py_CLEAR(self->coro);
    if (self->flags & PROMISE_PY_CALLBACK) {
        PyTrack_CLEAR(self->fulfilled);
        PyTrack_CLEAR(self->rejected);
    }
    return 0;
}

static void
promise_finalize(Promise *self)
{
    LOG("%p", self);
    if (!self->coro) {
        return;
    }

    // We're only here for coroutine
    PyObject *error_type, *error_value, *error_traceback;
    PyErr_Fetch(&error_type, &error_value, &error_traceback);

    _CTX_set(self);
    PySys_FormatStderr("Exception ignored in: %S\n", self->coro);
    PySys_WriteStderr("Traceback (most recent call last):\n");
    PyObject *result = _PyObject_CallOneArg(S(print_stack), (PyObject *) ((PyCoroObject *) self->coro)->cr_frame);
    if (!result) {
        PyErr_WriteUnraisable(self->coro->coro);
    }
    PySys_WriteStderr("RuntimeError: a coroutine awaits a promise that will never be fulfilled\n");
    Py_XDECREF(result);

    PyErr_Restore(error_type, error_value, error_traceback);
}

static void
promise_dealloc(Promise *self)
{
    _CTX_set(self);
    if ((self->flags & PROMISE_REJECTED) && (!(self->flags & PROMISE_VALUABLE))) {
        print_unhandled_exception_from_dealloc(self->value);
    }

    if (self->coro) {
        LOG("coro %p, me %p", self->coro, self);
        if (PyObject_CallFinalizerFromDealloc((PyObject *) self) < 0) {
            // resurrected.
            return;
        }
    }

    if (!(self->flags & PROMISE_SCHEDULED)) {
        S(promise_count)--;
        LOG("promise_count=%zd", S(promise_count));
    }

    PyTrack_MarkDeleted(self);
    PyObject_GC_UnTrack(self);
    promise_clear(self);
    Freelist_GC_Delete(PromiseType, self);
}

static PyObject *
promise_repr(PyObject *self)
{
    unsigned int flags = ((Promise *) self)->flags;
    if (flags & PROMISE_RESOLVED) {
        if (flags & PROMISE_FULFILLED) {
            return PyUnicode_FromFormat("<Promise object at %p | FULFILLED | RESOLVED (%R)>", self,
                                        ((Promise *) self)->value);
        } else if (flags & PROMISE_REJECTED) {
            return PyUnicode_FromFormat("<Promise object at %p | REJECTED | RESOLVED (%R)>", self,
                                        ((Promise *) self)->value);
        }
    } else if (flags & PROMISE_RESOLVING) {
        if (flags & PROMISE_FULFILLED) {
            return PyUnicode_FromFormat("<Promise object at %p | FULFILLED | RESOLVING (%R)>", self,
                                        ((Promise *) self)->value);
        } else if (flags & PROMISE_REJECTED) {
            return PyUnicode_FromFormat("<Promise object at %p | REJECTED | RESOLVING (%R)>", self,
                                        ((Promise *) self)->value);
        }
    } else {
        if (flags & PROMISE_FULFILLED) {
            return PyUnicode_FromFormat("<Promise object at %p | FULFILLED | SCHEDULED (%R)>", self,
                                        ((Promise *) self)->value);
        } else if (flags & PROMISE_REJECTED) {
            return PyUnicode_FromFormat("<Promise object at %p | REJECTED | SCHEDULED (%R)>", self,
                                        ((Promise *) self)->value);
        }
    }
    return PyUnicode_FromFormat("<Promise object at %p | PENDING>", self);
}

static PyType_Slot promise_slots[] = {
    {Py_tp_doc, (char *) promise_doc},
    {Py_tp_new, forbidden_new},
    {Py_tp_methods, promise_methods},
    {Py_tp_dealloc, promise_dealloc},
    {Py_tp_finalize, promise_finalize},
    {Py_tp_traverse, promise_traverse},
    {Py_tp_clear, promise_clear},
    {Py_tp_repr, promise_repr},
    {Py_am_await, promiseiter_new},
    {0, 0},
};

static PyType_Spec promise_spec = {
    "promisedio.promise.Promise",
    sizeof(Promise),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE,
    promise_slots,
};

PyDoc_STRVAR(deferred_doc, "A Deferred object is used to provide a new promise "
                           "along with methods to change its state.\n");

static PyMethodDef deferred_methods[] = {
    PROMISE_DEFERRED_RESOLVE_METHODDEF
    PROMISE_DEFERRED_REJECT_METHODDEF
    PROMISE_DEFERRED_PROMISE_METHODDEF
    {NULL} /* Sentinel */
};

/*[clinic input]
promise.deferred -> object(typed="Deferred")

Create new `Deferred` object.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_deferred_impl(PyObject *module)
/*[clinic end generated code: output=4760b84ba7d768a3 input=631990e13a3e9106]*/
{
    _CTX_set_module(module);
    Promise *promise = Promise_New(_ctx);
    if (!promise)
        return NULL;
    Deferred *self = (Deferred *) Freelist_GC_New(DeferredType);
    if (!self) {
        Py_DECREF(promise);
        return NULL;
    }
    _CTX_save(self);
    self->promise = promise;
    PyTrack_MarkAllocated(self);
    PyObject_GC_Track(self);
    return (PyObject *) self;
}

/*[clinic input]
class promise.Deferred "Deferred *" "&DeferredType"
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=0a0fbb23a0253343]*/

/*[clinic input]
promise.Deferred.resolve -> object(typed="None")
    value: object(typed='Any')

Resolve related `Promise` object with the given `value`.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Deferred_resolve_impl(Deferred *self, PyObject *value)
/*[clinic end generated code: output=f055b923264841e2 input=574b17c9e2491ba7]*/
{
    if (!(self->promise->flags & PROMISE_SCHEDULED)) {
        _Promise_ResolveEx(self->promise, value, 1);
    }
    Py_RETURN_NONE;
}

/*[clinic input]
promise.Deferred.reject -> object(typed="None")
    value: object(typed='Exception')

Reject related `Promise` object with the given exception `value`.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Deferred_reject_impl(Deferred *self, PyObject *value)
/*[clinic end generated code: output=65ffe03c0340f128 input=af6763873c5d715d]*/
{
    if (!PyExceptionClass_Check(value) && !PyExceptionInstance_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "exceptions must be classes deriving BaseException or "
                                         "instances of such a class");
        return NULL;
    }
    if (!(self->promise->flags & PROMISE_SCHEDULED)) {
        _Promise_RejectEx(self->promise, value, 1);
    }
    Py_RETURN_NONE;
}

/*[clinic input]
promise.Deferred.promise -> object(typed="Promise")

Get related `Promise` object.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Deferred_promise_impl(Deferred *self)
/*[clinic end generated code: output=77601f45478590bb input=b7eb4ec92f5b3bc4]*/
{
    Py_INCREF(self->promise);
    return (PyObject *) self->promise;
}

static int
deferred_traverse(Deferred *self, visitproc visit, void *arg)
{
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->promise);
    return 0;
}

static int
deferred_clear(Deferred *self)
{
    Py_CLEAR(self->promise);
    return 0;
}

static void
deferred_dealloc(Deferred *self)
{
    _CTX_set(self);
    PyTrack_MarkDeleted(self);
    PyObject_GC_UnTrack(self);
    deferred_clear(self);
    Freelist_GC_Delete(DeferredType, self);
}

static PyObject *
deferred_repr(PyObject *self)
{
    return PyUnicode_FromFormat("<Deferred object at %p>", self);
}

static PyType_Slot deferred_slots[] = {
    {Py_tp_doc, (char *) deferred_doc},
    {Py_tp_new, forbidden_new},
    {Py_tp_methods, deferred_methods},
    {Py_tp_dealloc, deferred_dealloc},
    {Py_tp_traverse, deferred_traverse},
    {Py_tp_clear, deferred_clear},
    {Py_tp_repr, deferred_repr},
    {0, 0},
};

static PyType_Spec deferred_spec = {
    "promisedio.promise.Deferred",
    sizeof(Deferred),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE,
    deferred_slots,
};


/*[clinic input]
class promise.Lock "Lock *" "_CTX_get_type(type)->LockType"
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=dc5e70ca7a8c9155]*/

CAPSULE_API(Lock *)
Lock_New(_ctx_var)
{
    return (Lock *) promise_Lock_impl(S(LockType));
}

CAPSULE_API(Promise *)
Lock_Acquire(Lock *self)
{
    _CTX_set(self);
    Promise *promise = Promise_New(_ctx);
    if (promise) {
        if (self->locked) {
            Py_INCREF(self);
            Py_INCREF(promise);
            Chain_APPEND(self, promise);
        } else {
            schedule_promise(promise, Py_None, PROMISE_FULFILLED, 1);
        }
        self->locked++;
    }
    return promise;
}

CAPSULE_API(void)
Lock_Release(Lock *self)
{
    if (self->locked) {
        _CTX_set(self);
        Promise *it;
        Chain_PULLALL(it, self) {
            self->locked--;
            schedule_promise(it, Py_None, PROMISE_FULFILLED, 1);
            Py_DECREF(it);
            Py_DECREF(self);
            break;
        }
    }
}

/*[clinic input]
@classmethod
promise.Lock.__new__

Create new `Lock` object.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Lock_impl(PyTypeObject *type)
/*[clinic end generated code: output=d9149ff17417bda6 input=74427d9b18c612ad]*/
{
    Lock *self = (Lock *) Py_New(type);
    if (!self)
        return NULL;

    _CTX_set_type(type);
    self->locked = 0;
    _CTX_save(self);
    Chain_INIT(self);
    PyTrack_MarkAllocated(self);
    return (PyObject *) self;
}

/*[clinic input]
promise.Lock.acquire -> object(typed="Promise")

Acquire the lock.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Lock_acquire_impl(Lock *self)
/*[clinic end generated code: output=20d044ffec9c1f84 input=acc97f55cb9a1470]*/
{
    return (PyObject *) Lock_Acquire(self);
}

/*[clinic input]
promise.Lock.release -> object(typed="Promise")

Release the lock.
[clinic start generated code]*/

Py_LOCAL_INLINE(PyObject *)
promise_Lock_release_impl(Lock *self)
/*[clinic end generated code: output=b1c748e07809746e input=9ade0e12692d0229]*/
{
    Lock_Release(self);
    Py_RETURN_NONE;
}

static void
lock_dealloc(Lock *self)
{
    Py_Delete(self);
}

static PyMethodDef lock_methods[] = {
    PROMISE_LOCK_ACQUIRE_METHODDEF
    PROMISE_LOCK_RELEASE_METHODDEF
    {NULL} /* Sentinel */
};

static PyType_Slot lock_slots[] = {
    {Py_tp_new, promise_Lock},
    {Py_tp_methods, lock_methods},
    {Py_tp_dealloc, lock_dealloc},
    {0, 0},
};

static PyType_Spec lock_spec = {
    "promisedio.promise.Lock",
    sizeof(Lock),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_IMMUTABLETYPE,
    lock_slots,
};

static PyType_Slot nullvalue_slots[] = {
    {0, 0},
};

static PyType_Spec nullvalue_spec = {
    "promisedio.promise.NoArgs",
    sizeof(NoArgs),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_IMMUTABLETYPE,
    nullvalue_slots
};

static PyMethodDef promisemodule_methods[] = {
    PROMISE_CLEARFREELISTS_METHODDEF
    PROMISE_SETFREELISTLIMITS_METHODDEF
    PROMISE_DEFERRED_METHODDEF
    PROMISE_EXECASYNC_METHODDEF
    PROMISE_PROCESS_PROMISE_CHAIN_METHODDEF
    PROMISE_RUN_FOREVER_METHODDEF
    PROMISE_GET_CONTEXT_METHODDEF
    {NULL, NULL},
};

static int
promisemodule_init(PyObject *module)
{
    LOG("(%p)", module);
    _CTX_set_module(module);
    Freelist_GC_INIT(PromiseType, 1024);
    Freelist_GC_INIT(DeferredType, 1024);
    Freelist_GC_INIT(PromiseiterType, 1024);
    Freelist_GC_INIT(CoroutineType, 1024);
    Chain_INIT(&(S(promisechain)));
    S(in_chain_routine) = 0;
    S(unlockloop_func) = NULL;
    S(unlockloop_ctx) = NULL;
    S(await_event) = NULL;
    S(promise_count) = 0;
    S(PromiseType) = (PyTypeObject *) PyType_FromModuleAndSpec(module, &promise_spec, NULL);
    if (S(PromiseType) == NULL)
        return -1;
    S(DeferredType) = (PyTypeObject *) PyType_FromModuleAndSpec(module, &deferred_spec, NULL);
    if (S(DeferredType) == NULL)
        return -1;
    S(PromiseiterType) = (PyTypeObject *) PyType_FromModuleAndSpec(module, &promiseiter_spec, NULL);
    if (S(PromiseiterType) == NULL)
        return -1;
    S(CoroutineType) = (PyTypeObject *) PyType_FromModuleAndSpec(module, &coroutine_spec, NULL);
    if (S(CoroutineType) == NULL)
        return -1;
    S(LockType) = (PyTypeObject *) PyType_FromModuleAndSpec(module, &lock_spec, NULL);
    if (S(LockType) == NULL)
        return -1;
    S(NoArgs) = PyType_FromModuleAndSpec(module, &nullvalue_spec, NULL);
    if (S(NoArgs) == NULL)
        return -1;
    PyObject *threading = PyImport_ImportModule("threading");
    if (!threading)
        return -1;
    S(EventType) = PyObject_GetAttrString(threading, "Event");
    Py_DECREF(threading);
    if (S(EventType) == NULL) {
        return -1;
    }
    PyObject *d = PyModule_GetDict(module);
    if (PyDict_SetItemString(d, "Promise", (PyObject *) S(PromiseType)) < 0)
        return -1;
    if (PyDict_SetItemString(d, "Lock", (PyObject *) S(LockType)) < 0)
        return -1;
    PyObject *traceback = PyImport_ImportModule("traceback");
    if (!traceback)
        return -1;
    S(print_stack) = PyObject_GetAttrString(traceback, "print_stack");
    Py_DECREF(traceback);
    if (S(print_stack) == NULL)
        return -1;
    return 0;
}

/*[capsule:export PROMISE_API_FUNCS]*/

/*[capsule:__exportblock__]*/
#define PROMISE_API promise_api_eaa656ec04c4f7d919b0cc30615e2c30
#define PROMISE_API_FUNCS {\
  [0] = Promise_StartLoop,\
  [1] = Promise_StopLoop,\
  [2] = Promise_New,\
  [3] = Promise_Callback,\
  [4] = Promise_PyCallback,\
  [5] = Promise_NewResolved,\
  [6] = Promise_Then,\
  [7] = _Promise_ResolveEx,\
  [8] = _Promise_RejectEx,\
  [9] = _Promise_RejectArgsEx,\
  [10] = _Promise_RejectStringEx,\
  [11] = Promise_ClearChain,\
  [12] = Promise_ProcessChain,\
  [13] = Promise_GetStats,\
  [14] = Lock_New,\
  [15] = Lock_Acquire,\
  [16] = Lock_Release,\
}
/*[capsule:__endexportblock__]*/

static int
promisemodule_create_api(PyObject *module)
{
    LOG("(%p)", module);
    Capsule_CREATE(module, PROMISE_API, PROMISE_API_FUNCS);
    return 0;
}

static int
promisemodule_traverse(PyObject *module, visitproc visit, void *arg)
{
    _CTX_set_module(module);
    Py_VISIT(S(PromiseType));
    Py_VISIT(S(DeferredType));
    Py_VISIT(S(PromiseiterType));
    Py_VISIT(S(CoroutineType));
    Py_VISIT(S(LockType));
    Py_VISIT(S(EventType));
    Py_VISIT(S(NoArgs));
    Py_VISIT(S(print_stack));
    Py_VISIT(Chain_HEAD(&S(promisechain)));
    return 0;
}

static int
promisemodule_clear(PyObject *module)
{
    _CTX_set_module(module);
    Py_CLEAR(S(PromiseType));
    Py_CLEAR(S(DeferredType));
    Py_CLEAR(S(PromiseiterType));
    Py_CLEAR(S(CoroutineType));
    Py_CLEAR(S(LockType));
    Py_CLEAR(S(EventType));
    Py_CLEAR(S(NoArgs));
    Py_CLEAR(S(print_stack));
    Promise_ClearChain(_ctx);
    return 0;
}

static void
promisemodule_free(void *module)
{
    LOG("(%p)", module);
    _CTX_set_module(module);
    Freelist_GC_Clear(PromiseType);
    Freelist_GC_Clear(DeferredType);
    Freelist_GC_Clear(PromiseiterType);
    Freelist_GC_Clear(CoroutineType);
    promisemodule_clear((PyObject *) module);
}

static PyModuleDef_Slot promisemodule_slots[] = {
    {Py_mod_exec, promisemodule_init},
    {Py_mod_exec, promisemodule_create_api},
    {0, NULL},
};

static struct PyModuleDef promisemodule_def = {
    PyModuleDef_HEAD_INIT,
    "promisedio.promise",
    NULL,
    sizeof(_modulestate),
    promisemodule_methods,
    promisemodule_slots,
    promisemodule_traverse,
    promisemodule_clear,
    promisemodule_free,
};

PyMODINIT_FUNC
PyInit__promise(void)
{
    return PyModuleDef_Init(&promisemodule_def);
}

PyMODINIT_FUNC
PyInit__promise_debug(void)
{
    return PyModuleDef_Init(&promisemodule_def);
}