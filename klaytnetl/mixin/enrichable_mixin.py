# MIT License
#
# Modifications Copyright (c) klaytn authors
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class EnrichableMixin(object):
    """
    Enrichable mixin
    ===
    The object inheriting this mixin has property `enrich`, which determines an enrichness
    of a result item. The `enrich` property has two rules:

    1. For every enrichable object with `enrich == True`, it only can register enrichable
       objects as a child. For all violation cases, it ignores the registration itself.
    2. Enrichness must be inherited to children. For dismatches, it overrides the child's
       property.
    """

    def __init__(self, enrich: bool = False, **kwargs):
        self.enrich = enrich

    @property
    def enrich(self) -> bool:
        return self._enrich

    @enrich.setter
    def enrich(self, enrich: bool):
        self._enrich = enrich
