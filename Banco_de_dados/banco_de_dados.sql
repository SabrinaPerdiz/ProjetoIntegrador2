-- Tabela Clientes
CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(20),
    data_nascimento DATE,
    endereco VARCHAR(255),
    facebook VARCHAR(255),
    instagram VARCHAR(255)
);

-- Tabela Usuários
CREATE TABLE usuarios (
  id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(255) NULL,
  senha VARCHAR(45) NULL
);

-- Tabela Agendamentos
CREATE TABLE Agendamentos (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_procedimento INT,
    data_agendamento DATE,
    hora_agendamento TIME,
    data_realizacao DATE,
    tipo_servico ENUM('montagem', 'reforma', 'instalações'),
    descricao_servico,
    status ENUM('pendente', 'confirmado', 'realizado', 'cancelado'),
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_procedimento) REFERENCES Procedimentos(id_procedimento)
);


