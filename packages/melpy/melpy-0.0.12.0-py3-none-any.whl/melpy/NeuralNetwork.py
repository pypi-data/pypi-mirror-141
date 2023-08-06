import numpy as np

class Layer:
    def __init__(self):
        self.inputs = None
        self.targets = None
        self.outputs = None
        self.dX = None
        self.dY = None
        self.dW = None
        self.dB = None

    def derivative(self):
        pass
    def forward(self):
        pass
    def backward(self):
        pass

class Loss:
    def loss(self):
        pass
    def derivative(self):
        pass
    
#%%Cost Functions
class Binary_CrossEntropy(Loss):   
    def __init__(self):
        super().__init__()
        
    def loss(self, targets, outputs):
        e = 1e-10
        return -(np.sum(targets * np.log(outputs + e) + (1-targets) * np.log(1-outputs + e))) / len(targets)
    
    def derivative(self, targets, outputs):
        e = 1e-10
        return -(targets / outputs - (1 - targets + e) / (1 - outputs + e)) / len(outputs) 
    
class Categorical_CrossEntropy(Loss):
    def __init__(self):
        super().__init__()
        
    def loss(self, targets, outputs):
        targets_clipped = np.clip(outputs, 1e-7, 1 - 1e-7)
        if len(targets.shape) == 1:
            correct_confidences = targets_clipped[
            range(len(outputs)),
            targets
            ]
        elif len(targets.shape) == 2:
            correct_confidences = np.sum(
            targets_clipped*targets,
            axis=1
            )
        negative_log_likelihoods = -np.log(correct_confidences)
        return np.mean(negative_log_likelihoods)
    
    def derivative(self, targets, outputs):
        if len(targets.shape) == 1:
            targets = np.eye(len(outputs[0]))[targets]
        return ((-targets + 1e-5) / (outputs + 1e-5)) / len(outputs) 

#%%Activation Functions
class Dense(Layer):
    def __init__(self, n_in, n_out):
        super().__init__()
        self.weights = np.random.rand(n_in, n_out)
        self.biases = np.random.rand(1,n_out)
        self.w_momentum = np.zeros_like(self.weights)
        self.b_momentum = np.zeros_like(self.biases)
        
    def forward(self):
        self.outputs = np.dot(self.inputs, self.weights) + self.biases
        return np.dot(self.inputs, self.weights) + self.biases
    
    def backward(self, dX, lr, momentum):
        self.dY = dX
        self.dW = np.dot(self.inputs.T, self.dY)
        self.dB = np.sum(self.dY, axis=0, keepdims=True)
        self.dX = np.dot(self.dY, self.weights.T)
        
        if momentum is not None:
            weights = momentum * self.w_momentum - self.dW * lr
            biases = momentum * self.b_momentum - self.dB * lr
            
            self.w_momentum = weights
            self.b_momentum = biases
            self.weights += weights
            self.biases += biases
            
        elif momentum is None:
            self.weights -= self.dW * lr
            self.biases -= self.dB * lr
        
        self.dW *= np.zeros(self.dW.shape, dtype = np.float64)
        self.dB *= np.zeros(self.dB.shape, dtype = np.float64)
        
        return self.dX
    
class ReLU(Layer):
    def __init__(self):
        super().__init__()
        
    def derivative(self):
        self.inputs[self.inputs<=0] = 0
        self.inputs[self.inputs>0] = 1
        return self.inputs
        
    def forward(self):
        self.outputs = np.maximum(0,self.inputs)
        return np.maximum(0,self.inputs)
    
    def backward(self, dX, lr, momentum):
        self.dY = dX
        self.dX = self.dY * self.derivative()
        return self.dX

class Leaky_ReLU(Layer):
    def __init__(self):
        super().__init__()
    
    def derivative(self):
        dA = np.ones_like(self.inputs)
        dA[self.inputs < 0] = 0.01
        return dA
    
    def forward(self):
        self.outputs = np.where(self.inputs > 0, self.inputs, self.inputs * 0.01)
        return np.where(self.inputs > 0, self.inputs, self.inputs * 0.01)
    
    def backward(self, dX, lr, momentum):
        self.dY = dX
        self.dX = self.dY * self.derivative()
        return self.dX
    
class Sigmoid(Layer):
    def __init__(self):
        super().__init__()
    
    def derivative(self):
        return self.outputs * (1-self.outputs)
    
    def forward(self):
        self.outputs = 1 / (1+np.exp(-self.inputs))
        return 1 / (1+np.exp(-self.inputs))
    
    def backward(self, dX, lr, momentum):
        self.dY = dX
        self.dX = self.dY * self.derivative()
        return self.dX

class Softmax(Layer):
    def __init__(self):
        super().__init__()
        self.dK = None
        
    def forward(self):
        exp_values = np.exp(self.inputs - np.max(self.inputs, axis=1,keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1,keepdims=True)
        self.outputs = probabilities
        return self.outputs
    
    def backward(self, dX, lr, momentum):
        dA = np.empty_like(dX)
        for index, (single_output, single_dvalues) in enumerate(zip(self.outputs, dX)):
            single_output = single_output.reshape(-1, 1)
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
            dA[index] = np.dot(jacobian_matrix,
            single_dvalues)
        return dA

#%%LiveStats
class LiveStats():
    def __init__(self, type=-1, f1=0, f2=1, row_select="limited"):
        super().__init__()
        self.type = type
        self.f1 = f1
        self.f2 = f2
        self.row_select = row_select
    
    def run(self, model, figure):
        import matplotlib.pyplot as plt
        if self.type == 1:
            figure.clear()
            
            plt.subplot(1,2,1)
            plt.title("Loss Evolution")
            plt.xlabel("Epoch")
            plt.ylabel("Loss")
            plt.plot(model.train_loss_records, color="#1f77b4", label=f"training dataset: {round(float(model.train_loss_records[-1]), 3)}")
            if model.val_inputs is not None and model.val_targets is not None:
                plt.plot(model.val_loss_records, color="orange", label=f"validation dataset: {round(float(model.val_loss_records[-1]), 3)}")
            plt.legend()
            
            plt.subplot(1,2,2)
            plt.title("Accuracy Evolution")
            plt.xlabel("Epoch")
            plt.ylabel("Accuracy")
            plt.plot(model.train_accuracy_records, color="#1f77b4", label=f"training dataset: {round(float(model.train_accuracy_records[-1]), 3)}")
            if model.val_inputs is not None and model.val_targets is not None:
                plt.plot(model.val_accuracy_records, color="orange", label=f"validation dataset: {round(float(model.val_accuracy_records[-1]), 3)}")
            plt.legend()
            
            figure.canvas.draw()
            figure.canvas.flush_events()
            
        elif self.type == 2:
            figure.clear()
            
            plt.subplot(1,1,1)
            if len(model.train_inputs[0,:]) <= 2 and len(model.train_targets[0,:]) == 1:
                if len(model.train_inputs[:,0]) > 1000 and self.row_select=="limited":
                    X_set, y_set = model.train_inputs[:1000,:], model.train_targets[:1000,:]
                elif len(model.train_inputs[:,0]) > 1000 and self.row_select=="full":
                    X_set, y_set = model.train_inputs, model.train_targets
                elif (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="full") or (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="limited"):
                    X_set, y_set = model.train_inputs, model.train_targets
                else:
                    raise ValueError("invalid value for 'row_select'")
                    
                X1, X2 = np.meshgrid(np.arange(start = X_set[:, self.f1].min() - 1, stop = X_set[:, self.f1].max() + 1, step = 0.01),
                                     np.arange(start = X_set[:, self.f2].min() - 1, stop = X_set[:, self.f2].max() + 1, step = 0.01))
                plt.contourf(X1, X2, model.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                             alpha = 0.3, cmap = "coolwarm")
            
            if len(model.train_inputs[:,0]) > 1000 and self.row_select=="limited":
                plt.scatter(model.train_inputs[:1000,self.f1], model.train_inputs[:1000,self.f2], c=model.train_outputs[:1000,:], cmap="coolwarm", alpha=1)
            elif len(model.train_inputs[:,0]) > 1000 and self.row_select=="full":
                plt.scatter(model.train_inputs[:,self.f1], model.train_inputs[:,self.f2], c=model.train_outputs[:,:], cmap="coolwarm", alpha=1)
            elif (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="full") or (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="limited"):
                plt.scatter(model.train_inputs[:,self.f1], model.train_inputs[:,self.f2], c=model.train_outputs[:,:], cmap="coolwarm", alpha=1)
            else:
                raise ValueError("invalid value for 'row_select'")
                
            figure.canvas.draw()
            figure.canvas.flush_events()
            
        elif self.type == -1:
            figure.clear()
            
            plt.subplot(1, 2, 2)
            if len(model.train_inputs[0,:]) <= 2 and len(model.train_targets[0,:]) == 1:
                if len(model.train_inputs[:,0]) > 1000 and self.row_select=="limited":
                    X_set, y_set = model.train_inputs[:1000,:], model.train_targets[:1000,:]
                elif len(model.train_inputs[:,0]) > 1000 and self.row_select=="full":
                    X_set, y_set = model.train_inputs, model.train_targets
                elif (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="full") or (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="limited"):
                    X_set, y_set = model.train_inputs, model.train_targets
                else:
                    raise ValueError("invalid value for 'row_select'")
                X1, X2 = np.meshgrid(np.arange(start = X_set[:, self.f1].min() - 1, stop = X_set[:, self.f1].max() + 1, step = 0.01),
                                     np.arange(start = X_set[:, self.f2].min() - 1, stop = X_set[:, self.f2].max() + 1, step = 0.01))
                plt.contourf(X1, X2, model.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                             alpha = 0.3, cmap = "coolwarm")
                
            if len(model.train_inputs[:,0]) > 1000 and self.row_select=="limited":
                plt.scatter(model.train_inputs[:1000,self.f1], model.train_inputs[:1000,self.f2], c=model.train_outputs[:1000,:], cmap="coolwarm", alpha=1)
            elif len(model.train_inputs[:,0]) > 1000 and self.row_select=="full":
                plt.scatter(model.train_inputs[:,self.f1], model.train_inputs[:,self.f2], c=model.train_outputs[:,:], cmap="coolwarm", alpha=1)
            elif (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="full") or (len(model.train_inputs[:,0]) <= 1000 and self.row_select=="limited"):
                plt.scatter(model.train_inputs[:,self.f1], model.train_inputs[:,self.f2], c=model.train_outputs[:,:], cmap="coolwarm", alpha=1)
            else:
                raise ValueError("invalid value for 'row_select'")
            
            plt.subplot(2,2,1)
            plt.title("Loss Evolution")
            plt.ylabel("Loss")
            plt.plot(model.train_loss_records, color="#1f77b4", label=f"training dataset: {round(float(model.train_loss_records[-1]), 3)}")
            if model.val_inputs is not None and model.val_targets is not None:
                plt.plot(model.val_loss_records, color="orange", label=f"validation dataset: {round(float(model.val_loss_records[-1]), 3)}")
            plt.legend()
            
            plt.subplot(2,2,3)
            plt.title("Accuracy Evolution")
            plt.xlabel("Epoch")
            plt.ylabel("Accuracy")
            plt.plot(model.train_accuracy_records, color="#1f77b4", label=f"training dataset: {round(float(model.train_accuracy_records[-1]), 3)}")
            if model.val_inputs is not None and model.val_targets is not None:
                plt.plot(model.val_accuracy_records, color="orange", label=f"validation dataset: {round(float(model.val_accuracy_records[-1]), 3)}")
            plt.legend()
            
            figure.canvas.draw()
            figure.canvas.flush_events()
            
#%%Sequential 
class Sequential():
    def __init__(self, train_inputs, train_targets, val_inputs = None, val_targets = None):
        self.train_inputs = train_inputs
        self.train_targets = train_targets
        self.train_outputs = None
        self.val_inputs = val_inputs
        self.val_targets = val_targets
        self.val_outputs = None
        self.prediction = None
        self.train_layers = []
        self.val_layers = []
        self.train_loss = None
        self.val_loss = None
        self.train_loss_records = []
        self.val_loss_records = []
        self.train_accuracy_records = []
        self.val_accuracy_records =  []
        self.train_cost_fn = None
        self.val_cost_fn = None
        self.__activation_functions__ = {"ReLU": ReLU(),
                                         "Leaky_ReLU": Leaky_ReLU(),
                                         "Sigmoid": Sigmoid(),
                                         "Softmax": Softmax()}
        
        self.__cost_functions__ = {"binary_crossentropy": Binary_CrossEntropy(),
                                   "categorical_crossentropy": Categorical_CrossEntropy()}
        self.__is_trained__ = False
        self.runtime = 0.0
    
    def add(self, ac_fn, n_in, n_out):
        import copy
        train_activation_functions = copy.deepcopy(self.__activation_functions__)
        for name,function in train_activation_functions.items():
            if ac_fn == name:
                self.train_layers.append(Dense(n_in, n_out))
                self.train_layers.append(function)
                break
        if self.val_inputs is not None and self.val_targets is not None:
            val_activation_functions =  copy.deepcopy(self.__activation_functions__)
            for name,function in val_activation_functions.items():
                if ac_fn == name:
                    self.val_layers.append(Dense(n_in, n_out))
                    self.val_layers.append(function)
                    break
            
    def forward(self):
        self.train_layers[0].inputs = self.train_inputs
        for i in range(len(self.train_layers)):
            if i+1 == len(self.train_layers):
                self.train_outputs = self.train_layers[i].forward()
            else:
                self.train_layers[i+1].inputs = self.train_layers[i].forward()
        if self.val_inputs is not None and self.val_targets is not None:
            self.val_layers[0].inputs = self.val_inputs
            for i in range(len(self.val_layers)):
                if i+1 == len(self.val_layers):
                    self.val_outputs = self.val_layers[i].forward()
                else:
                    self.val_layers[i+1].inputs = self.val_layers[i].forward()
                
    def predict(self,X):
            self.train_layers[0].inputs = X
            for i in range(len(self.train_layers)):
                if i+1 == len(self.train_layers):
                    self.prediction = np.around(self.train_layers[i].forward())
                    return self.train_layers[i].forward()
                else:
                    self.train_layers[i+1].inputs = self.train_layers[i].forward()
            
    def backward(self, lr, momentum):
        self.dX = self.train_cost_fn.derivative(self.train_targets, self.train_outputs)
        for layer in reversed(self.train_layers):
                self.dX = layer.backward(self.dX, lr, momentum)
        if self.val_inputs is not None and self.val_targets is not None:
            for i in range(len(self.val_layers)):
                if isinstance(self.val_layers[i], Dense):
                    self.val_layers[i].weights = self.train_layers[i].weights
                    self.val_layers[i].biases = self.train_layers[i].biases
            
    def accuracy(self, targets, outputs):
        accuracy = 1e-10
        outputs = np.array(outputs)
        if outputs.shape[1] > 1:
            for i in range(outputs.shape[0]):
                outputs[i][np.argmax(outputs[i], axis=0)] = 1.0
        for i in range(outputs.shape[1]):
            if i+2 > outputs.shape[1]:
                accuracy = np.array(np.sum(np.around(outputs[:,i]) == targets[:,i]) / len(targets[:,i]))
                return accuracy
            else:
                accuracy = np.array(np.sum(np.around(outputs[:,i]) == targets[:,i]) / len(targets[:,i])) * np.array(np.sum(np.around(outputs[:,i+1]) == targets[:,i+1]) / len(targets[:,i+1]))
        
    def verbose(self,verbose,epoch,epochs,start):
        import time
        
        if verbose == 2:
            if epoch+1 < epochs:
                if self.val_inputs is not None and self.val_targets is not None:
                    print(f"[{epoch+1}/{epochs}] | train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} | val_loss: {np.around(self.val_cost_fn.loss(self.val_targets, self.val_outputs),5)} · val_accuracy: {np.around(self.accuracy(self.val_targets,self.val_outputs),5)}\n")
                else:
                    print(f"[{epoch+1}/{epochs}] | train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} | train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)}\n")
            elif epoch+1 == epochs:
                if self.val_inputs is not None and self.val_targets is not None:
                    self.runtime = time.time() - start
                    line_length1 = len(f"| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |")
                    line_length2 = len(f"| val_loss: {np.around(self.val_cost_fn.loss(self.val_targets, self.val_outputs),5)} · val_accuracy: {np.around(self.accuracy(self.val_targets,self.val_outputs),5)}")
                    print(line_length1 * "-" + f"\n| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |\n" + line_length1 * "-" + f"\n| val_loss: {np.around(self.val_cost_fn.loss(self.val_targets, self.val_outputs),5)} · val_accuracy: {np.around(self.accuracy(self.val_targets,self.val_outputs),5)}" + (line_length1-line_length2-1) * " " + "|\n" + line_length1 * "-")
                    print(f"{round(self.runtime, 5)} seconds")
                else:
                    self.runtime = time.time() - start
                    line_length1 = len(f"| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |")
                    print(line_length1 * "-" + f"\n| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |\n" + line_length1 * "-")
                    print(f"{round(self.runtime, 5)} seconds")
        elif verbose == 1:
            if epoch+1 == epochs:
                if self.val_inputs is not None and self.val_targets is not None:
                    line_length1 = len(f"| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |")
                    line_length2 = len(f"| val_loss: {np.around(self.val_cost_fn.loss(self.val_targets, self.val_outputs),5)} · val_accuracy: {np.around(self.accuracy(self.val_targets,self.val_outputs),5)}")
                    print("\n" + line_length1 * "-" + f"\n| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |\n" + line_length1 * "-" + f"\n| val_loss: {np.around(self.val_cost_fn.loss(self.val_targets, self.val_outputs),5)} · val_accuracy: {np.around(self.accuracy(self.val_targets,self.val_outputs),5)}" + (line_length1-line_length2-1) * " " + "|\n" + line_length1 * "-")
                else:
                    line_length = len(f"| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |")
                    print("\n" + line_length * "-" + f"\n| train_loss: {np.around(self.train_cost_fn.loss(self.train_targets, self.train_outputs),5)} · train_accuracy: {np.around(self.accuracy(self.train_targets,self.train_outputs),5)} |\n" + line_length * "-")
        elif verbose == 0:
            return 
        else:
            raise ValueError("invalid value for 'verbose'")
    
    def fit(self, cost_fn, epochs = 1000, lr = 0.1, momentum = None, verbose = 1, live_stats = None, extension = None):
        if live_stats == None:
            live_stats = LiveStats()
        elif live_stats == -1:
            live_stats = LiveStats(type=-1)
        elif live_stats == 0:
            live_stats = LiveStats(type=0)
        elif live_stats == 1:
            live_stats = LiveStats(type=1)
        elif live_stats == 2:
            live_stats = LiveStats(type=2)
            
        for n in [-1,0,1,2]:
            if live_stats.type == n:
                break
            elif n == 2 and live_stats.type != n:
                raise ValueError("invalid value for 'live_stats.type'")

        if live_stats.row_select != "full" and live_stats.row_select != "limited":
            raise ValueError("invalid value for 'live_stats.row_select'")
        
        if type(live_stats.f1) != int:
            raise ValueError("invalid value for 'live_stats.f1'")
        
        if type(live_stats.f2) != int:
            raise ValueError("invalid value for 'live_stats.f2'")
            
        self.__is_trained__ = True
        import copy
        from tqdm import tqdm
        import matplotlib.pyplot as plt
        import time
        start = time.time()
        
        train_cost_functions = copy.deepcopy(self.__cost_functions__)
        for name,function in train_cost_functions.items():
            if cost_fn == name:
                self.train_cost_fn = function
                break
            
        if self.val_inputs is not None and self.val_targets is not None:
            val_cost_functions = copy.deepcopy(self.__cost_functions__)
            for name,function in val_cost_functions.items(): 
                if cost_fn == name:
                    self.val_cost_fn = function
                    break
        
        if live_stats.type == -1:
            update = 50
            figure = plt.figure()
        elif live_stats.type == 0:
            update = 1
            figure = None
        elif live_stats.type == 1 or live_stats.type == 2: 
            update = 25
            figure = plt.figure()
            
        if verbose == 1:
            for epoch in tqdm(range(epochs)):
                self.forward()
                if epoch % update == 0 or epoch == 1:
                    self.train_loss_records.append(self.train_cost_fn.loss(self.train_targets, self.train_outputs))
                    self.train_accuracy_records.append(self.accuracy(self.train_targets, self.train_outputs))
                if self.val_inputs is not None and self.val_targets is not None:
                    if epoch % update == 0 or epoch == 1:
                        self.val_loss_records.append(self.val_cost_fn.loss(self.val_targets, self.val_outputs))
                        self.val_accuracy_records.append(self.accuracy(self.val_targets, self.val_outputs))
                self.backward(lr, momentum)
                
                if live_stats.type != 0:
                    if epoch % update == 0:
                        live_stats.run(self, figure)
                            
                self.verbose(verbose, epoch, epochs, start)
                
                if callable(extension):
                    extension()
        else:
            for epoch in range(epochs):
                self.forward()
                if epoch % update == 0 or epoch == 1:
                    self.train_loss_records.append(self.train_cost_fn.loss(self.train_targets, self.train_outputs))
                    self.train_accuracy_records.append(self.accuracy(self.train_targets, self.train_outputs))
                if self.val_inputs is not None and self.val_targets is not None:
                    if epoch % update == 0 or epoch == 1:
                        self.val_loss_records.append(self.val_cost_fn.loss(self.val_targets, self.val_outputs))
                        self.val_accuracy_records.append(self.accuracy(self.val_targets, self.val_outputs))
                self.backward(lr, momentum)
                
                if live_stats.type != 0:
                    if epoch % update == 0:
                        live_stats.run(self, figure)
                        
                self.verbose(verbose, epoch, epochs, start)
                
                if callable(extension):
                    extension()
        
    def results(self):
        if self.__is_trained__ == True:
            import matplotlib.pyplot as plt
            
            figure,axs = plt.subplots(1,2)
            
            axs[0].set_title("Loss Evolution")
            axs[0].set_xlabel("Epoch")
            axs[0].set_ylabel("Loss")
            axs[0].plot(self.train_loss_records, label="training dataset")
            if self.val_inputs is not None and self.val_targets is not None:
                axs[0].plot(self.val_loss_records, label="validation dataset")
            
            axs[1].set_title("Accuracy Evolution")
            axs[1].set_xlabel("Epoch")
            axs[1].set_ylabel("Accuracy")
            axs[1].plot(self.train_accuracy_records, label="training dataset")
            if self.val_inputs is not None and self.val_targets is not None:
                axs[1].plot(self.val_accuracy_records, label="validation dataset")
                
            axs[0].legend()
            axs[1].legend()
            
            plt.show()
        else:
            raise RuntimeError("model not trained")
            
    def save_params(self, name="parameters"):
        if self.__is_trained__ == True:
            import pickle
            parameters = {"weights": None, "biases": None}
            weights = []
            biases = []
            for layer in self.train_layers:
                if isinstance(layer, Dense):
                    weights.append(layer.weights)
                    biases.append(layer.biases)
                else:
                    weights.append(np.array(0.0))
                    biases.append(np.array(0.0))
            parameters["weights"] = weights
            parameters["biases"] = biases
            with open(name+".pkl", 'wb') as f:
                pickle.dump(parameters, f)
            return parameters
        else:
            raise RuntimeError("model not trained")
        
    def load_params(self, parameters = None, path="parameters.pkl"):
        if type(parameters) == dict or parameters == None:
            import pickle
            if parameters == None:
                with open(path, 'rb') as f:
                    parameters = pickle.load(f)
            for i in range(len(self.train_layers)):
                if isinstance(self.train_layers[i], Dense):
                    self.train_layers[i].weights = parameters["weights"][i]
                    self.train_layers[i].biases = parameters["biases"][i]
        else:
            raise TypeError("'parameters' should be a dictionnary")