#pragma once
#include "types.hpp"

namespace chm {
	struct Node {
		float dist;
		uint id;

		Node();
		Node(const float dist, const uint id);
	};

	struct FarComparator {
		constexpr bool operator()(const Node& a, const Node& b) const noexcept {
			return a.dist < b.dist;
		}
	};

	struct NearComparator {
		constexpr bool operator()(const Node& a, const Node& b) const noexcept {
			return a.dist > b.dist;
		}
	};
}
