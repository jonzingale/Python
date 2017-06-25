# TensorFlow experiments
import tensorflow as tf
from pprint import pprint as pp
from pdb import set_trace as st
import os

from tensorflow.examples.tutorials.mnist import input_data

def helloworld():
  hello = tf.constant('Hello, TensorFlow!')
  sess = tf.Session()
  print(sess.run(hello))


def mnist():
  # SETUP
  mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

  x = tf.placeholder(tf.float32, [None, 784]) # placeholder input
  W = tf.Variable(tf.zeros([784, 10])) # weight, tensor full of zeros
  bb = tf.Variable(tf.zeros([10])) # contant, tensor full of zeros

  # implementation of model.
  y = tf.nn.softmax(tf.matmul(x, W) + bb)

  # implement cross-entropy for training
  y_ = tf.placeholder(tf.float32, [None, 10]) # placeholder
  cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
  
  # optimize against the cross-entropy via GradientDescent
  train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)

  # SESSION
  # launch session
  sess = tf.InteractiveSession()

  # initialize variables
  tf.global_variables_initializer().run()

  # train for 1000 steps
  for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  # TEST
  os.system('clear')
  correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

mnist()