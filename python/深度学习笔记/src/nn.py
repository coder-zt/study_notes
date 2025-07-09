# from xml.etree.ElementPath import ops
import math
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops
# import tensorflow.compat.v1 as tf

tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

def create_placeholders(n_x, n_y):
    X = tf.compat.v1.placeholder(tf.float32, shape=(n_x, None), name='X')
    Y = tf.compat.v1.placeholder(tf.float32, shape=(n_y, None), name='Y')    
    return X, Y

def initialize_parameters(): 
    tf.compat.v1.set_random_seed(1)         #tensorflow.contrib          
    W1 = tf.compat.v1.get_variable("W1", [25, 12288], initializer = tf.keras.initializers.GlorotUniform(seed=1))
    b1 = tf.compat.v1.get_variable("b1", [25, 1], initializer = tf.zeros_initializer())
    W2 = tf.compat.v1.get_variable("W2", [12, 25], initializer = tf.keras.initializers.GlorotUniform(seed=1))
    b2 = tf.compat.v1.get_variable("b2", [12, 1], initializer = tf.zeros_initializer())
    W3 = tf.compat.v1.get_variable("W3", [6, 12], initializer = tf.keras.initializers.GlorotUniform(seed=1))
    b3 = tf.compat.v1.get_variable("b3", [6,1], initializer = tf.zeros_initializer())

    parameters = {"W1": W1,                 
                  "b1": b1,   
                  "W2": W2, 
                  "b2": b2, 
                  "W3": W3,  
                  "b3": b3}   
    return parameters

def forward_propagation(X, parameters):    
    """
    Implements the forward propagation for the model: LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SOFTMAX
    """
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']

    Z1 = tf.add(tf.matmul(W1, X), b1)                    
    A1 = tf.nn.relu(Z1)                               
    Z2 = tf.add(tf.matmul(W2, A1), b2)                
    A2 = tf.nn.relu(Z2)                                  
    Z3 = tf.add(tf.matmul(W3, A2), b3)                  
    return Z3


def compute_cost(Z3, Y):
    logits = tf.transpose(Z3)
    labels = tf.transpose(Y)

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels = labels))    
    return cost

def random_mini_batches(X, Y, mini_batch_size=64, seed=None):
    """
    从数据集中创建随机小批量
    
    参数：
    X -- 输入数据，维度为 (n_x, m)
    Y -- 真实标签，维度为 (n_y, m)
    mini_batch_size -- 小批量的大小
    seed -- 随机种子（可选）
    
    返回：
    mini_batches -- 包含 (mini_batch_X, mini_batch_Y) 元组的列表
    """
    
    if seed is not None:
        np.random.seed(seed)
    
    m = X.shape[1]  # 训练样本数量
    mini_batches = []
    
    # 第一步：打乱数据顺序
    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation]
    
    # 第二步：将数据分割为完整的小批量
    num_complete_minibatches = m // mini_batch_size
    
    for k in range(0, num_complete_minibatches):
        # 获取第k个小批量
        start_idx = k * mini_batch_size
        end_idx = (k + 1) * mini_batch_size
        
        mini_batch_X = shuffled_X[:, start_idx:end_idx]
        mini_batch_Y = shuffled_Y[:, start_idx:end_idx]
        
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # 第三步：处理最后一个小批量（如果样本数不是批量大小的整数倍）
    if m % mini_batch_size != 0:
        start_idx = num_complete_minibatches * mini_batch_size
        mini_batch_X = shuffled_X[:, start_idx:]
        mini_batch_Y = shuffled_Y[:, start_idx:]
        
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches

def model(X_train, Y_train, X_test, Y_test, learning_rate = 0.0001,
          num_epochs = 1500, minibatch_size = 32, print_cost = True):
    ops.reset_default_graph()                    
    tf.random.set_seed(1)                          
    seed = 3                                         
    (n_x, m) = X_train.shape                       
    n_y = Y_train.shape[0]                          
    costs = []                                   

    # Create Placeholders of shape (n_x, n_y)
    X, Y = create_placeholders(n_x, n_y)    # Initialize parameters
    parameters = initialize_parameters()    # Forward propagation: Build the forward propagation in the tensorflow graph

    Z3 = forward_propagation(X, parameters)    # Cost function: Add cost function to tensorflow graph
    cost = compute_cost(Z3, Y)    # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.
    optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

    init = tf.compat.v1.global_variables_initializer() 
    
    with tf.compat.v1.Session() as sess:        # Run the initialization
        sess.run(init)        # Do the training loop
        for epoch in range(num_epochs):
            print(f"=====> epoch:{epoch}")
            epoch_cost = 0.                    
            num_minibatches = int(m / minibatch_size) 
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)            
            for minibatch in minibatches:                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch
                _ , minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                epoch_cost += minibatch_cost / num_minibatches            # Print the cost every epoch
            if print_cost == True and epoch % 100 == 0:                
                print ("Cost after epoch %i: %f" % (epoch, epoch_cost))           
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()        # lets save the parameters in a variable
        parameters = sess.run(parameters)        
        print ("Parameters have been trained!")        # Calculate the correct predictions
        correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))       
        print ("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))        
        print ("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))        
        return parameters
