#include "Connections.hpp"

namespace chm {
	std::vector<uint>::iterator Connections::begin() {
		return this->current;
	}

	void Connections::clear() {
		*this->count = 0;
	}

	Connections::Connections(const uint maxNodeCount, const uint mMax, const uint mMax0)
		: maxLen(mMax + 1), maxLen0(mMax0 + 1) {

		this->layer0.resize(maxNodeCount * this->maxLen0, 0);
		this->upperLayers.resize(maxNodeCount);
	}

	std::vector<uint>::iterator Connections::end() {
		return this->current + this->len();
	}

	void Connections::fillFrom(const FarHeap& h, Node& nearest) {
		std::vector<uint>::iterator iter = this->current;
		const auto len = h.len();
		*this->count = uint(len);

		{
			const auto& node = h[0];
			*iter = node.id;
			nearest.dist = node.dist;
			nearest.id = node.id;
		}

		for(size_t i = 1; i < len; i++) {
			iter++;
			const auto& node = h[i];
			*iter = node.id;

			if(node.dist < nearest.dist) {
				nearest.dist = node.dist;
				nearest.id = node.id;
			}
		}
	}

	void Connections::init(const uint id, const uint level) {
		if(level)
			this->upperLayers[id].resize(this->maxLen * level, 0);
	}

	uint Connections::len() const {
		return *this->count;
	}

	void Connections::push(const uint id) {
		*(this->current + *this->count) = id;
		(*this->count)++;
	}

	void Connections::use(const uint id, const uint lc) {
		this->count = lc
			? this->upperLayers[id].begin() + this->maxLen * (lc - 1)
			: this->layer0.begin() + this->maxLen0 * id;
		this->current = this->count + 1;
	}
}
