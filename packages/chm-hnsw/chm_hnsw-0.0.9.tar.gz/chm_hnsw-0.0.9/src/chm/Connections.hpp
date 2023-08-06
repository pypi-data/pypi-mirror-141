#pragma once
#include "Heap.hpp"

namespace chm {
	class Connections {
		std::vector<uint>::iterator count;
		std::vector<uint>::iterator current;
		std::vector<uint> layer0;
		const uint maxLen;
		const uint maxLen0;
		std::vector<std::vector<uint>> upperLayers;

	public:
		std::vector<uint>::iterator begin();
		void clear();
		Connections(const uint maxNodeCount, const uint mMax, const uint mMax0);
		std::vector<uint>::iterator end();
		void fillFrom(const FarHeap& h, Node& nearest);
		void init(const uint id, const uint level);
		uint len() const;
		void push(const uint id);
		void use(const uint id, const uint lc);
	};
}
