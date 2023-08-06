#pragma once
#include <functional>
#include <string>

namespace chm {
	using DistFunc = std::function<float(const float*, const float*, const size_t, const size_t, const size_t, const size_t)>;

	struct DistanceInfo {
		const size_t dimLeft;
		const DistFunc distFunc;
		const std::string name;

		DistanceInfo() = default;
		DistanceInfo(const size_t dimLeft, const DistFunc distFunc, const std::string name);
	};
}
