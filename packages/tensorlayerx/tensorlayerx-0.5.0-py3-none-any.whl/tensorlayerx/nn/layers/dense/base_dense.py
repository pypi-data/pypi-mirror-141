#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorlayerx as tlx
from tensorlayerx import logging
from tensorlayerx.nn.core import Module

__all__ = [
    'Dense',
]


class Dense(Module):
    """The :class:`Dense` class is a fully connected layer.

    Parameters
    ----------
    n_units : int
        The number of units of this layer.
    act : activation function
        The activation function of this layer.
    W_init : initializer or str
        The initializer for the weight matrix.
    b_init : initializer or None or str
        The initializer for the bias vector. If None, skip biases.
    in_channels: int
        The number of channels of the previous layer.
        If None, it will be automatically detected when the layer is forwarded for the first time.
    name : None or str
        A unique layer name. If None, a unique name will be automatically generated.

    Examples
    --------
    With TensorLayer

    >>> net = tlx.nn.Input([100, 50], name='input')
    >>> dense = tlx.nn.Dense(n_units=800, act=tlx.ReLU, in_channels=50, name='dense_1')
    >>> print(dense)
    Dense(n_units=800, relu, in_channels='50', name='dense_1')
    >>> tensor = tlx.nn.Dense(n_units=800, act=tlx.ReLU, name='dense_2')(net)
    >>> print(tensor)
    tf.Tensor([...], shape=(100, 800), dtype=float32)

    Notes
    -----
    If the layer input has more than two axes, it needs to be flatten by using :class:`Flatten`.

    """

    def __init__(
        self,
        n_units,
        act=None,
        W_init='truncated_normal',
        b_init='constant',
        in_channels=None,
        name=None,  # 'dense',
    ):

        super(Dense, self).__init__(name, act=act)

        self.n_units = n_units
        self.W_init = self.str_to_init(W_init)
        self.b_init = self.str_to_init(b_init)
        self.in_channels = in_channels

        if self.in_channels is not None:
            self.build(self.in_channels)
            self._built = True

        logging.info(
            "Dense  %s: %d %s" %
            (self.name, self.n_units, self.act.__class__.__name__ if self.act is not None else 'No Activation')
        )

    def __repr__(self):
        actstr = self.act.__class__.__name__ if self.act is not None else 'No Activation'
        s = ('{classname}(n_units={n_units}, ' + actstr)
        if self.in_channels is not None:
            s += ', in_channels=\'{in_channels}\''
        if self.name is not None:
            s += ', name=\'{name}\''
        s += ')'
        return s.format(classname=self.__class__.__name__, **self.__dict__)

    def build(self, inputs_shape):
        if self.in_channels is None and len(inputs_shape) < 2:
            raise AssertionError("The dimension of input should not be less than 2")
        if self.in_channels:
            shape = [self.in_channels, self.n_units]
        else:
            self.in_channels = inputs_shape[-1]
            shape = [self.in_channels, self.n_units]

        self.W = self._get_weights("weights", shape=tuple(shape), init=self.W_init)

        self.b_init_flag = False
        if self.b_init:
            self.b = self._get_weights("biases", shape=(self.n_units, ), init=self.b_init)
            self.b_init_flag = True
            self.bias_add = tlx.ops.BiasAdd(data_format='NHWC')

        self.act_init_flag = False
        if self.act:
            self.act_init_flag = True

        self.matmul = tlx.ops.MatMul()

    def forward(self, inputs):
        if self._forward_state == False:
            if self._built == False:
                self.build(tlx.get_tensor_shape(inputs))
                self._built = True
            self._forward_state = True

        z = self.matmul(inputs, self.W)
        if self.b_init_flag:
            z = self.bias_add(z, self.b)
        if self.act_init_flag:
            z = self.act(z)
        return z
