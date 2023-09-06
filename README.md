# bus_ticket_system
## Projeto de um sistema de compra de passagens de ônibus.
Criei a ideia do projeto baseado em experiências de viagens que fiz e para entender um pouco a lógica, observei alguns Websites de compra de passagem de ônibus.

O projeto ainda está bem simples, muitas lógicas estão incoerentes com a realidade, mas já dá pra entender o conceito.

## As tecnologias usadas foram:
  - Python
  - Flask
  - Psycopg2
  - PostgreSQL
## Tabelas
### O projeto possui 7 tabelas no banco de dados:
  - Bus (Representa o ônibus)
  - Seat (Representa o assento do ônibus)
  - Line (Representa a linha da viagem, ex: de Brasília para Recife) 
  - Route (Representa a rota da linha, ex: Brasília, Formosa, Correntina, ...,  Caruaru, Recife)
  - Trip (Representa a viagem. Ex: de Formosa para Correntina, dia 01/09/2023, ônibus convencional etc)
  - Passenger (Representa o passageiro)
  - Ticket (Representa a compra da viagem. Essa tabela está relacionada com todas as anteriores, diretamente ou indiretamente.)

### Cada Tabela dessa possui um endereço http para realizar o add, get, delete etc que são as rotas.
Nem Todas as tabelas têm as rotas add, delete etc. Criei as rotas de acordo com a minha lógica.
Por exemplo, a tabela Seat não tem as rotas add nem delete, pois no momento em que eu crio um ônibus, o sistema deve criar automaticamente os assentos vinculados à esse ônibus e de acordo com a quantidade que eu defini ao criar o ônibus.

### Atributos das tabelas:
PK: Chave Primária.
FK: Chave Estrangeira.

- Bus:
  id (PK)- valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica o Ônibus;
  license_plate - placa do ônibus. Tem o padrão AAA9A99, onde A podem ser letras e 9 podem ser números;
  type - tipo do ônibus. pode ser somente: Convencional, Executivo, Semi-Leito ou Leito;
  amount_seats - quantidade de poltronas do ônibus. Não tem um padrão;

- Seat:
  id (PK): Valor caratere, não repetível e auto incrementário pelo sistema, que identifica a Poltrona. é presentado pela placa do ônibus a qual pertence + a numeração da poltrona. Ex: YSL1A78-2, YSL1A78-18;	
  number - Numeração do Assento;
  is_free - TRUE (assento está vago), FALSE (Assento ocupado).
  vacant_in - NULL (Indica que o assento está livre), "nome da cidade" (indica a cidade em que o assento vai desocupar); Caso is_free TRUE, vacant_in deve ser NULL, caso is_free FALSE, vacant_in deve conter o nome da cidade.
  bus_id (Fk) - id do ônibus a qual o assento pertence;

- Line:
  id (PK)- valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica a Linha;
  origin - cidade de origem ou última cidade da linha;
  destination - cidade de destino ou última cidade da linha;
  departure_time - horário que o ônibus sai da cidade de origem;
  arrival_time - horário que o ônibus chega na cidade de destino; 
  total_price - Preço da linha;

- Route:
  id (PK) - valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica a Rota;
  city - cidade da rota (que está na linha);
  time - horário que o ônibus passa na cidade;
  price - valor da cidade à cidade de destino (última cidade da linha);
  line_id (FK) - id da linha a qual a rota pertence;

- Trip
  id (PK) - valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica a Viagem;
  date - data da viagem;
  line_id (FK) - id da linha a qual a viagem pertence; 
  bus_id (FK) - id do ônibus a qual a viagem percente;

- Passenger
  id (PK) - valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica o Passageiro;
  name - nome do passageiro;
  phone - telefone do passageiro. Tem o padrão: (xx)9xxxx-xxxx onde x é valor numérico.

- Ticket
  id (PK) - valor numérico, não repetível e auto incrementário pelo banco de dados, que identifica a Compra da passagem;
  trip_id (FK) - id da viagem da compra;
  origin_id (FK) - id da rota origem da viagem da compra(o line_id da rota deve ser o mesmo do line_id da viagem);
  destination_id (FK) - id da rota destino da viagem da compra (o line_id da rota deve ser o mesmo do line_id da viagem);
  passenger_id (FK) - id do passageiro que está comprando a passagem;
  seat_id (FK) - id da poltrona que o passageiro vai comprar
  route_price - preço da rota escolhida pelo passageiro, calculado automatimente pelo sistema;
  
* Os valores monetários estão no formato americano (17.99, 1.00 etc).
* Os valores de horário estão no formato brasileiro (07:00, 21:55 etc).
* Os valores de data estão no formato ano-mês-dia (2023-09-17).

## Endpoints
Endereço =  http://127.0.0.1:5000/ ou http://localhost:5000/
ex: endereço para adicionar um novo ônibus
    http://127.0.0.1:5000/bus/ (método POST)
    
### Bus
- bus/
  POST - Cria um ônibus caso não exista um ônibus com a mesma placa (atributos license_plate, type e amount_seats no body);
  GET - Retona Todos os ônibus cadastrados;
  GET (com o parâmetro de consulta "license_plate") - Retorna o ônibus de acordo com a placa;
  GET (com o parâmetro de consulta "type") - Retorna todos os ônibus de acordo com o tipo;
  
- bus/id
  GET - Retona o ônibus de acordo com o id;
  DELETE - Deleta o ônibus de acordo com o id;
  PUT - Atualiza o ônibus de acordo com o id (colocar todos os atributos no body);


### Seat
- seat/
  GET (com o parâmetro de consulta "bus_id")- Retorna todos os assentos vinculados ao ônibus de acordo com o id do ônibus;
  
- seat/bus_id
  GET  - Retorna a poltrona de acordo com seu id; 
  PUT - Atualiza a poltrona de acordo com o id (atributos is_free e vacant_in no body);

* Obs: não existe o método POST nem DELETE pois essas funcionalidades só devem ser acessadas pelo sistema.
 
 
### Line
- line/
  POST - Cria uma linha (atributos no Body: origin, destination, departure_time, arrival_time e total_price)
  GET - Retorna todas as linhas cadastradas;
 
- line/id
  GET - Retorna a linha de acordo com o id;
  DELETE - Deleta a linha de acordo com o id;
  PUT - Atualiza a linha (atributos no Body: origin, destination, departure_time, arrival_time e total_price); 
  
  
### Route
- route/
  POST - Cria uma nova rota vinculada a uma linha (atributos city, time, price, line_id no body);
  GET - Retorna todas as rotas cadastradas;
  GET (com o parâmetro de consulta line_id) - Retorna todas as rotas de acordo com o id da linha.
  

- route/id
  GET - Retorna a rota de acordo com o id;
  PUT - Atualiza a rota (atributos city, time, price, line_id no body);
  DELETE - Deleta a rota de acordo com o id;
  
  
### Trip
- trip/
  POST - Cria uma nova viagem vinculada a uma linha (atributos date, line_id e bus_id no body);
  GET - Retorna todas as viagens cadastradas;
 
- trip/id
  GET - Retorna a viagem de acordo com o id;
  PUT - Atualiza a rota de acordo com o id (atributos date, line_id e bus_id no body);
  DELETE - Deleta a viagem de acordo com o id;
  

### Passenger
- passenger/
  POST - Cria um novo passageiro (atributos name e phone no body);
  GET - Retorna todas os passageiros cadastrados;
 
- passanger/id
  GET - Retorna o passageiro de acordo com o id;
  PUT - Atualiza o passageiro de acordo com o id (atributos name e phone no body);
  DELETE - Deleta o passageiro de acordo com o id;
 

### Ticket
- ticket/
  POST - Cria um novo ticket (atributos trip_id, origin_id, destination_id, passenger_id e seat_id body);
  GET - Retorna todas os tickets cadastrados;
 
- ticket/id
  GET - Retorna o ticket de acordo com o id;
  PUT - Atualiza o ticket de acordo com o id (atributos trip_id, origin_id, destination_id, passenger_id e seat_id body);
  DELETE - Deleta o ticket de acordo com o id;
