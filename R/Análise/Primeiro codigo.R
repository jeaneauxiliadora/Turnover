# Importando a biblioteca que será usada
library(tidyverse)
library(janitor)
library(palmerpenguins)
library(ggthemes)


# Ctrl + shift + c cria um comentário no texto selecionado
students <- read_csv("https://pos.it/r4ds-students-csv", na = c("N/A", ""))

# Limpa os nomes das colunas
students <- students |> clean_names()

students

# Faz a mutação na coluna age
students <- students |> 
  mutate(
    age = parse_number(if_else(age == "five", "5", age))
  )

# Salva o resultado em um arquivo CSV
students |> write_csv("aula.csv")

# Atalho pipi é ctrl + shift + m
# Atalho <- é alt + menos

# Vendo a tabela nova instalada
penguins

# Visualizando como se fosse excel
View(penguins)

#Visualizando como se fosse invertido linha para coluna
glimpse(penguins)


# Plotando gráficos - Reservando a área para o gráfico, mas não plota nada
ggplot(data = penguins)


# Plotando gráfico de pontos
p <- penguins |> ggplot(mapping = aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point()
p


# Plotando gráfico de linha
p <- penguins |> ggplot(mapping = aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_line()
p


# Plotando gráfico de pontos com tema bw
p <- penguins |> ggplot(mapping = aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point() +
  theme_bw()
p


# Verificando a quantidade de NA de cada coluna em penguins
penguins |> map(\(x) sum(is.na(x)))

penguins |> map_dfc(\(x) sum(is.na(x)))



# Gráfico clorido
p <- ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g, color = species)
) +
  geom_point() +
  theme(legend.position = "bottom")

p