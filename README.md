# planet-api-python
API de planetas de Star Wars

## Decisões de projeto

### Frameworks
Para esse projeto descartei o Django por se tratar de um framework muito grande para um projeto tão simples, apesar dele ter o Django-rest-framework que torna a criação de APIs bem simples.

Cogitei principalmente Flask e Tornado.
Gosto bastante do Tornado pelo fato dele trabalhar com requisições assíncronas e não blocantes, mas pela minha experiência a maioria dos desenvolvedores não entende bem o framework e acaba não usando o potencial que ele tem.

Fiquei então com o Flask, que é um framework mais enxuto, bastante simples de entender e dar manutenção.

Poderia ter usado nesse projeto o flask-restful para facilitar a criação de uma api RestFull, mas ai não sobraria muito código meu para ser avaliado.

### Banco de dados
Para uma API simples como essa normalmente eu usaria um banco relacional MySQL, mas como no desafio a escolha era entre Postgress ou MongoDb optei pelo Postgress. Já trabalhei com projetos com Mongo, a sensação inicial de simplicidade é ótima mas a manutenção ao longo do tempo costuma ser mais cara. Além disso o argumento de performance do Mongo só é realmente válido quando se trata de dados muito acoplados onde seriam necessários alguns JOINs em SQL para cumprir o objetivo.

### Testes
Para evitar que os testes façam requests na Swapi e fiquem lentos existe um mock do método responsável por buscar as informações de filmes da API. E nos testes desse método o acesso a API é feito para garantir a integração.
