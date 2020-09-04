
population = {}

with open("population.txt") as file:
    for line in file:
        words = line.split()
        dep, pop = words[0], words[-1]

        try:
            idep = int(dep)
        except ValueError:
            # Corse
            continue

        if idep > 100:
            continue

        dep = f"{idep:02d}"

        population[dep] = int(pop)
