#pragma once
#include <vector>
#include "types.hpp"

namespace chm {
	class VisitedSet {
		std::vector<bool> v;

	public:
		void prepare(const uint count, const uint entryID);
		bool insert(const uint id);
	};
}
