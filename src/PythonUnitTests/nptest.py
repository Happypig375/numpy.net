import numpy as np
import numpy.core.numeric as _nx
from numpy.core import linspace, atleast_1d, atleast_2d, transpose
#from numpy.core.numeric import (
#    ones, zeros, arange, concatenate, array, asarray, asanyarray, empty,
#    empty_like, ndarray, around, floor, ceil, take, dot, where, intp, multiply,
#    integer, isscalar, absolute, AxisError
#    )
from numpy.core.umath import (
    pi, add, arctan2, frompyfunc, cos, less_equal, sqrt, sin,
    mod, exp, log10, not_equal, subtract
    )
from numpy.core.fromnumeric import (
    ravel, nonzero, sort, partition, mean, any, sum
    )
from numpy.core.numerictypes import typecodes, number
from numpy.lib.twodim_base import diag

from numpy.core.multiarray import (
    _insert, add_docstring, digitize, bincount, normalize_axis_index,
    interp as compiled_interp, interp_complex as compiled_interp_complex
    )
from numpy.core.umath import _add_newdoc_ufunc as add_newdoc_ufunc
from numpy.compat import long
from numpy.compat.py3k import basestring
from numpy.core import iinfo, transpose

from numpy.core.numeric import (
    absolute, asanyarray, arange, zeros, greater_equal, multiply, ones,
    asarray, where, int8, int16, int32, int64, empty, promote_types, diagonal,
    nonzero
    )

import operator

class nptest(object):
 
 
    @staticmethod
    def insert(arr, obj, values, axis=None):
        """
        Insert values along the given axis before the given indices.

        Parameters
        ----------
        arr : array_like
            Input array.
        obj : int, slice or sequence of ints
            Object that defines the index or indices before which `values` is
            inserted.

            .. versionadded:: 1.8.0

            Support for multiple insertions when `obj` is a single scalar or a
            sequence with one element (similar to calling insert multiple
            times).
        values : array_like
            Values to insert into `arr`. If the type of `values` is different
            from that of `arr`, `values` is converted to the type of `arr`.
            `values` should be shaped so that ``arr[...,obj,...] = values``
            is legal.
        axis : int, optional
            Axis along which to insert `values`.  If `axis` is None then `arr`
            is flattened first.

        Returns
        -------
        out : ndarray
            A copy of `arr` with `values` inserted.  Note that `insert`
            does not occur in-place: a new array is returned. If
            `axis` is None, `out` is a flattened array.

        See Also
        --------
        append : Append elements at the end of an array.
        concatenate : Join a sequence of arrays along an existing axis.
        delete : Delete elements from an array.

        Notes
        -----
        Note that for higher dimensional inserts `obj=0` behaves very different
        from `obj=[0]` just like `arr[:,0,:] = values` is different from
        `arr[:,[0],:] = values`.

        Examples
        --------
        >>> a = np.array([[1, 1], [2, 2], [3, 3]])
        >>> a
        array([[1, 1],
               [2, 2],
               [3, 3]])
        >>> np.insert(a, 1, 5)
        array([1, 5, 1, 2, 2, 3, 3])
        >>> np.insert(a, 1, 5, axis=1)
        array([[1, 5, 1],
               [2, 5, 2],
               [3, 5, 3]])

        Difference between sequence and scalars:

        >>> np.insert(a, [1], [[1],[2],[3]], axis=1)
        array([[1, 1, 1],
               [2, 2, 2],
               [3, 3, 3]])
        >>> np.array_equal(np.insert(a, 1, [1, 2, 3], axis=1),
        ...                np.insert(a, [1], [[1],[2],[3]], axis=1))
        True

        >>> b = a.flatten()
        >>> b
        array([1, 1, 2, 2, 3, 3])
        >>> np.insert(b, [2, 2], [5, 6])
        array([1, 1, 5, 6, 2, 2, 3, 3])

        >>> np.insert(b, slice(2, 4), [5, 6])
        array([1, 1, 5, 2, 6, 2, 3, 3])

        >>> np.insert(b, [2, 2], [7.13, False]) # type casting
        array([1, 1, 7, 0, 2, 2, 3, 3])

        >>> x = np.arange(8).reshape(2, 4)
        >>> idx = (1, 3)
        >>> np.insert(x, idx, 999, axis=1)
        array([[  0, 999,   1,   2, 999,   3],
               [  4, 999,   5,   6, 999,   7]])

        """
        wrap = None
        if type(arr) is not ndarray:
            try:
                wrap = arr.__array_wrap__
            except AttributeError:
                pass

        arr = asarray(arr)
        ndim = arr.ndim
        arrorder = 'F' if arr.flags.fnc else 'C'
        if axis is None:
            if ndim != 1:
                arr = arr.ravel()
            ndim = arr.ndim
            axis = ndim - 1
        elif ndim == 0:
            # 2013-09-24, 1.9
            warnings.warn(
                "in the future the special handling of scalars will be removed "
                "from insert and raise an error", DeprecationWarning, stacklevel=2)
            arr = arr.copy(order=arrorder)
            arr[...] = values
            if wrap:
                return wrap(arr)
            else:
                return arr
        else:
            axis = normalize_axis_index(axis, ndim)
        slobj = [slice(None)]*ndim
        N = arr.shape[axis]
        newshape = list(arr.shape)

        if isinstance(obj, slice):
            # turn it into a range object
            indices = arange(*obj.indices(N), **{'dtype': intp})
        else:
            # need to copy obj, because indices will be changed in-place
            indices = np.array(obj)
            if indices.dtype == bool:
                # See also delete
                warnings.warn(
                    "in the future insert will treat boolean arrays and "
                    "array-likes as a boolean index instead of casting it to "
                    "integer", FutureWarning, stacklevel=2)
                indices = indices.astype(intp)
                # Code after warning period:
                #if obj.ndim != 1:
                #    raise ValueError('boolean array argument obj to insert '
                #                     'must be one dimensional')
                #indices = np.flatnonzero(obj)
            elif indices.ndim > 1:
                raise ValueError(
                    "index array argument obj to insert must be one dimensional "
                    "or scalar")
        if indices.size == 1:
            index = indices.item()
            if index < -N or index > N:
                raise IndexError(
                    "index %i is out of bounds for axis %i with "
                    "size %i" % (obj, axis, N))
            if (index < 0):
                index += N

            # There are some object array corner cases here, but we cannot avoid
            # that:
            values = array(values, copy=False, ndmin=arr.ndim, dtype=arr.dtype)
            if indices.ndim == 0:
                # broadcasting is very different here, since a[:,0,:] = ... behaves
                # very different from a[:,[0],:] = ...! This changes values so that
                # it works likes the second case. (here a[:,0:1,:])
                values = nptest.moveaxis(values, 0, axis)
            numnew = values.shape[axis]
            newshape[axis] += numnew
            new = empty(newshape, arr.dtype, arrorder)
            slobj[axis] = slice(None, index)
            new[slobj] = arr[slobj]
            slobj[axis] = slice(index, index+numnew)
            new[slobj] = values
            slobj[axis] = slice(index+numnew, None)
            slobj2 = [slice(None)] * ndim
            slobj2[axis] = slice(index, None)
            new[slobj] = arr[slobj2]
            if wrap:
                return wrap(new)
            return new
        elif indices.size == 0 and not isinstance(obj, np.ndarray):
            # Can safely cast the empty list to intp
            indices = indices.astype(intp)

        if not np.can_cast(indices, intp, 'same_kind'):
            # 2013-09-24, 1.9
            warnings.warn(
                "using a non-integer array as obj in insert will result in an "
                "error in the future", DeprecationWarning, stacklevel=2)
            indices = indices.astype(intp)

        indices[indices < 0] += N

        numnew = len(indices)
        order = indices.argsort(kind='mergesort')   # stable sort
        indices[order] += np.arange(numnew)

        newshape[axis] += numnew
        old_mask = ones(newshape[axis], dtype=bool)
        old_mask[indices] = False

        new = empty(newshape, arr.dtype, arrorder)
        slobj2 = [slice(None)]*ndim
        slobj[axis] = indices
        slobj2[axis] = old_mask
        new[slobj] = values
        new[slobj2] = arr

        if wrap:
            return wrap(new)
        return new

    @staticmethod
    def moveaxis(a, source, destination):
        """
        Move axes of an array to new positions.

        Other axes remain in their original order.

        .. versionadded:: 1.11.0

        Parameters
        ----------
        a : np.ndarray
            The array whose axes should be reordered.
        source : int or sequence of int
            Original positions of the axes to move. These must be unique.
        destination : int or sequence of int
            Destination positions for each of the original axes. These must also be
            unique.

        Returns
        -------
        result : np.ndarray
            Array with moved axes. This array is a view of the input array.

        See Also
        --------
        transpose: Permute the dimensions of an array.
        swapaxes: Interchange two axes of an array.

        Examples
        --------

        >>> x = np.zeros((3, 4, 5))
        >>> np.moveaxis(x, 0, -1).shape
        (4, 5, 3)
        >>> np.moveaxis(x, -1, 0).shape
        (5, 3, 4)

        These all achieve the same result:

        >>> np.transpose(x).shape
        (5, 4, 3)
        >>> np.swapaxes(x, 0, -1).shape
        (5, 4, 3)
        >>> np.moveaxis(x, [0, 1], [-1, -2]).shape
        (5, 4, 3)
        >>> np.moveaxis(x, [0, 1, 2], [-1, -2, -3]).shape
        (5, 4, 3)

        """
        try:
            # allow duck-array types if they define transpose
            transpose = a.transpose
        except AttributeError:
            a = asarray(a)
            transpose = a.transpose

        source = nptest.normalize_axis_tuple(source, a.ndim, 'source')
        destination = nptest.normalize_axis_tuple(destination, a.ndim, 'destination')
        if len(source) != len(destination):
            raise ValueError('`source` and `destination` arguments must have '
                             'the same number of elements')

        order = [n for n in range(a.ndim) if n not in source]

        for dest, src in sorted(zip(destination, source)):
            order.insert(dest, src)

        result = transpose(order)
        return result

    @staticmethod
    def normalize_axis_tuple(axis, ndim, argname=None, allow_duplicate=False):
        """
        Normalizes an axis argument into a tuple of non-negative integer axes.

        This handles shorthands such as ``1`` and converts them to ``(1,)``,
        as well as performing the handling of negative indices covered by
        `normalize_axis_index`.

        By default, this forbids axes from being specified multiple times.

        Used internally by multi-axis-checking logic.

        .. versionadded:: 1.13.0

        Parameters
        ----------
        axis : int, iterable of int
            The un-normalized index or indices of the axis.
        ndim : int
            The number of dimensions of the array that `axis` should be normalized
            against.
        argname : str, optional
            A prefix to put before the error message, typically the name of the
            argument.
        allow_duplicate : bool, optional
            If False, the default, disallow an axis from being specified twice.

        Returns
        -------
        normalized_axes : tuple of int
            The normalized axis index, such that `0 <= normalized_axis < ndim`

        Raises
        ------
        AxisError
            If any axis provided is out of range
        ValueError
            If an axis is repeated

        See also
        --------
        normalize_axis_index : normalizing a single scalar axis
        """
        try:
            axis = [operator.index(axis)]
        except TypeError:
            axis = tuple(axis)
        axis = tuple(normalize_axis_index(ax, ndim, argname) for ax in axis)
        if not allow_duplicate and len(set(axis)) != len(axis):
            if argname:
                raise ValueError('repeated axis in `{}` argument'.format(argname))
            else:
                raise ValueError('repeated axis')
        return axis
    @staticmethod
    def tri(N, M=None, k=0, dtype=float):
        """
        An array with ones at and below the given diagonal and zeros elsewhere.

        Parameters
        ----------
        N : int
            Number of rows in the array.
        M : int, optional
            Number of columns in the array.
            By default, `M` is taken equal to `N`.
        k : int, optional
            The sub-diagonal at and below which the array is filled.
            `k` = 0 is the main diagonal, while `k` < 0 is below it,
            and `k` > 0 is above.  The default is 0.
        dtype : dtype, optional
            Data type of the returned array.  The default is float.

        Returns
        -------
        tri : ndarray of shape (N, M)
            Array with its lower triangle filled with ones and zero elsewhere;
            in other words ``T[i,j] == 1`` for ``i <= j + k``, 0 otherwise.

        Examples
        --------
        >>> np.tri(3, 5, 2, dtype=int)
        array([[1, 1, 1, 0, 0],
               [1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1]])

        >>> np.tri(3, 5, -1)
        array([[ 0.,  0.,  0.,  0.,  0.],
               [ 1.,  0.,  0.,  0.,  0.],
               [ 1.,  1.,  0.,  0.,  0.]])

        """
        if M is None:
            M = N

        A = arange(N, dtype=nptest._min_int(0, N))
        B = arange(-k, M-k, dtype=nptest._min_int(-k, M - k))

        try:
            alen = len(A)
            blen = len(B)
            r = empty([alen,blen])
            for i in range(len(A)):
                for j in range(len(B)):
                    r[i,j] = greater_equal(A[i], B[j]) # op = ufunc in question
        except Exception as e:
            print(e)

        M1 = r
        #try:
        #    m = np.greater_equal.outer(T1)
        #except Exception as e:
        #    print(e)

        m = np.greater_equal.outer(arange(N, dtype=nptest._min_int(0, N)),
                                arange(-k, M-k, dtype=nptest._min_int(-k, M - k)))

        # Avoid making a copy if the requested type is already bool
        m = m.astype(dtype, copy=False)

        return m

    
    i1 = iinfo(int8)
    i2 = iinfo(int16)
    i4 = iinfo(int32)

    @staticmethod
    def _min_int(low, high):
        """ get small int that fits the range """
        if high <= nptest.i1.max and low >= nptest.i1.min:
            return int8
        if high <= nptest.i2.max and low >= nptest.i2.min:
            return int16
        if high <= nptest.i4.max and low >= nptest.i4.min:
            return int32
        return int64

    @staticmethod
    def _unpack_tuple(x):
        """ Unpacks one-element tuples for use as return values """
        if len(x) == 1:
            return x[0]
        else:
            return x

    @staticmethod
    def unique(ar, return_index=False, return_inverse=False,
               return_counts=False, axis=None):
        """
        Find the unique elements of an array.

        Returns the sorted unique elements of an array. There are three optional
        outputs in addition to the unique elements:

        * the indices of the input array that give the unique values
        * the indices of the unique array that reconstruct the input array
        * the number of times each unique value comes up in the input array

        Parameters
        ----------
        ar : array_like
            Input array. Unless `axis` is specified, this will be flattened if it
            is not already 1-D.
        return_index : bool, optional
            If True, also return the indices of `ar` (along the specified axis,
            if provided, or in the flattened array) that result in the unique array.
        return_inverse : bool, optional
            If True, also return the indices of the unique array (for the specified
            axis, if provided) that can be used to reconstruct `ar`.
        return_counts : bool, optional
            If True, also return the number of times each unique item appears
            in `ar`.

            .. versionadded:: 1.9.0

        axis : int or None, optional
            The axis to operate on. If None, `ar` will be flattened. If an integer,
            the subarrays indexed by the given axis will be flattened and treated
            as the elements of a 1-D array with the dimension of the given axis,
            see the notes for more details.  Object arrays or structured arrays
            that contain objects are not supported if the `axis` kwarg is used. The
            default is None.

            .. versionadded:: 1.13.0

        Returns
        -------
        unique : ndarray
            The sorted unique values.
        unique_indices : ndarray, optional
            The indices of the first occurrences of the unique values in the
            original array. Only provided if `return_index` is True.
        unique_inverse : ndarray, optional
            The indices to reconstruct the original array from the
            unique array. Only provided if `return_inverse` is True.
        unique_counts : ndarray, optional
            The number of times each of the unique values comes up in the
            original array. Only provided if `return_counts` is True.

            .. versionadded:: 1.9.0

        See Also
        --------
        numpy.lib.arraysetops : Module with a number of other functions for
                                performing set operations on arrays.

        Notes
        -----
        When an axis is specified the subarrays indexed by the axis are sorted.
        This is done by making the specified axis the first dimension of the array
        and then flattening the subarrays in C order. The flattened subarrays are
        then viewed as a structured type with each element given a label, with the
        effect that we end up with a 1-D array of structured types that can be
        treated in the same way as any other 1-D array. The result is that the
        flattened subarrays are sorted in lexicographic order starting with the
        first element.

        Examples
        --------
        >>> np.unique([1, 1, 2, 2, 3, 3])
        array([1, 2, 3])
        >>> a = np.array([[1, 1], [2, 3]])
        >>> np.unique(a)
        array([1, 2, 3])

        Return the unique rows of a 2D array

        >>> a = np.array([[1, 0, 0], [1, 0, 0], [2, 3, 4]])
        >>> np.unique(a, axis=0)
        array([[1, 0, 0], [2, 3, 4]])

        Return the indices of the original array that give the unique values:

        >>> a = np.array(['a', 'b', 'b', 'c', 'a'])
        >>> u, indices = np.unique(a, return_index=True)
        >>> u
        array(['a', 'b', 'c'],
               dtype='|S1')
        >>> indices
        array([0, 1, 3])
        >>> a[indices]
        array(['a', 'b', 'c'],
               dtype='|S1')

        Reconstruct the input array from the unique values:

        >>> a = np.array([1, 2, 6, 4, 2, 3, 2])
        >>> u, indices = np.unique(a, return_inverse=True)
        >>> u
        array([1, 2, 3, 4, 6])
        >>> indices
        array([0, 1, 4, 3, 1, 2, 1])
        >>> u[indices]
        array([1, 2, 6, 4, 2, 3, 2])

        """
        ar = np.asanyarray(ar)
        if axis is None:
            ret = _unique1d(ar, return_index, return_inverse, return_counts)
            return _unpack_tuple(ret)

        # axis was specified and not None
        try:
            ar = np.swapaxes(ar, axis, 0)
        except np.AxisError:
            # this removes the "axis1" or "axis2" prefix from the error message
            raise np.AxisError(axis, ar.ndim)

        # Must reshape to a contiguous 2D array for this to work...
        orig_shape, orig_dtype = ar.shape, ar.dtype
        ar = ar.reshape(orig_shape[0], -1)
        ar = np.ascontiguousarray(ar)
        dtype = [('f{i}'.format(i=i), ar.dtype) for i in range(ar.shape[1])]

        try:
            consolidated = ar.view(dtype)
           
        except TypeError:
            # There's no good way to do this for object arrays, etc...
            msg = 'The axis argument to unique is not supported for dtype {dt}'
            raise TypeError(msg.format(dt=ar.dtype))

        def reshape_uniq(uniq):
            uniq = uniq.view(orig_dtype)
            uniq = uniq.reshape(-1, *orig_shape[1:])
            uniq = np.swapaxes(uniq, 0, axis)
            return uniq

        output = nptest._unique1d(consolidated, return_index,
                           return_inverse, return_counts)
        output = (reshape_uniq(output[0]),) + output[1:]
        return _unpack_tuple(output)

    @staticmethod
    def _unique1d(ar1, return_index=False, return_inverse=False,
                  return_counts=False):
        """
        Find the unique elements of an array, ignoring shape.
        """
        ar = np.asanyarray(ar1).flatten()

        optional_indices = return_index or return_inverse

        if optional_indices:
            perm = ar.argsort(kind='mergesort' if return_index else 'quicksort')
            aux = ar[perm]
        else:
            ar.sort()
            aux = ar
        mask = np.empty(aux.shape, dtype=np.bool_)
        mask[:1] = True
        mask[1:] = aux[1:] != aux[:-1]

        ret = (aux[mask],)
        if return_index:
            ret += (perm[mask],)
        if return_inverse:
            imask = np.cumsum(mask) - 1
            inv_idx = np.empty(mask.shape, dtype=np.intp)
            inv_idx[perm] = imask
            ret += (inv_idx,)
        if return_counts:
            idx = np.concatenate(np.nonzero(mask) + ([mask.size],))
            ret += (np.diff(idx),)
        return ret

    @staticmethod
    def stack(arrays, axis=0, out=None):
        """
        Join a sequence of arrays along a new axis.

        The `axis` parameter specifies the index of the new axis in the dimensions
        of the result. For example, if ``axis=0`` it will be the first dimension
        and if ``axis=-1`` it will be the last dimension.

        .. versionadded:: 1.10.0

        Parameters
        ----------
        arrays : sequence of array_like
            Each array must have the same shape.
        axis : int, optional
            The axis in the result array along which the input arrays are stacked.
        out : ndarray, optional
            If provided, the destination to place the result. The shape must be
            correct, matching that of what stack would have returned if no
            out argument were specified.

        Returns
        -------
        stacked : ndarray
            The stacked array has one more dimension than the input arrays.

        See Also
        --------
        concatenate : Join a sequence of arrays along an existing axis.
        split : Split array into a list of multiple sub-arrays of equal size.
        block : Assemble arrays from blocks.

        Examples
        --------
        >>> arrays = [np.random.randn(3, 4) for _ in range(10)]
        >>> np.stack(arrays, axis=0).shape
        (10, 3, 4)

        >>> np.stack(arrays, axis=1).shape
        (3, 10, 4)

        >>> np.stack(arrays, axis=2).shape
        (3, 4, 10)

        >>> a = np.array([1, 2, 3])
        >>> b = np.array([2, 3, 4])
        >>> np.stack((a, b))
        array([[1, 2, 3],
               [2, 3, 4]])

        >>> np.stack((a, b), axis=-1)
        array([[1, 2],
               [2, 3],
               [3, 4]])

        """
        arrays = [asanyarray(arr) for arr in arrays]
        if not arrays:
            raise ValueError('need at least one array to stack')

        shapes = set(arr.shape for arr in arrays)
        if len(shapes) != 1:
            raise ValueError('all input arrays must have the same shape')

        result_ndim = arrays[0].ndim + 1
        axis = normalize_axis_index(axis, result_ndim)

        sl = (slice(None),) * axis + (_nx.newaxis,)
        expanded_arrays = [arr[sl] for arr in arrays]
        return _nx.concatenate(expanded_arrays, axis=axis, out=out)

    @staticmethod
    def get_array_prepare(*args):
        return None

    @staticmethod
    def get_array_wrap(*args):
        return None


    @staticmethod
    def kron(a, b):

        b = np.asanyarray(b)
        a = np.array(a, copy=False, subok=True, ndmin=b.ndim)
        ndb, nda = b.ndim, a.ndim
        if (nda == 0 or ndb == 0):
            return _nx.multiply(a, b)
        as_ = a.shape
        bs = b.shape
        if not a.flags.contiguous:
            a = reshape(a, as_)
        if not b.flags.contiguous:
            b = reshape(b, bs)
        nd = ndb
        if (ndb != nda):
            if (ndb > nda):
                as_ = (1,)*(ndb-nda) + as_
            else:
                bs = (1,)*(nda-ndb) + bs
                nd = nda
        result = np.outer(a, b).reshape(as_+bs)
        axis = nd-1
        for _ in range(nd):
            print("input = ", result)
            result = np.concatenate(result, axis=axis)
            print("output = ", result)
            kk = 1

        #wrapper = get_array_prepare(a, b)
        #if wrapper is not None:
        #    result = wrapper(result)
        #wrapper = get_array_wrap(a, b)
        #if wrapper is not None:
        #    result = wrapper(result)
        return result

    @staticmethod
    def tile(A, reps):
        try:
            tup = tuple(reps)
        except TypeError:
            tup = (reps,)
        d = len(tup)
        if all(x == 1 for x in tup) and isinstance(A, _nx.ndarray):
            # Fixes the problem that the function does not make a copy if A is a
            # numpy array and the repetitions are 1 in all dimensions
            return _nx.array(A, copy=True, subok=True, ndmin=d)
        else:
            # Note that no copy of zero-sized arrays is made. However since they
            # have no data there is no risk of an inadvertent overwrite.
            c = _nx.array(A, copy=False, subok=True, ndmin=d)
        if (d < c.ndim):
            tup = (1,)*(c.ndim-d) + tup
        shape_out = tuple(s*t for s, t in zip(c.shape, tup))
        n = c.size
        if n > 0:
            for dim_in, nrep in zip(c.shape, tup):
                if nrep != 1:
                    c = c.reshape(-1, n).repeat(nrep, 0)
                n //= dim_in
        return c.reshape(shape_out)

    @staticmethod
    def select(condlist, choicelist, default=0):
        n = len(condlist)
        n2 = len(choicelist)
        if n2 != n:
            raise ValueError("list of cases must be same length as list of conditions")
        choicelist = [default] + choicelist
        S = 0
        pfac = 1
        for k in range(1, n+1):
            S += k * pfac * np.asarray(condlist[k-1])
            if k < n:
                pfac *= (1-np.asarray(condlist[k-1]))
        # handle special case of a 1-element condition but
        #  a multi-element choice
        if type(S) in np.ScalarType or max(asarray(S).shape)==1:
            pfac = asarray(1)
            for k in range(n2+1):
                pfac = pfac + asarray(choicelist[k])
            if type(S) in ScalarType:
                S = S*np.ones(asarray(pfac).shape, type(S))
            else:
                S = S*np.ones(asarray(pfac).shape, S.dtype)
        return np.choose(S, tuple(choicelist))


    
    @staticmethod
    def rollaxis(a, axis, start=0):

        n = a.ndim
        axis = normalize_axis_index(axis, n)
        if start < 0:
            start += n
        msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
        if not (0 <= start < n + 1):
            raise AxisError(msg % ('start', -n, 'start', n + 1, start))
        if axis < start:
            # it's been removed
            start -= 1
        if axis == start:
            return a[...]
        axes = list(range(0, n))
        axes.remove(axis)
        axes.insert(start, axis)
        return a.transpose(axes)

    @staticmethod
    def percentile(a, q, axis=None, out=None,
               overwrite_input=False, interpolation='linear', keepdims=False):
        """
        Compute the qth percentile of the data along the specified axis.

        Returns the qth percentile(s) of the array elements.

        Parameters
        ----------
        a : array_like
            Input array or object that can be converted to an array.
        q : array_like of float
            Percentile or sequence of percentiles to compute, which must be between
            0 and 100 inclusive.
        axis : {int, tuple of int, None}, optional
            Axis or axes along which the percentiles are computed. The
            default is to compute the percentile(s) along a flattened
            version of the array.

            .. versionchanged:: 1.9.0
                A tuple of axes is supported
        out : ndarray, optional
            Alternative output array in which to place the result. It must
            have the same shape and buffer length as the expected output,
            but the type (of the output) will be cast if necessary.
        overwrite_input : bool, optional
            If True, then allow the input array `a` to be modified by intermediate
            calculations, to save memory. In this case, the contents of the input
            `a` after this function completes is undefined.
        interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
            This optional parameter specifies the interpolation method to
            use when the desired quantile lies between two data points
            ``i < j``:
                * linear: ``i + (j - i) * fraction``, where ``fraction``
                  is the fractional part of the index surrounded by ``i``
                  and ``j``.
                * lower: ``i``.
                * higher: ``j``.
                * nearest: ``i`` or ``j``, whichever is nearest.
                * midpoint: ``(i + j) / 2``.

            .. versionadded:: 1.9.0
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left in
            the result as dimensions with size one. With this option, the
            result will broadcast correctly against the original array `a`.

            .. versionadded:: 1.9.0

        Returns
        -------
        percentile : scalar or ndarray
            If `q` is a single percentile and `axis=None`, then the result
            is a scalar. If multiple percentiles are given, first axis of
            the result corresponds to the percentiles. The other axes are
            the axes that remain after the reduction of `a`. If the input
            contains integers or floats smaller than ``float64``, the output
            data-type is ``float64``. Otherwise, the output data-type is the
            same as that of the input. If `out` is specified, that array is
            returned instead.

        See Also
        --------
        mean
        median : equivalent to ``percentile(..., 50)``
        nanpercentile

        Notes
        -----
        Given a vector ``V`` of length ``N``, the ``q``-th percentile of
        ``V`` is the value ``q/100`` of the way from the minimum to the
        maximum in a sorted copy of ``V``. The values and distances of
        the two nearest neighbors as well as the `interpolation` parameter
        will determine the percentile if the normalized ranking does not
        match the location of ``q`` exactly. This function is the same as
        the median if ``q=50``, the same as the minimum if ``q=0`` and the
        same as the maximum if ``q=100``.

        Examples
        --------
        >>> a = np.array([[10, 7, 4], [3, 2, 1]])
        >>> a
        array([[10,  7,  4],
               [ 3,  2,  1]])
        >>> np.percentile(a, 50)
        3.5
        >>> np.percentile(a, 50, axis=0)
        array([[ 6.5,  4.5,  2.5]])
        >>> np.percentile(a, 50, axis=1)
        array([ 7.,  2.])
        >>> np.percentile(a, 50, axis=1, keepdims=True)
        array([[ 7.],
               [ 2.]])

        >>> m = np.percentile(a, 50, axis=0)
        >>> out = np.zeros_like(m)
        >>> np.percentile(a, 50, axis=0, out=out)
        array([[ 6.5,  4.5,  2.5]])
        >>> m
        array([[ 6.5,  4.5,  2.5]])

        >>> b = a.copy()
        >>> np.percentile(b, 50, axis=1, overwrite_input=True)
        array([ 7.,  2.])
        >>> assert not np.all(a == b)

        """
        q = np.true_divide(q, 100.0)  # handles the asarray for us too
        if not nptest._quantile_is_valid(q):
            raise ValueError("Percentiles must be in the range [0, 100]")
        return nptest._quantile_unchecked(
            a, q, axis, out, overwrite_input, interpolation, keepdims)

    @staticmethod
    def _quantile_unchecked(a, q, axis=None, out=None, overwrite_input=False,
                        interpolation='linear', keepdims=False):
        """Assumes that q is in [0, 1], and is an ndarray"""
        r, k = nptest._ureduce(a, func=nptest._quantile_ureduce_func, q=q, axis=axis, out=out,
                        overwrite_input=overwrite_input,
                        interpolation=interpolation)
        if keepdims:
            return r.reshape(q.shape + k)
        else:
            return r

    @staticmethod
    def _quantile_is_valid(q):
        # avoid expensive reductions, relevant for arrays with < O(1000) elements
        if q.ndim == 1 and q.size < 10:
            for i in range(q.size):
                if q[i] < 0.0 or q[i] > 1.0:
                    return False
        else:
            # faster than any()
            if np.count_nonzero(q < 0.0) or np.count_nonzero(q > 1.0):
                return False
        return True



    @staticmethod
    def _ureduce(a, func, **kwargs):
        """
        Internal Function.
        Call `func` with `a` as first argument swapping the axes to use extended
        axis on functions that don't support it natively.

        Returns result and a.shape with axis dims set to 1.

        Parameters
        ----------
        a : array_like
            Input array or object that can be converted to an array.
        func : callable
            Reduction function capable of receiving a single axis argument.
            It is called with `a` as first argument followed by `kwargs`.
        kwargs : keyword arguments
            additional keyword arguments to pass to `func`.

        Returns
        -------
        result : tuple
            Result of func(a, **kwargs) and a.shape with axis dims set to 1
            which can be used to reshape the result to the same shape a ufunc with
            keepdims=True would produce.

        """
        a = np.asanyarray(a)
        axis = kwargs.get('axis', None)
        if axis is not None:
            keepdim = list(a.shape)
            nd = a.ndim
            axis = _nx.normalize_axis_tuple(axis, nd)

            for ax in axis:
                keepdim[ax] = 1

            if len(axis) == 1:
                kwargs['axis'] = axis[0]
            else:
                keep = set(range(nd)) - set(axis)
                nkeep = len(keep)
                # swap axis that should not be reduced to front
                for i, s in enumerate(sorted(keep)):
                    a = a.swapaxes(i, s)
                # merge reduced axis
                a = a.reshape(a.shape[:nkeep] + (-1,))
                kwargs['axis'] = -1
            keepdim = tuple(keepdim)
        else:
            keepdim = (1,) * a.ndim

        r = func(a, **kwargs)
        return r, keepdim


    @staticmethod
    def _quantile_ureduce_func(a, q, axis=None, out=None, overwrite_input=False,
                               interpolation='linear', keepdims=False):
        a = asarray(a)
        if q.ndim == 0:
            # Do not allow 0-d arrays because following code fails for scalar
            zerod = True
            q = q[None]
        else:
            zerod = False

        # prepare a for partitioning
        if overwrite_input:
            if axis is None:
                ap = a.ravel()
            else:
                ap = a
        else:
            if axis is None:
                ap = a.flatten()
            else:
                ap = a.copy()

        if axis is None:
            axis = 0

        Nx = ap.shape[axis]
        indices = q * (Nx - 1)

        # round fractional indices according to interpolation method
        if interpolation == 'lower':
            indices = floor(indices).astype(intp)
        elif interpolation == 'higher':
            indices = ceil(indices).astype(intp)
        elif interpolation == 'midpoint':
            indices = 0.5 * (floor(indices) + ceil(indices))
        elif interpolation == 'nearest':
            indices = around(indices).astype(intp)
        elif interpolation == 'linear':
            pass  # keep index as fraction and interpolate
        else:
            raise ValueError(
                "interpolation can only be 'linear', 'lower' 'higher', "
                "'midpoint', or 'nearest'")

        n = np.array(False, dtype=bool) # check for nan's flag
        if indices.dtype == intp:  # take the points along axis
            # Check if the array contains any nan's
            if np.issubdtype(a.dtype, np.inexact):
                indices = concatenate((indices, [-1]))

            ap.partition(indices, axis=axis)
            # ensure axis with qth is first
            ap = np.moveaxis(ap, axis, 0)
            axis = 0

            # Check if the array contains any nan's
            if np.issubdtype(a.dtype, np.inexact):
                indices = indices[:-1]
                n = np.isnan(ap[-1:, ...])

            if zerod:
                indices = indices[0]
            r = take(ap, indices, axis=axis, out=out)


        else:  # weight the points above and below the indices
            indices_below = floor(indices).astype(intp)
            indices_above = indices_below + 1
            indices_above[indices_above > Nx - 1] = Nx - 1

            # Check if the array contains any nan's
            if np.issubdtype(a.dtype, np.inexact):
                indices_above = concatenate((indices_above, [-1]))

            weights_above = indices - indices_below
            weights_below = 1.0 - weights_above

            weights_shape = [1, ] * ap.ndim
            weights_shape[axis] = len(indices)
            weights_below.shape = weights_shape
            weights_above.shape = weights_shape

            ap.partition(concatenate((indices_below, indices_above)), axis=axis)

            # ensure axis with qth is first
            ap = np.moveaxis(ap, axis, 0)
            weights_below = np.moveaxis(weights_below, axis, 0)
            weights_above = np.moveaxis(weights_above, axis, 0)
            axis = 0

            # Check if the array contains any nan's
            if np.issubdtype(a.dtype, np.inexact):
                indices_above = indices_above[:-1]
                n = np.isnan(ap[-1:, ...])

            x1 = take(ap, indices_below, axis=axis) * weights_below
            x2 = take(ap, indices_above, axis=axis) * weights_above

            # ensure axis with qth is first
            x1 = np.moveaxis(x1, axis, 0)
            x2 = np.moveaxis(x2, axis, 0)

            if zerod:
                x1 = x1.squeeze(0)
                x2 = x2.squeeze(0)

            if out is not None:
                r = add(x1, x2, out=out)
            else:
                r = add(x1, x2)

        if np.any(n):
            warnings.warn("Invalid value encountered in percentile",
                          RuntimeWarning, stacklevel=3)
            if zerod:
                if ap.ndim == 1:
                    if out is not None:
                        out[...] = a.dtype.type(np.nan)
                        r = out
                    else:
                        r = a.dtype.type(np.nan)
                else:
                    r[..., n.squeeze(0)] = a.dtype.type(np.nan)
            else:
                if r.ndim == 1:
                    r[:] = a.dtype.type(np.nan)
                else:
                    r[..., n.repeat(q.size, 0)] = a.dtype.type(np.nan)

        return r


    def _chbevl(x, vals):
        b0 = vals[0]
        b1 = 0.0

        for i in range(1, len(vals)):
            b2 = b1
            b1 = b0
            b0 = x*b1 - b2 + vals[i]

        return 0.5*(b0 - b2)


    def _i0_1(x):
        return exp(x) * _chbevl(x/2.0-2, _i0A)


    def _i0_2(x):
        return exp(x) * _chbevl(32.0/x - 2.0, _i0B) / sqrt(x)


    @staticmethod
    def corrcoef(x, y=None, rowvar=True, bias=np._NoValue, ddof=np._NoValue):

        if bias is not np._NoValue or ddof is not np._NoValue:
            # 2015-03-15, 1.10
            warnings.warn('bias and ddof have no effect and are deprecated',
                          DeprecationWarning, stacklevel=2)
        c = np.cov(x, y, rowvar)
        try:
            d = diag(c)
        except ValueError:
            # scalar covariance
            # nan if incorrect value (nan, inf, 0), 1 otherwise
            return c / c
        stddev = sqrt(d.real)

        s1 = stddev[:, None, None, None]
        s2 = stddev[None, :]

        c /= stddev[:, None]
        c /= stddev[None, :]

        # Clip real and imaginary parts to [-1, 1].  This does not guarantee
        # abs(a[i,j]) <= 1 for complex arrays, but is the best we can do without
        # excessive work.
        np.clip(c.real, -1, 1, out=c.real)
        if np.iscomplexobj(c):
            np.clip(c.imag, -1, 1, out=c.imag)

        return c


    _i0A = [
        -4.41534164647933937950E-18,
        3.33079451882223809783E-17,
        -2.43127984654795469359E-16,
        1.71539128555513303061E-15,
        -1.16853328779934516808E-14,
        7.67618549860493561688E-14,
        -4.85644678311192946090E-13,
        2.95505266312963983461E-12,
        -1.72682629144155570723E-11,
        9.67580903537323691224E-11,
        -5.18979560163526290666E-10,
        2.65982372468238665035E-9,
        -1.30002500998624804212E-8,
        6.04699502254191894932E-8,
        -2.67079385394061173391E-7,
        1.11738753912010371815E-6,
        -4.41673835845875056359E-6,
        1.64484480707288970893E-5,
        -5.75419501008210370398E-5,
        1.88502885095841655729E-4,
        -5.76375574538582365885E-4,
        1.63947561694133579842E-3,
        -4.32430999505057594430E-3,
        1.05464603945949983183E-2,
        -2.37374148058994688156E-2,
        4.93052842396707084878E-2,
        -9.49010970480476444210E-2,
        1.71620901522208775349E-1,
        -3.04682672343198398683E-1,
        6.76795274409476084995E-1
        ]


    _i0B = [
        -7.23318048787475395456E-18,
        -4.83050448594418207126E-18,
        4.46562142029675999901E-17,
        3.46122286769746109310E-17,
        -2.82762398051658348494E-16,
        -3.42548561967721913462E-16,
        1.77256013305652638360E-15,
        3.81168066935262242075E-15,
        -9.55484669882830764870E-15,
        -4.15056934728722208663E-14,
        1.54008621752140982691E-14,
        3.85277838274214270114E-13,
        7.18012445138366623367E-13,
        -1.79417853150680611778E-12,
        -1.32158118404477131188E-11,
        -3.14991652796324136454E-11,
        1.18891471078464383424E-11,
        4.94060238822496958910E-10,
        3.39623202570838634515E-9,
        2.26666899049817806459E-8,
        2.04891858946906374183E-7,
        2.89137052083475648297E-6,
        6.88975834691682398426E-5,
        3.36911647825569408990E-3,
        8.04490411014108831608E-1
        ]

    @staticmethod
    def _chbevl(x, vals):
        b0 = vals[0]
        b1 = 0.0

        for i in range(1, len(vals)):
            b2 = b1
            b1 = b0
            b0 = x*b1 - b2 + vals[i]

        return 0.5*(b0 - b2)

    @staticmethod
    def _i0_1(x):
        return exp(x) *  nptest._chbevl(x/2.0-2, nptest._i0A)

    @staticmethod
    def _i0_2(x):
        return exp(x) *  nptest._chbevl(32.0/x - 2.0, nptest._i0B) / sqrt(x)


    @staticmethod
    def i0(x):
        x = np.atleast_1d(x).copy()
        y = np.empty_like(x)
        ind = (x < 0)
        x[ind] = -x[ind]
        ind = (x <= 8.0)
        y[ind] = nptest._i0_1(x[ind])
        ind2 = ~ind
        y[ind2] = nptest._i0_2(x[ind2])
        return y.squeeze()

    @staticmethod
    def kaiser(M, beta):

        if M == 1:
            return np.array([1.])
        n = arange(0, M)
        alpha = (M-1)/2.0

        div = nptest.i0(float(beta))

        a2 = n-alpha
        a1 = a2/alpha
        s = sqrt(1-a1**2.0)

        return nptest.i0(beta * s)/div

    @staticmethod
    def median(a, axis=None, out=None, overwrite_input=False, keepdims=False):

        r, k = nptest._ureduce(a, func=nptest._median, axis=axis, out=out,
                        overwrite_input=overwrite_input)
        if keepdims:
            return r.reshape(k)
        else:
            return r

    @staticmethod
    def _median(a, axis=None, out=None, overwrite_input=False):
        # can't be reasonably be implemented in terms of percentile as we have to
        # call mean to not break astropy
        a = np.asanyarray(a)

        # Set the partition indexes
        if axis is None:
            sz = a.size
        else:
            sz = a.shape[axis]
        if sz % 2 == 0:
            szh = sz // 2
            kth = [szh - 1, szh]
        else:
            kth = [(sz - 1) // 2]
        # Check if the array contains any nan's
        if np.issubdtype(a.dtype, np.inexact):
            kth.append(-1)

        if overwrite_input:
            if axis is None:
                part = a.ravel()
                part.partition(kth)
            else:
                a.partition(kth, axis=axis)
                part = a
        else:
            part = partition(a, kth, axis=axis)

        if part.shape == ():
            # make 0-D arrays work
            return part.item()
        if axis is None:
            axis = 0

        indexer = [slice(None)] * part.ndim
        index = part.shape[axis] // 2
        if part.shape[axis] % 2 == 1:
            # index with slice to allow mean (below) to work
            indexer[axis] = slice(index, index+1)
        else:
            indexer[axis] = slice(index-1, index+1)

        # Check if the array contains any nan's
        if np.issubdtype(a.dtype, np.inexact) and sz > 0:
            # warn and return nans like mean would
            rout = mean(part[indexer], axis=axis, out=out)
            return np.lib.utils._median_nancheck(part, rout, axis, out)
        else:
            # if there are no nans
            # Use mean in odd and even case to coerce data type
            # and check, use out array.
            return np.mean(part[indexer], axis=axis, out=out)

    @staticmethod
    def nanmedian(a, axis=None, out=None, overwrite_input=False, keepdims=np._NoValue):

        a = np.asanyarray(a)
        # apply_along_axis in _nanmedian doesn't handle empty arrays well,
        # so deal them upfront
        if a.size == 0:
            return np.nanmean(a, axis, out=out, keepdims=keepdims)

        r, k = nptest._ureduce(a, func=nptest._nanmedian, axis=axis, out=out,
                                      overwrite_input=overwrite_input)
        if keepdims and keepdims is not np._NoValue:
            return r.reshape(k)
        else:
            return r

    @staticmethod
    def _nanmedian1d(arr1d, overwrite_input=False):

        arr1d, overwrite_input = nptest._remove_nan_1d(arr1d,
            overwrite_input=overwrite_input)
        if arr1d.size == 0:
            return np.nan

        return np.median(arr1d, overwrite_input=overwrite_input)

    @staticmethod
    def _nanmedian(a, axis=None, out=None, overwrite_input=False):
 
        if axis is None or a.ndim == 1:
            part = a.ravel()
            if out is None:
                return nptest._nanmedian1d(part, overwrite_input)
            else:
                out[...] = nptest._nanmedian1d(part, overwrite_input)
                return out
        else:
            # for small medians use sort + indexing which is still faster than
            # apply_along_axis
            # benchmarked with shuffled (50, 50, x) containing a few NaN
            #if a.shape[axis] < 600:
            #    return nptest._nanmedian_small(a, axis, out, overwrite_input)
            result = np.apply_along_axis(nptest._nanmedian1d, axis, a, overwrite_input)
            if out is not None:
                out[...] = result
            return result

    @staticmethod
    def _nanmedian_small(a, axis=None, out=None, overwrite_input=False):

        a = np.ma.masked_array(a, np.isnan(a))
        m = np.ma.median(a, axis=axis, overwrite_input=overwrite_input)
        for i in range(np.count_nonzero(m.mask.ravel())):
            warnings.warn("All-NaN slice encountered", RuntimeWarning, stacklevel=3)
        if out is not None:
            out[...] = m.filled(np.nan)
            return out
        return m.filled(np.nan)



    @staticmethod
    def _remove_nan_1d(arr1d, overwrite_input=False):
        
        c = np.isnan(arr1d)
        s = np.nonzero(c)[0]
        if s.size == arr1d.size:
            warnings.warn("All-NaN slice encountered", RuntimeWarning, stacklevel=4)
            return arr1d[:0], True
        elif s.size == 0:
            return arr1d, overwrite_input
        else:
            if not overwrite_input:
                arr1d = arr1d.copy()
            # select non-nans at end of array
            enonan = arr1d[-s.size:][~c[-s.size:]]
            # fill nans in beginning of array with non-nans of end
            arr1d[s[:enonan.size]] = enonan

            return arr1d[:-s.size], True

    @staticmethod
    def apply_along_axis(func1d, axis, arr, *args, **kwargs):

        # handle negative axes
        arr = asanyarray(arr)
        nd = arr.ndim
        axis = normalize_axis_index(axis, nd)

        # arr, with the iteration axis at the end
        in_dims = list(range(nd))
        inarr_view = transpose(arr, in_dims[:axis] + in_dims[axis+1:] + [axis])

        # compute indices for the iteration axes, and append a trailing ellipsis to
        # prevent 0d arrays decaying to scalars, which fixes gh-8642
        inds = np.ndindex(inarr_view.shape[:-1])
        inds = (ind + (Ellipsis,) for ind in inds)

        # invoke the function on the first item
        try:
            ind0 = next(inds)
        except StopIteration:
            raise ValueError('Cannot apply_along_axis when any iteration dimensions are 0')

        kevin = inarr_view[ind0]
        res = asanyarray(func1d(inarr_view[ind0], *args, **kwargs))

        # build a buffer for storing evaluations of func1d.
        # remove the requested axis, and add the new ones on the end.
        # laid out so that each write is contiguous.
        # for a tuple index inds, buff[inds] = func1d(inarr_view[inds])
        buff = zeros(inarr_view.shape[:-1] + res.shape, res.dtype)

        # permutation of axes such that out = buff.transpose(buff_permute)
        buff_dims = list(range(buff.ndim))
        buff_permute = (
            buff_dims[0 : axis] +
            buff_dims[buff.ndim-res.ndim : buff.ndim] +
            buff_dims[axis : buff.ndim-res.ndim]
        )

        # matrices have a nasty __array_prepare__ and __array_wrap__
        if True: # not isinstance(res, matrix):
            buff = res.__array_prepare__(buff)

        # save the first result, then compute and save all remaining results
        buff[ind0] = res
        for ind in inds:
            buff[ind] = asanyarray(func1d(inarr_view[ind], *args, **kwargs))

        if True: #not isinstance(res, np.matrix):
            # wrap the array, to preserve subclasses
            buff = res.__array_wrap__(buff)

            # finally, rotate the inserted axes back to where they belong
            return transpose(buff, buff_permute)

        else:
            # matrices have to be transposed first, because they collapse dimensions!
            out_arr = transpose(buff, buff_permute)
            return res.__array_wrap__(out_arr)

    @staticmethod
    def nanpercentile(a, q, axis=None, out=None, overwrite_input=False,
                  interpolation='linear', keepdims=np._NoValue):

        a = np.asanyarray(a)
        q = np.true_divide(q, 100.0)  # handles the asarray for us too
 
        return nptest._nanquantile_unchecked(
            a, q, axis, out, overwrite_input, interpolation, keepdims)

    @staticmethod
    def _nanquantile_unchecked(a, q, axis=None, out=None, overwrite_input=False,
                           interpolation='linear', keepdims=np._NoValue):
        """Assumes that q is in [0, 1], and is an ndarray"""
        # apply_along_axis in _nanpercentile doesn't handle empty arrays well,
        # so deal them upfront
        if a.size == 0:
            return np.nanmean(a, axis, out=out, keepdims=keepdims)

        r, k = nptest._ureduce(
            a, func=nptest._nanquantile_ureduce_func, q=q, axis=axis, out=out,
            overwrite_input=overwrite_input, interpolation=interpolation
        )
        if keepdims and keepdims is not np._NoValue:
            return r.reshape(q.shape + k)
        else:
            return r

    @staticmethod
    def _nanquantile_ureduce_func(a, q, axis=None, out=None, overwrite_input=False,
                              interpolation='linear'):
        """
        Private function that doesn't support extended axis or keepdims.
        These methods are extended to this function using _ureduce
        See nanpercentile for parameter usage
        """
        if axis is None or a.ndim == 1:
            part = a.ravel()
            result = nptest._nanquantile_1d(part, q, overwrite_input, interpolation)
        else:
            result = np.apply_along_axis( nptest._nanquantile_1d, axis, a, q,
                                         overwrite_input, interpolation)
            # apply_along_axis fills in collapsed axis with results.
            # Move that axis to the beginning to match percentile's
            # convention.
            if q.ndim != 0:
                result = np.moveaxis(result, axis, 0)

        if out is not None:
            out[...] = result
        return result

    @staticmethod
    def _nanquantile_1d(arr1d, q, overwrite_input=False, interpolation='linear'):
        """
        Private function for rank 1 arrays. Compute quantile ignoring NaNs.
        See nanpercentile for parameter usage
        """
        arr1d, overwrite_input = nptest._remove_nan_1d(arr1d,
            overwrite_input=overwrite_input)
        if arr1d.size == 0:
            return np.full(q.shape, np.nan)[()]  # convert to scalar

        return nptest._quantile_unchecked(
            arr1d, q, overwrite_input=overwrite_input, interpolation=interpolation)

    
    @staticmethod
    def _replace_nan(a, val):
        """
        If `a` is of inexact type, make a copy of `a`, replace NaNs with
        the `val` value, and return the copy together with a boolean mask
        marking the locations where NaNs were present. If `a` is not of
        inexact type, do nothing and return `a` together with a mask of None.

        Note that scalars will end up as array scalars, which is important
        for using the result as the value of the out argument in some
        operations.

        Parameters
        ----------
        a : array-like
            Input array.
        val : float
            NaN values are set to val before doing the operation.

        Returns
        -------
        y : ndarray
            If `a` is of inexact type, return a copy of `a` with the NaNs
            replaced by the fill value, otherwise return `a`.
        mask: {bool, None}
            If `a` is of inexact type, return a boolean mask marking locations of
            NaNs, otherwise return None.

        """
        a = np.array(a, subok=True, copy=True)

        if a.dtype == np.object_:
            # object arrays do not support `isnan` (gh-9009), so make a guess
            mask = a != a
        elif issubclass(a.dtype.type, np.inexact):
            mask = np.isnan(a)
        else:
            mask = None

        if mask is not None:
            np.copyto(a, val, where=mask)

        return a, mask


    @staticmethod
    def _copyto(a, val, mask):
        """
        Replace values in `a` with NaN where `mask` is True.  This differs from
        copyto in that it will deal with the case where `a` is a numpy scalar.

        Parameters
        ----------
        a : ndarray or numpy scalar
            Array or numpy scalar some of whose values are to be replaced
            by val.
        val : numpy scalar
            Value used a replacement.
        mask : ndarray, scalar
            Boolean array. Where True the corresponding element of `a` is
            replaced by `val`. Broadcasts.

        Returns
        -------
        res : ndarray, scalar
            Array with elements replaced or scalar `val`.

        """
        if isinstance(a, np.ndarray):
            np.copyto(a, val, where=mask, casting='unsafe')
        else:
            a = a.dtype.type(val)
        return a

    @staticmethod
    def _divide_by_count(a, b, out=None):
        """
        Compute a/b ignoring invalid results. If `a` is an array the division
        is done in place. If `a` is a scalar, then its type is preserved in the
        output. If out is None, then then a is used instead so that the
        division is in place. Note that this is only called with `a` an inexact
        type.

        Parameters
        ----------
        a : {ndarray, numpy scalar}
            Numerator. Expected to be of inexact type but not checked.
        b : {ndarray, numpy scalar}
            Denominator.
        out : ndarray, optional
            Alternate output array in which to place the result.  The default
            is ``None``; if provided, it must have the same shape as the
            expected output, but the type will be cast if necessary.

        Returns
        -------
        ret : {ndarray, numpy scalar}
            The return value is a/b. If `a` was an ndarray the division is done
            in place. If `a` is a numpy scalar, the division preserves its type.

        """
        with np.errstate(invalid='ignore', divide='ignore'):
            if isinstance(a, np.ndarray):
                if out is None:
                    return np.divide(a, b, out=a, casting='unsafe')
                else:
                    return np.divide(a, b, out=out, casting='unsafe')
            else:
                if out is None:
                    return a.dtype.type(a / b)
                else:
                    # This is questionable, but currently a numpy scalar can
                    # be output to a zero dimensional array.
                    return np.divide(a, b, out=out, casting='unsafe')


    @staticmethod
    def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue):

        arr, mask = nptest._replace_nan(a, 0)
        if mask is None:
            return np.var(arr, axis=axis, dtype=dtype, out=out, ddof=ddof,
                      keepdims=keepdims)

        if dtype is not None:
            dtype = np.dtype(dtype)
        if dtype is not None and not issubclass(dtype.type, np.inexact):
            raise TypeError("If a is inexact, then dtype must be inexact")
        if out is not None and not issubclass(out.dtype.type, np.inexact):
            raise TypeError("If a is inexact, then out must be inexact")

        # Compute mean
        if type(arr) is np.matrix:
            _keepdims = np._NoValue
        else:
            _keepdims = True
        # we need to special case matrix for reverse compatibility
        # in order for this to work, these sums need to be called with
        # keepdims=True, however matrix now raises an error in this case, but
        # the reason that it drops the keepdims kwarg is to force keepdims=True
        # so this used to work by serendipity.
        cnt = np.sum(~mask, axis=axis, dtype=np.intp, keepdims=_keepdims)
        avg = np.sum(arr, axis=axis, dtype=dtype, keepdims=_keepdims)
        avg = nptest._divide_by_count(avg, cnt)

        # Compute squared deviation from mean.
        np.subtract(arr, avg, out=arr, casting='unsafe')
        arr = nptest._copyto(arr, 0, mask)
        if issubclass(arr.dtype.type, np.complexfloating):
            sqr = np.multiply(arr, arr.conj(), out=arr).real
        else:
            sqr = np.multiply(arr, arr, out=arr)

        # Compute variance.
        var = np.sum(sqr, axis=axis, dtype=dtype, out=out, keepdims=keepdims)
        if var.ndim < cnt.ndim:
            # Subclasses of ndarray may ignore keepdims, so check here.
            cnt = cnt.squeeze(axis)
        dof = cnt - ddof
        var = nptest._divide_by_count(var, dof)

        isbad = (dof <= 0)
        if np.any(isbad):
            warnings.warn("Degrees of freedom <= 0 for slice.", RuntimeWarning, stacklevel=2)
            # NaN, inf, or negative numbers are all possible bad
            # values, so explicitly replace them with NaN.
            var = nptest._copyto(var, np.nan, isbad)
        return var


    @staticmethod
    def test_multiply(a, b, axis):

        multiply.accumulate(a, out=b, axis=axis)

        return

    @staticmethod
    def block(arrays):

        bottom_index, arr_ndim = nptest._block_check_depths_match(arrays)
        list_ndim = len(bottom_index)
        return nptest._block(arrays, list_ndim, max(arr_ndim, list_ndim))

    @staticmethod
    def _block(arrays, max_depth, result_ndim):
        """
        Internal implementation of block. `arrays` is the argument passed to
        block. `max_depth` is the depth of nested lists within `arrays` and
        `result_ndim` is the greatest of the dimensions of the arrays in
        `arrays` and the depth of the lists in `arrays` (see block docstring
        for details).
        """
        def atleast_nd(a, ndim):
            # Ensures `a` has at least `ndim` dimensions by prepending
            # ones to `a.shape` as necessary
            return np.array(a, ndmin=ndim, copy=False, subok=True)

        def block_recursion(arrays, depth=0):
            if depth < max_depth:
                if len(arrays) == 0:
                    raise ValueError('Lists cannot be empty')
                arrs = [block_recursion(arr, depth+1) for arr in arrays]
                return _nx.concatenate(arrs, axis=-(max_depth-depth))
            else:
                # We've 'bottomed out' - arrays is either a scalar or an array
                # type(arrays) is not list
                return atleast_nd(arrays, result_ndim)

        try:
            return block_recursion(arrays)
        finally:
            # recursive closures have a cyclic reference to themselves, which
            # requires gc to collect (gh-10620). To avoid this problem, for
            # performance and PyPy friendliness, we break the cycle:
            block_recursion = None

    @staticmethod
    def _block_check_depths_match(arrays, parent_index=[]):
        """
        Recursive function checking that the depths of nested lists in `arrays`
        all match. Mismatch raises a ValueError as described in the block
        docstring below.

        The entire index (rather than just the depth) needs to be calculated
        for each innermost list, in case an error needs to be raised, so that
        the index of the offending list can be printed as part of the error.

        The parameter `parent_index` is the full index of `arrays` within the
        nested lists passed to _block_check_depths_match at the top of the
        recursion.
        The return value is a pair. The first item returned is the full index
        of an element (specifically the first element) from the bottom of the
        nesting in `arrays`. An empty list at the bottom of the nesting is
        represented by a `None` index.
        The second item is the maximum of the ndims of the arrays nested in
        `arrays`.
        """
        def format_index(index):
            idx_str = ''.join('[{}]'.format(i) for i in index if i is not None)
            return 'arrays' + idx_str
        if type(arrays) is tuple:
            # not strictly necessary, but saves us from:
            #  - more than one way to do things - no point treating tuples like
            #    lists
            #  - horribly confusing behaviour that results when tuples are
            #    treated like ndarray
            raise TypeError(
                '{} is a tuple. '
                'Only lists can be used to arrange blocks, and np.block does '
                'not allow implicit conversion from tuple to ndarray.'.format(
                    format_index(parent_index)
                )
            )
        elif type(arrays) is list and len(arrays) > 0:
            idxs_ndims = (nptest._block_check_depths_match(arr, parent_index + [i])
                          for i, arr in enumerate(arrays))

            first_index, max_arr_ndim = next(idxs_ndims)
            for index, ndim in idxs_ndims:
                if ndim > max_arr_ndim:
                    max_arr_ndim = ndim
                if len(index) != len(first_index):
                    raise ValueError(
                        "List depths are mismatched. First element was at depth "
                        "{}, but there is an element at depth {} ({})".format(
                            len(first_index),
                            len(index),
                            format_index(index)
                        )
                    )
            return first_index, max_arr_ndim
        elif type(arrays) is list and len(arrays) == 0:
            # We've 'bottomed out' on an empty list
            return parent_index + [None], 0
        else:
            # We've 'bottomed out' - arrays is either a scalar or an array
            return parent_index, _nx.ndim(arrays)

    @staticmethod
    def tensordot(a, b, axes=2):

        try:
            iter(axes)
        except Exception:
            axes_a = list(range(-axes, 0))
            axes_b = list(range(0, axes))
        else:
            axes_a, axes_b = axes
        try:
            na = len(axes_a)
            axes_a = list(axes_a)
        except TypeError:
            axes_a = [axes_a]
            na = 1
        try:
            nb = len(axes_b)
            axes_b = list(axes_b)
        except TypeError:
            axes_b = [axes_b]
            nb = 1

        a, b = asarray(a), asarray(b)
        as_ = a.shape
        nda = a.ndim
        bs = b.shape
        ndb = b.ndim
        equal = True
        if na != nb:
            equal = False
        else:
            for k in range(na):
                if as_[axes_a[k]] != bs[axes_b[k]]:
                    equal = False
                    break
                if axes_a[k] < 0:
                    axes_a[k] += nda
                if axes_b[k] < 0:
                    axes_b[k] += ndb
        if not equal:
            raise ValueError("shape-mismatch for sum")

        # Move the axes to sum over to the end of "a"
        # and to the front of "b"
        notin = [k for k in range(nda) if k not in axes_a]
        newaxes_a = notin + axes_a
        N2 = 1
        for axis in axes_a:
            N2 *= as_[axis]
        newshape_a = (int(multiply.reduce([as_[ax] for ax in notin])), N2)
        olda = [as_[axis] for axis in notin]

        notin = [k for k in range(ndb) if k not in axes_b]
        newaxes_b = axes_b + notin
        N2 = 1
        for axis in axes_b:
            N2 *= bs[axis]
        newshape_b = (N2, int(multiply.reduce([bs[ax] for ax in notin])))
        oldb = [bs[axis] for axis in notin]

        at = a.transpose(newaxes_a).reshape(newshape_a)
        bt = b.transpose(newaxes_b).reshape(newshape_b)
        res = np.dot(at, bt)
        return res.reshape(olda + oldb)

    

    @staticmethod
    def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):

        if axis is not None:
            axisa, axisb, axisc = (axis,) * 3
        a = asarray(a)
        b = asarray(b)
        # Check axisa and axisb are within bounds
        axisa = normalize_axis_index(axisa, a.ndim, msg_prefix='axisa')
        axisb = normalize_axis_index(axisb, b.ndim, msg_prefix='axisb')

        # Move working axis to the end of the shape
        a = np.moveaxis(a, axisa, -1)
        b = np.moveaxis(b, axisb, -1)
        msg = ("incompatible dimensions for cross product\n"
               "(dimension must be 2 or 3)")
        if a.shape[-1] not in (2, 3) or b.shape[-1] not in (2, 3):
            raise ValueError(msg)

        # Create the output array
        shape = np.broadcast(a[..., 0], b[..., 0]).shape
        if a.shape[-1] == 3 or b.shape[-1] == 3:
            shape += (3,)
            # Check axisc is within bounds
            axisc = normalize_axis_index(axisc, len(shape), msg_prefix='axisc') 
        dtype = promote_types(a.dtype, b.dtype)
        cp = empty(shape, dtype)

        # create local aliases for readability
        a0 = a[..., 0]
        a1 = a[..., 1]
        if a.shape[-1] == 3:
            a2 = a[..., 2]
        b0 = b[..., 0]
        b1 = b[..., 1]
        if b.shape[-1] == 3:
            b2 = b[..., 2]
        if cp.ndim != 0 and cp.shape[-1] == 3:
            cp0 = cp[..., 0]
            cp1 = cp[..., 1]
            cp2 = cp[..., 2]

        if a.shape[-1] == 2:
            if b.shape[-1] == 2:
                # a0 * b1 - a1 * b0
                multiply(a0, b1, out=cp)
                cp -= a1 * b0
                return cp
            else:
                assert b.shape[-1] == 3
                # cp0 = a1 * b2 - 0  (a2 = 0)
                # cp1 = 0 - a0 * b2  (a2 = 0)
                # cp2 = a0 * b1 - a1 * b0
                multiply(a1, b2, out=cp0)
                multiply(a0, b2, out=cp1)
                np.negative(cp1, out=cp1)
                multiply(a0, b1, out=cp2)
                cp2 -= a1 * b0
        else:
            assert a.shape[-1] == 3
            if b.shape[-1] == 3:
                # cp0 = a1 * b2 - a2 * b1
                # cp1 = a2 * b0 - a0 * b2
                # cp2 = a0 * b1 - a1 * b0
                multiply(a1, b2, out=cp0)
                tmp = np.array(a2 * b1)
                cp0 -= tmp
                multiply(a2, b0, out=cp1)
                multiply(a0, b2, out=tmp)
                cp1 -= tmp
                multiply(a0, b1, out=cp2)
                multiply(a1, b0, out=tmp)
                cp2 -= tmp
            else:
                assert b.shape[-1] == 2
                # cp0 = 0 - a2 * b1  (b2 = 0)
                # cp1 = a2 * b0 - 0  (b2 = 0)
                # cp2 = a0 * b1 - a1 * b0
                multiply(a2, b1, out=cp0)
                negative(cp0, out=cp0)
                multiply(a2, b0, out=cp1)
                multiply(a0, b1, out=cp2)
                cp2 -= a1 * b0

        return moveaxis(cp, -1, axisc)

