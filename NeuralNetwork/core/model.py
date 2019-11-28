import logging
import os
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from glob import glob
from functools import partial
from .utils import load_geometry, batch_gen


class TFModel():
    def __init__(self,
                 batch_size,
                 epochs,
                 learning_rate,
                 save_file,
                 fixed_x,
                 fixed_y,
                 **kwargs):
        self._logger = logging.getLogger(__name__)
        self._logger.info("initializing {}".format(__name__))
        # config
        self._batch_size = batch_size
        self._epochs = epochs
        self._learning_rate = learning_rate
        self._fixed_x = fixed_x
        self._fixed_y = fixed_y
        self._save_file = save_file
        # session
        self._sess = tf.Session()
        self._global_step = tf.Variable(0, name='global_step', trainable=False)
        # tensors
        self._input_ph = tf.placeholder(dtype=tf.float32, shape=[None, fixed_x, fixed_y])
        self._target_ph = tf.placeholder(dtype=tf.float32, shape=[None, ])
        self._build_model(**kwargs)
        self._init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self._sess.run(self._init)

    def _build_model(self, l1_filters, l1_kernel, l1_dropout, l2_filters, l2_kernel, l2_dropout, l3_filters, l3_kernel,
                     l3_dropout, l4_units, l4_dropout, l5_units, n_hidden_1, n_hidden_2, **kwargs):
        """
        with tf.variable_scope("model", reuse=tf.AUTO_REUSE):
            with tf.variable_scope("vars", reuse=tf.AUTO_REUSE):
                weight = tf.Variable(tf.random_normal([n_hidden_2, 1]), name='weight')
                bias = tf.Variable(tf.random_normal([1]), name='bias')
            with tf.variable_scope("L0", reuse=tf.AUTO_REUSE):
                _batch_size = tf.shape(self._input_ph)[0]
                L0 = tf.reshape(tensor=self._input_ph, shape=[_batch_size, -1])
                L0.set_shape([None, self._fixed_x * self._fixed_y])
            with tf.variable_scope("L1", reuse=tf.AUTO_REUSE):
                L1 = tf.layers.dense(
                    inputs=L0,
                    units=n_hidden_1,
                    activation=tf.nn.leaky_relu,
                    kernel_initializer=tf.random_normal_initializer(0., 0.3),
                    bias_initializer=tf.constant_initializer(0.1)
                )
            with tf.variable_scope("L2", reuse=tf.AUTO_REUSE):
                L2 = tf.layers.dense(
                    inputs=L1,
                    units=n_hidden_2,
                    activation=tf.nn.leaky_relu,
                    kernel_initializer=tf.random_normal_initializer(0., 0.3),
                    bias_initializer=tf.constant_initializer(0.1)
                )
            self._out = tf.einsum('bi,ij->bj', L2, weight) + bias
            with tf.variable_scope("loss", reuse=tf.AUTO_REUSE):
                self._loss = tf.reduce_mean(tf.squared_difference(self._target_ph, self._out))
            with tf.variable_scope("opt", reuse=tf.AUTO_REUSE):
                optim = tf.train.AdamOptimizer(learning_rate=self._learning_rate)
                self._train_op = optim.minimize(self._loss, global_step=self._global_step)
        self._logger.info("successfully build tensorflow graph")
        """
        with tf.variable_scope('transform', reuse=tf.AUTO_REUSE):
            L0 = tf.reshape(self._input_ph, (-1, self._fixed_x, self._fixed_x, 1))
        with tf.variable_scope("model", reuse=tf.AUTO_REUSE):
            with tf.variable_scope('L0', reuse=tf.AUTO_REUSE):
                L0 = tf.layers.dense(
                    inputs=L0,
                    units=n_hidden_1,
                    activation=tf.nn.leaky_relu,
                    kernel_initializer=tf.random_normal_initializer(0., 0.3),
                    bias_initializer=tf.constant_initializer(0.1)
                )

            with tf.variable_scope('L1', reuse=tf.AUTO_REUSE):
                L1 = tf.layers.conv2d(L0, l1_filters, l1_kernel, reuse=tf.AUTO_REUSE)
                L1 = tf.layers.max_pooling2d(L1, [2, 2], [2, 2])
                L1 = tf.layers.dropout(L1, l1_dropout, True)
            with tf.variable_scope('L2', reuse=tf.AUTO_REUSE):
                L2 = tf.layers.conv2d(L1, l2_filters, l2_kernel, reuse=tf.AUTO_REUSE)
                L2 = tf.layers.max_pooling2d(L2, [2, 2], [2, 2])
                L2 = tf.layers.dropout(L2, l2_dropout, True)
            with tf.variable_scope('L3', reuse=tf.AUTO_REUSE):
                L3 = tf.layers.conv2d(L2, l3_filters, l3_kernel, reuse=tf.AUTO_REUSE)
                L3 = tf.layers.max_pooling2d(L3, [2, 2], [2, 2])
                L3 = tf.layers.dropout(L3, l3_dropout, True)
            with tf.variable_scope('L4', reuse=tf.AUTO_REUSE):
                L4 = tf.contrib.layers.flatten(L3)
                L4 = tf.layers.dense(L4, l4_units, activation=tf.nn.leaky_relu)
                L4 = tf.layers.dropout(L4, l4_dropout, True)
            with tf.variable_scope('L5', reuse=tf.AUTO_REUSE):
                L5 = tf.layers.dense(L4, l5_units, activation=tf.nn.leaky_relu)
            with tf.variable_scope('LF', reuse=tf.AUTO_REUSE):
                LF = tf.layers.dense(L5, 1, activation=None)
                self._out = LF
            with tf.variable_scope("loss", reuse=tf.AUTO_REUSE):
                self._loss = tf.reduce_mean(tf.squared_difference(self._target_ph, self._out))
            with tf.variable_scope("opt", reuse=tf.AUTO_REUSE):
                optim = tf.train.AdamOptimizer(learning_rate=self._learning_rate)
                self._train_op = optim.minimize(self._loss, global_step=self._global_step)
        self._logger.info("successfully build tensorflow graph")

    def load(self, filepath=None):
        filepath = filepath if filepath is not None else self._save_file
        cpfile = tf.train.latest_checkpoint(os.path.dirname(filepath))
        saver = tf.train.Saver()
        try:
            saver.restore(self._sess, cpfile)
            self._logger.info("Loaded model {} from {}".format(self.__class__.__name__, cpfile))
        except ValueError:
            self._logger.error("Couldn't load model {} from file='{}'".format(self.__class__.__name__, self._save_file))

    def save(self, filepath=None):
        filepath = filepath if filepath is not None else self._save_file
        saver = tf.train.Saver()
        path = saver.save(self._sess, filepath, global_step=self._global_step)
        self._logger.info("Saved model {} in {}".format(self.__class__.__name__, path))

    def train(self, geometry_dir, scores, input_regexp='*.pickle'):
        assert os.path.exists(geometry_dir), "geometry_dir='{}' must exist"
        input_file_paths = glob(os.path.join(geometry_dir, input_regexp))
        self._logger.info("starting to train for {} epochs over {} geometries".format(self._epochs, len(scores)))
        self._logger.debug("input_file_paths: {}".format(input_file_paths))
        self._logger.debug("target_scores: {}".format(scores))
        for input_file_path in input_file_paths:
            _file_name = os.path.split(input_file_path)[-1].rsplit('.', 1)[0]
            assert _file_name in scores, "pre-calculated score for geometry_file='{}' not found"\
                .format(input_file_path)

        # iter and vars
        t = tqdm(range(1, self._epochs + 1), desc="{}".format(self.__class__.__name__), unit="epoch")
        losses = []
        _load = partial(load_geometry, fixed_x=self._fixed_x, fixed_y=self._fixed_y)

        # for each epoch
        for epoch in t:
            batches = batch_gen(iterable=input_file_paths, batch_size=self._batch_size)
            for batch_num, batch in enumerate(batches):
                batch_input_paths = batch
                batch_input_names = [os.path.split(f)[-1].rsplit('.', 1)[0] for f in batch_input_paths]
                batch_target = list(map(scores.__getitem__, batch_input_names))
                batch_input_values = list(map(_load, batch_input_paths))
                _, loss = self._sess.run([self._train_op, self._loss], feed_dict={
                    self._input_ph: batch_input_values,
                    self._target_ph: batch_target,
                })
                msg = "batch-{}-loss={:.3E}, epoch-{}-loss={:.3E}".format(batch_num, loss, epoch, np.mean(losses))
                t.set_postfix_str(msg)
                self._logger.debug(msg)
                losses.append(loss)
            self._logger.info("finished epoch-{} with loss={:.3E}".format(epoch, np.mean(losses)))
            losses.clear()
        self._logger.info("finished training")

    def inference(self, geometry):
        return self._sess.run(self._out, feed_dict={
            self._input_ph: [geometry]
        })[0]
