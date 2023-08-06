#include "Hnsw.hpp"

namespace chm {
	PYBIND11_MODULE(chm_hnsw, m) {
		m.doc() = "Python bindings for Matej-Chmel/hnsw-index.";

		py::enum_<SpaceKind>(m, "Space")
			.value("ANGULAR", SpaceKind::ANGULAR)
			.value("EUCLIDEAN", SpaceKind::EUCLIDEAN)
			.value("INNER_PRODUCT", SpaceKind::INNER_PRODUCT);

		py::class_<Hnsw>(m, "Hnsw")
			.def(
				py::init<const size_t, const uint, const uint, const uint, const uint, const SpaceKind>(),
				py::arg("dim"), py::arg("efConstruction"), py::arg("maxCount"),
				py::arg("mMax"), py::arg("seed"), py::arg("spaceKind")
			)
			.def("__str__", [](const Hnsw& h) { return h.getString(); })
			.def("push", py::overload_cast<const NumpyArray>(&Hnsw::push), py::arg("data"))
			.def(
				"query", py::overload_cast<const NumpyArray, const uint>(&Hnsw::query),
				py::arg("data"), py::arg("k")
			)
			.def("setEfSearch", &Hnsw::setEfSearch, py::arg("efSearch"));
	}
}
