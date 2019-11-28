# -*- coding: utf-8 -*-

# should be under __main__ but __future__ imports
# are special and don't behave like other imports
# so this has to be at the beginning
from __future__ import print_function

from collections import deque


# this subclasses `object` because
# it has to be a new-style class in order
# for the @property decorator to work
class ResizableDeque(object):
    def __init__(self, *args, **kwargs):
        self.internal = deque(*args, **kwargs)

        # create a list of attributes we want to skip
        # then also
        # create a list of all special attributes
        # so we can skip those as well
        skip_list = [
            # no need to explicitly skip __class__ anymore
            # '__class__',
            'maxlen'
        ] + [attr for attr in dir(deque) if attr.startswith('__') and
             attr.endswith('__')]

        for attr in dir(deque):
            # self[attr] = self.internal[attr]
            if attr not in skip_list:
                setattr(self, attr, getattr(self.internal, attr))
                # uncomment these 2 lines to see if the attributes
                # are being created properly

                # print(attr, end=' ')
                # print(getattr(self, attr) == getattr(self.internal, attr))

    @property
    def maxlen(self):
        return self.internal.maxlen

    @maxlen.setter
    def maxlen(self, value):
        templist = list(self.internal)
        self.internal = deque(templist, value)

    # even though inspecting them in the interpreter
    # shows that these two correctly point to the
    # internal deque's methods, they don't work
    # unless they're overriden in this way

    # answer found at:
    # http://stackoverflow.com/questions/11635489/why-doesnt-python-call-instance-method-init-on-instance-creation-but-call
    # https://docs.python.org/dev/reference/datamodel.html#special-lookup
    #
    # but if it has to be set on the class
    # why does the reference to self.internal work?
    def __str__(self):
        return self.internal.__str__()

    def __repr__(self):
        return self.internal.__repr__()

    # and more stuff that needs to be overriden... :'(
    def __getitem__(self, value):
        return self.internal.__getitem__(value)

    def __setitem__(self, index, value):
        return self.internal.__setitem__(index, value)

    # these have not been tested
    def __copy__(self):
        return self.internal.__copy__()

    def __delitem__(self, index):
        return self.internal.__delitem__(index)

    # don't override comparison methods yet
    # def __eq__(self, other):
    #     return self.internal.__eq__(other)

    # def __ge__(self, other):
    #     return self.internal.__ge__(other)

    # def __gt__(self, other):
    #     return self.internal.__gt__(other)

    def __iadd__(self, other):
        return self.internal.__iadd__(other)

    # def __iter__(self):
    #     return self.internal.__iter__()

    # def __le__(self, other):
    #     return self.internal.__le__(other)

    def __len__(self):
        return self.internal.__len__()

    # def __lt__(self, other):
    #     return self.internal.__lt__(other)

    # def __ne__(self, other):
    #     return self.internal.__ne__(other)

    # doesn't seem to be necessary
    # def __reveresed__(self):
    #     return self.internal.__reversed__()

    # not sure if overriding __sizeof__ is wise this way
    def __sizeof__(self):
        return self.__sizeof__() + self.internal.__sizeof__()

    # deque's __hash__ is None
    # but this class's __hash__ works fine
    # not sure what to do here
    # def __hash__(self):
    #     pass

    # pretty sure this is ok
    def __format__(self, spec):
        return self.internal.__format__(spec)

    # doesn't seem to be necessary
    # def __reduce__(self):
    #     pass

    # strangely I can iterate over an object of this class
    # as if it were a deque
    # without having to override __iter__

if __name__ == "__main__":
    import unittest

    class TestResizableDeque(unittest.TestCase):

        testvalues = [
            'lol',
            'foo',
            'bar'
        ]

        testlen = 5

        def setUp(self):
            self.d = ResizableDeque(self.testvalues, self.testlen)
            self.f = deque(self.testvalues, self.testlen)

        def test_init(self):
            self.assertEqual(self.d.internal, self.f)

        def test_append(self):
            self.d.append(self.testvalues)
            self.f.append(self.testvalues)
            self.assertEqual(self.d.internal, self.f)

        def test_appendleft(self):
            self.d.appendleft(self.testvalues)
            self.f.appendleft(self.testvalues)
            self.assertEqual(self.d.internal, self.f)

        def test_clear(self):
            self.d.clear()
            self.f.clear()
            self.assertEqual(self.d.internal, self.f)

        def test_count(self):
            c1 = self.d.count(self.testvalues[0])
            c2 = self.f.count(self.testvalues[0])
            self.assertEqual(c1, c2)

        def test_extend(self):
            self.d.extend(self.testvalues)
            self.f.extend(self.testvalues)
            self.assertEqual(self.d.internal, self.f)

        def test_extendleft(self):
            self.d.extendleft(self.testvalues)
            self.f.extendleft(self.testvalues)
            self.assertEqual(self.d.internal, self.f)

        def test_maxlen_get(self):
            c1 = self.d.maxlen
            c2 = self.f.maxlen
            self.assertEqual(c1, c2)

        def test_maxlen_set(self):
            i = ResizableDeque(self.testvalues, len(self.testvalues))
            j = deque(self.testvalues, len(self.testvalues)*2)

            i.maxlen = len(self.testvalues)*2
            self.assertEqual(i.internal, j)

        def test_pop(self):
            self.d.pop()
            self.f.pop()
            self.assertEqual(self.d.internal, self.f)

        def test_popleft(self):
            self.d.popleft()
            self.f.popleft()
            self.assertEqual(self.d.internal, self.f)

        def test_remove(self):
            self.d.remove(self.testvalues[0])
            self.f.remove(self.testvalues[0])
            self.assertEqual(self.d.internal, self.f)

        def test_reverse(self):
            self.d.reverse()
            self.f.reverse()
            self.assertEqual(self.d.internal, self.f)

        def test_rotate(self):
            self.d.rotate(3)
            self.f.rotate(3)
            self.assertEqual(self.d.internal, self.f)

        def test_index(self):
            c1 = self.d[2]
            c2 = self.f[2]
            self.assertEqual(c1, c2)

        # not implemented yet
        # def test_pickle(self):
        #     pass

    suite = unittest.TestLoader().loadTestsFromTestCase(TestResizableDeque)
    unittest.TextTestRunner(verbosity=2).run(suite)