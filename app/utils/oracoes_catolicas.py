"""Biblioteca de orações católicas para uso no Apostolado."""
from __future__ import annotations

from typing import TypedDict


class Oracao(TypedDict):
    id: str
    titulo: str
    categoria: str
    texto: str
    tags: list[str]


def _o(oid: str, titulo: str, categoria: str, texto: str, *tags: str) -> Oracao:
    return {
        "id": oid,
        "titulo": titulo,
        "categoria": categoria,
        "texto": texto.strip(),
        "tags": list(tags),
    }


ORACOES: list[Oracao] = [
    _o(
        "rosario_tomista",
        "Santo Rosário — método tomista (mente, corpo, alma e espírito)",
        "Santo Rosário",
        """
**Como Santo Tomás de Aquino compreende o homem em oração**

Na tradição tomista, **não confundimos “alma” com “espírito”**:
- **Alma** (anima): princípio de vida; alma racional com **inteligência e vontade**, e potências **sensitivas** (imaginação, memória, afeto).
- **Espírito**: aqui designamos a **ação do Espírito Santo** sobre inteligência e vontade (dons, inspiração, elevatio ad Deum) — não é “outra alma”, mas **Deus que eleva** a alma.

Assim rezamos o Rosário **exercitando**:

| Dimensão | O que exercitar | Como no terço |
|----------|-----------------|---------------|
| **Mente** (intelecto) | Meditar os mistérios de Cristo e da Virgem | Antes de cada dezena: ler o mistério e **parar** 30–60 s em silêncio |
| **Corpo** | Reverência, disciplina, presença | Sinal da cruz, genuflexão ao iniciar, contas nos dedos, postura recolhida |
| **Alma** (sentidos e afeto) | Imaginação e coração no Evangelho | Visualizar a cena; oferecer intenções; sentir gratidão, compaixão, confiança |
| **Espírito** (Espírito Santo) | Pedir luz e amor sobrenatural | Invocar o Espírito Santo; pedir um **dom** (sabedoria, fortaleza…) a cada mistério |

---

### Preparação (corpo e espírito)

**Sinal da cruz**  
Em nome do Pai, e do Filho, e do Espírito Santo. Amém.

**Invocação ao Espírito Santo**  
Vinde, Espírito Santo, enchei os corações dos vossos fiéis e acendei neles o fogo do vosso amor. Enviai o vosso Espírito e tudo será criado, e renovareis a face da terra.  
*Oremos:* Deus, que instruístes os corações dos vossos fiéis com a luz do Espírito Santo, fazei que apreciemos retamente todas as coisas segundo o mesmo Espírito, e gozemos sempre da sua consolação. Por Cristo, Senhor nosso. Amém.

**Oferecimento**  
Ofereço-Vos, Senhor, este terço em honra da Santíssima Trindade, pelas intenções do Santo Padre, pela Igreja, pelas almas e pelas minhas necessidades.

---

### Abertura do terço

**Credo dos Apóstolos** (dias dominicais e solenes)  
Creio em Deus Pai todo-poderoso, Criador do céu e da terra. E em Jesus Cristo, seu único Filho, nosso Senhor, que foi concebido pelo Espírito Santo, nasceu da Virgem Maria, padeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado. Desceu à mansão dos mortos, ressuscitou ao terceiro dia, subiu aos céus, está sentado à direita de Deus Pai todo-poderoso, donde há de vir a julgar os vivos e os mortos. Creio no Espírito Santo, na santa Igreja Católica, na comunhão dos santos, na remissão dos pecados, na ressurreição da carne e na vida eterna. Amém.

**Pai-Nosso** (1×)  
Pai-Nosso que estais nos céus, santificado seja o vosso nome; venha a nós o vosso reino; seja feita a vossa vontade, assim na terra como no céu. O pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém.

**Três Ave-Marias** (fé, esperança e caridade)  
Rezar meditando: **fé** no primeiro, **esperança** no segundo, **caridade** no terceiro.

---

### Meditação de cada mistério (mente + alma + espírito)

Para **cada** dos 5 mistérios do dia:
1. **Anunciar** o mistério e o **fruto** (ex.: “Anunciação — humildade”).
2. **Meditar** em silêncio (mente e imaginação).
3. **Pedir** ao Espírito Santo um dom concreto (espírito).
4. **Pai-Nosso** (1×), **Ave-Maria** (10×), **Glória** (1×).
5. Opcional: *“Ó meu Jesus, perdoai-nos, livrai-nos do fogo do inferno…”*

**Glória ao Pai**  
Glória ao Pai, e ao Filho, e ao Espírito Santo. Como era no princípio, agora e sempre. Amém.

**Ave-Maria**  
Ave, Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. Santa Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora da nossa morte. Amém.

---

### Mistérios da semana

**Segunda e sábado — Gozosos:** Anunciação; Visitação; Nascimento; Apresentação no Templo; Perdido e encontrado no Templo.

**Terça e sexta — Dolorosos:** Agonia no Horto; Flagelação; Coroação de espinhos; Carregamento da cruz; Crucifixão.

**Quarta e domingo — Gloriosos:** Ressurreição; Ascensão; Descida do Espírito Santo; Assunção; Coroação de Maria.

**Quinta — Luminosos:** Batismo no Jordão; Bodas de Caná; Anúncio do Reino; Transfiguração; Instituição da Eucaristia.

---

### Conclusão

**Salve-Rainha**  
Salve, Rainha, Mãe de misericórdia, vida, doçura e esperança nossa, salve! A vós bradamos, os degredados filhos de Eva; a vós suspiramos, gemendo e chorando neste vale de lágrimas. Eia, pois, advogada nossa, esses vossos olhos misericordiosos a nós volvei; e, depois deste desterro, mostrai-nos Jesus, bendito fruto do vosso ventre. Ó clemente, ó piedosa, ó doce Virgem Maria!

**Oração final (São Bernardo ou tradicional)**  
Ó Deus, cujo Filho Unigênito, pela vida, morte e ressurreição, nos mereceu o prêmio da salvação eterna, concedei-nos que, meditando estes mistérios do Santíssimo Rosário da bem-aventurada Virgem Maria, imitemos o que contêm e alcancemos o que prometem. Por Cristo, Senhor nosso. Amém.

**Sinal da cruz**
""",
        "rosario",
        "tomás",
        "aquino",
        "terço",
    ),
    _o(
        "ladainha_humildade",
        "Ladainha da Humildade",
        "Ladainhas",
        """
**Ladainha da Humildade**  
*(atribuída ao Cardeal Merry del Val)*

Senhor, tende piedade de nós.  
Cristo, tende piedade de nós.  
Senhor, tende piedade de nós.

Cristo, ouvi-nos.  
Cristo, atendei-nós.

Deus Pai do céu, tende piedade de nós.  
Deus Filho, Redentor do mundo, tende piedade de nós.  
Deus Espírito Santo, tende piedade de nós.  
Santíssima Trindade, que sois um só Deus, tende piedade de nós.

**Invocações** *(responder: “concedei-me” ou “ouvi-me”)*

Jesus, manso e humilde de coração, ouvi-me.  
Jesus, manso e humilde de coração, ouve-me.  
Jesus, manso e humilde de coração, atende-me.  
Jesus, manso e humilde de coração, concedei-me a graça de desejar ardentemente as coisas celestes.  
Jesus, manso e humilde de coração, concedei-me a graça de desprezar as terrestres.  
Jesus, manso e humilde de coração, concedei-me a graça de não me preocupar com o amor-próprio.  
Jesus, manso e humilde de coração, concedei-me a graça de não desejar ostentação.  
Jesus, manso e humilde de coração, concedei-me a graça de procurar sinceramente a humildade.  
Jesus, manso e humilde de coração, concedei-me a graça de submeter-me às vontades alheias.  
Jesus, manso e humilde de coração, concedei-me a graça de suportar com mansidão os contrários.  
Jesus, manso e humilde de coração, concedei-me a graça de não discutir sem necessidade.  
Jesus, manso e humilde de coração, concedei-me a graça de não inquietar-me por contradições.  
Jesus, manso e humilde de coração, concedei-me a graça de não me entristecer por ingratidões.  
Jesus, manso e humilde de coração, concedei-me a graça de aceitar com alegria humilhações.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na mansidão.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na humildade.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na paciência.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na obediência.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na caridade.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na simplicidade.  
Jesus, manso e humilde de coração, concedei-me a graça de imitar-Vos na pureza de intenção.  
Jesus, manso e humilde de coração, concedei-me a graça de amar-Vos sobre todas as coisas.  
Jesus, manso e humilde de coração, concedei-me a graça de confiar plenamente em Vós.

**Oração final**

Ó Jesus, manso e humilde de coração, ouvi-me.  
Ó Jesus, manso e humilde de coração, ouve-me.  
Ó Jesus, manso e humilde de coração, atende-me.  
Ó Jesus, manso e humilde de coração, concedei-me a graça de procurar a humildade e a mansidão que Vos agradam, para imitar-Vos até a morte e alcançar a glória eterna convosco. Amém.
""",
        "humildade",
        "ladainha",
    ),
    _o(
        "oferecimento_ao",
        "Oferecimento diário ao Sagrado Coração (Apostolado da Oração)",
        "Apostolado / Sagrado Coração",
        """
**Oferecimento ao Sagrado Coração de Jesus** *(rezar diariamente)*

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro dos meus males escondidos,*
*dentro das minhas inquietações, dentro dos meus limites, dentro da minha fragilidade,*
*na minha aflição e no meu cansaço: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro das minhas necessidades,*
*dentro dos meus esforços, dentro das minhas lutas, dentro dos meus desejos de bem,*
*na minha solidão e na minha angústia: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro dos meus projetos,*
*dentro dos meus trabalhos, dentro dos meus sonhos, dentro dos meus anseios,*
*na minha tristeza e na minha dor: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. E, se me for possível, alivia o meu sofrimento;*
*se não, dá-me resignação. Concede-me uma fé viva, uma esperança firme e um amor ardente a Ti.*
*Faze com que eu repita sempre: **Jesus, eu confio em Vós!***
""",
        "apostolado",
        "sagrado coração",
    ),
    _o(
        "pai_nosso",
        "Pai-Nosso (Nossa Senhora)",
        "Orações básicas",
        """
Pai-Nosso que estais nos céus, santificado seja o vosso nome; venha a nós o vosso reino; seja feita a vossa vontade, assim na terra como no céu. O pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém.
""",
        "nossa senhora",
    ),
    _o(
        "ave_maria",
        "Ave-Maria",
        "Orações básicas",
        """
Ave, Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. Santa Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora da nossa morte. Amém.
""",
        "maria",
    ),
    _o(
        "gloria",
        "Glória ao Pai",
        "Orações básicas",
        """
Glória ao Pai, e ao Filho, e ao Espírito Santo. Como era no princípio, agora e sempre. Amém.
""",
    ),
    _o(
        "credo_apostolos",
        "Credo dos Apóstolos",
        "Orações básicas",
        """
Creio em Deus Pai todo-poderoso, Criador do céu e da terra. E em Jesus Cristo, seu único Filho, nosso Senhor, que foi concebido pelo Espírito Santo, nasceu da Virgem Maria, padeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado. Desceu à mansão dos mortos, ressuscitou ao terceiro dia, subiu aos céus, está sentado à direita de Deus Pai todo-poderoso, donde há de vir a julgar os vivos e os mortos. Creio no Espírito Santo, na santa Igreja Católica, na comunhão dos santos, na remissão dos pecados, na ressurreição da carne e na vida eterna. Amém.
""",
        "credo",
    ),
    _o(
        "credo_niceno",
        "Credo de Nicéia-Constantinopla (resumo litúrgico)",
        "Orações básicas",
        """
Creio em um só Deus, Pai todo-poderoso, Criador do céu e da terra, de tudo o que se vê e se não vê. E em um só Senhor, Jesus Cristo, Filho Unigênito de Deus, nascido do Pai antes de todos os séculos: Deus de Deus, Luz da Luz, Deus verdadeiro de Deus verdadeiro, gerado, não criado, consubstancial ao Pai. Por ele todas as coisas foram feitas. Por nós, homens, e para nossa salvação, desceu dos céus e se encarnou pelo Espírito Santo, no seio da Virgem Maria, e se fez homem. Foi crucificado também por nós; sofreu sob Pôncio Pilatos, foi sepultado e ressuscitou ao terceiro dia, conforme as Escrituras. Subiu aos céus, está sentado à direita do Pai e de novo há de vir, em sua glória, para julgar os vivos e os mortos; e o seu Reino não terá fim. Creio no Espírito Santo, Senhor que dá a vida, e procede do Pai e do Filho; com o Pai e o Filho é adorado e glorificado; falou pelos profetas. Creio na Igreja, una, santa, católica e apostólica. Professo um só batismo para remissão dos pecados. E espero a ressurreição dos mortos e a vida do mundo que há de vir. Amém.
""",
    ),
    _o(
        "salve_rainha",
        "Salve-Rainha",
        "Nossa Senhora",
        """
Salve, Rainha, Mãe de misericórdia, vida, doçura e esperança nossa, salve! A vós bradamos, os degredados filhos de Eva; a vós suspiramos, gemendo e chorando neste vale de lágrimas. Eia, pois, advogada nossa, esses vossos olhos misericordiosos a nós volvei; e, depois deste desterro, mostrai-nos Jesus, bendito fruto do vosso ventre. Ó clemente, ó piedosa, ó doce Virgem Maria!
""",
        "maria",
    ),
    _o(
        "memorare",
        "Memorare (a Nossa Senhora)",
        "Nossa Senhora",
        """
Memorare, ó piíssima Virgem Maria, que nunca se ouviu dizer que algum daqueles que a vós recorreram, invocaram vosso auxílio e imploraram vossa proteção fosse por vós desamparado. Animado com esta confiança, a vós recorro, ó Mãe, Virgem das virgens; a vós venho, diante de vós me prostro, gemendo e chorando. Não desprezeis as minhas súplicas, ó advogada dos necessitados, mas dignai-vos de ouvi-las propícia e de me alcançar o que vos rogo. Amém.
""",
    ),
    _o(
        "angelus",
        "Angelus",
        "Nossa Senhora",
        """
*(Três vezes ao dia: 6h, 12h, 18h — a campainha do Angelus)*

**V.** O Anjo do Senhor anunciou a Maria.  
**R.** E ela concebeu do Espírito Santo.

Ave, Maria…

**V.** Eis aqui a serva do Senhor.  
**R.** Faça-se em mim segundo a vossa palavra.

Ave, Maria…

**V.** E o Verbo se fez carne.  
**R.** E habitou entre nós.

Ave, Maria…

**V.** Rogai por nós, Santa Mãe de Deus.  
**R.** Para que sejamos dignos das promessas de Cristo.

**Oremos:** Infundi, Senhor, a vossa graça em nossos corações, para que, conhecendo pela anunciação do Anjo a encarnação de Cristo, vosso Filho, cheguemos, pela sua paixão e cruz, à glória da ressurreição. Por Cristo, Senhor nosso. Amém.
""",
        "maria",
    ),
    _o(
        "regina_caeli",
        "Regina Caeli (tempo pascal)",
        "Nossa Senhora",
        """
**V.** Regina caeli, laetare, alleluia!  
**R.** Quia quem meruisti portare, alleluia!

**V.** Resurrexit, sicut dixit, alleluia!  
**R.** Ora pro nobis Deum, alleluia!

**V.** Gaude et laetare, Virgo Maria, alleluia!  
**R.** Quia surrexit Dominus vere, alleluia!

**Oremos:** Deus, que pela ressurreição do vosso Filho, Senhor nosso, nos alegrastes, concedei-nos, pela intercessão da sua Mãe, a Virgem Maria, alcançar a alegria da vida eterna. Por Cristo, Senhor nosso. Amém.
""",
    ),
    _o(
        "ladainha_loreto",
        "Ladainha de Nossa Senhora (de Loreto)",
        "Ladainhas",
        """
Senhor, tende piedade de nós.  
Cristo, tende piedade de nós.  
Senhor, tende piedade de nós.

*(Invocações — responder: “Rogai por nós”)*

Santa Maria, rogai por nós.  
Santa Mãe de Deus, rogai por nós.  
Santa Virgem das virgens, rogai por nós.  
Mãe de Cristo, rogai por nós.  
Mãe da Igreja, rogai por nós.  
Mãe da divina graça, rogai por nós.  
Mãe puríssima, rogai por nós.  
Mãe castíssima, rogai por nós.  
Mãe sempre virgem, rogai por nós.  
Mãe imaculada, rogai por nós.  
Mãe amabilíssima, rogai por nós.  
Mãe admirável, rogai por nós.  
Mãe do bom conselho, rogai por nós.  
Mãe do Criador, rogai por nós.  
Mãe do Salvador, rogai por nós.  
Virgem prudentíssima, rogai por nós.  
Virgem venerável, rogai por nós.  
Virgem louvável, rogai por nós.  
Virgem poderosa, rogai por nós.  
Virgem clemente, rogai por nós.  
Virgem fiel, rogai por nós.  
Espelho de justiça, rogai por nós.  
Sede da sabedoria, rogai por nós.  
Causa da nossa alegria, rogai por nós.  
Vaso espiritual, rogai por nós.  
Vaso honorífico, rogai por nós.  
Vaso insigne de devoção, rogai por nós.  
Rosa mística, rogai por nós.  
Torre de Davi, rogai por nós.  
Torre de marfim, rogai por nós.  
Casa de ouro, rogai por nós.  
Arca da aliança, rogai por nós.  
Porta do céu, rogai por nós.  
Estrela da manhã, rogai por nós.  
Saúde dos enfermos, rogai por nós.  
Refúgio dos pecadores, rogai por nós.  
Consoladora dos aflitos, rogai por nós.  
Auxílio dos cristãos, rogai por nós.  
Rainha dos anjos, rogai por nós.  
Rainha dos patriarcas, rogai por nós.  
Rainha dos profetas, rogai por nós.  
Rainha dos apóstolos, rogai por nós.  
Rainha dos mártires, rogai por nós.  
Rainha dos confessores, rogai por nós.  
Rainha das virgens, rogai por nós.  
Rainha de todos os santos, rogai por nós.  
Rainha concebida sem pecado original, rogai por nós.  
Rainha assunta ao céu, rogai por nós.  
Rainha do santo rosário, rogai por nós.  
Rainha da paz, rogai por nós.

**Cordeiro de Deus**  
Cordeiro de Deus, que tirais o pecado do mundo, perdoai-nos, Senhor.  
Cordeiro de Deus, que tirais o pecado do mundo, ouvi-nos, Senhor.  
Cordeiro de Deus, que tirais o pecado do mundo, tende piedade de nós.

**Oração final**  
Concedei-nos, Senhor, a graça de Vossa proteção, para que, imitando a bem-aventurada Virgem Maria, possamos chegar à glória eterna. Por Cristo, Senhor nosso. Amém.
""",
        "maria",
        "ladainha",
    ),
    _o(
        "ladainha_sagrado_coracao",
        "Ladainha do Sagrado Coração de Jesus",
        "Ladainhas",
        """
Senhor, tende piedade de nós.  
Cristo, tende piedade de nós.  
Senhor, tende piedade de nós.

*(Invocações — “Havei piedade de nós”)*

Coração de Jesus, Filho do Pai eterno, havei piedade de nós.  
Coração de Jesus, formado no seio da Virgem Maria, havei piedade de nós.  
Coração de Jesus, substancialmente unido à Palavra divina, havei piedade de nós.  
Coração de Jesus, de majestade infinita, havei piedade de nós.  
Coração de Jesus, santuário divino, havei piedade de nós.  
Coração de Jesus, tabernáculo da justiça e do amor, havei piedade de nós.  
Coração de Jesus, cheio de bondade e de amor, havei piedade de nós.  
Coração de Jesus, abismo de virtudes e de tesouros, havei piedade de nós.  
Coração de Jesus, nosso refúgio e repouso, havei piedade de nós.  
Coração de Jesus, vítima de nossos pecados, havei piedade de nós.  
Coração de Jesus, esmagado por nossas iniquidades, havei piedade de nós.  
Coração de Jesus, obediente até a morte, havei piedade de nós.  
Coração de Jesus, lança do soldado transpassado, havei piedade de nós.  
Coração de Jesus, fonte de toda consolação, havei piedade de nós.  
Coração de Jesus, vida e ressurreição nossa, havei piedade de nós.  
Coração de Jesus, paz e reconciliação nossa, havei piedade de nós.  
Coração de Jesus, vítima por nossos pecados, havei piedade de nós.  
Coração de Jesus, salvação dos que em Vós esperam, havei piedade de nós.  
Coração de Jesus, esperança dos que morrem em Vós, havei piedade de nós.  
Coração de Jesus, delícia de todos os santos, havei piedade de nós.

**Cordeiro de Deus** *(como na Ladainha de Loreto)*

**Oração final**  
Deus onipotente e eterno, olhai para o Coração do vosso Filho amado e pelos méritos da paixão que Ele sofreu por nós pecadores, tende piedade de nós e do mundo inteiro. Amém.
""",
        "sagrado coração",
    ),
    _o(
        "ladainha_sao_jose",
        "Ladainha de São José",
        "Ladainhas",
        """
Senhor, tende piedade de nós.  
Cristo, tende piedade de nós.  
Senhor, tende piedade de nós.

*(Invocações — “Rogai por nós”)*

Nobilíssimo descendente de Davi, rogai por nós.  
Luz dos patriarcas, rogai por nós.  
Esposo da Mãe de Deus, rogai por nós.  
Guarda castíssimo da Virgem, rogai por nós.  
Pai putativo do Filho de Deus, rogai por nós.  
Zeloso defensor de Cristo, rogai por nós.  
Servo fiel da santa família, rogai por nós.  
Espelho da paciência, rogai por nós.  
Amante da pobreza, rogai por nós.  
Modelo dos trabalhadores, rogai por nós.  
Glória da vida doméstica, rogai por nós.  
Guarda dos virgens, rogai por nós.  
Amparo das famílias, rogai por nós.  
Consolo dos aflitos, rogai por nós.  
Esperança dos enfermos, rogai por nós.  
Patrono dos moribundos, rogai por nós.  
Terror dos demônios, rogai por nós.  
Protetor da santa Igreja, rogai por nós.

**Cordeiro de Deus** *(como acima)*

**Oração final**  
Concedei-nos, Senhor, a graça de imitar São José na obediência e no trabalho, e de alcançar a felicidade eterna. Por Cristo, Senhor nosso. Amém.
""",
        "são josé",
    ),
    _o(
        "anima_christi",
        "Anima Christi",
        "Eucaristia / Comunhão",
        """
Alma de Cristo, santificai-me.  
Corpo de Cristo, salvai-me.  
Sangue de Cristo, inebriai-me.  
Água do lado de Cristo, lavai-me.  
Paixão de Cristo, confortai-me.  
Ó bom Jesus, ouvi-me.  
Dentro dos vossos flancos, escondei-me.  
Não permitais que me separe de Vós.  
Do mal inimigo, defendei-me.  
Na hora da minha morte, chamai-me.  
E mandai-me ir para Vós, para que com os vossos santos Vos louve por todos os séculos. Amém.
""",
        "comunhão",
    ),
    _o(
        "ato_fe_esperanca_caridade",
        "Atos de fé, esperança e caridade",
        "Actos",
        """
**Ato de fé**  
Meu Deus, creio firmemente que sois um só Deus em três Pessoas: Pai, Filho e Espírito Santo; creio tudo o que a santa Igreja Católica propõe para crermos, porque sois a infalível verdade. Amém.

**Ato de esperança**  
Meu Deus, espero firmemente que me dareis a vida eterna e as graças necessárias para merecê-la, porque sois infinitamente bom e fiel às vossas promessas. Amém.

**Ato de caridade**  
Meu Deus, amo-Vos sobre todas as coisas, de todo o coração, porque sois infinitamente bom e digno de ser amado; e por amor de Vós, amo o próximo como a mim mesmo. Amém.
""",
    ),
    _o(
        "ato_contricao",
        "Ato de contrição",
        "Actos",
        """
Meu Deus, eu me arrependo, de todo o coração, de todos os meus pecados, e os abomino, porque pecando ofendi a Vós, que sois o sumo bem e digno de ser amado sobre todas as coisas. Proponho firmemente, com a vossa graça, nunca mais pecar e fugir das ocasiões próximas de pecado. Senhor, tende piedade de mim, pecador. Amém.
""",
        "confissão",
    ),
    _o(
        "confiteor",
        "Confiteor (Confissão / Missa)",
        "Actos",
        """
Confesso a Deus todo-poderoso, a bem-aventurada sempre Virgem Maria, ao bem-aventurado São Miguel Arcanjo, ao bem-aventurado São João Batista, aos santos Apóstolos Pedro e Paulo, a todos os santos, e a vós, irmãos, que pequei muitas vezes por pensamentos e palavras, por obras e omissões. Por minha culpa, minha culpa, minha tão grande culpa. Por isso peço à bem-aventurada sempre Virgem Maria, a São Miguel Arcanjo, a São João Batista, aos santos Apóstolos Pedro e Paulo, a todos os santos, e a vós, irmãos, que rogueis por mim a Deus, nosso Senhor.
""",
    ),
    _o(
        "oracao_sao_tomas_comunhao",
        "Oração de Santo Tomás de Aquino (antes da Comunhão)",
        "Santo Tomás de Aquino",
        """
Alma de Cristo, santificai-me. Corpo de Cristo, salvai-me. Sangue de Cristo, inebriai-me. Água do lado de Cristo, lavai-me. Paixão de Cristo, fortalecei-me. Ó bom Jesus, ouvi-me. Escondi-me dentro do vosso Coração. Nunca permitais que eu me separe de Vós. Do inimigo maligno, defendei-me. Na hora da minha morte, chamai-me. Mandai-me ir para Vós, para que com os vossos santos Vos louve por todos os séculos. Amém.

**Adó-te, ó Deus** *(após a Comunhão)*  
Adó-te, ó Deus, escondido debaixo destas aparências, verdadeiramente presente aqui. A Vós seja dada toda a honra e glória. Creio firmemente, Senhor, que sois presente no Sacramento do altar. Amém.
""",
        "tomás",
        "eucaristia",
    ),
    _o(
        "oracao_sao_tomas_estudo",
        "Oração de Santo Tomás (antes do estudo ou trabalho)",
        "Santo Tomás de Aquino",
        """
Concedei-me, ó Deus onipotente, compreender com clareza, interpretar com retidão, falar com eloquência e praticar com perfeição o que é do vosso agrado, para honra e glória do vosso nome. Amém.

**Outra (breve):**  
Veni, Sancte Spiritus, reple tuorum corda fidelium, et tui amoris in eis ignem accende. *(Vinde, Espírito Santo, enchei os corações dos vossos fiéis e acendei neles o fogo do vosso amor.)*
""",
        "tomás",
    ),
    _o(
        "veni_creator",
        "Veni Creator (Vinde, Espírito Criador)",
        "Espírito Santo",
        """
Vinde, Espírito Criador, visitai as almas dos vossos filhos; enchei de celeste vigor os corações que criastes.

Vós, chamado Paráclito, dom da glória do Altíssimo, fonte viva, fogo, caridade e espiritual unção.

Vós sois o doador dos sete dons; sois a mão, o dedo do Pai; sois o prometido do Pai, que derramais sobre nós a palavra.

Acendei a luz dos sentidos; infundi o amor no peito; sustentai com vossa força infirma a nossa carne.

Repeli de nossas almas o inimigo; dai-nos a paz; sendo vós nosso guia, evitaremos todo mal.

Por vós conheceremos o Pai; conheceremos também o Filho; e vós, de ambos procedendo, nos dareis a conhecer cada vez mais.

A vós louvores ao Pai e ao Filho, e ao Espírito Paráclito; a vós, ó Trindade santa, agora e por todos os séculos. Amém.
""",
    ),
    _o(
        "oracao_fatima",
        "Oração de Fátima (após cada mistério)",
        "Santo Rosário",
        """
Ó meu Jesus, perdoai-nos, livrai-nos do fogo do inferno, levai as almas todas para o céu, especialmente as que mais precisarem.
""",
        "rosário",
        "fátima",
    ),
    _o(
        "terco_misericordia",
        "Terço da Divina Misericórdia",
        "Santo Rosário",
        """
**Início:** Pai-Nosso, Ave-Maria, Credo.

**Nas contas grandes:** “Eterno Pai, eu Vos ofereço o Corpo e Sangue, Alma e Divindade de vosso diletíssimo Filho, Nosso Senhor Jesus Cristo, em expiação dos nossos pecados e do mundo inteiro.”

**Nas dezenas (10×):** “Pela sua dolorosa Paixão, tende misericórdia de nós e do mundo inteiro.”

**Ao final (3×):** “Deus Santo, Deus Forte, Deus Imortal, tende piedade de nós e do mundo inteiro.”

**Oração final:**  
Deus eterno, em quem a misericórdia é infinita e o tesouro de compaixão inesgotável, eu Vos suplico, pelo Coração doloroso de vosso Filho, pelos seus sofrimentos, tende misericórdia de nós e do mundo inteiro. Amém.
""",
        "misericórdia",
    ),
    _o(
        "oracao_sao_miguel",
        "Oração a São Miguel Arcanjo",
        "Santos",
        """
São Miguel Arcanjo, defendei-nos no combate; sede o nosso auxílio contra as maldades e ciladas do demônio. Ordene-lhe Deus, instantemente o pedimos, e vós, príncipe da milícia celeste, pela virtude divina, precipitai no inferno a Satanás e aos outros espíritos malignos que andam pelo mundo para perder as almas. Amém.
""",
    ),
    _o(
        "oracao_sao_francisco",
        "Oração de São Francisco de Assis (paz)",
        "Santos",
        """
Senhor, fazei de mim um instrumento da vossa paz. Onde houver ódio, que eu leve o amor; onde houver ofensa, que eu leve o perdão; onde houver discórdia, que eu leve a união; onde houver dúvida, que eu leve a fé; onde houver erro, que eu leve a verdade; onde houver desespero, que eu leve a esperança; onde houver tristeza, que eu leve a alegria; onde houver trevas, que eu leve a luz.

Ó Mestre, fazei que eu procure mais consolar do que ser consolado; compreender do que ser compreendido; amar do que ser amado. Pois é dando que se recebe, é perdoando que se é perdoado, e é morrendo que se vive para a vida eterna. Amém.
""",
    ),
    _o(
        "magnificat",
        "Magnificat (cântico de Maria)",
        "Nossa Senhora",
        """
A minha alma glorifica o Senhor, e o meu espírito exulta em Deus, meu Salvador, porque olhou para a humildade de sua serva. Doravante todas as gerações me chamarão bem-aventurada, porque o Poderoso fez em mim maravilhas. Santo é o seu nome; sua misericórdia se estende de geração em geração sobre os que o temem. Manifestou a força do seu braço e dispersou os soberbos; derrubou os poderosos de seus tronos e exaltou os humildes. Encheu de bens os famintos e despediu os ricos de mãos vazias. Socorreu Israel, seu servo, lembrando-se de sua misericórdia, conforme prometera a nossos pais, a Abraão e à sua descendência, para sempre. Amém.
""",
    ),
    _o(
        "consagracao_sagrado_coracao",
        "Consagração ao Sagrado Coração de Jesus (breve)",
        "Apostolado / Sagrado Coração",
        """
Ó Sagrado Coração de Jesus, eu me consagro inteiramente a Vós, e Vos entrego minha alma, minha vida, minhas obras e minhas famílias. Reinai sobre nós, fazei de nós apóstolos do vosso amor, e concedei-nos a graça de viver e morrer como filhos do vosso Coração. Maria, Mãe do Apostolado, rogai por nós. Amém.
""",
        "apostolado",
    ),
    _o(
        "consagracao_imaculada",
        "Consagração à Imaculada (São Luís de Montfort — forma breve)",
        "Nossa Senhora",
        """
Ó Imaculada Conceição, eu me consagro inteiramente a vós, e entrego-vos minha alma, meu corpo, minhas ações e toda a minha vida. Sede minha Mãe e minha Rainha; conduzi-me a Jesus, vosso Filho amado. Amém.
""",
    ),
    _o(
        "jaculatorias",
        "Jaculatórias (orações breves do dia)",
        "Orações do dia",
        """
**Manhã**  
Senhor, abençoai o meu dia.  
Jesus, eu confio em Vós!  
Maria, Mãe minha, guardai-me.

**Durante o dia**  
Meu Deus e meu tudo!  
Jesus, manso e humilde de coração, fazei o meu coração semelhante ao vosso.  
Espírito Santo, vinde!

**Tentações**  
Em nome de Jesus, afastai-vos!  
Maria, auxílio dos cristãos, rogai por nós!

**Noite**  
Into thy hands, O Lord — *Nas vossas mãos, Senhor, entrego o meu espírito.*  
Nossa Senhora, rogai por nós que recorremos a vós.
""",
        "breves",
    ),
    _o(
        "via_crucis_breve",
        "Via-Sacra — meditação das 14 estações",
        "Quaresma / Paixão",
        """
Rezar diante de cada estação: **“V. Nós Vos adoramos, Cristo, e Vos bendizemos. R. Porque pela vossa santa Cruz redimistes o mundo.”**  
Depois: **Pai-Nosso, Ave-Maria, Glória.**

1. Jesus é condenado à morte.  
2. Jesus carrega a cruz.  
3. Jesus cai pela primeira vez.  
4. Jesus encontra sua Mãe.  
5. Simão de Cirene ajuda Jesus a carregar a cruz.  
6. Verônica enxuga o rosto de Jesus.  
7. Jesus cai pela segunda vez.  
8. Jesus consola as filhas de Jerusalém.  
9. Jesus cai pela terceira vez.  
10. Jesus é despojado de suas vestes.  
11. Jesus é crucificado.  
12. Jesus morre na cruz.  
13. Jesus é descido da cruz e entregue a Maria.  
14. Jesus é sepultado.

**Oração final:**  
Senhor Jesus Cristo, que por amor a nós padecestes caminho da cruz até a morte, concedei-nos a graça de imitar vosso amor e chegar à glória da ressurreição. Amém.
""",
        "paixão",
    ),
    _o(
        "terco_sao_jose",
        "Terço de São José (7 domingos)",
        "Santo Rosário",
        """
Medita-se **7 domingos** sobre **7 agonia/sorrows/joys** de São José (tradição popular), com **1 Pai-Nosso e 7 Ave-Marias** em cada meditação, terminando com **Glória** e invocação:

**São José, rogai por nós.**  
**São José, modelo de obediência, rogai por nós.**  
**São José, guarda de Jesus e Maria, rogai por nós.**

*(Adaptar meditações conforme folheto paroquial ou Manual do Apostolado.)*
""",
        "são josé",
    ),
    _o(
        "oracao_antes_miss",
        "Oração antes da Santa Missa",
        "Missal / Liturgia",
        """
Senhor, purificai o meu coração e preparai a minha alma para participar dignamente do sacrifício eucarístico. Uniai as minhas intenções ao vosso Coração e concedei-me a graça de receber-Vos com fé viva e amor ardente. Amém.
""",
    ),
    _o(
        "oracao_depois_miss",
        "Ação de graças após a Comunhão",
        "Missal / Liturgia",
        """
Dou-Vos graças, Senhor, santo Pai, Deus eterno e todo-poderoso, porque me fizestes participar deste banquete celeste. Fazei que este sacramento não seja para o meu juízo, mas para remissão dos pecados, fortaleza da alma e união com vós. Amém.
""",
    ),
    _o(
        "te_deum",
        "Te Deum (A Vós, ó Deus) — início",
        "Louvor",
        """
A Vós, ó Deus, louvamos; a Vós, Senhor, cantamos. A vós, Eterno Pai, adora toda a terra. A Vós todos os anjos, a Vós os céus e todas as potestades. A Vós querubins e serafins clamam sem cessar: Santo, Santo, Santo, Senhor, Deus do universo! Os céus e a terra proclamam a vossa glória. A Vós, glorioso Apostolado. A Vós, louvor digno do vosso nome…

*(Continuação completa no Missal ou Breviário.)*
""",
    ),
    _o(
        "oracao_papa",
        "Oração pelas intenções do Papa",
        "Apostolado / Sagrado Coração",
        """
Ó Maria, Mãe do Apostolado, rogai por nós e pelas intenções do Santo Padre [nome do Papa], para que a Igreja seja santa e missionária, e o Reino de Cristo se estenda sobre a terra. Amém.
""",
        "papa",
    ),
    _o(
        "oracao_almas",
        "Oração pelas almas do Purgatório",
        "Orações do dia",
        """
Eterno Pai, eu Vos ofereço o Corpo e Sangue, Alma e Divindade de vosso diletíssimo Filho, Nosso Senhor Jesus Cristo, em suffragio das almas do Purgatório, especialmente [nome], e de todas as que mais precisam. Amém.

**Eterno descanso:**  
V. Eterno descanso dai-lhes, Senhor.  
R. E a luz perpetua lhes brilhe.  
V. Descansem em paz.  
R. Amém.
""",
        "finados",
    ),
    _o(
        "oracao_familia",
        "Oração pela família (Apostolado)",
        "Orações do dia",
        """
Senhor Jesus, consagrai a nossa família ao vosso Sagrado Coração e ao Coração Imaculado de Maria. Sede o centro da nossa casa, a paz entre nós e o modelo de nossas vidas. Protegei nossos filhos, nossos idosos e todos os que sofrem. Amém.
""",
        "família",
    ),
]


def listar_categorias() -> list[str]:
    cats = sorted({o["categoria"] for o in ORACOES})
    return cats


def buscar_oracoes(texto: str = "", categoria: str = "Todas") -> list[Oracao]:
    q = (texto or "").strip().lower()
    out: list[Oracao] = []
    for o in ORACOES:
        if categoria != "Todas" and o["categoria"] != categoria:
            continue
        if q:
            blob = " ".join(
                [o["titulo"], o["categoria"], o["texto"], " ".join(o["tags"])]
            ).lower()
            if q not in blob:
                continue
        out.append(o)
    return out


def obter_oracao(oid: str) -> Oracao | None:
    for o in ORACOES:
        if o["id"] == oid:
            return o
    return None
