import csv
import math

df = {}
reader = csv.DictReader(open('PS_2025.09.20_12.48.22.csv'))
for header in reader.fieldnames:
    df[header] = []
for row in reader:
    for header, value in row.items():
        try:
            df[header].append(float(value))
        except:
            df[header].append(value)

print(df['pl_eqt'][1000])

m = len(df["pl_eqt"])
# radius > 50, orbsmax > 10, insol > 8000, period >500
x = [df["pl_eqt"], df["pl_insol"], df["pl_orbeccen"], df["pl_orbsmax"], df["pl_orbper"], []]
y = df["pl_rade"]

w_old = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
w = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001,] 

iterations = 500

# print(len(x[0]))
# print(len(y))

del_array = []
for i in range(m):
    if y[i] > 50:
        # print(y[i])
        del_array.append(i)
    # if x[1][i] > 8000:
    #     print(x[1][i])
    #     del_array.append(i)
    # if x[3][i] > 10:
    #     print(x[3][i])
    #     del_array.append(i)
    # if x[4][i] > 500:
    #     print(x[4][i])
    #     del_array.append(i)
    x[-1].append(1)

print('-')
for j in range(len(del_array)-1, 0, -1):
    i = del_array[j]
    m -= 1;
    # print(y[i])
    y.pop(i)
    for list in x:
        list.pop(i)

x_test = [[],[],[],[],[],[]]
y_test = []
for i in range(0, m, 5):
    y_test.append(y[i])
    for j in range(len(x_test)):
        x_test[j].append(x[j][i])

for i in range(m-1, int(0.8 * m), -1):
    m -= 1;
    # print(y[i])
    y.pop(i)
    for list in x:
        list.pop(i)

def log(x, n):
    if n == 1:
        return math.log(1 + x)
    if n > 1:
        return math.log(1 + log(x, n - 1))
    
def exp(x, n):
    if n == 1:
        return math.e ** x - 1
    if n > 1:
        return math.e ** exp(x, n - 1) - 1

for i in range(len(y)):
    y[i] = log(y[i], 3)

def run_model(x, w):
    return exp(dot(x, w), 3)

# def lin_cost(x, w, y):
#     x_1, x_2, x_3, x_4, x_5 = x
#     w_1, w_2, w_3, w_4, b = w

#     print(x)
#     cost_sum = 0
#     for i in range(m):
#         f_wb = w_1 * x_1[i] + w_2 * x_2[i] + w_3 * x_3[i] + w_4 * x_4[i] + b
#         cost = (f_wb - y[i]) ** 2
#         cost_sum += cost
#     total_cost = (1 / (2 * m)) * cost_sum
#     return total_cost

def dot(v1, v2):
    assert len(v1) == len(v2), str(v1) + " != " + str(v2)
    sum = 0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum


def sub(v1, v2):
    assert len(v1) == len(v2)
    output = []
    for i in range(len(v1)):
        output.append(v1[i] - v2[i])
    return output


def scale(v, s):
    for i in range(len(v)):
        v[i] *= s
    return v


def del_J_component(x, w, y, j):
    x_1, x_2, x_3, x_4, x_5, x_6 = x
    w_1, w_2, w_3, w_4, w_5, b = w
    cost_sum = 0
    for i in range(m):
        # print(x_1[i])
        f_wb = w_1 * x_1[i] + w_2 * x_2[i] + w_3 * x_3[i] + w_4 * x_4[i] + w_5 * x_5[i] + b
        cost = (f_wb - y[i]) * x[j][i]
        cost_sum += cost
    return cost_sum / m


def del_J(x, w, y):
    output = []
    for i in range(len(x)):
        output.append(del_J_component(x, w, y, i))
    # output = scale(output, 1 / (math.sqrt(dot(output, output))))
    return output


def learning_rate(w, w_old, x, y):
    delta_w = sub(w, w_old)
    delta_grad_w = sub(del_J(x, w, y), del_J(x, w_old, y))
    denom = dot(delta_grad_w, delta_grad_w)
    if denom < 5.0 * 10 ** -15:
        denom = 5.0 * 10 ** -15
    learn_rate = (1 / denom) * abs(dot(delta_w, delta_grad_w))
    # print(learn_rate)
    return learn_rate


def update_w(w, w_old, x, y):
    w_1, w_2, w_3, w_4, w_5, b = w
    w = sub(w, scale(del_J(x, w, y), learning_rate(w, w_old, x, y)))
    # w = sub(w, scale(del_J(x, w, y), 0.02))
    # w = sub(w, scale(del_J(x, w, y), learning_rate(w, w_old, x, y)))
    return w


for i in range(iterations):
    if i % 100 == 0:
        print(i, ': ', w)
    temp = update_w(w, w_old, x, y)
    w_old = w
    w = temp

print("--")
print(f"weights = {w}")


avg_deviation = 0
avg_percent = 0
for i in range(len(y_test)):
    deviation = abs(run_model([x_test[0][i], x_test[1][i], x_test[2][i], x_test[3][i], x_test[4][i], x_test[5][i]], w) - y_test[i])
    avg_deviation += deviation
    avg_percent += deviation / y_test[i]
avg_deviation /= len(y_test)
avg_percent = 100.00 * (avg_percent / len(y_test))

print(f"avg_deviation = {avg_deviation}")
print(f"avg_percent = {avg_percent}")

