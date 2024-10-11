create schema DB;

CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(20),
    endereco VARCHAR(100),
    cpf VARCHAR (100),
    email VARCHAR(100),
    tipoServico VARCHAR(100),
    agenda VARCHAR(100)
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
    descricao_servico ENUM('pendente', 'confirmado', 'realizado', 'cancelado'),
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
    );