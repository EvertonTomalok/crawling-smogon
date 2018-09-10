# crawling-smogon
<br>

Projeto de raspagem de dados do site www.smogon.com, o qual foi utilizado scrapy e selenium para obtenção dos dados.
<br>
<br>
Este site foi escolhido, pois existe uma grande dificuldade em obtenção dos dados (além de que eu sou um grande fã de pokemon), 
já que ela é uma página bem dinâmica, e requer muita execução de código em javascript. Existem algumas opções para se executar 
JavaScript em uma página dinâmica, e após isso efetuar a raspagem dos dados, tais quais como o uso do Splash, Selenium, ou mesmo a 
utilização baixo nível de Ajax.<br>
<br>
Após verificar a página, visualizei a necessidade de scrollar a página para gerar conteúdo, ou seja,a cada novo scroll, 
são inseridos novos elementos na página, em forma de carregamento de url/conteúdo dinâmico.

<br>

## Etapas do projeto

### Primeira etapa

- Crawl urls pokemons:

Todos o pokemons estão listados nesta página, www.smogon.com/dex/rs/pokemon/ , o qual exige que a página toda seja
scrollada, para gerar todo conteúdo disponível.
Após scrollar a página toda, a spider smogon_crawl irá adquirir todas as urls, que serão salvas e passadas para o segundo parser.
 
### Segunda Etapa

- Crawl informações de cada pokemon

O segundo parser, irá abrir uma pagína no google chrome, em modo headless, de cada url crawleada na etapa 1.
Após isso, as informações de cada pokemon serão salvas no formato escolhido. 
No caso, ao chamar a spider, escolhi o output no formato .json<br>
<br><br>
As informações crawleadas, estão disponibilizadas no .json de nome pokemons.json ("smogon/pokemons.json").

### Terceira Etapa

- Crawl informações de todos os golpes disponíveis, na url www.smogon.com/dex/rs/moves/

A spider crawlmoves, irá abrir esta url em uma guia no chrome, e irá efetuar a rolagem da página, do topo, ao final da página, 
adquirindo as informações dispostas na tela.
As informações crawleadas desta url, estão disponíveis no .json de nome moves.json ("smogon/moves.json").

### Quarta Etapa

- Crawl informações de todos as habilidade disponíveis, na url www.smogon.com/dex/rs/abilities/

A spider crawlabilities, irá abrir esta url em uma guia no chrome, e irá efetuar a rolagem da página, do topo, ao final da página, 
adquirindo as informações dispostas na tela.
As informações crawleadas desta url, estão disponíveis no .json de nome moves.json ("smogon/abilities.json").
