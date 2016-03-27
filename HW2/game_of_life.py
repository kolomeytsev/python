class Life(object):
    def __init__(self, field, n_generations):
        self.field = field
        self.n_generations = n_generations
        self.n_rows = len(field)
        self.n_cols = len(field[0])

    def make_border(self):
        new_row = [4 for col in range(self.n_cols + 2)]
        for row in range(self.n_rows):
            self.field[row].insert(0, 4)
            self.field[row].append(4)
        self.field.insert(0, new_row)
        self.field.append(new_row)
        self.n_rows += 2
        self.n_cols += 2

    def print_field(self):
        for row in range(1, self.n_rows - 1):
            lst = map(str, self.field[row][1:-1])
            print ' '.join(lst)

    # counts how much neighbours, who have value = param
    def count_neighbours(self, row, col, param):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0) or (j != 0):
                    if self.field[row + i][col + j] == param:
                        count += 1
        return count

    def decide_who_dies(self):
        who_dies_array = []
        for row in range(0, self.n_rows):
            who_dies_array.append([0 for col in range(0, self.n_cols)])
        for row in range(1, self.n_rows - 1):
            for col in range(1, self.n_cols - 1):
                species = self.field[row][col]
                if species > 1:
                    neighbours = self.count_neighbours(row, col, species)
                    if (neighbours > 3) or (neighbours < 2):
                        who_dies_array[row][col] = 1
        return who_dies_array

    # param = 2 -> fish, param = 3 -> shrimp
    def decide_who_borns(self, param):
        who_borns_array = []
        for row in range(0, self.n_rows):
            who_borns_array.append([0 for col in range(0, self.n_cols)])
        for row in range(1, self.n_rows - 1):
            for col in range(1, self.n_cols - 1):
                if self.field[row][col] == 0:
                    neighbours = self.count_neighbours(row, col, param)
                    if neighbours == 3:
                        who_borns_array[row][col] = 1
        return who_borns_array

    def make_step(self):
        who_dies_array = self.decide_who_dies()
        who_borns_fish = self.decide_who_borns(2)
        who_borns_shrimp = self.decide_who_borns(3)
        for row in range(1, self.n_rows - 1):
            for col in range(1, self.n_cols - 1):
                if who_dies_array[row][col] == 1:
                    self.field[row][col] = 0
                else:
                    if who_borns_shrimp[row][col] == 1:
                        self.field[row][col] = 3
                    if who_borns_fish[row][col] == 1:
                        self.field[row][col] = 2

    def play(self):
        self.make_border()
        for iteration in range(n_generations):
            self.make_step()
        self.print_field()

n_generations = int(raw_input())
size_str = raw_input()
n_rows = int(size_str.split()[0])
n_cols = int(size_str.split()[1])
array = []
for it in range(n_rows):
    lst = map(int, raw_input().split())
    array.append(lst)
obj_life = Life(array, n_generations)
obj_life.play()
