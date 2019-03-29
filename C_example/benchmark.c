//https://medium.com/practo-engineering/execute-python-code-at-the-speed-of-c-extending-python-93e081b53f04
#include <Python.h>
#include <stdio.h>
static PyObject *foo_bar(PyObject *self, PyObject *args);
static PyMethodDef FooMethods[] = {
	{"calc",  foo_bar, METH_VARARGS},
	{NULL, NULL}  /* Sentinel */
};
static struct PyModuleDef benchmark = {
	PyModuleDef_HEAD_INIT,
	"benchmark", /* module name */
	NULL, /* module documentation */
	-1, /* size of per-interpreter state of module or -1 if keeps state in global variables*/
	FooMethods
	
};
PyMODINIT_FUNC PyInit_benchmark(void)
{
	return PyModule_Create(&benchmark);
}
static PyObject *foo_bar(PyObject *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	long long a = 100234234;  long long b = 22342342;  long long c = 341342;
		for(int i = 1; i <= 10000000; i++){
			a = (a * a * b)%c;
			b = (a * b * b)%c;
		}
	return Py_BuildValue("L", a+b);
}
