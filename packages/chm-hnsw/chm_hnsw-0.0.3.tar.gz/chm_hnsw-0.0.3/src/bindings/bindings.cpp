#include "chm/HnswOptim.hpp"
#include "ChmIndex.hpp"

namespace chm {
	template<typename Dist>
	void bindIndices(py::module_& m, const std::string& typeName) {
		bindChmIndex<HnswOptim<Dist>, Dist>(m, ("ChmOptimIndex" + typeName).c_str());
	}

	PYBIND11_MODULE(chm_hnsw, m) {
		m.doc() = "Python bindings for Matej-Chmel/hnsw-index.";
		bindSpaceEnum(m);
		bindIndices<float>(m, "Float32");
	}
}
