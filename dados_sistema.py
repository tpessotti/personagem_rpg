from collections import defaultdict

class DadosSistema:
    def __init__(self):
        # ====== Atributos Base ======
        self.atributos_base = ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]

        self.bonus_proficiencia_por_nivel = {
            1: 2, 2: 2, 3: 2, 4: 2,
            5: 3, 6: 3, 7: 3, 8: 3,
            9: 4, 10: 4
        }

        # ====== Classes Disponíveis ======
        self.classes_disponiveis = [
            "Marujo", "Duelista", "Explorador", "Charlatão",
            "Médico", "Sacerdote", "Sabotador", "Erudito"
        ]

        # ====== Especializações por Classe ======
        self.especializacoes_por_classe = {
            "Marujo": ["Piloto", "Corsário", "Contrabandista"],
            "Duelista": ["Mosqueteiro", "Espadachim", "Brigão"],
            "Explorador": ["Batedor", "Caçador de Relíquias", "Montanhista"],
            "Charlatão": ["Hipnotizador", "Dissimulado", "Língua Afiada"],
            "Médico": ["Cirurgião de Navio", "Erudito Naturalista", "Médico de Guerra"],
            "Sacerdote": ["Orador Visionário", "Manipulador Místico", "Cultista Oculto"],
            "Sabotador": ["Demolidor", "Espião", "Assassino Urbano"],
            "Erudito": ["Cartógrafo", "Alquimista", "Engenheiro"]
        }

        self.descricao_classes = {
            "Marujo": {
                1: "Início da carreira marítima, o Marujo domina noções básicas de navegação, lida com tarefas de bordo e aprende a sobreviver no ambiente naval.",
                2: "Aprofunda sua habilidade em Combate Naval e Vida no Mar, desenvolvendo maior resistência e adaptabilidade às rotinas duras do convés.",
                3: "Alcança um patamar de experiência em alto-mar (Aviso: escolha ou atualize sua Especialização). As habilidades iniciais de resistência e pilotagem mostram seu potencial.",
                4: "Refina táticas de abordagem, aprimorando manobras e rapidez nos comandos do navio, mantendo firmeza em tempestades e conflitos.",
                5: "Amplia sua compreensão de rotas e marés (Aviso: escolha ou atualize sua Especialização), tornando-se uma presença confiável em qualquer tripulação.",
                6: "Desenvolve técnicas avançadas de manutenção do navio e coordenação de tripulação, reduzindo falhas e imprevistos a bordo.",
                7: "A vivência em múltiplas expedições (Aviso: escolha ou atualize sua Especialização) confere maior autoridade e domínio nas decisões náuticas.",
                8: "Especializa-se ainda mais na coordenação de tripulações, lidando com manobras complexas e ameaças piratas ou corsárias com maior facilidade.",
                9: "Reflete vasta experiência em rotas distantes, ampliando contatos em portos aliados e superando desafios do mar aberto.",
                10: "No ápice da vida marítima (Aviso: escolha ou atualize sua Especialização), o Marujo manifesta supremacia naval, tornando-se referência entre navegadores."
            },

            "Duelista": {
                1: "O Duelista surge como especialista em combate individual, empunhando espada ou pistola com refinamento e honra ou astúcia.",
                2: "Desenvolve reflexos mais rápidos e técnicas de duelo aprimoradas, equilibrando precisão e postura em confronto direto.",
                3: "Reconhecido pela perícia em desafios um contra um (Aviso: escolha ou atualize sua Especialização). Passa a inspirar respeito ou temor.",
                4: "Aprimora etiqueta e combate tático, dominando golpes que exigem coordenação fina e autoconfiança no campo de batalha.",
                5: "Aprofunda-se na arte do duelo (Aviso: escolha ou atualize sua Especialização), combinando técnica, honra ou malícia para vencer oponente.",
                6: "Adquire maestria ao interpretar a postura do adversário, antecipando movimentos e contra-atacando com velocidade mortal.",
                7: "Experimenta novos estilos (Aviso: escolha ou atualize sua Especialização), seja em espadas, pistolas ou táticas mistas, afinando ainda mais reflexos.",
                8: "Refina feints e estocadas com precisão cirúrgica, punindo qualquer brecha na defesa do inimigo.",
                9: "Combina experiência de diversos duelos vencidos, conquistando reputação lendária entre mercenários e nobres.",
                10: "No auge da habilidade (Aviso: escolha ou atualize sua Especialização), o Duelista torna-se referência em combate, raramente encontrando rival à altura."
            },

            "Explorador": {
                1: "O Explorador inicia sua jornada dominando rastreamento, sobrevivência em terrenos hostis e senso de orientação aguçado.",
                2: "Aprimora a capacidade de navegar florestas, montanhas e ruínas, agindo como guia ou batedor experiente.",
                3: "Reconhecido por achar rotas ou trilhas improváveis (Aviso: escolha ou atualize sua Especialização). Prevalece em ambientes perigosos.",
                4: "Torna-se referência ao identificar ameaças naturais, conhecer fauna e flora, e evitar emboscadas inesperadas.",
                5: "Refina instintos de exploração (Aviso: escolha ou atualize sua Especialização), garantindo eficiência em missões de reconhecimento.",
                6: "Melhora a análise de rastros e pegadas, localizando alvos com rapidez ou guiando companheiros em terreno hostil.",
                7: "Desenvolve formas avançadas de lidar com armadilhas, ruínas antigas e obstáculos naturais (Aviso: escolha ou atualize sua Especialização).",
                8: "Aprende atalhos e estratagemas de locomoção, economizando recursos e tempo em expedições longas.",
                9: "Consolida reputação de aventureiro lendário, requisitado para mapear regiões inexploradas ou guardadas por lendas.",
                10: "No ápice da carreira (Aviso: escolha ou atualize sua Especialização), o Explorador descortina os lugares mais inóspitos, superando os piores perigos."
            },

            "Charlatão": {
                1: "O Charlatão surge como mestre da persuasão e do engano, usando palavras suaves ou truques hipnóticos.",
                2: "Aprimora disfarces, manipulação de discursos e leitura das emoções alheias para tirar proveito de situações.",
                3: "Ganha notoriedade na arte do blefe (Aviso: escolha ou atualize sua Especialização). Impacta negociações e intrigas políticas.",
                4: "Combina retórica convincente a ilusões rápidas, confundindo inimigos ou acalmando multidões.",
                5: "Refina a lábia (Aviso: escolha ou atualize sua Especialização), explorando fraquezas psicológicas com maior sofisticação.",
                6: "Interpreta sinais sutis e domina técnicas de enganação complexas, tornando-se adversário temido em conspirações.",
                7: "Adquire renome ou infâmia (Aviso: escolha ou atualize sua Especialização), arquitetando golpes elaborados e fugas inesperadas.",
                8: "Eleva a capacidade de improvisar mentiras plausíveis e manipular testemunhos até mesmo sob forte vigilância.",
                9: "Reconhecido por golpes grandiosos, assume papéis falsos com naturalidade, enganando até os mais cautelosos.",
                10: "Chega ao auge (Aviso: escolha ou atualize sua Especialização), podendo selar tramas de grande escala, moldando rumores e crenças coletivas."
            },

            "Médico": {
                1: "O Médico inicia entendendo anatomia básica, primeiros socorros e uso de ervas curativas.",
                2: "Aprimora diagnóstico, dominando melhores práticas de atendimento em campo de batalha ou ambientes hostis.",
                3: "Reconhecido pela precisão cirúrgica (Aviso: escolha ou atualize sua Especialização). Alivia ferimentos graves em cenários extremos.",
                4: "Especializa-se em tratamentos de emergência, reduzindo tempo de cura e risco de complicações nas expedições.",
                5: "Aprofunda práticas médicas (Aviso: escolha ou atualize sua Especialização), usando alquimia básica ou métodos mais avançados de sutura.",
                6: "Obtém amplo conhecimento de doenças e venenos, desenvolvendo contramedidas e antídotos, mesmo em condições precárias.",
                7: "Adquire fama de salvador (Aviso: escolha ou atualize sua Especialização), curando doenças raras e improváveis ferimentos.",
                8: "Cria técnicas inovadoras de regeneração ou procedimentos cirúrgicos, equiparando a medicina local a padrões elevados.",
                9: "Reconhecido em portos e vilas distantes, é requisitado por governantes e tripulações que buscam cura ou proteção.",
                10: "No ápice da arte médica (Aviso: escolha ou atualize sua Especialização), o Médico domina saberes avançados, tornando-se uma lenda da cura."
            },

            "Sacerdote": {
                1: "O Sacerdote nasce como guia religioso ou espiritual, invocando crenças e rituais simbólicos para inspirar fiéis.",
                2: "Aprimora a Palavra Inspiradora, unificando grupos e infundindo coragem, seja em templos ou campos de batalha.",
                3: "Recebe maior poder e respeito (Aviso: escolha ou atualize sua Especialização), realizando doutrinas ou bênçãos singulares.",
                4: "Expande rituais e cerimônias, confortando aliados e minando adversários por meio da fé ou doutrinas secretas.",
                5: "Aprofunda a conexão espiritual (Aviso: escolha ou atualize sua Especialização), conduzindo multidões ou executando exorcismos.",
                6: "Reforça a influência moral ou manipuladora, dependendo da vertente de crença, moldando crenças populares.",
                7: "Eleva rituais (Aviso: escolha ou atualize sua Especialização), sendo visto como profeta, protetor ou temido líder fanático.",
                8: "Possui um círculo de seguidores fiéis, realizando façanhas que parecem milagres ou temíveis julgamentos divinos.",
                9: "Reflete sabedoria mística, auxiliando alianças poderosas ou abalando estruturas políticas pela força da fé.",
                10: "No ápice do poder (Aviso: escolha ou atualize sua Especialização), o Sacerdote consolida sua doutrina, marcando a história do mundo ao seu redor."
            },

            "Sabotador": {
                1: "O Sabotador começa dominando explosivos e táticas furtivas, servindo a propósitos de espionagem ou demolição.",
                2: "Aprimora técnicas de infiltração, abrindo fechaduras e aprendendo a evadir vigilâncias com maior eficácia.",
                3: "Domina golpes oportunistas (Aviso: escolha ou atualize sua Especialização), executando ataques pontuais e letais.",
                4: "Fica ainda mais versátil em manipular pólvora, engenhocas explosivas e artifícios de distração.",
                5: "Aprofunda planos de sabotagem (Aviso: escolha ou atualize sua Especialização), atuando em missões-chave de espionagem.",
                6: "Torna-se mestre em emboscadas urbanas, usando rotas secretas, disfarces e ataques cirúrgicos.",
                7: "Consolida fama de terror silencioso (Aviso: escolha ou atualize sua Especialização), sendo requisitado ou caçado por facções rivais.",
                8: "Refina trabalho em equipe ou execução solitária, garantindo o sucesso de missões arriscadas mesmo sob pressão extrema.",
                9: "Vence barreiras de segurança complexas e manipula cenários inimagináveis com pequenos dispositivos engenhosos.",
                10: "Alcança o auge do ofício (Aviso: escolha ou atualize sua Especialização), definindo o destino de fortalezas e grandes operações militares."
            },

            "Erudito": {
                1: "O Erudito inicia a carreira como estudioso do mundo, lendo mapas, manuscritos e teorias acadêmicas.",
                2: "Expande o Conhecimento Acadêmico, compreendendo ciências naturais, história e descobertas marítimas.",
                3: "Já é visto como consultor de valor (Aviso: escolha ou atualize sua Especialização), auxiliando em problemas técnicos e enigmas.",
                4: "Domina Ferramentas da Ciência, aplicando experimentos e soluções criativas em cenários diversos.",
                5: "Avança em teorias e práticas (Aviso: escolha ou atualize sua Especialização), criando objetos ou fórmulas científicas avançadas.",
                6: "Explora engenharia, cartografia ou alquimia de modo mais profundo, contribuindo para o avanço das expedições.",
                7: "Constrói reputação intelectual (Aviso: escolha ou atualize sua Especialização), requisitado por autoridades e exploradores.",
                8: "Desenvolve métodos inovadores para resolver problemas náuticos, mecânicos ou químicos, tornando-se um polímata.",
                9: "Especialista em teorias raras e obras antigas, ajuda a decifrar segredos ou artefatos intrigantes.",
                10: "No ápice da erudição (Aviso: escolha ou atualize sua Especialização), o Erudito domina áreas de conhecimento capazes de mudar rumos de nações."
            }}

        self.descricao_especializacoes = {
            "Marujo": {
                "Piloto": {
                3: "Piloto (Marujo) nível 3. Você aprofunda conhecimentos em navegação precisa, dominando manobras para evitar recifes e ler correntes. Fica apto a liderar rotações de turno no leme, transmitindo confiança à tripulação.",
                5: "Piloto (Marujo) nível 5. Avança em técnicas de cartografia simples, traçando rotas otimizadas para reduzir riscos em águas hostis. Habilidade em manobrar grandes velas sob tempestades.",
                7: "Piloto (Marujo) nível 7. Domina pilotagem de embarcações de maior porte, ajustando velas para reagir rapidamente a mudanças de vento e clima. Cria métodos próprios de navegação alternativa.",
                10: "Piloto (Marujo) nível 10. No auge, você praticamente se torna um 'mestre dos mares', fazendo rotas que desafiam a lógica, realizando travessias em tempo recorde e salvando a tripulação de tormentas fatais."
                },
                "Corsário": {
                3: "Corsário (Marujo) nível 3. Aprimora combate naval e treinamento da tripulação. Recebe autorização semioficial para atacar navios de nações rivais, ampliando táticas de abordagem.",
                5: "Corsário (Marujo) nível 5. Atua com maior desenvoltura diplomática em portos, negociando prêmios de captura e reforçando alianças com autoridades que apoiam sua cruzada marítima.",
                7: "Corsário (Marujo) nível 7. Passa a liderar operações de caça a piratas, aprimorando bombardeios de canhão e coordenando ataques cirúrgicos a embarcações inimigas.",
                10: "Corsário (Marujo) nível 10. Torna-se um nome temido e respeitado no Atlântico, agindo como força quase independente e recebendo honrarias ou desconfiança das coroas europeias."
                },
                "Contrabandista": {
                3: "Contrabandista (Marujo) nível 3. Desenvolve maestria em esconder mercadorias nos porões, desviando olhos da alfândega e enganando inspeções superficiais.",
                5: "Contrabandista (Marujo) nível 5. Amplia contatos em mercados negros e rotas clandestinas, usando códigos secretos para acordos discretos e transporte de cargas ilícitas.",
                7: "Contrabandista (Marujo) nível 7. Conquista prestígio entre facções clandestinas, criando rotas bem guardadas e cooptando informantes que ajudam a despistar autoridades.",
                10: "Contrabandista (Marujo) nível 10. Você domina a logística oculta, transpondo bloqueios navais e enriquecendo a tripulação, agindo como força econômica nas sombras."
                }
            },

            "Duelista": {
                "Mosqueteiro": {
                3: "Mosqueteiro (Duelista) nível 3. Fica mais preciso com armas de fogo de fecho, dominando recarga rápida e disparos à queima-roupa sem perder compostura.",
                5: "Mosqueteiro (Duelista) nível 5. Aprimora pontaria em distâncias maiores, usando visadas improvisadas e táticas de cobertura, assumindo papel de atirador de elite.",
                7: "Mosqueteiro (Duelista) nível 7. Integra esgrima a tiros curtos, alternando facilmente entre espada e mosquete. É capaz de manobras que surpreendem adversários menos versados.",
                10: "Mosqueteiro (Duelista) nível 10. Atirador lendário, suas balas parecem guiadas pelo instinto; intimida pelotões inteiros e é requisitado pelas maiores potências militares."
                },
                "Espadachim": {
                3: "Espadachim (Duelista) nível 3. Aprofunda a técnica de lâminas leves, refinando estocadas e contra-ataques fulminantes que demonstram total controle do embate.",
                5: "Espadachim (Duelista) nível 5. Domina feints e manobras de desarme. Luta como um artista, transformando qualquer duelo em espetáculo tenso e admirado.",
                7: "Espadachim (Duelista) nível 7. Aprendeu a ler microexpressões do oponente, prevendo ataques e vencendo combates mesmo em desvantagem numérica.",
                10: "Espadachim (Duelista) nível 10. Eleva a fama a níveis quase míticos; raros ousam enfrentar seu florete em campo aberto, e até nobres poderosos hesitam em desafiá-lo."
                },
                "Brigão": {
                3: "Brigão (Duelista) nível 3. Desenvolve um estilo de luta de rua, unindo golpes sujos e agarrões, punindo quem subestima sua abordagem impetuosa.",
                5: "Brigão (Duelista) nível 5. Faz uso de ambiente ao seu favor: garrafas, cadeiras, partes do cenário tornam-se armas improvisadas, garantindo vantagem sobre inimigos mais formais.",
                7: "Brigão (Duelista) nível 7. Consagra sua reputação como um lutador imprevisível; seus socos e chaves de braço surgem em ângulos inesperados.",
                10: "Brigão (Duelista) nível 10. Alcança nível temível, capaz de dispersar gangues sozinho; adversários temem a ferocidade e criatividade de suas investidas."
                }
            },

            "Explorador": {
                "Batedor": {
                3: "Batedor (Explorador) nível 3. Especialista em emboscadas e furtividade, infiltrando-se em territórios hostis sem ser notado.",
                5: "Batedor (Explorador) nível 5. Ganha percepção apurada em vigílias e patrulhas, auxiliando grupos a detectar ameaças antes que ocorram.",
                7: "Batedor (Explorador) nível 7. Consegue conduzir missões de espionagem nas linhas inimigas, movendo-se com destreza até em terreno acidentado.",
                10:"Batedor (Explorador) nível 10. Quase invisível à noite ou em florestas densas, seu grupo raramente é surpreendido, graças a informações antecipadas."
                },
                "Caçador de Relíquias": {
                3: "Caçador de Relíquias (Explorador) nível 3. Foca em arqueologia e identificação de itens antigos, compreendendo símbolos e inscrições rudimentares.",
                5: "Caçador de Relíquias (Explorador) nível 5. Domina melhor a leitura de mapas antigos e mecanismos em ruínas, descobrindo passagens secretas.",
                7: "Caçador de Relíquias (Explorador) nível 7. Consagra-se em expedições a templos perdidos, prevendo armadilhas antigas e mantendo o grupo seguro.",
                10:"Caçador de Relíquias (Explorador) nível 10. É referência em artefatos históricos, sabendo avaliar e lidar com objetos de valor inestimável ou natureza perigosa."
                },
                "Montanhista": {
                3: "Montanhista (Explorador) nível 3. Treinado em escalada e travessias rochosas, encontra rotas em penhascos e suportando baixas temperaturas.",
                5: "Montanhista (Explorador) nível 5. Aprende técnicas avançadas de rapel, construindo pontes rudimentares e auxiliando a equipe em terrenos íngremes.",
                7: "Montanhista (Explorador) nível 7. Desenvolve resistência extra a altitudes extremas, guiando expedições por cordilheiras traiçoeiras.",
                10:"Montanhista (Explorador) nível 10. Pode atravessar montanhas e glaciares com incrível facilidade, descobrindo até rotas consideradas impossíveis."
                }
            },

            "Charlatão": {
                "Hipnotizador": {
                3: "Hipnotizador (Charlatão) nível 3. Dominando técnicas avançadas de sugestão mental, induz breves transes em alvos descuidados.",
                5: "Hipnotizador (Charlatão) nível 5. Faz sessões de manipulação mais elaboradas, podendo extrair informações ou impor condutas temporárias.",
                7: "Hipnotizador (Charlatão) nível 7. Engana mesmo mentes fortes, penetrando bloqueios psicológicos com sutileza e cuidado.",
                10:"Hipnotizador (Charlatão) nível 10. Reconhecido como mestre da manipulação mental, podendo alterar lembranças superficiais e sentimentos em poucos instantes."
                },
                "Dissimulado": {
                3: "Dissimulado (Charlatão) nível 3. Especialista em disfarces e identidades falsas, enganando guardas e burocracias simples.",
                5: "Dissimulado (Charlatão) nível 5. Consegue manter papéis duplos por períodos longos, falsificando documentos e sotaques.",
                7: "Dissimulado (Charlatão) nível 7. Personifica figuras importantes com impressionante verossimilhança, escapando de cercos e investigações intensas.",
                10:"Dissimulado (Charlatão) nível 10. Alcança lendas do submundo, circulando em cortes e tabernas sem jamais ser reconhecido."
                },
                "Língua Afiada": {
                3: "Língua Afiada (Charlatão) nível 3. Deslumbra plateias e negocia favores com oratória persuasiva, moldando a verdade a seu favor.",
                5: "Língua Afiada (Charlatão) nível 5. Aperfeiçoa argumentos e intrigas, enganando conselhos ou grupos inteiros em discursos rápidos.",
                7: "Língua Afiada (Charlatão) nível 7. Seduz multidões e convence figuras poderosas a ceder terreno ou tesouro, mesmo contra a lógica.",
                10:"Língua Afiada (Charlatão) nível 10. Reconhecido como manipular supremo da fala, suas palavras podem iniciar ou encerrar conflitos de escala colossal."
                }
            },

            "Médico": {
                "Cirurgião de Navio": {
                3: "Cirurgião de Navio (Médico) nível 3. Aprende a realizar operações básicas em alto-mar, usando instrumentos improvisados e lidando com balanço do navio.",
                5: "Cirurgião de Navio (Médico) nível 5. Aperfeiçoa amputações e cirurgias emergenciais, salvando tripulantes em meio a combates navais.",
                7: "Cirurgião de Navio (Médico) nível 7. Desenvolve técnicas avançadas de esterilização e sutura, reduzindo drasticamente infecções pós-cirúrgicas.",
                10:"Cirurgião de Navio (Médico) nível 10. Tornou-se lenda nos portos, conseguindo reverter ferimentos quase fatais e estabilizar até casos extremos."
                },
                "Erudito Naturalista": {
                3: "Erudito Naturalista (Médico) nível 3. Especializa-se em fitoterapia, criando remédios e cataplasmas eficientes para feridas e males comuns.",
                5: "Erudito Naturalista (Médico) nível 5. Identifica doenças exóticas, coletando ervas e fungos raros para produzir antídotos específicos.",
                7: "Erudito Naturalista (Médico) nível 7. Elabora complexos estudos de fauna e flora, misturando substâncias que aceleram a cura ou reforçam imunidade.",
                10:"Erudito Naturalista (Médico) nível 10. Um cientista renomado, consultado por nações para resolver epidemias e criar soluções médicas de ponta."
                },
                "Médico de Guerra": {
                3: "Médico de Guerra (Médico) nível 3. Foca em socorros urgentes durante batalhas, movendo-se rápido pelo campo para reduzir baixas.",
                5: "Médico de Guerra (Médico) nível 5. Domina procedimentos de extração de balas e fragmentos, estabilizando soldados sob fogo inimigo.",
                7: "Médico de Guerra (Médico) nível 7. Consegue montar enfermarias provisórias, orquestrando auxiliares em meio ao caos de grandes confrontos.",
                10:"Médico de Guerra (Médico) nível 10. Alcança prestígio militar, requisitado para operações de alto risco, salvando regimentos inteiros da morte certa."
                }
            },

            "Sacerdote": {
                "Orador Visionário": {
                3: "Orador Visionário (Sacerdote) nível 3. Seus sermões inspiram coragem e esperança, unindo fiéis e atraindo novos seguidores.",
                5: "Orador Visionário (Sacerdote) nível 5. Desperta fervor intenso em multidões, canalizando uma eloquência quase profética.",
                7: "Orador Visionário (Sacerdote) nível 7. Pode acalmar tumultos ou incitar revoltas com palavras cuidadosamente escolhidas.",
                10:"Orador Visionário (Sacerdote) nível 10. Reverenciado como farol de fé, suas pregações podem moldar o destino de cidades ou nações inteiras."
                },
                "Manipulador Místico": {
                3: "Manipulador Místico (Sacerdote) nível 3. Usa rituais simbólicos e crenças populares para induzir fenômenos psicológicos poderosos.",
                5: "Manipulador Místico (Sacerdote) nível 5. Aprofunda técnicas de sugestão coletiva, levando grupos a 'ver sinais divinos' onde deseja.",
                7: "Manipulador Místico (Sacerdote) nível 7. Constrói cultos e doutrinas obscuras, atraindo fiéis que obedecem cegamente às suas instruções.",
                10:"Manipulador Místico (Sacerdote) nível 10. Alcança posto de líder religioso temido, movendo grandes massas pela convicção ou medo do sobrenatural."
                },
                "Cultista Oculto": {
                3: "Cultista Oculto (Sacerdote) nível 3. Explora símbolos e rituais macabros, manipulando crenças secretas para aumentar influência.",
                5: "Cultista Oculto (Sacerdote) nível 5. Funda seitas restritas, realizando cerimônias que despertam temor em adversários e devoção nos iniciados.",
                7: "Cultista Oculto (Sacerdote) nível 7. Execução de práticas ritualísticas intensifica efeitos psicológicos e místicos, gerando fama sinistra.",
                10:"Cultista Oculto (Sacerdote) nível 10. Poucos ousam desafiar seu poder, capaz de subverter sistemas inteiros por meio de conspirações religiosas."
                }
            },

            "Sabotador": {
                "Demolidor": {
                3: "Demolidor (Sabotador) nível 3. Aperfeiçoa uso de pólvora e explosivos simples, abrindo brechas em paredes ou abalando estrutura do alvo.",
                5: "Demolidor (Sabotador) nível 5. Planeja explosões controladas, causando danos focados e evitando colapsos indesejados.",
                7: "Demolidor (Sabotador) nível 7. É requisitado para destruir fortalezas, pontes ou navios estrategicamente, sem expor a própria equipe.",
                10:"Demolidor (Sabotador) nível 10. Conhecido globalmente por explodir alvos “impossíveis”, suas técnicas beiram o lendário."
                },
                "Espião": {
                3: "Espião (Sabotador) nível 3. Domina infiltração e recolhimento de informações, lendo documentos confidenciais e escapando despercebido.",
                5: "Espião (Sabotador) nível 5. Apura falsificações e codificação, interceptando mensagens e se passando por mensageiros inimigos.",
                7: "Espião (Sabotador) nível 7. Consegue blefar para autoridades de alto escalão, obtendo segredos cruciais em operações arriscadas.",
                10:"Espião (Sabotador) nível 10. Podendo desestabilizar reinos inteiros, manipula generais e embaixadores, conduzindo eventos à própria vontade."
                },
                "Assassino Urbano": {
                3: "Assassino Urbano (Sabotador) nível 3. Exercita golpes silenciosos em becos e vielas, eliminando alvos sem alertar guardas próximos.",
                5: "Assassino Urbano (Sabotador) nível 5. Aperfeiçoa uso de venenos e lâminas ocultas, assegurando abates rápidos em locais públicos.",
                7: "Assassino Urbano (Sabotador) nível 7. Distingue-se pela preparação meticulosa, evitando rastros e corrompendo investigações.",
                10:"Assassino Urbano (Sabotador) nível 10. Torna-se lenda na cidade, inatingível para milícias e espiões rivais, selecionando alvos de alto valor."
                }
            },

            "Erudito": {
                "Cartógrafo": {
                3: "Cartógrafo (Erudito) nível 3. Detalha mapas mais precisos, registrando pontos geográficos de interesse para futuros exploradores.",
                5: "Cartógrafo (Erudito) nível 5. Traça rotas novas, correlacionando anotações de navegação astronômica e relatos de marinheiros veteranos.",
                7: "Cartógrafo (Erudito) nível 7. Elabora mapas tridimensionais, destacando relevos e profundezas, vital para expedições complexas.",
                10:"Cartógrafo (Erudito) nível 10. Considerado um mestre, suas criações guiam nações e exploradores, definindo o rumo de grandes descobertas."
                },
                "Alquimista": {
                3: "Alquimista (Erudito) nível 3. Domina reações básicas, criando soluções ácidas e rudimentares, além de poções de efeito leve.",
                5: "Alquimista (Erudito) nível 5. Aperfeiçoa combinações mais estáveis e reativas, gerando substâncias inflamáveis ou que aceleram cura.",
                7: "Alquimista (Erudito) nível 7. Cria catalisadores complexos que podem afetar mente e corpo, elaborando compostos quase 'mágicos'.",
                10:"Alquimista (Erudito) nível 10. Alcança fama colossal, capaz de sintetizar elixires raríssimos ou criar reações imponentes que desafiam o entendimento comum."
                },
                "Engenheiro": {
                3: "Engenheiro (Erudito) nível 3. Constrói engenhocas simples, conhecendo fundamentos de mecânica e integração de peças metálicas.",
                5: "Engenheiro (Erudito) nível 5. Desenvolve maquinários e aprimora ferramentas, aplicando cálculos para otimizar estruturas em navios ou fortificações.",
                7: "Engenheiro (Erudito) nível 7. Lidera projetos mais audaciosos, como canhões modificados, mecanismos de elevação e defesas móveis.",
                10:"Engenheiro (Erudito) nível 10. Seu gênio inventivo marca avanços tecnológicos notáveis, redefinindo capacidades navais e militares de grandes potências."
                }
            }
            }

        # ====== Proezas Disponíveis ======
        self.proezas_disponiveis = {
            "Mestre em Duas Armas": "Você se tornou altamente eficiente no combate com duas armas...",
            "Atirador Preciso": "Você domina completamente o uso de armas à distância...",
            "Desvio Ágil": "Seus reflexos lhe permitem escapar ileso de ataques e explosões...",
            "Olhos de Águia": "Seus olhos treinados enxergam mais longe...",
            "Tiro Rápido": "Você aprendeu a disparar rapidamente sem comprometer sua precisão...",
            "Mira Letal": "Seus disparos são precisos e letais...",
            "Manuseio de Duas Mãos": "Você aprendeu a lidar com armas pesadas...",
            "Especialista em Combate à Distância": "Você treinou para ser eficiente à distância...",
            "Mestre em Armas de Fogo": "Você ganha proficiência com armas de fogo...",
            "Alerta": "Você está sempre um passo à frente dos inimigos...",
            "Ataque Extra": "Seu treinamento lhe permite atacar mais rápido...",
            "Golpe Brutal": "Você sabe exatamente onde acertar...",
            "Mestre em Contra-Ataques": "Você aprendeu a responder rapidamente aos erros...",
            "Demolidor Especialista": "Você aprendeu a lidar com explosivos...",
            "Mente Tática": "Você vê padrões e estratégias no caos...",
            "Mestre da Cura": "Você pode salvar qualquer um...",
            "Resiliência Espiritual": "Sua fé o fortalece contra provações...",
            "Artilheiro de Elite": "Você domina a arte da artilharia naval...",
            "Tático Naval": "Você se tornou um líder experiente no mar...",
            "Terror dos Mares": "Você é uma figura temida nos oceanos...",
            "Sobrevivente Implacável": "Você já esteve à beira da morte..."
        }

        # ====== Equipamentos ======
        # Tabelas de armas e armaduras
        self.tabela_armas = {
            "Punhal": ("1d4", "6m", "Leve, Arremessável", "Destreza"),
            "Clava": ("1d6", "—", "Impacto", "Força"),
            "Bastão": ("1d4", "—", "Versátil (1d6), Utilitário", "Força"),
            "Machado de Mão": ("1d6", "6m", "Leve, Arremessável", "Força/Destreza"),
            "Espada Curta": ("1d6", "—", "Versátil (1d8)", "Força/Destreza"),
            "Lança": ("1d6", "6m", "Arremessável, Versátil (1d8)", "Força/Destreza"),
            "Arco Curto": ("1d6", "30m", "Silencioso", "Destreza"),
            "Besta Leve": ("1d8", "24m", "Recarga, Silencioso", "Destreza"),
            "Sabre": ("1d8", "—", "Rápido (+1 Iniciativa)", "Força/Destreza"),
            "Faca de Arremesso (8)": ("1d4", "9m", "Leve, Arremessável", "Destreza"),
            "Pistola": ("1d10", "9m", "Recarga, Letal", "Destreza"),
            "Mosquete": ("1d12", "36m", "Pesado, Recarga Lenta, Impacto", "Destreza"),
            "Granada (6)": ("2d6", "9m", "Explosivo, Área de Efeito", "—"),
        }

        self.tabela_armaduras = {
            "Roupas Leves": ("10 + Destreza (DES)", "Leve", "Nenhuma", "Discreta"),
            "Couro Reforçado": ("12 + Destreza (DES)", "Leve", "Nenhuma", "Resistente a Cortes"),
            "Cota de Malha": ("14 + até 2 DES", "Média", "-1 metro", "Barulhenta"),
            "Roupas Clericais": ("11 + Sabedoria (SAB)", "Leve", "Nenhuma", "Simbólica, Resistente a Intempéries"),
        }

        # ====== Dados dos Equipamentos Iniciais ======
        self.equipamento_inicial = {
            "Marujo": {
                "Arma Primária": ["Sabre", "Machado de Mão"],
                "Arma Secundária": ["Besta Leve", "Arco Curto"],
                "Extras": ["Corda e Gancho", "Kit de Ferramentas Navais"]
            },
            "Duelista": {
                "Arma Primária": ["Espada Curta", "Sabre"],
                "Arma Secundária": ["Pistola", "Faca de Arremesso (8)", "Mosquete"],
                "Extras": ["Kit de Manutenção de Armas"]
            },
            "Explorador": {
                "Arma Primária": ["Arco Curto", "Lança"],
                "Arma Secundária": ["Pistola", "Faca de Arremesso (8)"],
                "Extras": ["Kit de Sobrevivência", "Mapa Regional"]
            },
            "Charlatão": {
                "Arma Primária": ["Punhal", "Espada Curta"],
                "Arma Secundária": ["Pistola"],
                "Extras": ["Kit de Disfarces", "Kit de Ferramentas de Ladrão"]
            },
            "Médico": {
                "Arma Primária": ["Clava", "Faca de Arremesso"],
                "Extras": ["Kit de Medicina", "Bandagens", "Poção de Cura Simples (2)"]
            },
            "Sacerdote": {
                "Arma Primária": ["Espada Curta", "Bastão"],
                "Extras": ["Kit de Escritura", "Roupas Clericais", "Amuleto Religioso"]
            },
            "Sabotador": {
                "Arma Primária": ["Punhal", "Lança"],
                "Arma Secundária": ["Besta Leve", "Granada (6)"],
                "Extras": ["Kit de Ferramentas de Sabotagem", "Kit de Explosivos Básico"]
            },
            "Erudito": {
                "Arma Primária": ["Bastão", "Faca de Arremesso (8)"],
                "Extras": ["Kit de Engenharia", "Kit de Alquimia", "Caderno de Anotações", "Óculos de Precisão"]
            },
        }

        self.armadura_inicial = {
            "Marujo": ["Couro Reforçado", "Cota de Malha"],
            "Duelista": ["Roupas Leves", "Couro Reforçado"],
            "Explorador": ["Couro Reforçado", "Roupas Leves"],
            "Charlatão": ["Roupas Leves"],
            "Médico": ["Roupas Leves"],
            "Sacerdote": ["Roupas Clericais", "Cota de Malha"],
            "Sabotador": ["Couro Reforçado"],
            "Erudito": ["Roupas Leves"]
        }

        # ====== Mapa de Atributos ======
        self.mapa_atributos = {
            "Atletismo": "Força", "Briga": "Força", "Furtividade": "Destreza", "Pontaria": "Destreza", "Reflexos": "Destreza",
            "Resistência": "Constituição", "Conhecimento Acadêmico": "Inteligência", "Engenharia e Mecânica": "Inteligência",
            "Estratégia": "Inteligência", "Percepção": "Sabedoria", "Sobrevivência": "Sabedoria", "Psicologia": "Sabedoria",
            "Persuasão": "Carisma", "Enganação": "Carisma", "Intimidação": "Carisma", "Navegação": "Inteligência",
            "Medicina": "Sabedoria", "Ocultismo": "Sabedoria", "Explosivos": "Inteligência"
        }

        # ====== Descrição das Habilidades ======
        self.descricao_habilidades = {
            "Atletismo": "Saltar, escalar, nadar e outras atividades físicas extenuantes.",
            "Briga": "Lutar desarmado ou usar força bruta em combate.",
            "Furtividade": "Mover-se silenciosamente, esconder-se e evitar ser detectado.",
            "Pontaria": "Usar armas de fogo e arremesso com precisão.",
            "Reflexos": "Agilidade para reagir rapidamente a situações inesperadas.",
            "Resistência": "Tolerância a venenos, fadiga e ferimentos.",
            "Conhecimento Acadêmico": "Cultura geral, ciências, história e línguas.",
            "Engenharia e Mecânica": "Construção, manutenção e entendimento de máquinas.",
            "Estratégia": "Planejamento tático, análise de batalhas e emboscadas.",
            "Percepção": "Notar detalhes escondidos e mudanças no ambiente.",
            "Sobrevivência": "Encontrar abrigo, rastrear presas e sobreviver em condições extremas.",
            "Psicologia": "Entender intenções e emoções alheias.",
            "Persuasão": "Convencer outros com palavras e argumentos.",
            "Enganação": "Mentir, fingir e disfarçar intenções.",
            "Intimidação": "Ameaçar e coagir usando força ou presença.",
            "Navegação": "Uso de mapas, estrelas e instrumentos náuticos.",
            "Medicina": "Diagnóstico e tratamento de doenças e ferimentos.",
            "Ocultismo": "Conhecimento sobre crenças, mitos e superstições.",
            "Explosivos": "Fabricação e uso de pólvora e bombas."
        }
        
        # ====== Habilidades ======
        self.habilidades = [
            "Atletismo", "Briga", "Furtividade", "Pontaria", "Reflexos", "Resistência",
            "Conhecimento Acadêmico", "Engenharia e Mecânica", "Estratégia",
            "Percepção", "Sobrevivência", "Psicologia",
            "Persuasão", "Enganação", "Intimidação",
            "Navegação", "Medicina", "Ocultismo", "Explosivos"
        ]
        
        # ====== Grupos de Habilidades ======
        self.habilidades_grupos = [
            ("Físicas", ["Atletismo", "Briga", "Furtividade", "Pontaria", "Reflexos", "Resistência"]),
            ("Intelectuais", ["Conhecimento Acadêmico", "Engenharia e Mecânica", "Estratégia", "Percepção", "Sobrevivência"]),
            ("Sociais", ["Psicologia", "Persuasão", "Enganação", "Intimidação"]),
            ("Técnicas", ["Navegação", "Medicina", "Ocultismo", "Explosivos"])
        ]
        
        # ====== Truques ======
        self.truques_disponiveis = [
        {
            "Nome": "Palavras Enfáticas",
            "Nível": "0",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você escolhe um alvo a até 6 metros e faz um Teste de Persuasão (DC 12). Se bem-sucedido, ele presta atenção total em você por 30 segundos, ignorando distrações leves.",
            "Requisitos": "O alvo precisa entender sua língua."
        },
        {
            "Nome": "Olhos Penetrantes",
            "Nível": "0",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode fazer um Teste de Intuição (DC 12) para detectar o estado emocional do alvo (nervoso, mentindo, assustado, calmo, etc.).",
            "Requisitos": "Precisa manter contato visual por pelo menos 5 segundos."
        },
        {
            "Nome": "Controle de Voz",
            "Nível": "0",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode alterar levemente sua voz (mais grave, mais aguda, rouca ou firme) por 5 minutos, tornando-a mais intimidadora ou persuasiva.",
            "Requisitos": "O efeito é apenas auditivo e não engana quem já conhece bem sua voz."
        },
        {
            "Nome": "Queima Controlada",
            "Nível": "0",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode acender ou apagar pequenas chamas (velas, lamparinas, fósforos) em um raio de 3 metros.",
            "Requisitos": "Precisa de uma fonte de fogo próxima."
        },
        {
            "Nome": "Teste de Veneno",
            "Nível": "0",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode identificar a presença de venenos ou drogas em um líquido com um Teste de Medicina (DC 12).",
            "Requisitos": "Precisa observar ou cheirar o líquido por pelo menos 10 segundos."
        },
        {
            "Nome": "Reação Química",
            "Nível": "0",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode misturar pequenas substâncias para produzir um estalo alto, fumaça leve ou um brilho breve.",
            "Requisitos": "Precisa ter acesso a materiais químicos básicos."
        },
        {
            "Nome": "Corte e Esterilização",
            "Nível": "0",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode limpar e desinfetar uma ferida pequena, prevenindo infecções. Se usado antes de um descanso, permite recuperar +1 PV.",
            "Requisitos": "Precisa de álcool ou outra substância desinfetante."
        },
        {
            "Nome": "Reflexo Enganoso",
            "Nível": "0",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode fazer com que uma luz seja refletida de forma a distrair ou cegar um alvo por 1 turno. O alvo deve fazer um Teste de Constituição (DC 12) ou sofrer desvantagem na próxima ação.",
            "Requisitos": "Precisa de um objeto metálico\"ou devidro."
        },
        {
            "Nome": "Passos Falsos",
            "Nível": "0",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode fazer um ruído semelhante ao som de passos vindo de um ponto a até 10 metros.",
            "Requisitos": "O local precisa ter materiais como madeira ou pedra para ecoar o som."
        },
        {
            "Nome": "Som Fantasma",
            "Nível": "0",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode imitar a voz de uma pessoa que já ouviu antes, mas apenas por frases curtas. Alvos desatentos devem fazer um Teste de Percepção (DC 12) para perceber a farsa.",
            "Requisitos": "O som não pode ter tons muito complexos, como grito\"s ou cantos."
        },
        {
            "Nome": "Tinta Invisível",
            "Nível": "0",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode escrever algo que só se tornará visível sob uma condição específica (exemplo: calor, água, luz forte).",
            "Requisitos": "Precisa ter uma tinta especial ou um reagente químico."
        },
        {
            "Nome": "Sussurros Espirituais",
            "Nível": "0",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode murmurar palavras indecifráveis que parecem vir de diferentes direções em um raio de 3 metros, assustando ouvintes desatentos.",
            "Requisitos": "Funciona melhor em locais silenciosos ou escuros."
        },
        {
            "Nome": "Símbolo de Proteção",
            "Nível": "0",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode desenhar um símbolo místico em um objeto ou parede. Pessoas supersticiosas precisarão fazer um Teste de Sabedoria (DC 12) para ignorá-lo.",
            "Requisitos": "Precisa de um material para desenhar, como carvão ou giz."
        },
        {
            "Nome": "Brisa Cerimonial",
            "Nível": "0",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode criar uma corrente de ar súbita que movimenta tecidos, velas ou faz a poeira subir levemente.",
            "Requisitos": "Precisa estar ao ar livre ou próximo de uma entrada aberta."
        },
        {
            "Nome": "Aura de Devoção",
            "Nível": "0",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Pessoas ao seu redor sentem uma leve confiança ou temor em relação a você, dependendo de sua intenção.",
            "Requisitos": "Precisa de um símbolo religioso visível."
        },
        {
            "Nome": "Falsa Lembrança",
            "Nível": "1",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você planta uma lembrança vaga e confusa na mente do alvo. Ele deve fazer um Teste de Inteligência (DC 12) ou acreditará que o evento aconteceu, mas sem detalhes claros.",
            "Requisitos": "O alvo precisa estar distraído ou receptivo\"à conversa."
        },
        {
            "Nome": "Névoa Cega",
            "Nível": "1",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você espalha um gás denso em uma área de 3 metros de raio. Criaturas dentro da área devem fazer um Teste de Constituição (DC 12) ou terão desvantagem em ataques à distância por 1d4 turnos.",
            "Requisitos": "Precisa de um frasco de reagente\"químico apropriado."
        },
        {
            "Nome": "Explosão Controlada",
            "Nível": "1",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode preparar e detonar uma carga explosiva pequena que causa 2d6 de dano em um raio de 1,5 metros. Criaturas no raio devem fazer um Teste de Destreza (DC 12) para reduzir o dano pela metade.",
            "Requisitos": "Precisa de pólv\"ora oumaterial inflamável."
        },
        {
            "Nome": "Óleo Deslizante",
            "Nível": "1",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você espalha uma substância escorregadia em um raio de 3 metros. Criaturas na área devem fazer um Teste de Destreza (DC 12) ou caem no chão.",
            "Requisitos": "Precisa de um frasco de óleo ou graxa."
        },
        {
            "Nome": "Tônico Revigorante",
            "Nível": "1",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Um aliado que beber a mistura recupera 1d6 PV imediatamente.",
            "Requisitos": "Precisa de ervas ou ingredientes medicinais."
        },
        {
            "Nome": "Sombra Ilusória",
            "Nível": "1",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você projeta uma sombra anormal e distorcida em uma parede ou chão. Criaturas que veem devem fazer um Teste de Sabedoria (DC 12) ou hesitam por 1 turno, tentando entender a ilusão.",
            "Requisitos": "Precisa de uma fonte de luz próxima."
        },
        {
            "Nome": "Voz Distante",
            "Nível": "1",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode falar como se sua voz viesse de outro ponto a até 12 metros. Criaturas desatentas devem fazer um Teste de Percepção (DC 12) para notar a farsa.",
            "Requisitos": "Sua boca não pode estar visível enquanto usa essa habilidade."
        },
        {
            "Nome": "Visão Turva",
            "Nível": "1",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você faz com que um alvo a 6 metros tenha sua visão embaralhada por 1 rodada. Ele deve fazer um Teste de Constituição (DC 12) ou sofrer desvantagem em ataques.",
            "Requisitos": "Precisa estar a pelo menos 6 metros do alvo."
        },
        {
            "Nome": "Bênção Espiritual",
            "Nível": "1",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você toca um aliado, concedendo-lhe +1 em um teste de habilidade ou ataque nos próximos 10 minutos.",
            "Requisitos": "Precisa tocar o alvo diretamente ou segurar um símbolo sagrado."
        },
        {
            "Nome": "Profecia Oportuna",
            "Nível": "1",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode fazer um Teste de Enganação (DC 14) para convencer alguém de que um evento iminente foi previsto. O alvo hesita antes de tomar uma decisão importante.",
            "Requisitos": "Precisa estar em um ambiente ritualístico ou ter sí\"mbolosdivinatórios."
        },
        {
            "Nome": "Aura de Reverência",
            "Nível": "1",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Criaturas dentro de um raio de 3 metros sentem um respeito inconsciente por você. Criaturas hostis devem fazer um Teste de Sabedoria (DC 12) ou hesitam antes de atacá-lo pela primeira vez.",
            "Requisitos": "Precisa de um objeto d\"e valor simbólico (medalhão, insígnia, manto)."
        },
        {
            "Nome": "Medo Sagrado",
            "Nível": "1",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você recita palavras místicas e foca sua presença em um alvo dentro de 9 metros. Ele deve fazer um Teste de Sabedoria (DC 12) ou ficará amedrontado por 1 turno.",
            "Requisitos": "Precisa estar em um ambiente onde a crença do alvo seja\"relevante (igreja, cemitério, altar)."
        },
        {
            "Nome": "Comando Irresistível",
            "Nível": "2",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você dá uma ordem curta e precisa para um alvo a até 9 metros. Ele deve fazer um Teste de Sabedoria (DC 14) ou seguirá o comando por 1d4 turnos (exemplo: \"\"\"\"Durma!\"\"\"\", \"\"\"\"Fuja!\"\"\"\", \"\"\"\"Ajoelhe-se!\"\"\"\").",
            "Requisitos": "O comando d\"eve ser algo que o alvo possa cumprir imediatamente e não pode ser autodestrutivo."
        },
        {
            "Nome": "Distorção da Memória",
            "Nível": "2",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você altera uma lembrança recente do alvo. Ele deve fazer um Teste de Inteligência (DC 14) ou passará a lembrar do evento de forma diferente.",
            "Requisitos": "O alvo deve estar distraído ou conversando com você por pelo menos\"30 segundos."
        },
        {
            "Nome": "Paralisia Mental",
            "Nível": "2",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Um alvo dentro de 6 metros faz um Teste de Sabedoria (DC 14). Se falhar, ele fica incapaz de agir por 1 turno, apenas olhando fixamente para você.",
            "Requisitos": "O alvo precisa estar consciente e não pode estar em combate inten\"so."
        },
        {
            "Nome": "Influência Duradoura",
            "Nível": "2",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você convence um NPC de que você é um aliado confiável. Ele deve fazer um Teste de Sabedoria (DC 14) ou será amigável com você por 1 hora, a menos que sofra dano ou tenha um motivo forte para suspeitar.",
            "Requisitos": "O alv\"o deveentender sua língua e não pode ser hostil no momento da tentativa."
        },
        {
            "Nome": "Fumaça Negra",
            "Nível": "2",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você cria uma nuvem de 6 metros de raio que obscurece a visão por 1d4 turnos. Criaturas dentro dela não podem ver nada além de 1 metro de distância.",
            "Requisitos": "Precisa de um recipiente com carvão em pó e substâncias inflamáveis."
        },
        {
            "Nome": "Soro da Verdade",
            "Nível": "2",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você mistura uma substância que força um alvo a revelar informações. Ele deve fazer um Teste de Constituição (DC 14) ou não poderá mentir por 10 minutos.",
            "Requisitos": "Precisa de ervas específicas ou um destilado químico refinado."
        },
        {
            "Nome": "Mistura Tóxica",
            "Nível": "2",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode criar um veneno que, quando ingerido ou aplicado em uma arma, causa 2d6 de dano e impõe desvantagem em Testes de Constituição por 1d4 turnos.",
            "Requisitos": "Precisa de veneno natural ou substâncias corrosivas."
        },
        {
            "Nome": "Óleo Inflamável",
            "Nível": "2",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você espalha um líquido altamente inflamável em uma área de 3 metros. Se uma chama atingir essa área, ela explode causando 2d6 de dano.",
            "Requisitos": "Precisa de um recipiente com óleo destilado."
        },
        {
            "Nome": "Disfarce Perfeito",
            "Nível": "2",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode alterar sua aparência por 1 hora, mudando detalhes como cor de cabelo, feições e até a voz. Um alvo deve fazer um Teste de Investigação (DC 14) para perceber a farsa.",
            "Requisitos": "Precisa de materiais de disfarce (tint\"a, maquiagem, tecidos)."
        },
        {
            "Nome": "Voz Fantasma",
            "Nível": "2",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode imitar perfeitamente a voz de alguém por 10 minutos, incluindo o tom e padrão de fala. Um alvo atento pode fazer um Teste de Percepção (DC 14) para perceber a farsa.",
            "Requisitos": "Precisa ter ouvido a voz da pessoa por pelo\"menos30 segundos."
        },
        {
            "Nome": "Silhueta Sombria",
            "Nível": "2",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode se esconder nas sombras de forma quase sobrenatural. Sempre que estiver em um ambiente escuro, ganha vantagem em Testes de Furtividade por 1d4 turnos.",
            "Requisitos": "Precisa estar em uma área com sombras fortes."
        },
        {
            "Nome": "O Chamado dos Espíritos",
            "Nível": "2",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você recita um cântico, criando um eco misterioso no ambiente. Criaturas supersticiosas devem fazer um Teste de Sabedoria (DC 14) ou acreditar que há uma presença sobrenatural.",
            "Requisitos": "Precisa estar em um local sil\"encioso e escuro."
        },
        {
            "Nome": "Maldição do Opressor",
            "Nível": "2",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você amaldiçoa um inimigo, fazendo-o duvidar de sua própria autoridade. Ele deve fazer um Teste de Sabedoria (DC 14) ou terá desvantagem em testes sociais por 1 hora.",
            "Requisitos": "Precisa de um objeto ligado ao alvo (assin\"atura,cabelo, símbolo pessoal)."
        },
        {
            "Nome": "Marca Ritualística",
            "Nível": "2",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você desenha um símbolo místico que só pode ser visto por aqueles que você escolher. O símbolo dura 24 horas.",
            "Requisitos": "Precisa de giz, carvão ou tinta."
        },
        {
            "Nome": "Bênção do Orador",
            "Nível": "2",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você toca um aliado e concede a ele +2 em Testes de Carisma por 10 minutos.",
            "Requisitos": "Precisa tocar o alvo diretamente ou recitar uma oração."
        },
        {
            "Nome": "Controle Indireto",
            "Nível": "3",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você implanta uma ordem na mente de um alvo dentro de 9 metros. Ele deve fazer um Teste de Sabedoria (DC 15). Se falhar, ele seguirá a ordem indiretamente, sem perceber que foi influenciado.",
            "Requisitos": "O alvo precisa confi\"ar minimamente em você ou estar distraído."
        },
        {
            "Nome": "Sugestão Avançada",
            "Nível": "3",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode sugerir uma ação para um alvo dentro de 9 metros, que deve fazer um Teste de Sabedoria (DC 15). Se falhar, ele obedecerá a sugestão por até 1 hora, desde que não seja autodestrutiva.",
            "Requisitos": "O alvo precisa ouv\"ir a sugestão e entendê-la."
        },
        {
            "Nome": "Dissociação Mental",
            "Nível": "3",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "O alvo dentro de 6 metros deve fazer um Teste de Inteligência (DC 15) ou terá dificuldade em distinguir o que é real, sofrendo desvantagem em Testes de Percepção por 10 minutos.",
            "Requisitos": "O alvo precisa estar confuso, al\"coolizado ou vulnerável emocionalmente."
        },
        {
            "Nome": "Dupla Personalidade",
            "Nível": "3",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode influenciar um alvo a assumir um comportamento oposto ao seu natural por 10 minutos. Ele deve fazer um Teste de Sabedoria (DC 15) para resistir.",
            "Requisitos": "O alvo precisa estar emocionalmente instável."
        },
        {
            "Nome": "Explosivo de Impacto",
            "Nível": "3",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você prepara um dispositivo que pode ser arremessado e explode ao impacto, causando 3d6 de dano em um raio de 3 metros. Criaturas no raio devem fazer um Teste de Destreza (DC 15) para reduzir o dano pela metade.\"",
            "Requisitos": "Preci\"sa de pólvora e materiais inflamáveis."
        },
        {
            "Nome": "Gás Enfraquecedor",
            "Nível": "3",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você libera um gás que afeta um raio de 4 metros. Criaturas expostas devem fazer um Teste de Constituição (DC 15) ou terão desvantagem em Testes de Força e Destreza por 1d4 turnos.",
            "Requisitos": "Precisa de uma ampola de vidro e\"um reagente químico."
        },
        {
            "Nome": "Veneno Mortal",
            "Nível": "3",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você prepara um veneno que, ao ser ingerido ou aplicado em uma arma, causa 4d6 de dano ao longo de 10 minutos. O alvo pode fazer um Teste de Constituição (DC 15) para reduzir o dano pela metade.",
            "Requisitos": "Precisa de substâncias\"altamente tóxicas."
        },
        {
            "Nome": "Neutralizador de Veneno",
            "Nível": "3",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode criar um antídoto capaz de remover os efeitos de venenos comuns e drogas.",
            "Requisitos": "Precisa de ingredientes alquímicos e um laboratório improvisado."
        },
        {
            "Nome": "Imagem Avançada",
            "Nível": "3",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode criar uma ilusão visual de até 2 metros de altura, que dura 10 minutos e pode se mover dentro da área desejada. Criaturas podem fazer um Teste de Inteligência (DC 15) para perceber a farsa.",
            "Requisitos": "Precisa de um obj\"eto focalizador como um espelho ou cristal."
        },
        {
            "Nome": "Som Atmosférico",
            "Nível": "3",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode gerar um ambiente sonoro falso (murmúrios, trovões, batidas) em um raio de 12 metros por 10 minutos.",
            "Requisitos": "Precisa estar em um ambiente onde o som possa ecoar."
        },
        {
            "Nome": "Ofuscação Total",
            "Nível": "3",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode fazer sua presença parecer insignificante, reduzindo sua chance de ser notado. Criaturas que não estiverem focadas em você devem fazer um Teste de Percepção (DC 15) para perceber sua presença.",
            "Requisitos": "Precisa estar\"em meio a uma multidão ou ambiente caótico."
        },
        {
            "Nome": "Chamado do Além",
            "Nível": "3",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você cria um efeito ritualístico assustador. Criaturas supersticiosas dentro de 9 metros devem fazer um Teste de Sabedoria (DC 15) ou ficarão amedrontadas por 1 minuto.",
            "Requisitos": "Precisa de um símbolo ritualístico ou um ambi\"ente adequado (cemitério, altar, ruínas)."
        },
        {
            "Nome": "Marca Espiritual",
            "Nível": "3",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode desenhar um símbolo que cria desconforto em quem o vê. Criaturas supersticiosas devem fazer um Teste de Sabedoria (DC 15) ou evitarão o local por medo.",
            "Requisitos": "Precisa de tinta especial ou sangue."
        },
        {
            "Nome": "Domínio da Palavra",
            "Nível": "3",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode convencer um grupo de até 6 pessoas dentro de 6 metros a seguir suas ordens por 1d4 turnos, desde que as ordens não sejam obviamente prejudiciais a eles.",
            "Requisitos": "Precisa estar em um ambiente onde sua voz possa\"se propagar (praça, templo, reunião)."
        },
        {
            "Nome": "Exibição Divina",
            "Nível": "3",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode criar um efeito visual simbólico (luz que brilha sobre você, sombras alongadas, fogo falso) que impressiona espectadores e aumenta sua credibilidade. NPCs religiosos fazem um Teste de Sabedoria (DC 15) pa\"ra res\"istir à crença de que você tem poder sobrenatural.",
            "Requisitos": "Precisa estar em um ambiente de crença religiosa ou usar um símbolo de poder."
        },
        {
            "Nome": "Sugestão Absoluta",
            "Nível": "4",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode ordenar uma ação complexa para um alvo dentro de 9 metros, que deve fazer um Teste de Sabedoria (DC 16). Se falhar, ele seguirá a ordem por até 1 hora ou até completar a tarefa.",
            "Requisitos": "O alvo precisa estar ou\"vindoe consciente."
        },
        {
            "Nome": "Controle Emocional",
            "Nível": "4",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode induzir um alvo dentro de 6 metros a sentir uma emoção específica (medo, raiva, tristeza, confiança). Ele deve fazer um Teste de Sabedoria (DC 16) para resistir. O efeito dura 10 minutos.",
            "Requisitos": "O alvo preci\"sa estar emocionalmente vulnerável."
        },
        {
            "Nome": "Implantação de Memória",
            "Nível": "4",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode modificar ou implantar uma lembrança no alvo. Ele deve fazer um Teste de Inteligência (DC 16). Se falhar, lembrará do evento como se fosse real.",
            "Requisitos": "A interação precisa durar pelo menos 5 minutos."
        },
        {
            "Nome": "Marionete Humana",
            "Nível": "4",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode induzir um alvo a imitar seus movimentos por 1d4 turnos. Ele deve fazer um Teste de Sabedoria (DC 16) para resistir.",
            "Requisitos": "Precisa estar a 3 metros do alvo e ser visível para ele."
        },
        {
            "Nome": "Explosivo Devastador",
            "Nível": "4",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você cria uma carga que pode ser detonada remotamente, causando 5d6 de dano em um raio de 6 metros. Criaturas na área fazem um Teste de Destreza (DC 16) para reduzir o dano pela metade.",
            "Requisitos": "Precisa de pólvora, chumb\"o e umdetonador mecânico."
        },
        {
            "Nome": "Gás Paralisante",
            "Nível": "4",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você libera um gás que cobre 6 metros de raio. Criaturas expostas devem fazer um Teste de Constituição (DC 16) ou ficarão paralisadas por 1d4 turnos.",
            "Requisitos": "Precisa de um composto químico refinado e um frasco pressurizado."
        },
        {
            "Nome": "Veneno Letal",
            "Nível": "4",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você cria um veneno mortal que, quando ingerido ou aplicado em uma arma, causa 6d6 de dano ao longo de 1 minuto. O alvo pode fazer um Teste de Constituição (DC 16) para reduzir o dano pela metade.",
            "Requisitos": "Precisa de substâncias\"altamente tóxicas e tempo para refiná-las."
        },
        {
            "Nome": "Elixir da Imunidade",
            "Nível": "4",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode criar um tônico que concede imunidade a venenos e doenças por 1 hora.",
            "Requisitos": "Precisa de ingredientes medicinais raros."
        },
        {
            "Nome": "Imagem Persistente",
            "Nível": "4",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode criar uma ilusão visual e auditiva de até 3 metros de altura, que dura 30 minutos. Criaturas podem fazer um Teste de Inteligência (DC 16) para perceber a farsa.",
            "Requisitos": "Precisa de um objeto focalizador como um es\"pelhoou cristal."
        },
        {
            "Nome": "Desaparecimento Fantasma",
            "Nível": "4",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode se tornar praticamente invisível em sombras ou fumaça por 5 minutos. Criaturas que tentarem te detectar fazem um Teste de Percepção (DC 16).",
            "Requisitos": "Precisa estar em um ambiente com sombras fortes ou neblin\"a."
        },
        {
            "Nome": "Duplicata Realista",
            "Nível": "4",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode criar uma ilusão idêntica a si mesmo que imita seus gestos por 1 minuto. Criaturas que atacarem você devem fazer um Teste de Inteligência (DC 16) ou atacarão a cópia.",
            "Requisitos": "Precisa estar em um local aberto onde\"a cópia possa se mover."
        },
        {
            "Nome": "Camuflagem Perfeita",
            "Nível": "4",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você se mistura completamente ao ambiente, ganhando vantagem em Furtividade por 10 minutos.",
            "Requisitos": "Precisa de roupas ou materiais que combinem com o ambiente."
        },
        {
            "Nome": "Visão Profética",
            "Nível": "4",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode convencer um grupo de até 10 pessoas de que previu um evento. Elas devem fazer um Teste de Sabedoria (DC 16) ou acreditar que suas previsões são reais.",
            "Requisitos": "Precisa de um ambiente cerimonial ou um objeto simbó\"lico."
        },
        {
            "Nome": "Marca do Destino",
            "Nível": "4",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode marcar um alvo com um símbolo místico visível apenas para certas pessoas. Ele dura 24 horas e pode ser reconhecido por outros cultistas ou seguidores.",
            "Requisitos": "Precisa de tinta ritualística ou sangue."
        },
        {
            "Nome": "Domínio Coletivo",
            "Nível": "4",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode influenciar um grupo de até 6 pessoas dentro de 9 metros para que sigam suas ordens por 1d4 turnos.",
            "Requisitos": "Precisa estar discursando ou realizando um gesto chamativo."
        },
        {
            "Nome": "Chama do Juízo",
            "Nível": "4",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode acender um fogo ritualístico que brilha intensamente, criando um efeito intimidador em quem vê. Criaturas supersticiosas devem fazer um Teste de Sabedoria (DC 16) ou ficarão amedrontadas.",
            "Requisitos": "Precisa de madeir\"a, óleo inflamável e um símbolo ritualístico."
        },
        {
            "Nome": "Submissão Total",
            "Nível": "5",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode comandar um alvo dentro de 9 metros a seguir uma ordem específica por até 1 hora. Ele deve fazer um Teste de Sabedoria (DC 18) para resistir.",
            "Requisitos": "O alvo precisa confiar minimamente em você ou estar em estado\"de vulnerabilidade emocional."
        },
        {
            "Nome": "Reformulação Mental",
            "Nível": "5",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode modificar traços da personalidade de um alvo, tornando-o mais agressivo, pacífico ou manipulável. Ele deve fazer um Teste de Inteligência (DC 18) ou aceitar a mudança como natural.",
            "Requisitos": "O alvo precisa est\"ar emuma conversa prolongada ou exposto a um estado alterado de consciência (álcool, meditação, exaustão)."
        },
        {
            "Nome": "Desconexão da Realidade",
            "Nível": "5",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Um alvo dentro de 9 metros deve fazer um Teste de Sabedoria (DC 18) ou perderá a conexão com o presente, agindo de forma confusa por 1d6 turnos.",
            "Requisitos": "O alvo deve estar em uma situação de estresse psicológico ou\"confusão."
        },
        {
            "Nome": "Controle de Grupo",
            "Nível": "5",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você pode influenciar até 5 alvos dentro de 6 metros, induzindo-os a seguir uma sugestão geral por 1 minuto. Eles fazem um Teste de Sabedoria (DC 18) para resistir.",
            "Requisitos": "Precisa estar discursando ou em uma posição de\"liderança."
        },
        {
            "Nome": "Explosão Demolidora",
            "Nível": "5",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você cria um dispositivo capaz de destruir estruturas e causar 6d6 de dano em um raio de 9 metros. Criaturas na área devem fazer um Teste de Destreza (DC 18) para reduzir o dano pela metade.",
            "Requisitos": "Precisa de pólvora re\"forçada, chumbo e um mecanismo de ativação."
        },
        {
            "Nome": "Nevoeiro Corrosivo",
            "Nível": "5",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você libera um gás tóxico que cobre um raio de 9 metros. Criaturas dentro da área fazem um Teste de Constituição (DC 18) ou sofrem 4d6 de dano ácido ao longo de 1 minuto.",
            "Requisitos": "Precisa de compostos químicos refinados e\"um método de dispersão."
        },
        {
            "Nome": "Toxina Letal",
            "Nível": "5",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode criar um veneno quase indetectável que, quando ingerido ou aplicado em uma arma, causa 8d6 de dano ao longo de 5 minutos. O alvo pode fazer um Teste de Constituição (DC 18) para reduzir o dano pela metade.",
            "Requisitos": "Pre\"cisa de veneno natural altamente refinado."
        },
        {
            "Nome": "Elixir do Imortal",
            "Nível": "5",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você pode criar um tônico que concede imunidade a venenos, doenças e efeitos intoxicantes por 24 horas.",
            "Requisitos": "Precisa de ingredientes extremamente raros e um laboratório improvisado."
        },
        {
            "Nome": "Miragem Perfeita",
            "Nível": "5",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode criar uma ilusão visual e auditiva de até 6 metros de altura, que dura 1 hora. Criaturas podem fazer um Teste de Inteligência (DC 18) para perceber a farsa.",
            "Requisitos": "Precisa de um objeto focalizador como um espelho\"ou cristal."
        },
        {
            "Nome": "Desvanecimento Total",
            "Nível": "5",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode desaparecer completamente por 5 minutos, tornando-se indetectável por métodos normais. Criaturas que tentarem te encontrar devem fazer um Teste de Percepção (DC 18).",
            "Requisitos": "Precisa estar em um ambiente onde se\"ja possível se esconder (sombra, multidão, fumaça)."
        },
        {
            "Nome": "Duplicata Perfeita",
            "Nível": "5",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode criar uma cópia idêntica de si mesmo que dura 10 minutos e pode se mover independentemente. Criaturas que atacarem você devem fazer um Teste de Inteligência (DC 18) ou atacarão a cópia.",
            "Requisitos": "Precisa estar em u\"m local aberto onde a cópia possa se mover livremente."
        },
        {
            "Nome": "Invisibilidade Sensorial",
            "Nível": "5",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você pode se tornar imperceptível para um alvo específico, que não notará sua presença a menos que seja tocado diretamente. O efeito dura 1 minuto.",
            "Requisitos": "Precisa de um foco para confundir o alvo (barulho, multidão,\"fumaça)."
        },
        {
            "Nome": "Influência Massiva",
            "Nível": "5",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode convencer um grupo de até 20 pessoas dentro de 9 metros de que suas palavras são a verdade absoluta. Eles devem fazer um Teste de Sabedoria (DC 18) ou seguirão suas instruções por 1 hora.",
            "Requisitos": "Precisa estar\"em umambiente de autoridade ou cerimonial (igreja, assembleia, tribunal)."
        },
        {
            "Nome": "Marca de Temor",
            "Nível": "5",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode marcar um local ou pessoa com um símbolo místico visível apenas para certos indivíduos. Quem vê a marca deve fazer um Teste de Sabedoria (DC 18) ou evitará o local por medo.",
            "Requisitos": "Precisa de um material ritualís\"tico ou um objeto consagrado."
        },
        {
            "Nome": "Domínio Completo",
            "Nível": "5",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode influenciar até 10 alvos dentro de 9 metros para que sigam suas ordens por 1d6 turnos.",
            "Requisitos": "Precisa estar em um evento público ou com seguidores fiéis."
        },
        {
            "Nome": "Manifestação Divina",
            "Nível": "5",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você pode criar um efeito visual avassalador (um raio atingindo um altar, fogo surgindo do nada, sombras se movimentando) que impressiona espectadores e reforça sua autoridade. NPCs supersticiosos fazem um Test\"e de S\"abedoria (DC 18) para resistir.",
            "Requisitos": "Precisa de um local sagrado ou uma ferramenta cerimonial (medalhão, cajado, insígnia)."
        },
        {
            "Nome": "Toque Incômodo",
            "Nível": "0",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "Você toca brevemente um inimigo e sussurra algo desconcertante. O alvo deve fazer um Teste de Sabedoria (DC 12) ou sofre desvantagem na próxima jogada de ataque.",
            "Requisitos": "O alvo precisa ser tocado voluntária ou involuntaria\"mente."
        },
        {
            "Nome": "Palma de Repulsa",
            "Nível": "0",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você ativa uma pequena reação química na palma da mão que emite uma faísca abrupta. O alvo deve fazer um Teste de Destreza (DC 12) ou é empurrado 1,5 metro para trás.",
            "Requisitos": "Precisa ter um reagente químico leve na mão."
        },
        {
            "Nome": "Fagulha Ilusória",
            "Nível": "0",
            "Tipo": "Ilusões e Truques",
            "Descrição": "Você projeta uma centelha ilusória que simula o início de um ataque. O alvo deve fazer um Teste de Reflexos (DES, DC 12) ou perde a reação até o próximo turno.",
            "Requisitos": "Alvo precisa estar olhando em sua direção."
        },
        {
            "Nome": "Escudo Simbólico",
            "Nível": "0",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Um símbolo breve brilha em sua frente ao ser atacado. Você rola 1d4 e adiciona esse valor ao seu PA contra o próximo ataque.",
            "Requisitos": "Precisa sussurrar o nome de uma divindade ou entidade protetora."
        },
        {
            "Nome": "Submissão Final",
            "Nível": "5",
            "Tipo": "Hipnose e Manipulação",
            "Descrição": "O alvo a até 6 metros deve fazer um Teste de Sabedoria (DC 18) ou ficará de joelhos, solta sua arma e não poderá agir por 1 turno.",
            "Requisitos": "O alvo precisa estar visivelmente ferido ou abalado"
        },
        {
            "Nome": "Carga Magnética",
            "Nível": "3",
            "Tipo": "Alquimia e Ciência",
            "Descrição": "Você prende uma pequena cápsula no alvo que atrai metais. No próximo ataque com arma metálica contra ele, o atacante rola com vantagem.",
            "Requisitos": "O alvo precisa estar usando ou próximo a metal"
        },
        {
            "Nome": "Barreira de Fé",
            "Nível": "2",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Você ergue um símbolo místico no chão. Aliados dentro de 3 metros ganham +2 no CA por 1 turno.",
            "Requisitos": "Um símbolo religioso esculpido ou desenhado"
        },
        {
            "Nome": "Ídolo Incandescente",
            "Nível": "4",
            "Tipo": "Rituais e Misticismo",
            "Descrição": "Um totem temporário é invocado e brilha como se abençoado. Criaturas inimigas em 6 metros devem fazer um Teste de Sabedoria (DC 16) ou sofrem -2 nas jogadas de ataque até o fim da cena.",
            "Requisitos": "Deve estar em área ceri\"monialou com símbolo consagrado"
        }
    ]

        self.truques_por_classe = {
            "Charlatão": {
                1: [("Hipnose e Manipulação", None)],
                5: [("Hipnose e Manipulação", ["Hipnotizador", "Língua de Prata"])],
                7: [("Ilusões e Truques", ["Dissimulado"])],
                10: [("Hipnose e Manipulação", ["Hipnotizador", "Língua de Prata"])]
            },
            "Sacerdote": {
                1: [("Rituais e Misticismo", None)],
                5: [
                    ("Rituais e Misticismo", ["Orador Visionário"]),
                    ("Ilusões e Truques", ["Manipulador Místico"])
                ],
                7: [("Alquimia e Ciência", ["Manipulador Místico"])],
                10: [("Rituais e Misticismo", ["Orador Visionário"])]
            },
            "Sabotador": {
                1: [("Alquimia e Ciência", None)],
                5: [("Ilusões e Truques", ["Espião"])],
                10: [("Alquimia e Ciência", ["Assassino Urbano"])]
            },
            "Erudito": {
                3: [("Alquimia e Ciência", ["Alquimista"])],
                7: [("Alquimia e Ciência", ["Engenheiro"])],
                10: [
                    ("Alquimia e Ciência", ["Alquimista"]),
                    ("Alquimia e Ciência", ["Engenheiro"])
                ]
            }
        }

    # Função para cálculo do modificador de atributo
    def calcular_nivel(self, personagem):
        classes = personagem.get("classes", [])
        if classes:
            niveis = defaultdict(int)
            especializacoes = {}
            for entrada in classes:
                nome = entrada["classe"]
                niveis[nome] = max(niveis[nome], entrada["nivel"])
                if "especializacao" in entrada:
                    especializacoes[nome] = entrada["especializacao"]
            nivel_total = sum(niveis.values())
            texto_classes = [
                f"{c} {niveis[c]} ({especializacoes[c]})" if especializacoes.get(c) else f"{c} {niveis[c]}"
                for c in niveis
            ]
            return nivel_total, ' | '.join(texto_classes)

        # ⚠️ Corrige erro ao não haver classes
        return 0, "Sem Classe"

    # Função para bônus de proficiência
    def calcular_bonus_proficiencia(self, nivel_total):
        return self.bonus_proficiencia_por_nivel.get(nivel_total, 2)

    # ====== Inicialização de Personagem ======
    def inicializar_personagem(self):
        return {
            "nome_jogador": "", "nome": "", "idade": 18, "altura": 170, "peso": 70,
            "genero": "", "etnia": "", "etnia_idx": 0, "genero_idx": 0,
            "origem": "", "historia": "", "imagem": None,
            "atributos_finais": {
            "Força": {"base": 8, "bonus_manual": 0, "final": 8},
            "Destreza": {"base": 8, "bonus_manual": 0, "final": 8},
            "Constituição": {"base": 8, "bonus_manual": 0, "final": 8},
            "Inteligência": {"base": 8, "bonus_manual": 0, "final": 8},
            "Sabedoria": {"base": 8, "bonus_manual": 0, "final": 8},
            "Carisma": {"base": 8, "bonus_manual": 0, "final": 8}
            },
            "habilidades": {}, "classes": [], "equipamento": {},
            "inventario": [], "truques": [],
            "misticismo": {"slots": {}, "arsenal": []},
            "status_gerais": {
                "hp": "10", "ca": "10", "velocidade": "6",
                "iniciativa": "0", "bonus_proficiencia": "1"
            },

            "tema_visual": {"brasao": None, "estilo": "pergaminho"},
            "versao": "1.0", "data_criacao": None
        }

    def calcular_status_gerais(self, personagem):
        def mod(val): return (val - 10) // 2

        nivel_total = len(personagem["classes"])
        atributos = personagem.get("atributos_finais", {})
        mod_des = mod(atributos.get("Destreza", {}).get("final", 10))
        mod_con = mod(atributos.get("Constituição", {}).get("final", 10))
        mod_sab = mod(atributos.get("Sabedoria", {}).get("final", 10))

        bonus_prof = 2 + ((nivel_total - 1) // 4)

        armadura = personagem.get("equipamentos", {}).get("armadura")
        arma_cc = personagem.get("equipamentos", {}).get("arma_cc")

        # Velocidade
        velocidade = 6
        if isinstance(armadura, str) and ("Cota de Malha" in armadura or "Brigandina" in armadura):
            velocidade -= 1
        elif armadura == "Armadura de Placas":
            velocidade -= 3
        if not isinstance(armadura, str):
            armadura = ""
        velocidade += personagem.get("bonus_velocidade", 0)

        # CA (Classe de Armadura)
        if armadura == "Roupas Leves":
            ca = 10 + max(mod_des,0)
        elif armadura == "Couro Reforçado":
            ca = 12 + max(mod_des,0)
        elif armadura == "Cota de Malha":
            ca = 14 + min(max(mod_des,0), 2)
        elif armadura == "Roupas Clericais":
            ca = 11 + max(mod_sab,0)
        elif armadura == "Brigandina":
            ca = 15
        elif armadura == "Armadura de Placas":
            ca = 17
        else:
            ca = 10

        # HP
        hp = 6 * nivel_total + mod_con * bonus_prof

        # Iniciativa
        iniciativa = max(mod_des,0) + (1 if arma_cc == "Sabre" else 0)

        personagem["status_gerais"] = {
            "hp": hp,
            "ca": ca,
            "velocidade": velocidade,
            "iniciativa": iniciativa,
            "bonus_proficiencia": bonus_prof
        }

        return personagem

    # Salva os atributos finais detalhadamente
    def calcular_atributos_finais(self, personagem, bonus_classe, bonus_manual_externo=None):
        personagem["atributos_finais"] = personagem.get("atributos_finais", {})

        # Inicializa se necessário
        for attr in self.atributos_base:
            if attr not in personagem["atributos_finais"]:
                personagem["atributos_finais"][attr] = {
                    "base": 8,
                    "bonus_classe": 0,
                    "bonus_manual": 0,
                    "final": 8
                }

        # Determina os atributos que receberam +1 e +2 a partir das classes
        manual_bonus = {attr: 0 for attr in self.atributos_base}
        if bonus_manual_externo:  # opcional, usado na aba de edição
            attr1 = bonus_manual_externo.get("+1")
            attr2 = bonus_manual_externo.get("+2")
            if attr1:
                manual_bonus[attr1] += 1
            if attr2:
                manual_bonus[attr2] += 2
        else:
            # Caso esteja só lendo o JSON já preenchido, usa os próprios valores armazenados
            for attr in self.atributos_base:
                manual_bonus[attr] = personagem["atributos_finais"].get(attr, {}).get("bonus_manual", 0)

        # Recalcula todos os valores finais
        for attr in self.atributos_base:
            base = personagem["atributos_finais"][attr].get("base", 8)
            bonus_m = manual_bonus.get(attr, 0)
            bonus_cl = bonus_classe.get(attr, 0)
            final = base + bonus_m + bonus_cl

            personagem["atributos_finais"][attr] = {
                "base": base,
                "bonus_classe": bonus_cl,
                "bonus_manual": bonus_m,
                "final": final
            }

        return personagem

    # Calcula bônus vindos de classe
    def calcular_bonus_classe(self, personagem, classes):
        bonus = {attr: 0 for attr in self.atributos_base}
        for entrada in classes:
            if entrada.get("bonus") == "atributo" and entrada.get("atributo_escolhido"):
                bonus[entrada["atributo_escolhido"]] += 1
        return bonus
    
    def tipos_truques_disponiveis(self, personagem):
        tipos = set()
        nivel_total = len(personagem.get("classes", []))
        for entrada in personagem.get("classes", []):
            classe = entrada["classe"]
            especializacao = entrada.get("especializacao")

            if classe in self.truques_por_classe:
                for nivel, truques in self.truques_por_classe[classe].items():
                    if nivel <= nivel_total:
                        for tipo, requisito in truques:
                            if requisito is None or (especializacao and especializacao in requisito):
                                tipos.add(tipo)
        return tipos
