#pragma once
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace chm {
	namespace py = pybind11;

	template<typename T>
	using NumpyArray = py::array_t<T, py::array::c_style | py::array::forcecast>;

	struct DataInfo {
		size_t count;
		const float* ptr;

		DataInfo(const NumpyArray<float>& data, const size_t dim);
	};

	struct KnnResults {
		const size_t count;
		float* distances;
		const size_t k;
		size_t* labels;

		KnnResults(const size_t count, const size_t k);
		py::tuple makeTuple() const;
		void setData(const size_t queryIdx, const size_t neighborIdx, const float distance, const size_t label);
	};
}
