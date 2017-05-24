/*
 * Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

// gcc -Wall -O2 -o liboctaveinvokewrapper.so liboctaveinvokewrapper.c -shared -fpic -I /usr/lib/jvm/default-java/include/

#include <jni.h>

// since Octave 3.8 trying to invoke an OctaveReference object results in an
// UnsatisfiedLinkError for the Java_org_octave_Octave_doInvoke symbol. the
// actual reason is unknown. it worked in Octave 3.6 where the Java support was
// in a separate Octave plugin (__java__.oct) that was loaded by Java using
// System.load(). in Octave 3.8 the Java support was merged into liboctinterp.so.
// both __java__.oct and liboctinterp.so export the required JNI symbols in the
// exact same correct way. the difference seems to be that in Octave 3.8 the
// liboctinterp.so is already loaded and Java doesn't load the .so file anymore.
// why that triggers an UnsatisfiedLinkError is unclear. but it helps to recreate
// the Octave 3.6 situation by creating this liboctaveinvokewrapper.so file that
// is loaded by Java using the System.load() method again

JNIIMPORT void JNICALL Java_org_octave_Octave_doInvoke(JNIEnv *, jclass, jint, jobjectArray);

JNIEXPORT void JNICALL Java_com_tinkerforge_IPConnection_doOctaveInvokeWrapper(JNIEnv *env, jclass klass, jint id, jobjectArray args)
{
	// Octave conveniently doesn't use the jclass parameter, this is helpful
	// because we don't have the correct value here to pass along anyway
	Java_org_octave_Octave_doInvoke(env, NULL, id, args);
}

