library(tidyverse)
library(janitor)
library(ggplot2)
library(reshape2)
library(ggthemes)
library(RColorBrewer)
library(naniar)
library(dplyr)
library(ggcorrplot)
library(corrplot)
library(gridExtra)

#Leitura de dados, e especificando dados ausentes (N/A) para evitar problemas futuros
turnover <- read_csv(file.path("dado", "IBM HR Data new.csv"),na = c("N/A", "", "NULL", "NaN"))

turnoverorigi <- read_csv(file.path("dado", "IBM HR Data.csv"),na = c("N/A", "", "NULL", "NaN"))

# Variáveis removidas
# 
# EmployeeNumber
# Application ID
# Over18 - Só contém um valor
# StandardHours - Só contém um valor
# EmployeeCoun - Só contém um valor

view(turnoverorigi)

view(turnover)

# a função é utilizada para listar a quantidade de NAs em cada uma das variaveis
gg_miss_var(turnover) 

# Quantidade exata de NA por coluna
colSums(is.na(turnover))



# Seleciona apenas as colunas numéricas do dataset 
numeric_vars <- turnover[, sapply(turnover, is.numeric)]


# Calcular a matriz de correlação
# use = "complete.obs" exclui linhas com dados incompletos 
#é uma função que aplica uma outra função (neste caso, is.numeric) a cada coluna do dataset
correlation_matrix <- cor(numeric_vars, use = "complete.obs")

# Visualizar a matriz de correlação
print(correlation_matrix)

#Deixar em branco as correlações não significativas
cor_pmat(correlation_matrix)

#plota a matriz de correlação
ggcorrplot(correlation_matrix,
           #method = "circle",
           #hc.order = TRUE, #agrupa valores
           type = "lower", #Esconder o espelhamento
           lab = TRUE, #valores
           lab_size = 2,
           #p.mat = cor_pmat(correlation_matrix),
           #insig = "blank"
          
)

#Converte a Attrition para categórico, ggplot não aplica cores automáticas se Attrition não estiver bem definido
turnover$Attrition <- as.factor(turnover$Attrition)


# Gráfico de dispersão para TotalWorkingYears e MonthlyIncome, colorido por Attrition
ggplot(turnover, aes(x = TotalWorkingYears, y = MonthlyIncome, color = Attrition)) +
  geom_point() +
  labs(title = "Relação entre Total Working Years e Monthly Income por Status de Attrition", 
       x = "Total Working Years", y = "Monthly Income") +
  theme_minimal()


# Para combinar múltiplos gráficos em um só

# Gráfico 1: Departamento em relação ao Attrition
g0<- ggplot(turnover, aes(x = factor(Department), fill = Attrition)) +
  geom_bar(position = "fill") +  
  labs(title = "Proporção de Departamento por Status de Attrition", 
       x = "Department", y = "Proporção de Funcionários") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotacionar rótulos do eixo X para melhor leitura

# Gráfico 2: YearsWithCurrManager em relação ao Attrition
g1<- ggplot(turnover, aes(x = factor(JobRole), fill = Attrition)) +
  geom_bar(position = "fill") +  
  labs(title = "Proporção de Cargo por Status de Attrition", 
       x = "Job Role", y = "Proporção de Funcionários") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotacionar rótulos do eixo X para melhor leitura

# Combinar os dois gráficos em um layout
grid.arrange(g0,g1, ncol = 2)

#

