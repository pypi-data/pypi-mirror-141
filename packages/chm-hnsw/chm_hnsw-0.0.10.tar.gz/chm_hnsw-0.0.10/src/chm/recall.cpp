#include "recall.hpp"

namespace chm {
	float getRecall(const NumpyArray<size_t> correctLabels, const NumpyArray<size_t> testedLabels) {
		LabelsWrapper correctWrapper(correctLabels), testedWrapper(testedLabels);
		size_t hits = 0;
		std::unordered_set<size_t> correctSet;
		correctSet.reserve(correctWrapper.yDim);

		for(size_t x = 0; x < correctWrapper.xDim; x++) {
			correctWrapper.fillSet(correctSet, x);

			for(size_t y = 0; y < correctWrapper.yDim; y++)
				if(correctSet.find(testedWrapper.get(x, y)) != correctSet.end())
					hits++;
		}

		return float(hits) / (correctWrapper.getComponentCount());
	}

	void LabelsWrapper::fillSet(std::unordered_set<size_t>& set, const size_t x) const {
		set.clear();

		for(size_t y = 0; y < this->yDim; y++)
			set.insert(this->get(x, y));
	}

	const size_t& LabelsWrapper::get(const size_t x, const size_t y) const {
		return this->data[x * this->yDim + y];
	}

	size_t LabelsWrapper::getComponentCount() const {
		return this->xDim * this->yDim;
	}

	LabelsWrapper::LabelsWrapper(const NumpyArray<size_t>& a)
		: buf(a.request()), data((const size_t* const)this->buf.ptr), xDim(this->buf.shape[0]), yDim(this->buf.shape[1]) {}
}
