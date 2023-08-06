#pragma once
#include "Config.hpp"
#include "Connections.hpp"
#include "HeapPair.hpp"
#include "LevelGenerator.hpp"
#include "KnnResults.hpp"
#include "Space.hpp"
#include "VisitedSet.hpp"

namespace chm {
	class Index {
		Config cfg;
		Connections conn;
		uint entryID;
		uint entryLevel;
		Node ep;
		LevelGenerator gen;
		HeapPair heaps;
		Space space;
		VisitedSet visited;

		void fillNearHeap(const uint queryID, const float* const latestData, const uint latestID);
		void push(const float* const data);
		FarHeap query(const float* const data, const uint k);
		void resetEp(const float* const query);

		template<bool searching>
		void searchLowerLayer(const float* const query, const uint ef, const uint lc, FarHeap& W, const uint countBeforeQuery);

		void searchUpperLayer(const float* const query, const uint lc);
		void selectNewNeighbors(const uint queryID, const uint lc);
		void shrinkNeighbors(const uint queryID, const uint lc, const uint M, const float* const latestData, const uint latestID);

	public:
		std::string getString() const;
		Index(
			const size_t dim, const uint efConstruction, const uint maxCount,
			const uint mMax, const uint seed, const SpaceKind spaceKind
		);
		void push(const NumpyArray<float> data);
		py::tuple query(const NumpyArray<float> data, const uint k);
		void setEfSearch(const uint efSearch);
	};

	template<bool searching>
	inline void Index::searchLowerLayer(
		const float* const query, const uint ef, const uint lc, FarHeap& W, const uint countBeforeQuery
	) {
		this->heaps.prepareLowerSearch(this->ep, W);
		this->visited.prepare(countBeforeQuery, this->entryID);
		auto& C = this->heaps.near;

		while(C.len()) {
			uint cand{};

			{
				const auto& c = C.top();
				const auto& f = W.top();

				if constexpr(searching) {
					if(c.dist > f.dist)
						break;
				} else {
					if(c.dist > f.dist && W.len() == ef)
						break;
				}

				cand = c.id;
			}

			this->conn.use(cand, lc);

			// Extract nearest from C.
			C.pop();

			for(const auto& id : this->conn) {
				if(this->visited.insert(id)) {
					const auto dist = this->space.getDistance(query, id);
					bool shouldAdd{};

					{
						const auto& f = W.top();
						shouldAdd = f.dist > dist || W.len() < ef;
					}

					if(shouldAdd) {
						this->heaps.push(dist, id, W);

						if(W.len() > ef)
							W.pop();
					}
				}
			}
		}
	}
}
