//https://medium.com/practo-engineering/execute-python-code-at-the-speed-of-c-extending-python-93e081b53f04
#include <Python.h>
#include <stdio.h>
/*	 Averages an arbitrary number of inputs	*/
static PyObject *avg(PyObject *self, PyObject *args);
static PyMethodDef sensorMethods[] = {
	{"avg",  avg, METH_VARARGS},
	{NULL, NULL}  /* Sentinel */
};
static struct PyModuleDef sensors_c = {
	PyModuleDef_HEAD_INIT,
	"sensors_c", /* module name */
	NULL, /* module documentation */
	-1, /* size of per-interpreter state of module or -1 if keeps state in global variables*/
	sensorMethods

};
PyMODINIT_FUNC PyInit_sensors_c(void)
{
	return PyModule_Create(&sensors_c);
}

//static PyObject *init_avg()
static PyObject *avg(PyObject *self, PyObject *args)
{
	//int *sensor_data
	//int length=0;
	PyObject * inputs = PyTuple_GET_ITEM(args,0);
	//PyObject * inputs;
	//PyArg_ParseTuple(args, "O", &inputs);

	//if (!PyArg_ParseTuple(args, "O", &inputs))
	//	return NULL;
	int8_t length = PyTuple_Size(inputs);
	float sum = 0.0;
	for(int8_t i = 0; i < length; i++) // up to 256 values
	{
		//PyObject * temp_tup = //PyTuple_GetSlice(inputs, i, i+1);
		sum +=PyFloat_AsDouble(PyTuple_GET_ITEM(inputs,i));
		//PyArg_ParseTuple(temp_tup, "d", &temp_sum);
		//sum += (temp_sum);
	}
	//double average = (double)(sum/length);
	return Py_BuildValue("f", (float)(sum/length));
}
