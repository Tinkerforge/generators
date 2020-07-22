/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_MACROS_H
#define TF_MACROS_H

#include <stddef.h>

#ifdef __clang__
	#define TF_ATTRIBUTE_FMT_PRINTF(fmtpos, argpos) __attribute__((__format__(__printf__, fmtpos, argpos)))
    #define TF_ATTRIBUTE_NONNULL(...) __attribute__((nonnull (__VA_ARGS__)))
    #define TF_ATTRIBUTE_NONNULL_ALL __attribute__((nonnull))
    #define TF_ATTRIBUTE_WARN_UNUSED_RESULT __attribute__ ((warn_unused_result))
#elif defined __GNUC__
	#ifndef __GNUC_PREREQ
		#define __GNUC_PREREQ(major, minor) ((((__GNUC__) << 16) + (__GNUC_MINOR__)) >= (((major) << 16) + (minor)))
	#endif
	#if __GNUC_PREREQ(4, 4)
		#define TF_ATTRIBUTE_FMT_PRINTF(fmtpos, argpos) __attribute__((__format__(__gnu_printf__, fmtpos, argpos)))
	#else
		#define TF_ATTRIBUTE_FMT_PRINTF(fmtpos, argpos) __attribute__((__format__(__printf__, fmtpos, argpos)))
	#endif
    #define TF_ATTRIBUTE_NONNULL(...) __attribute__((nonnull (__VA_ARGS__)))
    #define TF_ATTRIBUTE_NONNULL_ALL __attribute__((nonnull))
    #define TF_ATTRIBUTE_WARN_UNUSED_RESULT __attribute__ ((warn_unused_result))
#else
	#define TF_ATTRIBUTE_FMT_PRINTF(fmtpos, argpos) // FIXME
    #define TF_ATTRIBUTE_NONNULL(...)
    #define TF_ATTRIBUTE_NONNULL_ALL __attribute__((nonnull))
    #define TF_ATTRIBUTE_WARN_UNUSED_RESULT
#endif

#ifndef MIN
	#define MIN(a, b) ((a) < (b) ? (a) : (b))
#endif
#ifndef MAX
	#define MAX(a, b) ((a) > (b) ? (a) : (b))
#endif

#endif // DAEMONLIB_MACROS_H
