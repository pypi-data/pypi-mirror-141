#include "VisitedSet.hpp"

namespace chm {
	void VisitedSet::prepare(const uint count, const uint entryID) {
		this->v.clear();
		this->v.resize(count);
		this->v[entryID] = true;
	}

	bool VisitedSet::insert(const uint id) {
		if(this->v[id])
			return false;

		this->v[id] = true;
		return true;
	}
}
