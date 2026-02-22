Create database controle_renda_variavel;
Use controle_renda_variavel;

Create table receitas (
id int auto_increment primary key,
data date not null,
valor decimal(10,2) not null,
origem varchar(100),
criado_em timestamp default current_timestamp
);

Create table gastos (
id int auto_increment primary key,
data date not null,
valor decimal(10,2) not null,
categoria varchar(100),
tipo enum('normal', 'inesperado') not null,
criado_em timestamp default current_timestamp
);

Create table configuracoes (
id int auto_increment primary key,
meta_reserva decimal(10,2),
gasto_fixo_mensal decimal(10,2),
atualizado_em Timestamp default current_timestamp on update current_timestamp
);

Insert into receitas (data, valor, origem) values
('2026-02-01', 250.00, 'Freelancer');

Insert into gastos (data, valor, categoria, tipo) values
('2026-02-02', '100.00', 'Alimentação', 'normal');

Select
	Month(data) as mes,
    Year(data) as ano,
    SUM(valor) as total_receitas
From receitas
Group by ano, mes;

Select
	Month(data) as mes,
    Year(data) as ano,
    Sum(valor) as total_gastos
From gastos
Group by ano, mes;

Select
	Sum(valor) as total_inesperado
From gastos
Where tipo = 'inesperado'
And Month(data) = Month(current_date())
And Year(data) = Year(current_date()); 



