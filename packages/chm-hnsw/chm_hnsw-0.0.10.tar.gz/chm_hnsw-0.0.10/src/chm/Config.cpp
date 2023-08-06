#include <algorithm>
#include <cmath>
#include "Config.hpp"

namespace chm {
	Config::Config(const uint efConstruction, const uint mMax)
		: efSearch(DEFAULT_EF_SEARCH), efConstruction(efConstruction), mMax(mMax), mMax0(this->mMax * 2) {}

	uint Config::getEfSearch() const {
		return this->efSearch;
	}

	uint Config::getMaxEf(const uint k) const {
		return std::max(this->efSearch, k);
	}

	double Config::getML() const {
		return 1.0 / std::log(double(this->mMax));
	}

	void Config::setEfSearch(const uint efSearch) {
		this->efSearch = efSearch;
	}
}
