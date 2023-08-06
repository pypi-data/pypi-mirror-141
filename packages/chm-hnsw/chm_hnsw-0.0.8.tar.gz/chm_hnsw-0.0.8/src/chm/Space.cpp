#include <algorithm>
#include <cmath>
#include "euclideanDistance.hpp"
#include "innerProduct.hpp"
#include "Space.hpp"

namespace chm {
	float Space::getNorm(const float* const data) const {
		auto res = 0.f;

		for(size_t i = 0; i < this->dim; i++)
			res += data[i] * data[i];

		// GCC: sqrtf isn't a part of namespace std.
		return 1.f / (sqrtf(res) + 1e-30f);
	}

	uint Space::getCount() const {
		return this->count;
	}

	const float* const Space::getData(const uint id) const {
		return this->data.data() + id * this->dim;
	}

	float Space::getDistance(const uint aID, const uint bID) const {
		return this->getDistance(this->getData(aID), this->getData(bID));
	}

	float Space::getDistance(const float* const a, const float* const b) const {
		return this->distFunc(a, b, this->dim, this->dim4, this->dim16, this->dimLeft);
	}

	float Space::getDistance(const float* const aData, const uint bID) const {
		return this->getDistance(aData, this->getData(bID));
	}

	uint Space::getLatestID() const {
		return this->count - 1;
	}

	std::string Space::getName() const {
		return this->name;
	}

	bool Space::isEmpty() const {
		return !this->count;
	}

	void Space::normalizeData(const float* const data, float* const res) const {
		const auto norm = this->getNorm(data);

		for(size_t i = 0; i < this->dim; i++)
			res[i] = data[i] * norm;
	}

	const float* const Space::push(const float* const data) {
		float* const res = this->data.data() + this->count * this->dim;

		if(this->normalize)
			this->normalizeData(data, res);
		else
			std::copy(data, data + this->dim, res);

		this->count++;
		return res;
	}

	Space::Space(const size_t dim, const SpaceKind kind, const size_t maxCount)
		: count(0), dim4(dim >> 2 << 2), dim16(dim >> 4 << 4), normalize(kind == SpaceKind::ANGULAR), dim(dim) {

		this->data.resize(this->dim * maxCount);
		const auto info = kind == SpaceKind::EUCLIDEAN
			? getEuclideanInfo(this->dim, this->dim4, this->dim16)
			: getInnerProductInfo(this->dim, this->dim4, this->dim16);

		this->dimLeft = info.dimLeft;
		this->distFunc = info.distFunc;
		this->name = info.name;
	}
}
