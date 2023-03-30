import numpy as np
import warnings

warnings.filterwarnings("error")


class EasyMatrix:
    def __init__(self, array):
        for i in range(len(array)):
            if i > 0 and len(array[i]) != len(array[i - 1]):
                raise RuntimeError("not correct matrix size")
        self.h = len(array)
        self.w = len(array[0])
        self.mat = array

    def __add__(self, other):
        if self.w != other.w or self.h != other.h:
            raise RuntimeError("incorrect matrixes sizes")
        result_mat = [[self.mat[i][j] + other.mat[i][j]
                       for j in range(self.w)] for i in range(self.h)]
        return EasyMatrix(result_mat)

    def __mul__(self, other):
        if self.w != other.w or self.h != other.h:
            raise RuntimeError("incorrect matrixes sizes")
        result_mat = [[self.mat[i][j] * other.mat[i][j]
                       for j in range(self.w)] for i in range(self.h)]
        return EasyMatrix(result_mat)

    def __matmul__(self, other):
        if self.w != other.h:
            raise RuntimeError("incorrect matrixes sizes")
        result_mat = [[0 for j in range(other.w)] for i in range(self.h)]
        for i in range(self.h):
            for j in range(other.w):
                for k in range(self.w):
                    result_mat[i][j] += self.mat[i][k] * other.mat[k][j]
        return EasyMatrix(result_mat)

    def __str__(self):
        res = ""
        for i in range(self.h):
            res += str(self.mat[i])
            if i + 1 != self.h:
                res += "\n"
        return res


def eazy():
    mat_a = EasyMatrix(np.random.randint(0, 10, (10, 10)))
    mat_b = EasyMatrix(np.random.randint(0, 10, (10, 10)))
    with open("artifacts/easy/matrix+.txt", "w") as fout:
        print(mat_a + mat_b, file=fout)
    with open("artifacts/easy/matrix*.txt", "w") as fout:
        print(mat_a * mat_b, file=fout)
    with open("artifacts/easy/matrix@.txt", "w") as fout:
        print(mat_a @ mat_b, file=fout)


class MediumMatrix(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, value):
        self.value = np.asarray(value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray,)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MediumMatrix,)):
                return NotImplemented
        inputs = tuple(x.value if isinstance(x, MediumMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MediumMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __str__(self):
        res = ""
        space_count = 1
        for i in self.value:
            for j in i:
                space_count = max(space_count, len(str(j)) + 1)
        for i in self.value:
            line = ""
            for j in range(len(i)):
                line += str(i[j])
                line += " " * (space_count - len(str(i[j]))) + "|"
            res += line + "\n"
            res += "-" * len(line) + "\n"
        return res


def medium():
    mat_a = MediumMatrix(np.random.randint(0, 10, (10, 10)))
    mat_b = MediumMatrix(np.random.randint(0, 10, (10, 10)))
    with open("artifacts/medium/matrix+.txt", "w") as fout:
        print(mat_a + mat_b, file=fout)
    with open("artifacts/medium/matrix*.txt", "w") as fout:
        print(mat_a * mat_b, file=fout)
    with open("artifacts/medium/matrix@.txt", "w") as fout:
        print(mat_a @ mat_b, file=fout)


eazy()
medium()
