import numpy as np
import cvxopt
from firesvm.utils import *
from firesvm.kernels import *


class SVM:
    def __init__(self, kernel=rbf, C=None, tol = 1e-5, max_iter = 100, verbose = False):
        self.kernel = kernel
        self.C = C
        self.tol = tol
        self.max_iter = max_iter
        self.verbose = verbose

        if self.verbose == False:
            cvxopt.solvers.options['show_progress'] = False

    def fit(self, X, y):
        self.y = y
        self.X = X
        m, n = X.shape

        self.K = np.zeros((m, m))
        for i in range(m):
            self.K[i, :] = self.kernel(X[i, np.newaxis], self.X)

        P = cvxopt.matrix(np.outer(y, y) * self.K)
        q = cvxopt.matrix(-np.ones((m, 1)))
        A = cvxopt.matrix(y, (1, m), "d")
        b = cvxopt.matrix(np.zeros(1))

        if self.C is None:
            G = cvxopt.matrix(np.diag(-np.ones(m)))
            h = cvxopt.matrix(np.zeros(m))
        else:
            G = cvxopt.matrix(np.vstack((np.eye(m) * -1, np.eye(m))))
            h = cvxopt.matrix(np.hstack((np.zeros(m), np.ones(m) * self.C)))

        cvxopt.solvers.options["max_iter"] = self.max_iter

        sol = cvxopt.solvers.qp(P, q, G, h, A, b)
        self.alphas = np.array(sol["x"])

    def predict(self, X):
        y_predict = np.zeros((X.shape[0]))
        sv = self.get_parameters(self.alphas)

        for i in range(X.shape[0]):
            y_predict[i] = np.sum(
                self.alphas[sv]
                * self.y[sv, np.newaxis]
                * self.kernel(X[i], self.X[sv])[:, np.newaxis]
            )

        return np.sign(y_predict + self.b)

    def get_parameters(self, alphas):
        if self.C is not None:
            sv = ((alphas > self.tol) * (alphas < self.C)).flatten()
        else:
            sv = (alphas > self.tol).flatten()
        self.w = np.dot(self.X[sv].T, alphas[sv] * self.y[sv, np.newaxis])
        self.b = np.mean(
            self.y[sv, np.newaxis]
            - self.alphas[sv] * self.y[sv, np.newaxis] * self.K[sv, sv][:, np.newaxis]
        )
        return sv

