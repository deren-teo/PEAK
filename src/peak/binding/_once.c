/* Generated by Pyrex 0.4.6 on Sat Nov 30 14:56:47 2002 */

#include "Python.h"


static PyObject *__Pyx_UnpackItem(PyObject *, int); /*proto*/
static int __Pyx_EndUnpack(PyObject *, int); /*proto*/
static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static void __Pyx_ReRaise(void); /*proto*/
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
static PyObject *__Pyx_GetExcValue(void); /*proto*/
static PyObject *__Pyx_GetName(PyObject *dict, char *name); /*proto*/
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, char *name); /*proto*/
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
static int __Pyx_GetStarArgs(PyObject **args, PyObject **kwds, char *kwd_list[], int nargs, PyObject **args2, PyObject **kwds2); /*proto*/
static void __Pyx_WriteUnraisable(char *name); /*proto*/
static void __Pyx_AddTraceback(char *funcname); /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static char *__pyx_srcfile = "C:\\cygwin\\home\\pje\\PEAK\\src/peak/binding/_once.pyx";
static int __pyx_lineno;

staticforward PyTypeObject __pyx_type_OnceDescriptor;

struct __pyx_obj_OnceDescriptor {
  PyObject_HEAD
  PyObject *attrName;
};

staticforward PyTypeObject __pyx_type___attrName_Descriptor;

struct __pyx_obj___attrName_Descriptor {
  PyObject_HEAD
};
extern PyObject *(GET_DICTIONARY(PyObject *));


static int __pyx_f_14OnceDescriptor___set__(PyObject *__pyx_v_self, PyObject *__pyx_v_obj, void (*__pyx_v_value)); /*proto*/
static int __pyx_f_14OnceDescriptor___set__(PyObject *__pyx_v_self, PyObject *__pyx_v_obj, void (*__pyx_v_value)) {
  PyObject *__pyx_v_d;
  int __pyx_r;
  PyObject *__pyx_1 = 0;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_obj);
  __pyx_v_d = Py_None; Py_INCREF(__pyx_v_d);

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":19 */
  __pyx_1 = GET_DICTIONARY(__pyx_v_obj); if (!__pyx_1) {__pyx_lineno = 19; goto __pyx_L1;}
  Py_DECREF(__pyx_v_d);
  __pyx_v_d = __pyx_1;
  __pyx_1 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":21 */
  __pyx_2 = (__pyx_v_value != 0);
  if (__pyx_2) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":22 */
    __pyx_1 = (PyObject *)__pyx_v_value;
    Py_INCREF(__pyx_1);
    __pyx_3 = ((struct __pyx_obj_OnceDescriptor *)__pyx_v_self)->attrName; Py_INCREF(__pyx_3);
    if (PyObject_SetItem(__pyx_v_d, __pyx_3, __pyx_1) < 0) {__pyx_lineno = 22; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    goto __pyx_L2;
  }
  /*else*/ {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":25 */
    __pyx_3 = ((struct __pyx_obj_OnceDescriptor *)__pyx_v_self)->attrName; Py_INCREF(__pyx_3);
    if (PyObject_DelItem(__pyx_v_d, __pyx_3) < 0) {__pyx_lineno = 25; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
  }
  __pyx_L2:;

  __pyx_r = 0;
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  __Pyx_AddTraceback("__set__");
  __pyx_r = -1;
  __pyx_L0:;
  Py_DECREF(__pyx_v_d);
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_obj);
  return __pyx_r;
}


static PyObject *__pyx_f_14OnceDescriptor___get__(PyObject *__pyx_v_self, void (*__pyx_v_obj), void (*__pyx_v_typ)); /*proto*/
static PyObject *__pyx_f_14OnceDescriptor___get__(PyObject *__pyx_v_self, void (*__pyx_v_obj), void (*__pyx_v_typ)) {
  PyObject *__pyx_v_ob;
  PyObject *__pyx_v_n;
  PyObject *__pyx_v_d;
  PyObject *__pyx_v_value;
  PyObject *__pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  PyObject *__pyx_6 = 0;
  int __pyx_7;
  int __pyx_8;
  Py_INCREF(__pyx_v_self);
  __pyx_v_ob = Py_None; Py_INCREF(__pyx_v_ob);
  __pyx_v_n = Py_None; Py_INCREF(__pyx_v_n);
  __pyx_v_d = Py_None; Py_INCREF(__pyx_v_d);
  __pyx_v_value = Py_None; Py_INCREF(__pyx_v_value);

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":49 */
  __pyx_1 = (!(__pyx_v_obj != 0));
  if (__pyx_1) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":50 */
    Py_INCREF(__pyx_v_self);
    __pyx_r = __pyx_v_self;
    goto __pyx_L0;
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":52 */
  __pyx_2 = (PyObject *)__pyx_v_obj;
  Py_INCREF(__pyx_2);
  Py_DECREF(__pyx_v_ob);
  __pyx_v_ob = __pyx_2;
  __pyx_2 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":53 */
  __pyx_2 = ((struct __pyx_obj_OnceDescriptor *)__pyx_v_self)->attrName; Py_INCREF(__pyx_2);
  Py_DECREF(__pyx_v_n);
  __pyx_v_n = __pyx_2;
  __pyx_2 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":54 */
  __pyx_2 = GET_DICTIONARY(__pyx_v_ob); if (!__pyx_2) {__pyx_lineno = 54; goto __pyx_L1;}
  Py_DECREF(__pyx_v_d);
  __pyx_v_d = __pyx_2;
  __pyx_2 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":56 */
  __pyx_1 = PySequence_Contains(__pyx_v_d, __pyx_v_n); if (__pyx_1 < 0) {__pyx_lineno = 56; goto __pyx_L1;}
  if (__pyx_1) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":57 */
    __pyx_2 = PyObject_GetItem(__pyx_v_d, __pyx_v_n); if (!__pyx_2) {__pyx_lineno = 57; goto __pyx_L1;}
    __pyx_r = __pyx_2;
    __pyx_2 = 0;
    goto __pyx_L0;
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":59 */
  __pyx_1 = PyObject_IsTrue(__pyx_v_n); if (__pyx_1 < 0) {__pyx_lineno = 59; goto __pyx_L1;}
  if (!(__pyx_8 = (!__pyx_1))) {
    __pyx_2 = __Pyx_GetName(__pyx_b, "getattr"); if (!__pyx_2) {__pyx_lineno = 59; goto __pyx_L1;}
    __pyx_3 = PyObject_GetAttrString(__pyx_v_ob, "__class__"); if (!__pyx_3) {__pyx_lineno = 59; goto __pyx_L1;}
    __pyx_4 = __Pyx_GetName(__pyx_b, "None"); if (!__pyx_4) {__pyx_lineno = 59; goto __pyx_L1;}
    __pyx_5 = PyTuple_New(3); if (!__pyx_5) {__pyx_lineno = 59; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_5, 0, __pyx_3);
    Py_INCREF(__pyx_v_n);
    PyTuple_SET_ITEM(__pyx_5, 1, __pyx_v_n);
    PyTuple_SET_ITEM(__pyx_5, 2, __pyx_4);
    __pyx_3 = 0;
    __pyx_4 = 0;
    __pyx_6 = PyObject_CallObject(__pyx_2, __pyx_5); if (!__pyx_6) {__pyx_lineno = 59; goto __pyx_L1;}
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    __pyx_7 = __pyx_6 != __pyx_v_self;
    Py_DECREF(__pyx_6); __pyx_6 = 0;
    __pyx_8 = __pyx_7;
  }
  if (__pyx_8) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":60 */
    __pyx_3 = PyObject_GetAttrString(__pyx_v_self, "usageError"); if (!__pyx_3) {__pyx_lineno = 60; goto __pyx_L1;}
    __pyx_4 = PyTuple_New(0); if (!__pyx_4) {__pyx_lineno = 60; goto __pyx_L1;}
    __pyx_5 = PyObject_CallObject(__pyx_3, __pyx_4); if (!__pyx_5) {__pyx_lineno = 60; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    goto __pyx_L4;
  }
  __pyx_L4:;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":62 */
  __pyx_2 = __Pyx_GetName(__pyx_m, "NOT_FOUND"); if (!__pyx_2) {__pyx_lineno = 62; goto __pyx_L1;}
  if (PyObject_SetItem(__pyx_v_d, __pyx_v_n, __pyx_2) < 0) {__pyx_lineno = 62; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":64 */
  /*try:*/ {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":65 */
    __pyx_4 = PyObject_GetAttrString(__pyx_v_self, "computeValue"); if (!__pyx_4) {__pyx_lineno = 65; goto __pyx_L5;}
    __pyx_3 = PyTuple_New(3); if (!__pyx_3) {__pyx_lineno = 65; goto __pyx_L5;}
    Py_INCREF(__pyx_v_ob);
    PyTuple_SET_ITEM(__pyx_3, 0, __pyx_v_ob);
    Py_INCREF(__pyx_v_d);
    PyTuple_SET_ITEM(__pyx_3, 1, __pyx_v_d);
    Py_INCREF(__pyx_v_n);
    PyTuple_SET_ITEM(__pyx_3, 2, __pyx_v_n);
    __pyx_5 = PyObject_CallObject(__pyx_4, __pyx_3); if (!__pyx_5) {__pyx_lineno = 65; goto __pyx_L5;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_v_value);
    __pyx_v_value = __pyx_5;
    __pyx_5 = 0;
  }
  goto __pyx_L6;
  __pyx_L5:;
  Py_XDECREF(__pyx_2); __pyx_2 = 0;
  Py_XDECREF(__pyx_6); __pyx_6 = 0;
  Py_XDECREF(__pyx_3); __pyx_3 = 0;
  Py_XDECREF(__pyx_4); __pyx_4 = 0;
  Py_XDECREF(__pyx_5); __pyx_5 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":66 */
  /*except:*/ {
    __Pyx_AddTraceback("__get__");
    __pyx_2 = __Pyx_GetExcValue(); if (!__pyx_2) {__pyx_lineno = 66; goto __pyx_L1;}
    Py_DECREF(__pyx_2); __pyx_2 = 0;

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":67 */
    if (PyObject_DelItem(__pyx_v_d, __pyx_v_n) < 0) {__pyx_lineno = 67; goto __pyx_L1;}

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":68 */
    __Pyx_ReRaise();
    {__pyx_lineno = 68; goto __pyx_L1;}
    goto __pyx_L6;
  }
  __pyx_L6:;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":70 */
  if (PyObject_SetItem(__pyx_v_d, __pyx_v_n, __pyx_v_value) < 0) {__pyx_lineno = 70; goto __pyx_L1;}

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":72 */
  Py_INCREF(__pyx_v_value);
  __pyx_r = __pyx_v_value;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  Py_XDECREF(__pyx_6);
  __Pyx_AddTraceback("__get__");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_ob);
  Py_DECREF(__pyx_v_n);
  Py_DECREF(__pyx_v_d);
  Py_DECREF(__pyx_v_value);
  Py_DECREF(__pyx_v_self);
  return __pyx_r;
}


static PyObject *__pyx_f_21__attrName_Descriptor___get__(PyObject *__pyx_v_self, void (*__pyx_v_obj), void (*__pyx_v_typ)); /*proto*/
static PyObject *__pyx_f_21__attrName_Descriptor___get__(PyObject *__pyx_v_self, void (*__pyx_v_obj), void (*__pyx_v_typ)) {
  PyObject *__pyx_r;
  int __pyx_1;
  struct __pyx_obj_OnceDescriptor *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  Py_INCREF(__pyx_v_self);

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":90 */
  __pyx_1 = (!(__pyx_v_obj != 0));
  if (__pyx_1) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":91 */
    Py_INCREF(__pyx_v_self);
    __pyx_r = __pyx_v_self;
    goto __pyx_L0;
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":93 */
  __pyx_2 = (struct __pyx_obj_OnceDescriptor *)__pyx_v_obj;
  Py_INCREF(__pyx_2);
  __pyx_3 = ((struct __pyx_obj_OnceDescriptor *)__pyx_2)->attrName; Py_INCREF(__pyx_3);
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_r = __pyx_3;
  __pyx_3 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  __Pyx_AddTraceback("__get__");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  return __pyx_r;
}


static int __pyx_f_21__attrName_Descriptor___set__(PyObject *__pyx_v_self, PyObject *__pyx_v_obj, void (*__pyx_v_value)); /*proto*/
static int __pyx_f_21__attrName_Descriptor___set__(PyObject *__pyx_v_self, PyObject *__pyx_v_obj, void (*__pyx_v_value)) {
  int __pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_obj);
  if (!__Pyx_ArgTypeTest(((PyObject *)__pyx_v_obj), &__pyx_type_OnceDescriptor, "obj")) {__pyx_lineno = 96; goto __pyx_L1;}

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":97 */
  __pyx_1 = (!(__pyx_v_value != 0));
  if (__pyx_1) {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":98 */
    __pyx_2 = __Pyx_GetName(__pyx_b, "None"); if (!__pyx_2) {__pyx_lineno = 98; goto __pyx_L1;}
    Py_DECREF(((struct __pyx_obj_OnceDescriptor *)((PyObject *)__pyx_v_obj))->attrName);
    ((struct __pyx_obj_OnceDescriptor *)((PyObject *)__pyx_v_obj))->attrName = __pyx_2;
    __pyx_2 = 0;
    goto __pyx_L2;
  }
  /*else*/ {

    /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":100 */
    __pyx_2 = (PyObject *)__pyx_v_value;
    Py_INCREF(__pyx_2);
    Py_DECREF(((struct __pyx_obj_OnceDescriptor *)((PyObject *)__pyx_v_obj))->attrName);
    ((struct __pyx_obj_OnceDescriptor *)((PyObject *)__pyx_v_obj))->attrName = __pyx_2;
    __pyx_2 = 0;
  }
  __pyx_L2:;

  __pyx_r = 0;
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("__set__");
  __pyx_r = -1;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_obj);
  return __pyx_r;
}

static PyObject *__pyx_tp_new_OnceDescriptor(struct _typeobject *t, PyObject *a, PyObject *k) {
  PyObject *o = (*t->tp_alloc)(t, 0);
  struct __pyx_obj_OnceDescriptor *p = (struct __pyx_obj_OnceDescriptor *)o;
  p->attrName = Py_None; Py_INCREF(p->attrName);
  return o;
}

static void __pyx_tp_dealloc_OnceDescriptor(PyObject *o) {
  struct __pyx_obj_OnceDescriptor *p = (struct __pyx_obj_OnceDescriptor *)o;
  Py_XDECREF(p->attrName);
  (*o->ob_type->tp_free)(o);
}

static int __pyx_tp_traverse_OnceDescriptor(PyObject *o, visitproc v, void *a) {
  int e;
  struct __pyx_obj_OnceDescriptor *p = (struct __pyx_obj_OnceDescriptor *)o;
  e = (*v)(p->attrName, a); if (e) return e;
  return 0;
}

static int __pyx_tp_clear_OnceDescriptor(PyObject *o) {
  struct __pyx_obj_OnceDescriptor *p = (struct __pyx_obj_OnceDescriptor *)o;
  Py_XDECREF(p->attrName);
  p->attrName = Py_None; Py_INCREF(p->attrName);
  return 0;
}

static struct PyMethodDef __pyx_methods_OnceDescriptor[] = {
  {0, 0, 0, 0}
};

static PyNumberMethods __pyx_tp_as_number_OnceDescriptor = {
  0, /*nb_add*/
  0, /*nb_subtract*/
  0, /*nb_multiply*/
  0, /*nb_divide*/
  0, /*nb_remainder*/
  0, /*nb_divmod*/
  0, /*nb_power*/
  0, /*nb_negative*/
  0, /*nb_positive*/
  0, /*nb_absolute*/
  0, /*nb_nonzero*/
  0, /*nb_invert*/
  0, /*nb_lshift*/
  0, /*nb_rshift*/
  0, /*nb_and*/
  0, /*nb_xor*/
  0, /*nb_or*/
  0, /*nb_coerce*/
  0, /*nb_int*/
  0, /*nb_long*/
  0, /*nb_float*/
  0, /*nb_oct*/
  0, /*nb_hex*/
  0, /*nb_inplace_add*/
  0, /*nb_inplace_subtract*/
  0, /*nb_inplace_multiply*/
  0, /*nb_inplace_divide*/
  0, /*nb_inplace_remainder*/
  0, /*nb_inplace_power*/
  0, /*nb_inplace_lshift*/
  0, /*nb_inplace_rshift*/
  0, /*nb_inplace_and*/
  0, /*nb_inplace_xor*/
  0, /*nb_inplace_or*/
  0, /*nb_floor_divide*/
  0, /*nb_true_divide*/
  0, /*nb_inplace_floor_divide*/
  0, /*nb_inplace_true_divide*/
};

static PySequenceMethods __pyx_tp_as_sequence_OnceDescriptor = {
  0, /*sq_length*/
  0, /*sq_concat*/
  0, /*sq_repeat*/
  0, /*sq_item*/
  0, /*sq_slice*/
  0, /*sq_ass_item*/
  0, /*sq_ass_slice*/
  0, /*sq_contains*/
  0, /*sq_inplace_concat*/
  0, /*sq_inplace_repeat*/
};

static PyMappingMethods __pyx_tp_as_mapping_OnceDescriptor = {
  0, /*mp_length*/
  0, /*mp_subscript*/
  0, /*mp_ass_subscript*/
};

static PyBufferProcs __pyx_tp_as_buffer_OnceDescriptor = {
  0, /*bf_getreadbuffer*/
  0, /*bf_getwritebuffer*/
  0, /*bf_getsegcount*/
  0, /*bf_getcharbuffer*/
};

statichere PyTypeObject __pyx_type_OnceDescriptor = {
  PyObject_HEAD_INIT(0)
  0, /*ob_size*/
  "_once.OnceDescriptor", /*tp_name*/
  sizeof(struct __pyx_obj_OnceDescriptor), /*tp_basicsize*/
  0, /*tp_itemsize*/
  __pyx_tp_dealloc_OnceDescriptor, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  &__pyx_tp_as_number_OnceDescriptor, /*tp_as_number*/
  &__pyx_tp_as_sequence_OnceDescriptor, /*tp_as_sequence*/
  &__pyx_tp_as_mapping_OnceDescriptor, /*tp_as_mapping*/
  0, /*tp_hash*/
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  &__pyx_tp_as_buffer_OnceDescriptor, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_HAVE_GC, /*tp_flags*/
  "Data descriptor base class for \'Once\' bindings", /*tp_doc*/
  __pyx_tp_traverse_OnceDescriptor, /*tp_traverse*/
  __pyx_tp_clear_OnceDescriptor, /*tp_clear*/
  0, /*tp_richcompare*/
  0, /*tp_weaklistoffset*/
  0, /*tp_iter*/
  0, /*tp_iternext*/
  __pyx_methods_OnceDescriptor, /*tp_methods*/
  0, /*tp_members*/
  0, /*tp_getset*/
  0, /*tp_base*/
  0, /*tp_dict*/
  __pyx_f_14OnceDescriptor___get__, /*tp_descr_get*/
  __pyx_f_14OnceDescriptor___set__, /*tp_descr_set*/
  0, /*tp_dictoffset*/
  0, /*tp_init*/
  0, /*tp_alloc*/
  __pyx_tp_new_OnceDescriptor, /*tp_new*/
  0, /*tp_free*/
  0, /*tp_is_gc*/
  0, /*tp_bases*/
  0, /*tp_mro*/
  0, /*tp_cache*/
  0, /*tp_subclasses*/
  0, /*tp_weaklist*/
};

static PyObject *__pyx_tp_new___attrName_Descriptor(struct _typeobject *t, PyObject *a, PyObject *k) {
  PyObject *o = (*t->tp_alloc)(t, 0);
  struct __pyx_obj___attrName_Descriptor *p = (struct __pyx_obj___attrName_Descriptor *)o;
  return o;
}

static void __pyx_tp_dealloc___attrName_Descriptor(PyObject *o) {
  struct __pyx_obj___attrName_Descriptor *p = (struct __pyx_obj___attrName_Descriptor *)o;
  (*o->ob_type->tp_free)(o);
}

static int __pyx_tp_traverse___attrName_Descriptor(PyObject *o, visitproc v, void *a) {
  int e;
  struct __pyx_obj___attrName_Descriptor *p = (struct __pyx_obj___attrName_Descriptor *)o;
  return 0;
}

static int __pyx_tp_clear___attrName_Descriptor(PyObject *o) {
  struct __pyx_obj___attrName_Descriptor *p = (struct __pyx_obj___attrName_Descriptor *)o;
  return 0;
}

static struct PyMethodDef __pyx_methods___attrName_Descriptor[] = {
  {0, 0, 0, 0}
};

static PyNumberMethods __pyx_tp_as_number___attrName_Descriptor = {
  0, /*nb_add*/
  0, /*nb_subtract*/
  0, /*nb_multiply*/
  0, /*nb_divide*/
  0, /*nb_remainder*/
  0, /*nb_divmod*/
  0, /*nb_power*/
  0, /*nb_negative*/
  0, /*nb_positive*/
  0, /*nb_absolute*/
  0, /*nb_nonzero*/
  0, /*nb_invert*/
  0, /*nb_lshift*/
  0, /*nb_rshift*/
  0, /*nb_and*/
  0, /*nb_xor*/
  0, /*nb_or*/
  0, /*nb_coerce*/
  0, /*nb_int*/
  0, /*nb_long*/
  0, /*nb_float*/
  0, /*nb_oct*/
  0, /*nb_hex*/
  0, /*nb_inplace_add*/
  0, /*nb_inplace_subtract*/
  0, /*nb_inplace_multiply*/
  0, /*nb_inplace_divide*/
  0, /*nb_inplace_remainder*/
  0, /*nb_inplace_power*/
  0, /*nb_inplace_lshift*/
  0, /*nb_inplace_rshift*/
  0, /*nb_inplace_and*/
  0, /*nb_inplace_xor*/
  0, /*nb_inplace_or*/
  0, /*nb_floor_divide*/
  0, /*nb_true_divide*/
  0, /*nb_inplace_floor_divide*/
  0, /*nb_inplace_true_divide*/
};

static PySequenceMethods __pyx_tp_as_sequence___attrName_Descriptor = {
  0, /*sq_length*/
  0, /*sq_concat*/
  0, /*sq_repeat*/
  0, /*sq_item*/
  0, /*sq_slice*/
  0, /*sq_ass_item*/
  0, /*sq_ass_slice*/
  0, /*sq_contains*/
  0, /*sq_inplace_concat*/
  0, /*sq_inplace_repeat*/
};

static PyMappingMethods __pyx_tp_as_mapping___attrName_Descriptor = {
  0, /*mp_length*/
  0, /*mp_subscript*/
  0, /*mp_ass_subscript*/
};

static PyBufferProcs __pyx_tp_as_buffer___attrName_Descriptor = {
  0, /*bf_getreadbuffer*/
  0, /*bf_getwritebuffer*/
  0, /*bf_getsegcount*/
  0, /*bf_getcharbuffer*/
};

statichere PyTypeObject __pyx_type___attrName_Descriptor = {
  PyObject_HEAD_INIT(0)
  0, /*ob_size*/
  "_once.__attrName_Descriptor", /*tp_name*/
  sizeof(struct __pyx_obj___attrName_Descriptor), /*tp_basicsize*/
  0, /*tp_itemsize*/
  __pyx_tp_dealloc___attrName_Descriptor, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  &__pyx_tp_as_number___attrName_Descriptor, /*tp_as_number*/
  &__pyx_tp_as_sequence___attrName_Descriptor, /*tp_as_sequence*/
  &__pyx_tp_as_mapping___attrName_Descriptor, /*tp_as_mapping*/
  0, /*tp_hash*/
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  &__pyx_tp_as_buffer___attrName_Descriptor, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "The attribute name this descriptor will handle.", /*tp_doc*/
  __pyx_tp_traverse___attrName_Descriptor, /*tp_traverse*/
  __pyx_tp_clear___attrName_Descriptor, /*tp_clear*/
  0, /*tp_richcompare*/
  0, /*tp_weaklistoffset*/
  0, /*tp_iter*/
  0, /*tp_iternext*/
  __pyx_methods___attrName_Descriptor, /*tp_methods*/
  0, /*tp_members*/
  0, /*tp_getset*/
  0, /*tp_base*/
  0, /*tp_dict*/
  __pyx_f_21__attrName_Descriptor___get__, /*tp_descr_get*/
  __pyx_f_21__attrName_Descriptor___set__, /*tp_descr_set*/
  0, /*tp_dictoffset*/
  0, /*tp_init*/
  0, /*tp_alloc*/
  __pyx_tp_new___attrName_Descriptor, /*tp_new*/
  0, /*tp_free*/
  0, /*tp_is_gc*/
  0, /*tp_bases*/
  0, /*tp_mro*/
  0, /*tp_cache*/
  0, /*tp_subclasses*/
  0, /*tp_weaklist*/
};

static struct PyMethodDef __pyx_methods[] = {
  {0, 0, 0, 0}
};

static char (__pyx_k1[]) = "peak.api";
static char (__pyx_k2[]) = "NOT_FOUND";
static char (__pyx_k3[]) = "OnceDescriptor_attrName";
static char (__pyx_k4[]) = "OnceDescriptor";

DL_EXPORT(void) init_once(void); /*proto*/
DL_EXPORT(void) init_once(void) {
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  __pyx_m = Py_InitModule4("_once", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  __pyx_b = PyImport_AddModule("__builtin__");
  PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b);
  __pyx_type_OnceDescriptor.tp_free = _PyObject_GC_Del;
  if (PyType_Ready(&__pyx_type_OnceDescriptor) < 0) {__pyx_lineno = 1; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "OnceDescriptor", (PyObject *)&__pyx_type_OnceDescriptor) < 0) {__pyx_lineno = 1; goto __pyx_L1;}
  __pyx_type___attrName_Descriptor.tp_free = _PyObject_Del;
  if (PyType_Ready(&__pyx_type___attrName_Descriptor) < 0) {__pyx_lineno = 1; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "__attrName_Descriptor", (PyObject *)&__pyx_type___attrName_Descriptor) < 0) {__pyx_lineno = 1; goto __pyx_L1;}

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":1 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":5 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":8 */
  __pyx_1 = PyString_FromString(__pyx_k1); if (!__pyx_1) {__pyx_lineno = 8; goto __pyx_L1;}
  __pyx_2 = PyString_FromString(__pyx_k2); if (!__pyx_2) {__pyx_lineno = 8; goto __pyx_L1;}
  __pyx_3 = PyList_New(1); if (!__pyx_3) {__pyx_lineno = 8; goto __pyx_L1;}
  PyList_SET_ITEM(__pyx_3, 0, __pyx_2);
  __pyx_2 = 0;
  __pyx_4 = __Pyx_Import(__pyx_1, __pyx_3); if (!__pyx_4) {__pyx_lineno = 8; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  __pyx_5 = PyObject_GetAttrString(__pyx_4, "NOT_FOUND"); if (!__pyx_5) {__pyx_lineno = 8; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "NOT_FOUND", __pyx_5) < 0) {__pyx_lineno = 8; goto __pyx_L1;}
  Py_DECREF(__pyx_5); __pyx_5 = 0;
  Py_DECREF(__pyx_4); __pyx_4 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":11 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":15 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":17 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":42 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":83 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":88 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":96 */

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":103 */
  __pyx_2 = __Pyx_GetName(__pyx_m, "__attrName_Descriptor"); if (!__pyx_2) {__pyx_lineno = 103; goto __pyx_L1;}
  __pyx_1 = PyTuple_New(0); if (!__pyx_1) {__pyx_lineno = 103; goto __pyx_L1;}
  __pyx_3 = PyObject_CallObject(__pyx_2, __pyx_1); if (!__pyx_3) {__pyx_lineno = 103; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (PyObject_SetAttrString(__pyx_m, "OnceDescriptor_attrName", __pyx_3) < 0) {__pyx_lineno = 103; goto __pyx_L1;}
  Py_DECREF(__pyx_3); __pyx_3 = 0;

  /* "C:\cygwin\home\pje\PEAK\src/peak/binding/_once.pyx":105 */
  __pyx_4 = PyString_FromString(__pyx_k3); if (!__pyx_4) {__pyx_lineno = 105; goto __pyx_L1;}
  __pyx_5 = PyString_FromString(__pyx_k4); if (!__pyx_5) {__pyx_lineno = 105; goto __pyx_L1;}
  __pyx_1 = PyList_New(2); if (!__pyx_1) {__pyx_lineno = 105; goto __pyx_L1;}
  PyList_SET_ITEM(__pyx_1, 0, __pyx_4);
  PyList_SET_ITEM(__pyx_1, 1, __pyx_5);
  __pyx_4 = 0;
  __pyx_5 = 0;
  if (PyObject_SetAttrString(__pyx_m, "__all__", __pyx_1) < 0) {__pyx_lineno = 105; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  return;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  __Pyx_AddTraceback("_once");
}

/* Runtime support code */

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
  PyObject *py_srcfile = 0;
  PyObject *py_funcname = 0;
  PyObject *py_globals = 0;
  PyObject *empty_tuple = 0;
  PyObject *empty_string = 0;
  PyCodeObject *py_code = 0;
  PyFrameObject *py_frame = 0;
  
  py_srcfile = PyString_FromString(__pyx_srcfile);
  if (!py_srcfile) goto bad;
  py_funcname = PyString_FromString(funcname);
  if (!py_funcname) goto bad;
  py_globals = PyModule_GetDict(__pyx_m);
  if (!py_globals) goto bad;
  empty_tuple = PyTuple_New(0);
  if (!empty_tuple) goto bad;
  empty_string = PyString_FromString("");
  if (!empty_string) goto bad;
  py_code = PyCode_New(
    0,            /*int argcount,*/
    0,            /*int nlocals,*/
    0,            /*int stacksize,*/
    0,            /*int flags,*/
    empty_string, /*PyObject *code,*/
    empty_tuple,  /*PyObject *consts,*/
    empty_tuple,  /*PyObject *names,*/
    empty_tuple,  /*PyObject *varnames,*/
    empty_tuple,  /*PyObject *freevars,*/
    empty_tuple,  /*PyObject *cellvars,*/
    py_srcfile,   /*PyObject *filename,*/
    py_funcname,  /*PyObject *name,*/
    __pyx_lineno,   /*int firstlineno,*/
    empty_string  /*PyObject *lnotab*/
  );
  if (!py_code) goto bad;
  py_frame = PyFrame_New(
    PyThreadState_Get(), /*PyThreadState *tstate,*/
    py_code,             /*PyCodeObject *code,*/
    py_globals,          /*PyObject *globals,*/
    0                    /*PyObject *locals*/
  );
  if (!py_frame) goto bad;
  py_frame->f_lineno = __pyx_lineno;
  PyTraceBack_Here(py_frame);
bad:
  Py_XDECREF(py_srcfile);
  Py_XDECREF(py_funcname);
  Py_XDECREF(empty_tuple);
  Py_XDECREF(empty_string);
  Py_XDECREF(py_code);
  Py_XDECREF(py_frame);
}

static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, char *name) {
  if (PyObject_TypeCheck(obj, type))
    return 1;
  PyErr_Format(PyExc_TypeError,
    "Argument '%s' has incorrect type (expected %s, got %s)",
    name, type->tp_name, obj->ob_type->tp_name);
  return 0;
}

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
  PyObject *__import__ = 0;
  PyObject *empty_list = 0;
  PyObject *module = 0;
  PyObject *global_dict = 0;
  PyObject *empty_dict = 0;
  PyObject *list;
  __import__ = PyObject_GetAttrString(__pyx_b, "__import__");
  if (!__import__)
    goto bad;
  if (from_list)
    list = from_list;
  else {
    empty_list = PyList_New(0);
    if (!empty_list)
      goto bad;
    list = empty_list;
  }
  global_dict = PyModule_GetDict(__pyx_m);
  if (!global_dict)
    goto bad;
  empty_dict = PyDict_New();
  if (!empty_dict)
    goto bad;
  module = PyObject_CallFunction(__import__, "OOOO",
    name, global_dict, empty_dict, list);
bad:
  Py_XDECREF(empty_list);
  Py_XDECREF(__import__);
  Py_XDECREF(empty_dict);
  return module;
}

static PyObject *__Pyx_GetName(PyObject *dict, char *name) {
  PyObject *result;
  result = PyObject_GetAttrString(dict, name);
  if (!result)
    PyErr_SetString(PyExc_NameError, name);
  return result;
}

static PyObject *__Pyx_GetExcValue(void) {
  PyObject *type = 0, *value = 0, *tb = 0;
  PyObject *result = 0;
  PyThreadState *tstate = PyThreadState_Get();
  PyErr_Fetch(&type, &value, &tb);
  PyErr_NormalizeException(&type, &value, &tb);
  if (PyErr_Occurred())
    goto bad;
  if (!value) {
    value = Py_None;
    Py_INCREF(value);
  }
  Py_XDECREF(tstate->exc_type);
  Py_XDECREF(tstate->exc_value);
  Py_XDECREF(tstate->exc_traceback);
  tstate->exc_type = type;
  tstate->exc_value = value;
  tstate->exc_traceback = tb;
  result = value;
  Py_XINCREF(result);
  type = 0;
  value = 0;
  tb = 0;
bad:
  Py_XDECREF(type);
  Py_XDECREF(value);
  Py_XDECREF(tb);
  return result;
}

static void __Pyx_ReRaise(void) {
  PyThreadState *tstate = PyThreadState_Get();
  PyObject *type = tstate->exc_type;
  PyObject *value = tstate->exc_value;
  PyObject *tb = tstate->exc_traceback;
  Py_XINCREF(type);
  Py_XINCREF(value);
  Py_XINCREF(tb);
  PyErr_Restore(type, value, tb);
}