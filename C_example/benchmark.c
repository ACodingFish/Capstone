//https://medium.com/practo-engineering/execute-python-code-at-the-speed-of-c-extending-python-93e081b53f04
#include <Python.h>
#include <stdio.h>
static PyObject *calcfp(PyObject *self, PyObject *args);
static PyObject *mod(PyObject *self, PyObject *args);
static PyMethodDef benchmarkMethods[] = {
	{"calc",  calcfp, METH_VARARGS},
	{"mod", mod, METH_VARARGS},
	{NULL, NULL}  /* Sentinel */
};
static struct PyModuleDef benchmark = {
	PyModuleDef_HEAD_INIT,
	"benchmark", /* module name */
	NULL, /* module documentation */
	-1, /* size of per-interpreter state of module or -1 if keeps state in global variables*/
	benchmarkMethods
	
};
PyMODINIT_FUNC PyInit_benchmark(void)
{
	return PyModule_Create(&benchmark);
}
static PyObject *calcfp(PyObject *self, PyObject *args)
{
	long long a = 100234234;  long long b = 22342342;  long long c = 341342;
	if (!PyArg_ParseTuple(args, "LLL", &a, &b, &c))
		return NULL;

	for(long long i = 1; i < 10000000; ++i){
		a = (a * a * b)%c;
		b = (a * b * b)%c;
	}
	c = (a+b);
	return Py_BuildValue("L", c);
}
static PyObject *mod(PyObject *self, PyObject *args)
{
	long long a, b, c;
	if (!PyArg_ParseTuple(args, "LL", &a, &b))
		return NULL;
	c = a % b;
	return Py_BuildValue("L", c);
}
