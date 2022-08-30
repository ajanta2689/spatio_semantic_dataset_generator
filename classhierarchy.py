import random

from rdflib import OWL, URIRef


class ClassHierarchy:
    _hierarchy = {}
    T = OWL.Thing

    def __init__(self):
        self._hierarchy[self.T] = set()

    def get_random_subclass_of(self, cls: URIRef, include_superclass=False):
        subclasses: set[URIRef] = \
            self.get_subclasses_of(cls, include_superclass=include_superclass)

        subclasses_list = list(subclasses)

        return random.choice(subclasses_list)

    def add_subclass(self, superclass: URIRef, subclass: URIRef):
        superclass_children = self._hierarchy.get(superclass)

        if superclass_children is None:
            self._hierarchy[superclass] = set()

        self._hierarchy[superclass].add(subclass)

    def _get_subclasses_of(self, superclasses: set[URIRef]) -> set[URIRef]:
        subclasses = set()
        for superclass in superclasses:
            _subclasses: set[URIRef] = self._hierarchy.get(superclass)

            if _subclasses is None:
                _subclasses = set()
            elif not _subclasses:
                # Empty set returned. No need to call
                # _get_subclasses_of again
                pass
            else:
                # add subclasses
                subclasses = subclasses.union(_subclasses)

                # add subclasses of subclasses
                subclasses = subclasses.union(
                    self._get_subclasses_of(_subclasses))

        return subclasses

    def get_subclasses_of(
            self, superclass: URIRef, include_superclass=False
    ) -> set[URIRef]:

        subclasses = self._hierarchy.get(superclass)

        if subclasses is None:
            subclasses = set()

        else:
            subclasses = subclasses.union(self._get_subclasses_of(subclasses))

        if include_superclass:
            subclasses.add(superclass)

        return subclasses


class ClassHierarchyGenerator:
    cls_prefix_str = 'http://ex.com/ont/Cls%03i'

    def __init__(self, num_classes: int, num_clusters: int):
        """
        :param num_classes: Overall number of classes in the class hierarchy
        :param num_clusters: We assume that we have n distinct subclasses of
            OWL:Thing which represent each cluster's superclass. So n also
            represents the number of clusters.
        """
        self.num_classes = num_classes
        self.num_clusters = num_clusters

        assert self.num_clusters <= self.num_classes

        self.cls_cntr = 1

    def _next_class(self):
        cls = URIRef(self.cls_prefix_str % self.cls_cntr)
        self.cls_cntr += 1

        return cls

    def get_random_hierarchy(self):
        cluster_base_classes = []
        hierarchy = ClassHierarchy()
        number_of_classes_to_add = self.num_classes

        for i in range(self.num_clusters):
            cls = self._next_class()
            hierarchy.add_subclass(hierarchy.T, cls)
            cluster_base_classes.append(cls)
            number_of_classes_to_add -= 1

        for i in range(number_of_classes_to_add):
            cls = self._next_class()

            cluster_cls = random.choice(cluster_base_classes)

            super_cls = hierarchy.get_random_subclass_of(
                cluster_cls, include_superclass=True)

            hierarchy.add_subclass(super_cls, cls)

        return hierarchy


if __name__ == '__main__':
    generator = ClassHierarchyGenerator(20, 4)
    class_hierarchy = generator.get_random_hierarchy()

    print(class_hierarchy._hierarchy)
