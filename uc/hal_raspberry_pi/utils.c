/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include <errno.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

#include "utils.h"

void microsleep(uint32_t duration) {
    struct timespec ts;
    struct timespec tsr;

    ts.tv_sec = duration / 1000000;
    ts.tv_nsec = (duration % 1000000) * 1000;

    while (clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, &tsr) < 0 && errno == EINTR) {
        memcpy(&ts, &tsr, sizeof(ts));
    }
}

void millisleep(uint32_t duration) {
    microsleep(duration * 1000);
}

uint64_t microtime(void) { // monotonic
    struct timespec ts;

    if (clock_gettime(CLOCK_MONOTONIC, &ts) < 0) {
        abort(); // clock_gettime cannot fail under normal circumstances
    }

    return ts.tv_sec * 1000000 + ts.tv_nsec / 1000;
}

uint64_t millitime(void) { // monotonic
    return microtime() / 1000;
}

const char *get_errno_name(int error_code) {
    #define ERRNO_NAME(code) case code: return #code
    switch (error_code) {
    ERRNO_NAME(EPERM);
    ERRNO_NAME(ENOENT);
    ERRNO_NAME(ESRCH);
    ERRNO_NAME(EINTR);
    ERRNO_NAME(EIO);
    ERRNO_NAME(ENXIO);
    ERRNO_NAME(E2BIG);
    ERRNO_NAME(ENOEXEC);
    ERRNO_NAME(EBADF);
    ERRNO_NAME(ECHILD);
    ERRNO_NAME(EAGAIN);
    ERRNO_NAME(ENOMEM);
    ERRNO_NAME(EACCES);
    ERRNO_NAME(EFAULT);
#ifdef ENOTBLK
    ERRNO_NAME(ENOTBLK);
#endif
    ERRNO_NAME(EBUSY);
    ERRNO_NAME(EEXIST);
    ERRNO_NAME(EXDEV);
    ERRNO_NAME(ENODEV);
    ERRNO_NAME(ENOTDIR);
    ERRNO_NAME(EISDIR);
    ERRNO_NAME(EINVAL);
    ERRNO_NAME(ENFILE);
    ERRNO_NAME(EMFILE);
    ERRNO_NAME(ENOTTY);
#ifdef ETXTBSY
    ERRNO_NAME(ETXTBSY);
#endif
    ERRNO_NAME(EFBIG);
    ERRNO_NAME(ENOSPC);
    ERRNO_NAME(ESPIPE);
    ERRNO_NAME(EROFS);
    ERRNO_NAME(EMLINK);
    ERRNO_NAME(EPIPE);
    ERRNO_NAME(EDOM);
    ERRNO_NAME(ERANGE);
    ERRNO_NAME(EDEADLK);
    ERRNO_NAME(ENAMETOOLONG);
    ERRNO_NAME(ENOLCK);
    ERRNO_NAME(ENOSYS);
    ERRNO_NAME(ENOTEMPTY);

    ERRNO_NAME(ENOTSUP);
    ERRNO_NAME(ELOOP);
    #if EWOULDBLOCK != EAGAIN
    ERRNO_NAME(EWOULDBLOCK);
    #endif
    ERRNO_NAME(ENOMSG);
    ERRNO_NAME(EIDRM);
    ERRNO_NAME(ENOSTR);
    ERRNO_NAME(ENODATA);
    ERRNO_NAME(ETIME);
    ERRNO_NAME(ENOSR);
    ERRNO_NAME(EREMOTE);
    ERRNO_NAME(ENOLINK);
    ERRNO_NAME(EPROTO);
    ERRNO_NAME(EMULTIHOP);
    ERRNO_NAME(EBADMSG);
    ERRNO_NAME(EOVERFLOW);
    ERRNO_NAME(EUSERS);
    ERRNO_NAME(ENOTSOCK);
    ERRNO_NAME(EDESTADDRREQ);
    ERRNO_NAME(EMSGSIZE);
    ERRNO_NAME(EPROTOTYPE);
    ERRNO_NAME(ENOPROTOOPT);
    ERRNO_NAME(EPROTONOSUPPORT);
    ERRNO_NAME(ESOCKTNOSUPPORT);
    #if EOPNOTSUPP != ENOTSUP
    ERRNO_NAME(EOPNOTSUPP);
    #endif
    ERRNO_NAME(EPFNOSUPPORT);
    ERRNO_NAME(EAFNOSUPPORT);
    ERRNO_NAME(EADDRINUSE);
    ERRNO_NAME(EADDRNOTAVAIL);
    ERRNO_NAME(ENETDOWN);
    ERRNO_NAME(ENETUNREACH);
    ERRNO_NAME(ENETRESET);
    ERRNO_NAME(ECONNABORTED);
    ERRNO_NAME(ECONNRESET);
    ERRNO_NAME(ENOBUFS);
    ERRNO_NAME(EISCONN);
    ERRNO_NAME(ENOTCONN);
    ERRNO_NAME(ESHUTDOWN);
    ERRNO_NAME(ETOOMANYREFS);
    ERRNO_NAME(ETIMEDOUT);
    ERRNO_NAME(ECONNREFUSED);
    ERRNO_NAME(EHOSTDOWN);
    ERRNO_NAME(EHOSTUNREACH);
    ERRNO_NAME(EALREADY);
    ERRNO_NAME(EINPROGRESS);
    ERRNO_NAME(ESTALE);
    ERRNO_NAME(EDQUOT);
    ERRNO_NAME(ECANCELED);
    ERRNO_NAME(EOWNERDEAD);
    ERRNO_NAME(ENOTRECOVERABLE);

    ERRNO_NAME(ECHRNG);
    ERRNO_NAME(EL2NSYNC);
    ERRNO_NAME(EL3HLT);
    ERRNO_NAME(EL3RST);
    ERRNO_NAME(ELNRNG);
    ERRNO_NAME(EUNATCH);
    ERRNO_NAME(ENOCSI);
    ERRNO_NAME(EL2HLT);
    ERRNO_NAME(EBADE);
    ERRNO_NAME(EBADR);
    ERRNO_NAME(EXFULL);
    ERRNO_NAME(ENOANO);
    ERRNO_NAME(EBADRQC);
    ERRNO_NAME(EBADSLT);
    #if EDEADLOCK != EDEADLK
    ERRNO_NAME(EDEADLOCK);
    #endif
    ERRNO_NAME(EBFONT);
    ERRNO_NAME(ENONET);
    ERRNO_NAME(ENOPKG);
    ERRNO_NAME(EADV);
    ERRNO_NAME(ESRMNT);
    ERRNO_NAME(ECOMM);
    ERRNO_NAME(EDOTDOT);
    ERRNO_NAME(ENOTUNIQ);
    ERRNO_NAME(EBADFD);
    ERRNO_NAME(EREMCHG);
    ERRNO_NAME(ELIBACC);
    ERRNO_NAME(ELIBBAD);
    ERRNO_NAME(ELIBSCN);
    ERRNO_NAME(ELIBMAX);
    ERRNO_NAME(ELIBEXEC);
    ERRNO_NAME(EILSEQ);
    ERRNO_NAME(ERESTART);
    ERRNO_NAME(ESTRPIPE);
    ERRNO_NAME(EUCLEAN);
    ERRNO_NAME(ENOTNAM);
    ERRNO_NAME(ENAVAIL);
    ERRNO_NAME(EISNAM);
    ERRNO_NAME(EREMOTEIO);
    ERRNO_NAME(ENOMEDIUM);
    ERRNO_NAME(EMEDIUMTYPE);
    ERRNO_NAME(ENOKEY);
    ERRNO_NAME(EKEYEXPIRED);
    ERRNO_NAME(EKEYREVOKED);
    ERRNO_NAME(EKEYREJECTED);
    #ifdef ERFKILL
    ERRNO_NAME(ERFKILL);
    #endif

    // FIXME

    default: return "<unknown>";
    }

    #undef ERRNO_NAME
}

// calls close while preserving errno
int robust_close(int fd) {
    int saved_errno = errno;
    int rc;

    if (fd < 0) {
        return 0;
    }

    rc = close(fd);
    errno = saved_errno;

    return rc;
}
