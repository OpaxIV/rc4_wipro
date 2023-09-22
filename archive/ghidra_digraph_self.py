# -*- coding: utf-8 -*-				 # UTF-8 encoding

from ghidra.program.model.block import BasicBlockModel
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.util.graph import DirectedGraph
from ghidra.util.graph import Edge
from ghidra.util.graph import Vertex

# global vars
blockModel = BasicBlockModel(currentProgram)
digraph = DirectedGraph() 										# creates digraph, needs to be filled
listing = currentProgram.getListing()


# def of a basic block:
# int foo(x, y) {
#   // block A
#   int result = 0;
#   if x < y {
#     // block B
#         result = 1
#   } else {
#      /// block c
#     result = 2
#   }
#   /// block d
#   return result
# }



def addBasicBlocks():
	
	# getCodeBlocksContaining​(Address addr, TaskMonitor monitor) = Get all the code blocks containing the address.
	# getBody() = Get the address set for this namespace. ??
	
	fm = currentProgram.getFunctionManager()					# needed for managing functions of program
	funcs = fm.getFunctions(True)								# iterates over functions, true means forward
	for func in funcs:
		blocks = blockModel.getCodeBlocksContaining(func.getBody(), monitor)

		# iterate over blocks
		while(blocks.hasNext()):
			bb = blocks.next()
			dest = bb.getDestinations(monitor) 	# Get an Iterator over the CodeBlocks that are flowed to from this CodeBlock.
			while(dest.hasNext()):
				dbb = dest.next()

				#digraph.add(Vert)
				digraph.add(Edge(Vertex(bb), Vertex(dbb))) 		# adds edges/verticies to graph

# for testing
def printEdges():
	
	# print edges
	edges = digraph.edgeIterator()
	while edges.hasNext():
		edge = edges.next()
		from_vertex = edge.from()
		to_vertex = edge.to()
		print("  Edge from {} to {}".format(from_vertex, to_vertex))

# for testing
def printVertices():
	vertices = digraph.vertexIterator()
	while vertices.hasNext():
		vertex = vertices.next()
		print("  Vertex: {} (key: {})".format(vertex, vertex.key()))


def loopCounter():
	vertices = digraph.vertexIterator()
	while vertices.hasNext():
		vertex = vertices.next()
		loopcount = digraph.numLoops(vertex)					# The number of edges having v as both their terminal and terminal vertex.
		print("  Vertex: {} {}(key: {})".format(vertex, loopcount, vertex.key()))



if __name__ == "__main__": #to be removed in final
	addBasicBlocks()
	loopCounter()
	digraph.numEdges() 											# according to this, still no edges..
	