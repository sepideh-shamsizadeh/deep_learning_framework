import numpy as np


def sigmoid(z):
    return 1 / (1 + (np.exp(-z)))


def derivation_of_sigmoid(z):
    return sigmoid(z) * sigmoid(1 - z)


def tanh(z):
    return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))


def derivation_of_tanh(z):
    return 1 - tanh(z) ** 2


def ReLU(z):
    return np.max(0, z)


def derivation_of_ReLU(z):
    return 0 if z < 0 else 1


def leaky_ReLU(z):
    return np.max(0.01 * z, z)


def derivation_of_leaky_ReLU(z):
    return 0.01 if z < 0 else 1


def softmax(z):
    t = np.exp(z)
    return t / np.sum(t)


def forward(parameters, activation_function, last_layer_activation):
    cache = {}
    L = parameters['layer_numbers']
    for l in range(L - 1):
        cache['Z' + str(l + 1)] = parameters['W' + str(l + 1)] * cache["A" + str(l)] + parameters['b' + str(l + 1)]
        if activation_function == 'sigmoid':
            cache["A" + str(l + 1)] = sigmoid(cache['Z' + str(l + 1)])
        elif activation_function == 'tanh':
            cache["A" + str(l + 1)] = tanh(cache['Z' + str(l + 1)])
        elif activation_function == 'ReLU':
            cache["A" + str(l + 1)] = ReLU(cache['Z' + str(l + 1)])
        elif activation_function == 'leaky_ReLU':
            cache["A" + str(l + 1)] = leaky_ReLU(cache['Z' + str(l + 1)])
    cache['Z' + str(L)] = parameters['W' + str(L)] * cache["A" + str(L - 1)] + parameters['b' + str(L)]
    if last_layer_activation == 'sigmoid':
        cache['AL'] = sigmoid(cache['Z' + str(L)])
    elif last_layer_activation == 'softmax':
        cache['AL'] = softmax(cache['Z' + str(L)])
    return cache


def backward(cache, activation_function, parameters, optimization):
    m = parameters['m']
    L = parameters['layer_numbers']
    cache['dZL'] = cache['AL'] - parameters['Y']
    cache['dWL'] = (1 / m) * cache['dZL'] * cache['A' + str(L - 1)].T
    cache['dbL'] = (1 / m) * np.sum(cache['dZL'], axis=1, keepdims=True)
    for l in reversed(range(1, L)):
        if activation_function == 'sigmoid':
            cache['dZ' + str(l)] = cache['dW' + str(l + 1)].T * cache['dZ' + str(l + 1)] * derivation_of_sigmoid(
                cache['Z' + str(l)])
        elif activation_function == 'tanh':
            cache['dZ' + str(l)] = cache['dW' + str(l + 1)].T * cache['dZ' + str(l + 1)] * derivation_of_tanh(
                cache['Z' + str(l)])
        elif activation_function == 'ReLU':
            cache['dZ' + str(l)] = cache['dW' + str(l + 1)].T * cache['dZ' + str(l + 1)] * derivation_of_ReLU(
                cache['Z' + str(l)])
        elif activation_function == 'leaky_ReLU':
            cache['dZ' + str(l)] = cache['dW' + str(l + 1)].T * cache['dZ' + str(l + 1)] * derivation_of_leaky_ReLU(
                cache['Z' + str(l)])
        if optimization == 'gradient_descent':
            cache['dW' + str(l)], cache['db' + str(l)] = gradient_descent(
                l, m, cache['dZ' + str(l)], cache['A' + str(l - 1)]
            )
            # elif optimization == 'gradient_descent_momentum':
            # cache['dW' + str(l)], cache['db' + str(l)]  = gradient_descent_momentum(
            #   l, m, cache['dZ' + str(l)], cache['A' + str(l-1)]
            # )

    return cache


def cost(A, Y):
    return (-1 / len(Y)) * np.sum(np.multiply(np.log(A), Y) + np.multiply(np.log(1 - A), (1 - Y)))


def normalizing(X):
    mua = (1 / X.shape[1]) * np.sum(X)
    X = X - mua
    sigma = (1 / X.shape[1]) * np.sum(X ** 2)
    X /= sigma
    return X, mua, sigma


def initialization(parameters, activation_function):
    L = parameters['layer_numbers']
    for l in range(L):
        if activation_function == 'ReLU':
            parameters['W' + str(l + 1)] = np.random.randn() * np.squrt(2 / (parameters['n' + str(l)]))
        else:
            parameters['W' + str(l + 1)] = np.random.randn() * np.squrt(1 / (parameters['n' + str(l)]))
    return parameters


def gradient_descent(l, m, dZ, A):
    dw = (1 / m) * dZ * A.T
    db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
    return dw, db


def gradient_descent_momentum(vdw, vdb, beta, dw, db):
    vdw = beta * vdw + dw
    vdb = beta * vdb + db
    return vdw, vdb
