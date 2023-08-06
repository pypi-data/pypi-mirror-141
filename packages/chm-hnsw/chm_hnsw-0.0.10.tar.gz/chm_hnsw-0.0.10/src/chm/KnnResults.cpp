#include "KnnResults.hpp"

namespace chm {
	constexpr auto WRONG_DIM = "Data must be 1D or 2D array.";
	constexpr auto WRONG_FEATURES = "Number of features doesn't equal to number of dimensions.";

	void checkBufInfo(const py::buffer_info& buf, const size_t dim) {
		if (buf.ndim == 2) {
			if (buf.shape[1] != dim)
				throw std::runtime_error(WRONG_FEATURES);
		}
		else if (buf.ndim != 1)
			throw std::runtime_error(WRONG_DIM);
	}

	void freeWhenDone(void* d) {
		delete[] d;
	}

	DataInfo::DataInfo(const NumpyArray<float>& data, const size_t dim) {
		const auto buf = data.request();
		checkBufInfo(buf, dim);
		this->count = size_t(buf.shape[0]);
		this->ptr = (const float* const)buf.ptr;
	}

	KnnResults::KnnResults(const size_t count, const size_t k) : count(count), k(k) {
		const auto len = this->count * this->k;
		this->distances = new float[len];
		this->labels = new size_t[len];
	}

	py::tuple KnnResults::makeTuple() const {
		return py::make_tuple(
			py::array_t<size_t>(
				{this->count, this->k},
				{this->k * sizeof(size_t), sizeof(size_t)},
				this->labels,
				py::capsule(this->labels, freeWhenDone)
			),
			py::array_t<float>(
				{this->count, this->k},
				{this->k * sizeof(float), sizeof(float)},
				this->distances,
				py::capsule(this->distances, freeWhenDone)
			)
		);
	}

	void KnnResults::setData(const size_t queryIdx, const size_t neighborIdx, const float distance, const size_t label) {
		this->distances[queryIdx * this->k + neighborIdx] = distance;
		this->labels[queryIdx * this->k + neighborIdx] = label;
	}
}
