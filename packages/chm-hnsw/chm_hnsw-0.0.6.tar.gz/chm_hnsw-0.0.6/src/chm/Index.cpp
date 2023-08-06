#include <sstream>
#include "Index.hpp"

namespace chm {
	void Index::fillFarHeap(const uint currentID, const float* const query, const uint queryID) {
		const auto data = this->space.getData(currentID);
		this->heaps.far.clear();
		this->heaps.far.push(this->space.getDistance(data, query), queryID);

		for(const auto& id : this->conn)
			this->heaps.far.push(this->space.getDistance(data, id), id);
	}

	void Index::push(const float* const data) {
		const auto L = this->entryLevel;
		const auto l = this->gen.getNext();
		const auto query = this->space.push(data);
		const auto queryID = this->space.getLatestID();

		this->conn.init(queryID, l);
		this->resetEp(query);

		for(auto lc = L; lc > l; lc--)
			this->searchUpperLayer(query, lc);

		for(auto lc = std::min(L, l);; lc--) {
			this->searchLowerLayer<false>(query, this->cfg.efConstruction, lc, this->heaps.far);
			this->selectNeighborsHeuristic(this->cfg.mMax);

			this->conn.use(queryID, lc);
			this->conn.fillFrom(this->heaps.far);

			// ep = nearest from candidates
			{
				const auto& n = this->heaps.far.top();
				this->ep.dist = n.dist;
				this->ep.id = n.id;
			}
			const auto mLayer = !lc ? this->cfg.mMax0 : this->cfg.mMax;

			for(const auto& id : this->conn) {
				this->conn.use(id, lc);

				if(this->conn.len() < mLayer)
					this->conn.push(queryID);
				else {
					this->fillFarHeap(id, query, queryID);
					this->selectNeighborsHeuristic(mLayer);
					this->conn.fillFrom(this->heaps.far);
				}
			}

			if(!lc)
				break;
		}

		if(l > L) {
			this->entryID = queryID;
			this->entryLevel = l;
		}
	}

	FarHeap Index::query(const float* const data, const uint k) {
		const auto maxEf = std::max(this->cfg.getEfSearch(), k);
		FarHeap W{};
		this->heaps.reserve(std::max(maxEf, this->cfg.mMax0), W);
		this->resetEp(data);
		const auto L = this->entryLevel;

		for(auto lc = L; lc > 0; lc--)
			this->searchUpperLayer(data, lc);

		this->searchLowerLayer<true>(data, maxEf, 0, W);

		while(W.len() > k)
			W.pop();

		return W;
	}

	void Index::resetEp(const float* const query) {
		this->ep.dist = this->space.getDistance(query, this->entryID);
		this->ep.id = this->entryID;
	}

	void Index::searchUpperLayer(const float* const query, const uint lc) {
		uint prev{};

		do {
			this->conn.use(this->ep.id, lc);
			prev = this->ep.id;

			for(const auto& cand : this->conn) {
				const auto dist = this->space.getDistance(query, cand);

				if(dist < this->ep.dist) {
					this->ep.dist = dist;
					this->ep.id = cand;
				}
			}

		} while(this->ep.id != prev);
	}

	void Index::selectNeighborsHeuristic(const uint M) {
		if(this->heaps.far.len() < M)
			return;

		this->heaps.prepareHeuristic();
		auto& R = this->heaps.far;
		auto& W = this->heaps.near;

		while(W.len() && R.len() < M) {
			{
				const auto& e = W.top();
				const auto eData = this->space.getData(e.id);

				for(const auto& r : std::as_const(R))
					if(this->space.getDistance(eData, r.id) < e.dist)
						goto isNotCloser;

				R.push(e.dist, e.id);
			}

			isNotCloser:;

			// Extract nearest from W.
			W.pop();
		}
	}

	std::string Index::getString() const {
		std::stringstream s;
		s << "Index(efConstruction=" << this->cfg.efConstruction << ", mMax=" << this->cfg.mMax << ", distance=" << this->space.getName() << ')';
		return s.str();
	}

	Index::Index(
		const size_t dim, const uint efConstruction, const uint maxCount,
		const uint mMax, const uint seed, const SpaceKind spaceKind
	) : cfg(efConstruction, mMax), conn(maxCount, this->cfg.mMax, this->cfg.mMax0),
		entryID(0), entryLevel(0), ep{}, gen(this->cfg.getML(), seed),
		heaps(efConstruction, this->cfg.mMax), space(dim, spaceKind, maxCount), visited{} {}

	void Index::push(const NumpyArray data) {
		size_t i = 0;
		const DataInfo info(data, this->space.dim);

		if(this->space.isEmpty()) {
			i = 1;
			this->entryLevel = this->gen.getNext();
			this->conn.init(this->entryID, this->entryLevel);
			this->space.push(info.ptr);
		}

		for(; i < info.count; i++)
			this->push(info.ptr + i * this->space.dim);
	}

	py::tuple Index::query(const NumpyArray data, const uint k) {
		const DataInfo info(data, this->space.dim);
		std::vector<float> normData;
		KnnResults res(info.count, k);

		normData.resize(this->space.dim);
		auto normPtr = normData.data();

		for(size_t queryIdx = 0; queryIdx < info.count; queryIdx++) {
			this->space.normalizeData(info.ptr + queryIdx * this->space.dim, normPtr);
			auto heap = this->query(normPtr, k);

			for(auto neighborIdx = k - 1;; neighborIdx--) {
				{
					const auto& node = heap.top();
					res.setData(queryIdx, neighborIdx, node.dist, node.id);
				}
				heap.pop();

				if(!neighborIdx)
					break;
			}
		}

		return res.makeTuple();
	}

	void Index::setEfSearch(const uint efSearch) {
		this->cfg.setEfSearch(efSearch);
	}
}
