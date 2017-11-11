import tensorflow as tf 

x = tf.constant(32, dtype=tf.float32)

y = tf.placeholder(tf.float32)

z = x*y

session = tf.Session()

print(session.run(z, {y:[1,2,3]}))