# This file is part of PyOP2.
#
# PyOP2 is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PyOP2 is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# PyOP2.  If not, see <http://www.gnu.org/licenses>
#
# Copyright (c) 2011, Graham Markall <grm08@doc.ic.ac.uk> and others. Please see
# the AUTHORS file in the main source directory for a full list of copyright
# holders.

"""OP2 backend configuration and auxiliaries."""

import cuda
import opencl
import sequential
import void

backends = {
        'cuda': cuda,
        'sequential': sequential,
        'opencl': opencl,
        'void': void
        }

class BackendSelector(type):
    """Metaclass creating the backend class corresponding to the requested
    class."""

    _backend = void
    _defaultbackend = sequential

    def __call__(cls, *args, **kwargs):
        """Create an instance of the request class for the current backend"""

        # Try the selected backend first
        try:
            t = cls._backend.__dict__[cls.__name__]
        # Fall back to the default (i.e. sequential) backend
        except KeyError:
            t = cls._defaultbackend.__dict__[cls.__name__]
        # Invoke the constructor with the arguments given
        return t(*args, **kwargs)

def get_backend():
    """Get the OP2 backend"""

    return BackendSelector._backend.__name__

def set_backend(backend):
    """Set the OP2 backend"""

    assert backend in backends, "backend must be one of %r" % backends.keys()
    global BackendSelector
    BackendSelector._backend = backends[backend]
