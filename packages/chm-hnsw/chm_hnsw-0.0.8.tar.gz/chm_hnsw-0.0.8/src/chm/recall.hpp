#pragma once
#include <unordered_set>
#include "KnnResults.hpp"

namespace chm {
	float getRecall(const NumpyArray<size_t> correctLabels, const NumpyArray<size_t> testedLabels);

	struct LabelsWrapper {
		const py::buffer_info buf;
		const size_t* const data;
		const size_t xDim;
		const size_t yDim;

		void fillSet(std::unordered_set<size_t>& set, const size_t x) const;
		const size_t& get(const size_t x, const size_t y) const;
		size_t getComponentCount() const;
		LabelsWrapper(const NumpyArray<size_t>& a);
	};
}
