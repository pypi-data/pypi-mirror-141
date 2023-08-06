# Nait
# Neural Artificial Intelligence Tool
# Version 2.0.1

import random
import math
import copy
import time
import json

class Network:
    def __init__(self):

        # Generating layers
        self.weights = []
        for _ in range(2):
            layer = []

            for _ in range(4):
                layer.append([0]*4)
            self.weights.append(layer)

        self.biases = []
        for _ in range(2):
            self.biases.append([0]*4)

    def train(self,
              x,
              y,
              layer_size=4,
              layers=1,
              activation_function="linear",
              generate_network=True,
              learning_rate=0.01,
              optimizer="randomize",
              sample_size=10,
              epochs=100,
              exit_increase=0.1,
              backup=None):

        # Verifying training data
        print("INITIATING verifying training data")
        if len(x) != len(y):
            raise ValueError("length of x should equal the length of y")
        if layer_size < 1 or layer_size > 128:
            raise ValueError("layer size can not be below 1 or above 128")
        if layers < 1 or layers > 9:
            raise ValueError("can not have less hidden layers than 1 or more than 9")

        start_time = time.time()

        # Generating layers
        if generate_network == True:
            print("INITIATING creating network structure")
            self.activation_function = activation_function
            self.weights = []
            self.biases = []

            for _ in range(layers + 1):
                self.weights.append([[round(random.uniform(-1, 1), 8) for _ in range(layer_size)] for _ in range(layer_size)])
                self.biases.append([round(random.uniform(0, 0), 8) for _ in range(layer_size)])
            
            self.weights[0] = [[round(random.uniform(-1, 1), 8) for _ in range(len(x[0]))] for _ in range(layer_size)]
            self.weights[-1] = [[round(random.uniform(-1, 1), 8) for _ in range(layer_size)] for _ in range(len(y[0]))]

            self.biases[-1] = [0.0 for _ in range(len(y[0]))]

        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                neuron_output = sum(neuron_output) + layer_biases[neuron_index]
                
                if self.activation_function == 'relu':
                    if neuron_output < 0:
                        neuron_output = 0

                if self.activation_function == 'step':
                    if neuron_output >= 1:
                        neuron_output = 1
                    else:
                        neuron_output = 0

                if self.activation_function == 'sigmoid':
                    sig = 1 / (1 + math.exp(-neuron_output))
                    neuron_output = sig

                if self.activation_function == 'leaky_relu':
                    if neuron_output < 0:
                        neuron_output = neuron_output * 0.1

                #print(neuron_output)
                layer_output.append(round(neuron_output, 4))

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            activation_list = [network_input]
            network_output = network_input
            for weight_index in range(len(weights)):
                activation_list.append(layer_forward(network_output, weights[weight_index], biases[weight_index]))
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return (network_output, activation_list)

        # Training
        epoch = 0
        last_loss = float('Inf')
        exit_training = False

        while epoch < epochs and exit_training == False:

            epoch += 1

            # Generating batch
            batch_weights = [self.weights]
            batch_biases = [self.biases]

            if optimizer == "randomize":

                for _ in range(sample_size):
                    batch_weights.append(copy.deepcopy(self.weights))
                    batch_biases.append(copy.deepcopy(self.biases))

                    for layerindex in range(len(batch_weights[0])):
                        for neuronindex in range(len(batch_weights[0][layerindex])):
                            batch_biases[0][layerindex][neuronindex] = round(
                                random.uniform(learning_rate, learning_rate*-1) + batch_biases[0][layerindex][neuronindex], 8)

                            for weightindex in range(len(batch_weights[0][layerindex][neuronindex])):
                                batch_weights[0][layerindex][neuronindex][weightindex] = round(
                                    random.uniform(learning_rate, learning_rate*-1) + batch_weights[0][layerindex][neuronindex][weightindex], 8)

                    for layerindex in range(len(batch_weights[0])):
                        for neuronindex in range(len(batch_weights[0][layerindex])):
                            batch_biases[0][layerindex][neuronindex] = round(
                                random.uniform(learning_rate*0.1, learning_rate*-0.1) + batch_biases[0][layerindex][neuronindex], 8)

                            for weightindex in range(len(batch_weights[0][layerindex][neuronindex])):
                                batch_weights[0][layerindex][neuronindex][weightindex] = round(
                                    random.uniform(learning_rate*0.1, learning_rate*-0.1) + batch_weights[0][layerindex][neuronindex][weightindex], 8)

            elif optimizer == "backpropagate":
            
                for x_index in range(len(x)):
                    activation_list = network_forward(x[x_index], batch_weights[0], batch_biases[0])[1]
                    wanted_changes = [y[x_index][i] - activation_list[-1][i] for i in range(len(activation_list[-1]))]

                    for layer_backwards in range(len(self.weights)):

                        new_wanted_changes = [0 for _ in range(len(activation_list[(len(self.weights) - 1) - layer_backwards]))]

                        for neuron_index in range(len(batch_weights[0][(len(self.weights) - 1) - layer_backwards])):

                            batch_biases[0][(len(self.weights) - 1) - layer_backwards][neuron_index] += wanted_changes[neuron_index] * learning_rate

                            for weight_index in range(len(batch_weights[0][(len(self.weights) - 1) - layer_backwards][neuron_index])):

                                batch_weights[0][(len(self.weights) - 1) - layer_backwards][neuron_index][weight_index] += wanted_changes[neuron_index] * activation_list[(len(self.weights) - 1) - layer_backwards][weight_index] * learning_rate
                                batch_weights[0][(len(self.weights) - 1) - layer_backwards][neuron_index][weight_index] = round(batch_weights[0][(len(self.weights) - 1) - layer_backwards][neuron_index][weight_index], 8)
                                new_wanted_changes[weight_index] += batch_weights[0][(len(self.weights) - 1) - layer_backwards][neuron_index][weight_index] * learning_rate
                        
                        wanted_changes = new_wanted_changes

            # Selection
            losses = []
            for index in range(len(batch_weights)):
                current_loss = 0
                for x_index in range(len(x)):
                    network_output = network_forward(x[x_index], batch_weights[index], batch_biases[index])[0]
                    neuron_loss = 0
                    for output_index in range(len(y[x_index])):
                        neuron_loss += abs(network_output[output_index] - y[x_index][output_index])
                    current_loss += neuron_loss
                if math.isnan(current_loss):
                    losses.append(float('Inf'))
                else:
                    losses.append(current_loss)
            
            if min(losses) - last_loss > exit_increase:
                exit_training = True
                continue
            
            if min(losses) < last_loss:
                last_loss = min(losses)

            self.weights = batch_weights[losses.index(min(losses))]
            self.biases = batch_biases[losses.index(min(losses))]

            if epoch == 1:
                if (time.time() - start_time) * epochs >= 60:
                    print(f"TRAINING estimated time: {math.floor(((time.time() - start_time) * epochs) / 60)}m")
                else:
                    print(f"TRAINING estimated time: {math.floor((time.time() - start_time) * epochs)}s")

            filled_loadingbar = "█"
            unfilled_loadingbar = " "

            bar_filled = round(epoch / epochs * 40)

            if round(epoch % (epochs / 50), 0) == 0 or epoch == epochs:
                if ((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs)) >= 60:
                    print(f"TRAINING loss: {round(min(losses), 8)} average loss: {round(min(losses)/len(x), 8)} epoch {epoch}/{epochs} estimated remaining time: {math.floor((((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs))) / 60)}m" + " " * 50)
                else:
                    print(f"TRAINING loss: {round(min(losses), 8)} average loss: {round(min(losses)/len(x), 8)} epoch {epoch}/{epochs} estimated remaining time: {math.floor(((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs)))}s" + " " * 50)

                if backup != None and epoch != epochs:
                    data = {}
                    data['weights'] = self.weights
                    data['biases'] = self.biases
                    data['activation'] = self.activation_function

                    with open(backup, 'w') as backup_file:
                        json.dump(data, backup_file)

            else:
                print(f"TRAINING |{filled_loadingbar * bar_filled}{unfilled_loadingbar * (40 - bar_filled)}| {round((epoch / epochs) * 100, 1)}% loss: {round(min(losses), 8)} average loss: {round(min(losses)/len(x), 8)} epoch {epoch}/{epochs}" + " " * 50, end="\r")

        # Post training
        if (time.time() - start_time) * (epoch / epochs) >= 60:
            print(f"FINAL loss: {round(min(losses), 8)} average loss: {round(min(losses)/len(x), 8)} time: {math.floor(((time.time() - start_time) / (epoch / epochs)) / 60)}m")
        else:
            print(f"FINAL loss: {round(min(losses), 8)} average loss: {round(min(losses)/len(x), 8)} time: {math.floor((time.time() - start_time) / (epoch / epochs))}s")

    def predict(self, inputs):

        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                neuron_output = sum(neuron_output) + layer_biases[neuron_index]
                
                if self.activation_function == 'relu':
                    if neuron_output < 0:
                        neuron_output = 0

                if self.activation_function == 'step':
                    if neuron_output >= 1:
                        neuron_output = 1
                    else:
                        neuron_output = 0

                if self.activation_function == 'sigmoid':
                    sig = 1 / (1 + math.exp(-neuron_output))
                    neuron_output = sig

                if self.activation_function == 'leaky_relu':
                    if neuron_output < 0:
                        neuron_output = neuron_output * 0.1

                layer_output.append(neuron_output)

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            activation_list = []
            network_output = network_input
            for weight_index in range(len(weights)):
                activation_list.append(layer_forward(network_output, weights[weight_index], biases[weight_index]))
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return (network_output, activation_list)

        return network_forward(inputs, self.weights, self.biases)[0]
    
    def save(self, file):
        
        data = {}

        data['weights'] = self.weights
        data['biases'] = self.biases
        data['activation'] = self.activation_function

        with open(file, 'w') as file:
            json.dump(data, file)
    
    def load(self, file):

        with open(file, 'r') as file:
            data = json.load(file)

        self.weights = data['weights']
        self.biases = data['biases']
        self.activation_function = data['activation']
    
    def evaluate(self, x, y):

        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                layer_output.append(sum(neuron_output) + layer_biases[neuron_index])

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            network_output = network_input

            for weight_index in range(len(weights)):
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return network_output

        # Evaluation
        loss = 0
        for x_index in range(len(x)):
            network_output = network_forward(x[x_index], self.weights, self.biases)
            neuron_loss = 0
            for output_index in range(len(y[x_index])):
                neuron_loss += abs(network_output[output_index] - y[x_index][output_index])
            loss += neuron_loss
        print(f"EVALUATION loss: {round(loss, 8)} average loss: {round(loss/len(x), 8)}")