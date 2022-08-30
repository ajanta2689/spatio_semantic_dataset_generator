import unittest

from rdflib import URIRef, OWL

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

