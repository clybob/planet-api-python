# planet-api-python
API de planetas de Star Wars

## Como rodar

### Setup
```
make setup
```

### Run
```
make run
```

### Testes
```
make test
```

## Tecnologias
* Python
* Flask
* SQL Alchemy
* Requests
* Flask Caching
* Postgres
* Docker Compose

## API
* **GET:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/?search=Tatooine&page=1

Parâmetros de Get
* **search**: Busca por nome ou id do planeta
* **page**: Filtra por uma página específica

Retorno 200
```javascript
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Tatooine",
      "climate": "arid",
      "terrain": "desert",
      "films_count": 5
    }
  ]
}
```

* **POST:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/

Body
```javascript
{
  "name": "Tatooine",
  "climate": "arid",
  "terrain": "desert",
}
```

Retorno 201
```javascript
{
  "id": 1,
  "name": "Tatooine",
  "climate": "arid",
  "terrain": "desert",
  "films_count": 5
}
```

* **GET:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/1/

Retorno 200
```javascript
{
  "id": 1,
  "name": "Tatooine",
  "climate": "arid",
  "terrain": "desert",
  "films_count": 5
}
```

* **PUT:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/1/

Body
```javascript
{
  "name": "Tatooine New",
  "climate": "arid",
  "terrain": "desert",
}
```

Retorno 200
```javascript
{
  "id": 1,
  "name": "Tatooine New",
  "climate": "arid",
  "terrain": "desert",
  "films_count": 5
}
```

* **PATCH:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/1/

Body
```javascript
{
  "name": "Tatooine New"
}
```

Retorno 200
```javascript
{
  "id": 1,
  "name": "Tatooine New",
  "climate": "arid",
  "terrain": "desert",
  "films_count": 5
}
```

* **DELETE:** http://ec2-18-231-117-182.sa-east-1.compute.amazonaws.com:5000/planets/1/

Retorno 204


## Decisões de projeto

### Framework
Para esse projeto descartei o Django por se tratar de um framework muito grande para um projeto tão simples, apesar dele ter o Django-rest-framework que torna a criação de APIs bem simples.

Cogitei principalmente Flask e Tornado.
Gosto bastante do Tornado pelo fato dele trabalhar com requisições assíncronas e não blocantes, mas pela minha experiência a maioria dos desenvolvedores não entende bem o framework e acaba não usando o potencial que ele tem.

Fiquei então com o Flask, que é um framework mais enxuto, bastante simples de entender e dar manutenção.

Poderia ter usado nesse projeto o flask-restful para facilitar a criação de uma api RestFull, mas ai não sobraria muito código meu para ser avaliado.

### Banco de dados
Para uma API simples como essa normalmente eu usaria um banco relacional MySQL, mas como no desafio a escolha era entre Postgress ou MongoDb optei pelo Postgress. Já trabalhei com projetos com Mongo, a sensação inicial de simplicidade é ótima mas a manutenção ao longo do tempo costuma ser mais cara. Além disso o argumento de performance do Mongo só é realmente válido quando se trata de dados muito acoplados onde seriam necessários alguns JOINs em SQL para cumprir o objetivo.

### Testes
Para evitar que os testes façam requests na Swapi e fiquem lentos existe um mock do método responsável por buscar as informações de filmes da API. E nos testes desse método o acesso a API é feito para garantir a integração.

### Cache
Para evitar requests desnecessários na Swapi adicionei um memoize com timeout de 1 semana, assim cada planeta será pesquisado apenas 1 vez por semana, como não são lançados novos filmes novos com tanta frequência esse tempo de cache já é o suficiente. E quando lançar um novo filme pode-se limpar o cache pra ser mais rápido.

Nas rotas da API adicionei um cache de 30 segundos, isso pode ser o suficiente para não derrubar a API em caso de falhas do NGINX e ao mesmo tempo mantem o dinamismo necessário para um jogo.

O uso da estratégia de cache "simple" (em memória local) foi apenas para tornar a implementação mais facil. Em um sistema de produção usaria o Redis como backend para poder compartilhar o cache entre diversas instâncias.

### Features não implementadas
**Autenticação**
Para não ir muito além do enunciado do projeto decidi não implementar a autenticação, mas sei que se essa API fosse ao ar esse "detalhe" não poderia faltar.

**Rate Limit**
Seguindo a linha do item anterior seria interessante implementar um rate limit baseado no token de cada consumidor da API, esse controle poderia ser facilmente implementado usando o INCR do Redis.

**Prod**
Para a apresentação do desafio usei apenas uma instância EC2 rodando o próprio Flask. Se essa API realmente fosse usada em produçãp configuraria para funcionar com o Gunicorn e Nginx.
