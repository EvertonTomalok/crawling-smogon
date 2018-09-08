# crawling-smogon
<br>

Projeto de raspagem de dados do site https://www.smogon.com, o qual foi utilizado scrapy e selenium para obtenção dos dados.
<br>
<br>
Este site foi escolhido, pois existe uma grande dificuldade em obtenção dos dados, já que ela é uma página bem dinâmica,
e requer muita execução de código em javascript. Existem alguns opções para se executar JavaScript em uma página dinâmica,
e após isso efetuar a raspagem dos dados, tais quais como o uso do Splash, Selenium, ou mesmo a utilização baixo nível de 
Ajax.<br>
<br>
Após verificar a página, visualizei a necessidade de scrollar a página para gerar conteúdo, ou seja,a cada novo scroll, 
são inseridos novos elementos na página, em forma de carregamento de url/conteúdo dinâmico.

<br>

## Etapas do projeto

### Primeira etapa

- Crawl urls pokemons:

Todos o pokemons estão listados nesta página, www.smogon.com/dex/rs/pokemon/ , o qual exige que a página toda seja
scrollada, para gerar todo conteúdo disponível.
Após scrollar a página toda, todas as urls são salvas, e passadas para o segundo parser.
 
### Segunda Etapa

- Crawl informações de cada pokemon

O segundo parser, irá abrir uma pagína no google chrome, em modo headless, de cada url crawleada na etapa 1.
Após isso, cada informação dos pokemons será salvo, e salvo no formato escolhido. No caso, ao chamar a spider, escolhi
o output em .json<br>
<br>
As informações crawleadas, estão disponibilizadas no .json de nome "smogon/pokemons.json"
