import unittest

from rdflib import URIRef, OWL, Graph, RDF, RDFS

from classhierarchy import ClassHierarchy


class ClassHierarchyTest(unittest.TestCase):
    ns = 'http://ex.com/ont/'
    a = URIRef(ns + 'A')
    b = URIRef(ns + 'B')
    c = URIRef(ns + 'C')
    d = URIRef(ns + 'D')
    e = URIRef(ns + 'E')
    f = URIRef(ns + 'F')
    g = URIRef(ns + 'G')
    top = OWL.Thing

    def test_add_subclass(self):
        #      T
        #     /|\
        #    a b c
        #   / \   \
        #  e   f   g

        # after first addition
        target_hierarchy_1 = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.e, self.f},
        }

        # after second addition
        target_hierarchy_2 = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.e, self.f},
            self.c: {self.g}
        }

        working_hierarchy = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.e}
        }

        class_hierarchy = ClassHierarchy()
        class_hierarchy._hierarchy = working_hierarchy

        class_hierarchy.add_subclass(self.a, self.f)
        self.assertEqual(class_hierarchy._hierarchy, target_hierarchy_1)

        class_hierarchy.add_subclass(self.c, self.g)
        self.assertEqual(class_hierarchy._hierarchy, target_hierarchy_2)

    def test_get_subclasses_of(self):
        #      T
        #     /|\
        #    a b c
        #   / \   \
        #  d   e   f
        #          |
        #          g
        hierarchy = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.d, self.e},
            self.c: {self.f},
            self.f: {self.g}
        }

        class_hierarchy = ClassHierarchy()
        class_hierarchy._hierarchy = hierarchy

        # subclasses of a: e, f
        expected_subclasses = {self.d, self.e}
        self.assertEqual(
            class_hierarchy.get_subclasses_of(self.a),
            expected_subclasses
        )

        # subclasses of T: a, b, c, d, e, f, g
        expected_subclasses = {
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g
        }
        self.assertEqual(
            class_hierarchy.get_subclasses_of(self.top),
            expected_subclasses
        )

        # subclasses of T: T, a, b, c, d, e, f, g (including T)
        expected_subclasses = {
            self.top,
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g
        }
        self.assertEqual(
            class_hierarchy.get_subclasses_of(
                superclass=self.top, include_superclass=True),
            expected_subclasses
        )

    def test__build_full_dict(self):
        #      T
        #     /|\
        #    a b c
        #   / \   \
        #  d   e   f
        #          |
        #          g
        hierarchy = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.d, self.e},
            self.c: {self.f},
            self.f: {self.g}
        }

        class_hierarchy = ClassHierarchy()
        class_hierarchy._hierarchy = hierarchy

        expected_dict = {
            class_hierarchy.T: {
                self.a: {
                    self.d: {},
                    self.e: {}
                },
                self.b: {},
                self.c: {
                    self.f: {
                        self.g: {}
                    }
                }
            }
        }

        self.assertEqual(
            class_hierarchy._build_full_dict(),
            expected_dict
        )

    def test_as_graph(self):
        #      T
        #     /|\
        #    a b c
        #   / \   \
        #  d   e   f
        #          |
        #          g
        hierarchy = {
            self.top: {self.a, self.b, self.c},
            self.a: {self.d, self.e},
            self.c: {self.f},
            self.f: {self.g}
        }

        class_hierarchy = ClassHierarchy()
        class_hierarchy._hierarchy = hierarchy

        expected_graph = Graph()
        expected_graph.add((self.top, RDF.type, OWL.Class))
        expected_graph.add((self.a, RDF.type, OWL.Class))
        expected_graph.add((self.a, RDFS.subClassOf, self.top))
        expected_graph.add((self.b, RDF.type, OWL.Class))
        expected_graph.add((self.b, RDFS.subClassOf, self.top))
        expected_graph.add((self.c, RDF.type, OWL.Class))
        expected_graph.add((self.c, RDFS.subClassOf, self.top))
        expected_graph.add((self.d, RDF.type, OWL.Class))
        expected_graph.add((self.d, RDFS.subClassOf, self.a))
        expected_graph.add((self.e, RDF.type, OWL.Class))
        expected_graph.add((self.e, RDFS.subClassOf, self.a))
        expected_graph.add((self.f, RDF.type, OWL.Class))
        expected_graph.add((self.f, RDFS.subClassOf, self.c))
        expected_graph.add((self.g, RDF.type, OWL.Class))
        expected_graph.add((self.g, RDFS.subClassOf, self.f))

        self.assertTrue(expected_graph.isomorphic(class_hierarchy.as_graph()))

        # self.assertEqual(
        #     class_hierarchy.as_graph().serialize(format='turtle'),
        #     expected_graph.serialize(format='turtle')
        # )
