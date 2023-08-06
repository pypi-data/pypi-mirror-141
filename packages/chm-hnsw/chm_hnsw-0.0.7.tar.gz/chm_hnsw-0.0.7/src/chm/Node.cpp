#include "Node.hpp"

namespace chm {
	Node::Node() : dist(0), id(0) {}
	Node::Node(const float dist, const uint id) : dist(dist), id(id) {}
}
