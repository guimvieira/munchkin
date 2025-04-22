import random
import time


# --- Classes de Cartas --- #
class Carta:
    def __init__(self, nome, efeito, tipo):
        self.nome = nome
        self.efeito = efeito
        self.tipo = tipo  # 'porta' ou 'tesouro'

    def __str__(self):
        return f"Carta: {self.nome}, Efeito: {self.efeito}, Tipo: {self.tipo}"


class CartaDePorta(Carta):
    def __init__(self, nome, efeito, tipo, monstro=None, maldicao=None, raca=None, classe=None):
        super().__init__(nome, efeito, tipo)
        self.monstro = monstro
        self.maldicao = maldicao
        self.raca = raca
        self.classe = classe


class CartaDeTesouro(Carta):
    def __init__(self, nome, tipo, valor, boosts=None, restricoes=None):
        super().__init__(nome, None, tipo)
        self.valor = valor # Valor do item em ouro
        self.restricoes = restricoes or {}
        self.boosts = boosts or {}
    

class CartaEquipamento(CartaDeTesouro):
    def __init__(self, nome, tipo, valor, boosts=None, restricoes=None):
        super().__init__(nome, tipo, valor, boosts, restricoes)

    def pode_equipar(self, jogador):
        # Verifica as restrições de cada carta de equipamento
        if 'classe' in self.restricoes:
            if jogador.classe.__class__.__name__ not in self.restricoes['classe']:
                print(f"\n{jogador.nome} não pode equipar {self.nome} devido à sua classe.")
                return False

        if 'raça' in self.restricoes:
            if jogador.raca not in self.restricoes['raça']:
                print(f"\n{jogador.nome} não pode equipar {self.nome} devido à sua raça.")
                return False

        if 'sexo' in self.restricoes:
            if jogador.sexo not in self.restricoes['sexo']:
                print(f"\n{jogador.nome} não pode equipar {self.nome} devido ao seu sexo.")
                return False

        if self.tipo == "Arma mao unica":
            if len([item for item in jogador.itens_equipados if item.tipo == "Arma mao unica"]) >= 2:
                print(f"\n{jogador.nome} não pode equipar mais de 2 armas de mão única.")
                return False

            if len([item for item in jogador.itens_equipados if item.tipo == "Arma mao dupla"]) >= 1:
                print(f"\n{jogador.nome} não pode equipar uma arma de mão única junto com uma arma de mão dupla.")
                return False

        if self.tipo == "Arma mao dupla":
            if len([item for item in jogador.itens_equipados if item.tipo == "Arma mao dupla"]) >= 1:
                print(f"\n{jogador.nome} já possui uma arma de mão dupla equipada.")
                return False

            if len([item for item in jogador.itens_equipados if item.tipo == "Arma mao unica"]) >= 1:
                print(f"\n{jogador.nome} não pode equipar uma arma de mão dupla junto com uma arma de mão única.")
                return False

        return True

    def __str__(self):
        return f"{self.nome} (Valor: {self.valor} de ouro)"



class Maldicao(CartaDePorta):
    def __init__(self, nome, efeito):
        super().__init__(nome, efeito, 'porta', maldicao=True)

    def aplicaEfeito(self, jogador):
        # Função para aplicar efeitos das maldições (não foi implementada ainda)
        print(f"Aplicando maldição: {self.efeito} ao jogador {jogador.nome}")


class Monstro(CartaDePorta):
    def __init__(self, nome, efeito, nivel, efeito_derrota, recompensas=None, modificadores_poder=None):
        super().__init__(nome, efeito, 'porta', monstro=True)
        self.nivel = nivel
        self.recompensas = recompensas if recompensas else []
        self.efeito_derrota = efeito_derrota
        self.modificadores_poder = modificadores_poder if modificadores_poder else {}

    def aplicar_efeito_derrota(self, jogador):
        # Função para diminuir níveis e remover cartas da mão e equipadas após derrota em combate
        if isinstance(self.efeito_derrota, list):
            for efeito in self.efeito_derrota:
                if isinstance(efeito, dict):
                    for acao, quantidade in efeito.items():
                        if acao == "perder nivel":
                            jogador.descer_nivel(quantidade)
                        elif acao == "perder cartas":
                            jogador.perder_cartas(quantidade)
                        elif acao == "perder itens":
                            jogador.perder_itens_equipados(quantidade)
        elif isinstance(self.efeito_derrota, dict):
            for acao, quantidade in self.efeito_derrota.items():
                if acao == "perder nivel":
                    jogador.descer_nivel(jogador, quantidade)
                elif acao == "perder cartas":
                    jogador.perder_cartas_mao(jogador, quantidade)
                elif acao == "perder itens":
                    jogador.perder_itens_equipados(jogador, quantidade)

    def calcular_poder(self, jogador):
        # Função que calcula o poder do monstro com base na raça, sexo ou classe do jogador que está enfrentando
        # (ainda não implementada)
        poder_monstro = self.nivel

        if "Classe" in self.modificadores_poder and jogador.classe:
            classe_nome = jogador.classe.nome if jogador.classe.nome in self.modificadores_poder["Classe"] else None
            if classe_nome:
                poder_monstro += self.modificadores_poder["Classe"].get(classe_nome, 0)

        if "Raça" in self.modificadores_poder and jogador.raca:
            raca_nome = jogador.raca.nome if jogador.raca.nome in self.modificadores_poder["Raça"] else None
            if raca_nome:
                poder_monstro += self.modificadores_poder["Raça"].get(raca_nome, 0)

        if "Sexo" in self.modificadores_poder and jogador.sexo:
            if jogador.sexo in self.modificadores_poder["Sexo"]:
                poder_monstro += self.modificadores_poder["Sexo"].get(jogador.sexo, 0)

        return poder_monstro


    def __str__(self):
        return self.nome


class Raca(CartaDePorta):
    def __init__(self, nome, efeito, vantagens):
        super().__init__(nome, efeito, 'porta', raca=True)
        self.vantagens = vantagens

    def ativaVantagem(self, jogador):
        # Função que ativa vantagem de uma raça (ainda não implementada)
        print(f"Jogador {jogador.nome} recebe as vantagens de ser {self.nome}.")


class Classe(CartaDePorta):
    def __init__(self, nome, efeito, restricao, beneficios, habilidade=None):
        super().__init__(nome, efeito, 'porta', classe=True)
        self.restricao = restricao
        self.beneficios = beneficios

    def aplicaBeneficio(self, jogador):
        # Função que aplica os benefícios de uma classe (parcialmente implementada)
        print(f"Jogador {jogador.nome} recebeu o benefício da classe {self.nome}.")
        for beneficio in self.beneficios:
            beneficio(jogador)

    def habilidade_default(self, jogador, *args, **kwargs):
        # Habilidade default para jogadores com classe "Comum" (sem classe)
        print(f"A classe {self.nome} não tem habilidades especiais.")


class Ladrao(Classe):
    def __init__(self):
        super().__init__(
            nome = "Ladrão",
            efeito = None,
            restricao = None,
            beneficios = [],
            habilidade = self.roubar
        )

    def roubar(self, jogador, jogadores):
        # Habilidade única de Ladrão
        if not jogador.mao.cartas_na_mao:
            print(F"{jogador.nome} não tem cartas para descartar e tentar roubar.")
            return

        carta_descartada = jogador.mao.cartas_na_mao.pop(random.randint(0, len(jogador.mao) - 1))
        print(f"{jogador.nome} descartou a carta: {carta_descartada}")

        print("Escolha um alvo para tentar roubar um item pequeno: ")
        jogadores_disponiveis = [alvo for alvo in jogadores if alvo != jogador]
        for i, alvo in enumerate(jogadores_disponiveis, start=1):
            print(f"{i}. {alvo.nome}")

        try:
            escolha = int(input("Digite o número do jogador alvo: "))
            jogador_escolhido = jogadores_disponiveis[escolha - 1]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return
        
        itens_pequenos = [item for item in jogador_escolhido.itens_equipados if isinstance(item, CartaEquipamento) and item.tamanho == "Pequeno"]

        if not itens_pequenos:
            print(f"{jogador_escolhido.nome} não tem itens pequenos para roubar.")
            return
        
        dado = random.randint(1, 6)
        print(f"{jogador.nome} jogou o dado e tirou: {dado}")

        if dado >= 4:
            item_roubado = random.choice(itens_pequenos)
            jogador_escolhido.itens_equipados.remove(item_roubado)
            jogador.itens_equipados.append(item_roubado)
            print(f"{jogador.nome} roubou o item: {item_roubado} de {jogador_escolhido.nome}!")
        else:
            print(f"{jogador.nome} falhou no roubo e perdeu um nível!")
            jogador.descer_nivel()


class Guerreiro(Classe):
    def __init__(self):
        super().__init__(
            nome = "Guerreiro",
            efeito = None,
            restricao = None,
            beneficios = [],
            habilidade = self.furia
        )

    def furia(self, jogador):
        # Habilidade única de Guerreiro
        if len(jogador.mao.cartas_na_mao) == 0:
            print(f"Você não tem cartas suficientes para utilizar a habilidade Fúria.\n")
            return

        print(f"{jogador.nome} está ficando enfurecido!")
        print("Escolha até 3 cartas da sua mão para descartar e aumentar a sua força:\n")
        print("Cartas na mão:")
        for i, carta in enumerate(jogador.mao.cartas_na_mao, 1):
            print(f"{i}. {carta.nome}")

        try:
            escolha = int(input("Escolha quantas cartas deseja descartar (0 para não usar a habilidade): "))
            if escolha == 0:
                print(f"{jogador.nome} decidiu não usar a habilidade Fúria.")
                return

            if escolha > 3:
                print("Você pode descartar no máximo 3 cartas. Tentando descartar 3 cartas.")
                escolha = 3

            if escolha > len(jogador.mao.cartas_na_mao):
                print(f"{jogador.nome} não tem cartas suficientes na mão para descarregar {escolha} cartas!")
                return

            cartas_descartadas = []
            for _ in range(escolha):
                carta_escolhida = int(input(f"Escolha a carta para descartar (1 a {len(jogador.mao.cartas_na_mao)}): "))
                carta = jogador.mao.cartas_na_mao.pop(carta_escolhida - 1)
                cartas_descartadas.append(carta)
                jogador.jogo.baralho_descarte.adicionar_carta(carta)

            jogador.forca += escolha
            print(f"{jogador.nome} descartou {escolha} carta(s) e aumentou sua força para {jogador.forca}!")

        except (ValueError, IndexError):
            print("Escolha inválida! Tente novamente.")


# --- Classes de Baralho --- #
class Baralho:
    def __init__(self, cartas=None):
        self.cartas = cartas or []

    def embaralhar(self):
        # Reembaralha o baralho
        random.shuffle(self.cartas)

    def tirar_carta(self):
        # Tira uma carta do baralho
        if self.cartas:
            return self.cartas.pop()
        return None

    def adicionar_carta(self, carta):
        # Adiciona uma carta ao baralho
        self.cartas.append(carta)


class BaralhoPorta(Baralho):
    def __init__(self, cartas=None):
        super().__init__(cartas)

    def tirar_carta(self):
        # Herda tirar_carta de Baralho, mas contém uma verificação para ver se o baralho está vazio
        if not self.cartas:  
            print("O baralho de portas está vazio!")
            return None  

        carta = super().tirar_carta()  
        if carta:
            print(f"Carta de porta tirada!")
        return carta


class BaralhoTesouro(Baralho):
    def __init__(self, cartas=None):
        super().__init__(cartas)

    def tirar_carta(self):
        # Herda tirar_carta de Baralho
        carta = super().tirar_carta()
        if carta:
            print(f"Carta de tesouro tirada!")
        return carta


class BaralhoDescarte(Baralho):
    def __init__(self, cartas=None):
        super().__init__(cartas)

    def adicionar_carta(self, carta):
        # Adiciona cartas ao baralho de descarte
        self.cartas.append(carta)

    def reembaralhar_porta(self, baralho_porta):
        # Quando baralho de porta fica sem cartas, essa função é chamada e reembaralha as cartas de porta que aqui estão
        # e as mandam de volta para o baralho de porta
        baralho_porta.cartas.extend(self.cartas)
        self.cartas = []
        baralho_porta.embaralhar()

    def reembaralhar_tesouro(self, baralho_tesouro):
        # Quando baralho de tesouro fica sem cartas, essa função é chamada e reembaralha as cartas de tesouro que aqui estão
        # e as mandam de volta para o baralho de tesouro
        baralho_tesouro.cartas.extend(self.cartas)
        self.cartas = []
        baralho_tesouro.embaralhar()


class MaoJogador:
    def __init__(self, baralho_descarte):
        self.cartas_na_mao = []  
        self.baralho_descarte = baralho_descarte

    def adicionar_cartas(self, cartas):
        # Adiciona cartas na mão do jogador
        self.cartas_na_mao.extend(cartas)

    def mostrar_cartas(self):
        print(f"Cartas na sua mão: {[str(carta) for carta in self.cartas_na_mao]}")

    def remover_carta(self, carta, descartar=True):
        # Remove cartas da mão do jogador
        if carta in self.cartas_na_mao:
            self.cartas_na_mao.remove(carta)
            if descartar:
                self.baralho_descarte.adicionar_carta(carta)
    
    def quantidade_cartas(self):
        return len(self.cartas_na_mao)


# --- Classes do Jogo e Jogador --- #
class Jogador:
    def __init__(self, nome, baralho_descarte, jogo, classe=None):
        self.nome = nome
        self.nivel = 1
        self.forca = 1
        self.mao = MaoJogador(baralho_descarte)
        self.jogo = jogo
        self.itens_em_jogo = []
        self.itens_equipados = []
        self.raca = "Humano"
        self.classe = classe if classe else Classe("Comum", "Sem efeito", "Sem restrição", [])
        self.ouro = 0
        self.baralho_descarte = baralho_descarte

    def subir_nivel(self, quantidade=1):
        # Sobe nível do jogador no fim de um combate com base na recompensa
        if self.nivel < 10:
            self.nivel += quantidade
            if self.nivel > 10:
                self.nivel = 10
            print(f"{self.nome} subiu para o nível {self.nivel}!")

    def descer_nivel(self, quantidade=1):
        # Desce nível do jogador no fim de um combate com base na recompensa
        if self.nivel > 1:
            self.nivel -= quantidade
            self.nivel = max(self.nivel, 1)
            print(f"{self.nome} desceu para o nível {self.nivel}!")
        else:
            print(f"{self.nome} já está no Nível 1, não pode descer de nível.")

    def adicionar_raca(self, nova_raca):
        # Equipa uma carta de Raça no jogador (não foi implementado ainda)
        if self.raca:
            print(f"{self.nome} já possui é da raça {self.raca.nome}. Se tornando um {nova_raca.nome}")
        else:
            print(f"{self.nome} agora é da raça {nova_raca.nome}.")

        self.raca = nova_raca
        self.classe.ativaVantagem(self)

    def adicionar_classe(self, nova_classe):
        # Equipa uma carta de Classe no jogador
        if self.classe:
            print(f"{self.nome} já possui a classe {self.classe.nome}. Substituindo por {nova_classe.nome}")
        else:
            print(f"{self.nome} agora tem a classe {nova_classe.nome}.")

        self.classe = nova_classe
        self.classe.aplicaBeneficio(self)

        if nova_classe in self.mao.cartas_na_mao:
            self.mao.cartas_na_mao.remove(nova_classe)

    def equipar_item(self):
        # Equipa itens de equipamento no jogador
        print(f"\n{self.nome}, escolha os itens para equipar na sua preparação:")

        itens_equipaveis = [item for item in self.mao.cartas_na_mao if isinstance(item, CartaEquipamento)]

        if not itens_equipaveis:
            print("Você não tem itens equipáveis na sua mão!")
            return

        print("Itens disponíveis para equipar:")
        for i, item in enumerate(itens_equipaveis, 1):
            print(f"{i}. {item.nome} - {item.tipo}")

        itens_para_equipar = []
        while len(itens_para_equipar) < 4:
            try:
                escolha = int(input("Escolha o número do item para equipar (0 para parar): "))
                if escolha == 0:
                    break

                item_escolhido = itens_equipaveis[escolha - 1]

                if item_escolhido.pode_equipar(self):
                    # Verifica se já possui um item de um determinado tipo equipado
                    if item_escolhido.tipo == "Capacete":
                        if any(item.tipo == "Capacete" for item in self.itens_equipados):
                            print(f"\n{self.nome} já possui um capacete equipado.")
                        else:
                            self.itens_equipados.append(item_escolhido)
                            self.mao.cartas_na_mao.remove(item_escolhido)
                            print(f"\n{item_escolhido.nome} foi equipado.")
                    elif item_escolhido.tipo == "Armadura":
                        if any(item.tipo == "Armadura" for item in self.itens_equipados):
                            print(f"\n{self.nome} já possui uma armadura equipada.")
                        else:
                            self.itens_equipados.append(item_escolhido)
                            self.mao.cartas_na_mao.remove(item_escolhido)
                            print(f"\n{item_escolhido.nome} foi equipado.")
                    elif item_escolhido.tipo == "Botas":
                        if any(item.tipo == "Botas" for item in self.itens_equipados):
                            print(f"\n{self.nome} já possui um par de botas equipado.")
                        else:
                            self.itens_equipados.append(item_escolhido)
                            self.mao.cartas_na_mao.remove(item_escolhido)
                            print(f"\n{item_escolhido.nome} foi equipado.")
                    elif item_escolhido.tipo == "Arma mao unica":
                        if len([item for item in self.itens_equipados if item.tipo == "Arma mao unica"]) < 2:
                            self.itens_equipados.append(item_escolhido)
                            self.mao.cartas_na_mao.remove(item_escolhido)
                            print(f"\n{item_escolhido.nome} foi equipado.")
                        else:
                            print(f"\n{self.nome} já tem duas armas de mão única equipadas.")
                    elif item_escolhido.tipo == "Arma mao dupla":
                        if len([item for item in self.itens_equipados if item.tipo == "Arma mao dupla"]) < 1:
                            self.itens_equipados.append(item_escolhido)
                            self.mao.cartas_na_mao.remove(item_escolhido)
                            print(f"\n{item_escolhido.nome} foi equipado.")
                        else:
                            print(f"\n{self.nome} já possui uma arma de mão dupla equipada.")
                    else:
                        print(f"\n{item_escolhido.nome} não pode ser equipado neste momento.")

            except (ValueError, IndexError):
                print("Escolha inválida! Tente novamente.")
                continue

        print(f"\nVocê equipou os seguintes itens: {[item.nome for item in self.itens_equipados]}")

    def usar_item(self, item):
        print(f"{self.nome} usou {item.nome}.")

    def abrir_porta(self, baralho_porta):
        # Jogador abre a porta
        if not baralho_porta.cartas:
            print(f"\nO baralho de portas está vazio. Reembaralhando cartas do descarte...")
            self.baralho_descarte.reembaralhar_porta(baralho_porta)
            time.sleep(3)
        carta = baralho_porta.tirar_carta()
        if carta:
            if isinstance(carta, Monstro):
                print(f"Jogador entrou em combate com o monstro {carta.nome}")
                time.sleep(1)
            elif isinstance(carta, Maldicao):
                carta.aplicaEfeito(self)
            else:
                print(f"Carta de porta não tem efeito especial.")
            return carta
        else:
            print(f"{self.nome} não conseguiu abrir a porta porque o baralho está vazio.")
        return None

    def adicionar_carta_tesouro(self, quantidade=1, baralho_tesouro=None):
        # Tira uma carta de tesouro
        if not baralho_tesouro.cartas:
            print(f"O baralho de tesouro está vazio. Reembaralhando cartas do descarte...")
            self.baralho_descarte.reembaralhar_tesouro(baralho_tesouro)
        
        for _ in range(quantidade):
            carta = baralho_tesouro.tirar_carta()
            if carta:
                self.mao.cartas_na_mao.append(carta)
                print(f"{self.nome} ganhou a carta de tesouro: {carta}")
                time.sleep(0.5)

    def perder_cartas(self, quantidade=1):
        # Perde cartas da sua mão
        if len(self.mao.cartas_na_mao) == 0:
            print(f"{self.nome} não tem cartas para perder.")
            time.sleep(1)
            return

        print(f"{self.nome} perde {quantidade} carta(s) de sua mão.")
        for _ in range(quantidade):
            if len(self.mao.cartas_na_mao) > 0:
                carta = self.mao.cartas_na_mao.pop(random.randint(0, len(self.mao.cartas_na_mao) - 1))
                self.baralho_descarte.adicionar_carta(carta)
                print(f"{self.nome} perdeu a carta: {carta}")
            else:
                print(f"{self.nome} não possui cartas em sua mão suficientes para perder!")

    def perder_itens_equipados(self, quantidade=1):
        # Jogador perde itens que estão equipados
        print(f"{self.nome} perde {quantidade} item(s) equipado(s).")
        for _ in range(quantidade):
            if self.itens_equipados:
                item = self.itens_equipados.pop(random.randint(0, len(self.itens_equipados) - 1))
                self.baralho_descarte.adicionar_carta(item)
                print(f"{self.nome} perdeu o item previamente equipado: {item}")
            else:
                print(f"{self.nome} não possui itens equipados suficientes para perder!")

    def procurar_por_encrenca(self):
        # Jogador procura por encrenca (caso não tenha encontrado um monstro ao chutar uma porta)
        monstros_na_mao = [carta for carta in self.mao.cartas_na_mao if isinstance(carta, Monstro)]

        if not monstros_na_mao:
            print(f"{self.nome} não tem monstros na mão para procurar encrenca!")
            return

        print(f"{self.nome} está procurando por encrenca! Escolha um monstro para enfrentar: ")
        print("\n")

        for i, monstro in enumerate(monstros_na_mao, 1):
            print(f"{i}. {monstro.nome} (Nível: {monstro.nivel})")

        try:
            escolha = int(input(f"Escolha o número do monstro para enfrentar: "))
            monstro_escolhido = monstros_na_mao[escolha - 1]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return

        print(f"{self.nome} decidiu procurar encrenca com {monstro_escolhido.nome}!")
        combate = Combate(self, monstro_escolhido, self.jogo.baralho_tesouro, self.jogo.jogadores)
        combate.iniciar_combate(self)

    def usar_habilidade(self):
        # Usa a sua habilidade com base na sua classe equipada
        if isinstance(self.classe, Ladrao):
            self.classe.roubar(self, self.jogo.jogadores)
        elif isinstance(self.classe, Guerreiro):
            self.classe.furia(self)

    def __str__(self):
        return f"{self.nome} - Raça: {self.raca.nome}, Classe: {self.classe.nome}"


class Personagem:
    def __init__(self, nome, sexo):
        self.nome = nome
        self.sexo = sexo  # Pode ser "Masculino" ou "Feminino"

    def __str__(self):
        return f"{self.nome} ({self.sexo})"

  
class Restricao:
    def __init__(self, tipo, restricoes):
        self.tipo = tipo 
        self.restricoes = restricoes 

    def verifica_restricao(self, jogador):
        # Verifica as restrições para itens serem equipados
        if self.tipo == "raça":
            return jogador.raca.nome in self.restricoes
        elif self.tipo == "classe":
            return jogador.classe.nome in self.restricoes
        elif self.tipo == "sexo":
            return jogador.personagem.sexo in self.restricoes
        return False


class Combate:
    def __init__(self, jogador, monstro, baralho_tesouro, jogadores, ajudantes=None):
        self.jogador = jogador
        self.monstro = monstro
        self.ajudantes = ajudantes or []
        self.estado = "Em andamento"
        self.fuga = False
        self.baralho_tesouro = baralho_tesouro
        self.pedir_ajuda = None
        self.jogadores = jogadores

    def poder_atual(self):
        # Calcula o poder atual do jogador com base nos seus equipamentos e se possui ajudantes
        poder_total = self.jogador.forca
        for item in self.jogador.itens_equipados:
            for tipo_boost, valor in item.boosts.items():
                if tipo_boost == "poder":
                    poder_total += valor
        if self.pedir_ajuda and self.pedir_ajuda.aceito:
            poder_total += self.pedir_ajuda.jogador_ajudante.forca
            for item in self.pedir_ajuda.jogador_ajudante.itens_equipados:
                for tipo_boost, valor in item.boosts.items():
                    if tipo_boost == "poder":
                        poder_total += valor
        return poder_total

    def iniciar_combate(self, jogador):
        # Mecânica principal do combate
        print(f"\nIniciando combate entre {self.jogador.nome} e {self.monstro.nome}\n")
        time.sleep(1)

        poder_monstro = self.monstro.calcular_poder(jogador)
        poder_jogador = self.poder_atual()

        if self.pedir_ajuda and self.pedir_ajuda.aceito:
            print(f"\nO poder do jogador {self.jogador.nome} está em {poder_jogador} (Com ajudantes)")
        else:
            print(f"\nO poder do jogador {self.jogador.nome} está em {poder_jogador}")
        print(f"O poder do monstro {self.monstro.nome} está em {poder_monstro}")

        while True:
            print("\nEscolha uma ação:")
            print("1. Lutar com o monstro")
            print("2. Tentar fugir do combate")

            try:
                escolha = int(input("Digite o número da ação que deseja realizar: "))

                if escolha == 1:
                    input("\nPressione ENTER para seguir para o combate...")
                    break 
                elif escolha == 2:
                    self.tentar_fugir()
                    return 
                else:
                    print("Escolha inválida, tente novamente.")
            except ValueError:
                print("Escolha inválida, tente novamente.")

        if poder_jogador > poder_monstro:
            print(f"\n{self.jogador.nome} venceu o monstro {self.monstro.nome}!")
            time.sleep(1)
            self.terminar_combate(vitoria=True)
        elif poder_jogador == poder_monstro and jogador.classe.nome == "Guerreiro":
            # Habilidade passiva de Guerreiro
            print(f"\n{self.jogador.nome} venceu o monstro {self.monstro.nome}!")
            time.sleep(1)
            self.terminar_combate(vitoria=True)
        else:
            print(f"\n{self.jogador.nome} perdeu para o monstro {self.monstro.nome}!")
            time.sleep(1)
            self.terminar_combate(vitoria=False)

    def terminar_combate(self, vitoria):
        # Termina o combate e entrega as recompensas/aplica efeito de derrota
        if vitoria:
            print(f"{self.jogador.nome} ganhou tesouros!")

            # Não consegui fazer o print ficar mais bonito
            recompensa = ', '.join([str(item) for item in self.monstro.recompensas])
            print(f"As recompensas conquistadas: {recompensa}")
            
            time.sleep(1)
            self.aplicar_recompensas()

            if self.pedir_ajuda and self.pedir_ajuda.aceito:
                self.pedir_ajuda.aplicar_recompensas()


    def tentar_fugir(self):
        # Mecânica para tentar fugir do combate
        sucesso = random.randint(1, 6) >= 4
        print(f"\nVocê tirou {sucesso} no dado.\n")
        if sucesso:
            print(f"{self.jogador.nome} fugiu do combate!")
        else:
            print(f"{self.jogador.nome} falhou ao tentar fugir!")
            self.jogador.descer_nivel()

    def aplicar_recompensas(self):
        # Aplica as recompensas de vitória no combate
        for recompensa in self.monstro.recompensas:
            tipo, quantidade = recompensa
            if tipo == "nivel":
                self.jogador.subir_nivel(quantidade)
            elif tipo == "carta tesouro":
                self.jogador.adicionar_carta_tesouro(quantidade, self.baralho_tesouro)

    def pedir_ajuda(self):
        # Mecânica de pedir ajuda (não consegui implementar 100% funcional)
        print(f"{self.jogador.nome}, você precisa de ajuda para derrotar o monstro {self.monstro.nome}!")
        print("Escolha um jogador para pedir ajuda:")

        for i, jogador in enumerate(self.jogadores, start=1):
            print(f"{i}. {jogador.nome}")
        
        try:
            escolha = int(input("Escolha o número do jogador que deseja como ajudante: "))
            
            if escolha < 1 or escolha > len(self.jogadores):
                print("Escolha inválida! Nenhum ajudante selecionado.")
                return None
            
            jogador_ajudante = self.jogadores[escolha - 1]
            
            if jogador_ajudante == self.jogador:
                print("Você é incrível, mas não pode pedir ajuda a si mesmo!")
                return None
            
            pedido_ajuda = PedirAjuda(self.jogador, jogador_ajudante)
            pedido_ajuda.aceitar_participacao()
            
        except (ValueError, IndexError):
            print("Escolha inválida, tente novamente.")

    def negociar_recompensa(self, cartas_de_tesouro):
        # Negocia a recompensa (não foi implementado ainda)
        if self.pedir_ajuda:
            self.pedir_ajuda.negociar_recompensa(cartas_de_tesouro)


class PedirAjuda:
    def __init__(self, jogador_ajudante, combate):
        self.jogador_ajudante = jogador_ajudante
        self.combate = combate
        self.aceito = False
        self.recompensas = []

    def negociar_recompensa(self, cartas_de_tesouro):
        # Negocia a recompensa (não foi implementado ainda)
        self.recompensas = cartas_de_tesouro
        print(f"A recompensa negociada foi: {', '.join([carta.nome for carta in self.recompensas])}")
        self.aceito = True

    def aceitar_participacao(self):
        # Aceita/Rejeita participação em um combate
        escolha = input(f"{self.jogador_ajudante.nome}, você aceita ajudar no combate? (s/n) ")
        if escolha == 's':
            self.aceito = True
            print(f"{self.jogador_ajudante.nome} aceitou ajudar no combate!")
        else:
            print(f"{self.jogador_ajudante.nome} recusou o pedido de ajuda.")
            return self.aceito

    def aplicar_recompensas(self):
        # Aplica recompensas para o ajudante (não foi implementado ainda)
        if self.aceito:
            for carta in self.recompensas:
                print(f"{self.jogador_ajudante.nome} recebeu as seguintes cartas como recompensa: {carta.nome}")
                self.jogador_ajudante.receber_item(carta)
        else:
            print(f"{self.jogador_ajudante.nome} não ajudou no combate.")


class Fase:
    def __init__(self, nome):
        self.nome = nome
        self.fim = False

    def inicio_fase(self):
        # Inicia fase
        print(f"Iniciando a fase: {self.nome}")

    def fim_fase(self):
        # Termina fase
        self.fim = True
        print(f"Fim da fase: {self.nome}")


class Turno:
    def __init__(self, jogador):
        self.jogador = jogador
        self.fase_atual = None
        self.fim = False
        self.numero_turno = 0

    def iniciar_fase(self, fase):
        # Inicia fase do turno
        self.fase_atual = fase
        self.fase_atual.inicio_fase()

    def avancar_fase(self):
        # Avança fase do turno
        if self.fase_atual:
            self.fase_atual.fim_fase()
        self.fase_atual = None
        print(f"Avançando para a próxima fase.")

    def fim_turno(self):
        # Termina fase do turno
        self.fim = True
        print(f"Fim do turno de {self.jogador.nome}")


class GerenciaCartas:
    def __init__(self):
        self.cartas_porta = []
        self.cartas_tesouro = []

    def criar_cartas(self):
        # Cria as cartas de Monstro, Maldição, Equipamento, Classes (itens e raças ainda não implementados)
        monstros = [
            Monstro("3872 Orcs", "+6 contra Anões", 10, efeito_derrota=[{"perder nivel": 1}, {"perder itens": random.randint(1, 6)}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Large Angry Chicken", None, 2, efeito_derrota=[{"perder nivel": 1}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Flying Frogs", None, 2, efeito_derrota=[{"perder nivel": 1}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Harpies", "+5 contra Magos", 4, efeito_derrota=[{"perder nivel": 2}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Lame Goblin", None, 1, efeito_derrota=[{"perder nivel": 1}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Net Troll", None, 10, efeito_derrota=[{"perder cartas": random.randint(1, 6)}], recompensas=[("nivel", 1), ("carta tesouro", 3)]),
            Monstro("Undead Horse", "+5 contra Anões", 5, efeito_derrota=[{"perder cartas": 2}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Crabs", None, 1, efeito_derrota=[{"perder itens": 4}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Bigfoot", None, 12, efeito_derrota=[{"perder itens": 1}], recompensas=[("nivel", 1), ("carta tesouro", 3)]),
            Monstro("Lawyers", None, 6, efeito_derrota=[{"perder cartas": 5}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Drooling Slime", "+4 contra Elfos", 1, efeito_derrota=[{"perder itens": 1}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Gazebo", None, 8, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Ghoulfiends", None, 9, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Insurance Salesman", None, 14, efeito_derrota=[{"perder cartas": 3}], recompensas=[("nivel", 1), ("carta tesouro", 4)]),
            Monstro("Leprechaun", None, 4, efeito_derrota=[{"perder cartas": 2}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Maul Rat", "+3 contra Clérigos", 1, efeito_derrota=[{"perder nivel": 1}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Mr. Bones", None, 2, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("PitBull", None, 2, efeito_derrota=[{"perder nivel": 2}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Platycore", "+6 contra Magos", 6, efeito_derrota=[{"perder nivel": 2}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Plutonium Dragon", None, 20, efeito_derrota=[{"perder cartas": 6}, {"perder nivel": 3}], recompensas=[("nivel", 2), ("carta tesouro", 5)]),
            Monstro("Amazon", None, 8, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Bullrog", None, 18, efeito_derrota=[{"perder cartas": 6}, {"perder nivel": 3}], recompensas=[("nivel", 2), ("carta tesouro", 5)]),
            Monstro("Face Sucker", None, 8, efeito_derrota=[{"perder itens": 1}, {"perder nivel": 1}], recompensas=[("carta tesouro", 2)]),
            Monstro("Floating Nose", None, 10, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 3)]),
            Monstro("Gelatinous Octahedron", None, 2, efeito_derrota=[{"perder cartas": 2}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Hippogriff", None, 16, efeito_derrota=[{"perder cartas": 4}], recompensas=[("nivel", 2), ("carta tesouro", 4)]),
            Monstro("King Tut", None, 16, efeito_derrota=[{"perder cartas": 6}, {"perder nivel": 2}, {"perder itens": 5}], recompensas=[("nivel", 2), ("carta tesouro", 4)]),
            Monstro("Potted Plant", None, 1, efeito_derrota=[{"perder nivel": 0}], recompensas=[("nivel", 1), ("carta tesouro", 1)]),
            Monstro("Pukachu", None, 6, efeito_derrota=[{"perder cartas": 6}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
            Monstro("Tongue Demon", None, 12, efeito_derrota=[{"perder nivel": 2}], recompensas=[("nivel", 1), ("carta tesouro", 3)]),
            Monstro("Wight Brothers", None, 16, efeito_derrota=[{"perder nivel": 9}], recompensas=[("nivel", 2), ("carta tesouro", 4)]),
            Monstro("Wannabe Vampire", None, 12, efeito_derrota=[{"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 3)]),
            Monstro("Squidzilla", None, 18, efeito_derrota=[{"perder cartas": 6}, {"perder nivel": 3}], recompensas=[("nivel", 2), ("carta tesouro", 4)]),
            Monstro("Stoned Golem", None, 14, efeito_derrota=[{"perder cartas": 6}, {"perder nivel": 3}], recompensas=[("nivel", 1), ("carta tesouro", 4)]),
            Monstro("Snails on Speed", None, 4, efeito_derrota=[{"perder cartas": 4}], recompensas=[("nivel", 1), ("carta tesouro", 2)]),
        ]
        for monstro in monstros:
            self.cartas_porta.append(monstro)
        
        maldicoes = [
            Maldicao("Maldição! Perca sua classe", "Jogador perde sua classe"),
            Maldicao("Maldição! Troque sua classe", "Jogador deve trocar sua classe"),
            Maldicao("Maldição! Troque de sexo", "Jogador deve trocar de sexo"),
            Maldicao("Maldição! Pato do destino", "Jogador perde 2 níveis"),
            Maldicao("Maldição! Perca um nível", "Jogador perde 1 nível"),
            Maldicao("Maldição! Perca sua raça", "Jogador perde sua raça"),
            Maldicao("Maldição! Espelho maligno", "Jogador não ganhará efeitos bônus de itens além da Armadura"),
            Maldicao("Maldição! Perca duas cartas", "Jogador perde duas cartas"),
            Maldicao("Maldição! Perca suas botas", "Jogador perde suas botas"),
            Maldicao("Maldição! Perca um item pequeno", "Jogador perde um item pequeno"),
        ]
        for maldicao in maldicoes:
            self.cartas_porta.append(maldicao)
        
        tesouros = [
            CartaEquipamento("Bandana Maneira", "Capacete", 400, boosts={"poder": 3}, restricoes={"raça": "Anão", "raça": "Elfo", "raça": "Halfling"}),
            CartaEquipamento("Botas de Chutar Traseiro", "Botas", 400, boosts={"poder": 2}),
            CartaEquipamento("Armadura Flamejante", "Armadura", 400, boosts={"poder": 2}),
            CartaEquipamento("Armadura Gosmenta", "Armadura", 200, boosts={"poder": 1}),
            CartaEquipamento("Armadura Pequena e Larga", "Armadura", 400, boosts={"poder": 3}, restricoes={"raça": "Humano", "raça": "Halfling", "raça": "Elfo"}),
            CartaEquipamento("Chapéu Pontudo Poderoso", "Capacete", 400, boosts={"poder": 3}, restricoes={"classe": "Mago"}),
            CartaEquipamento("Armadura Mithril", "Armadura", 600, boosts={"poder": 3}, restricoes={"classe": "Ladrão", "classe": "Guerreiro", "classe": "Clerigo", "classe": "Comum"}),
            CartaEquipamento("Armadura de Couro", "Armadura", 200, boosts={"poder": 1}),
            CartaEquipamento("Botas de Corrida", "Botas", 400, boosts={"poder": 2}),
            CartaEquipamento("Capa da Escuridão", "Armadura", 600, boosts={"poder": 4}, restricoes={"classe": "Ladrão"}),
            CartaEquipamento("Elmo da Coragem", "Capacete", 200, boosts={"poder": 1}),
            CartaEquipamento("Capacete Pontudo", "Capacete", 600, boosts={"poder": 3}, restricoes={"raça": "Elfo"}),
            CartaEquipamento("Espada Grande", "Arma mao unica", 400, boosts={"poder": 3}),
            CartaEquipamento("Broquel Violento", "Arma mao unica", 400, boosts={"poder": 3}),
            CartaEquipamento("Serra Elétrica do Desmembramento", "Arma mao dupla", 600, boosts={"poder": 3}),
            CartaEquipamento("Ralador de Queijo da Paz", "Arma mao unica", 400, boosts={"poder": 3}, restricoes={"classe": "Clerigo"}),
            CartaEquipamento("Adaga da Traição", "Arma mao unica", 400, boosts={"poder": 3}, restricoes={"classe": "Ladrão"}),
            CartaEquipamento("Poste de 11 pés", "Arma mao dupla", 200, boosts={"poder": 1}),
            CartaEquipamento("Porrete do Cavalheiro", "Arma mao unica", 400, boosts={"poder": 3}),
            CartaEquipamento("Pedra Enorme", "Arma mao dupla", 0, boosts={"poder": 3}),
            CartaEquipamento("Cetro da Afiação", "Arma mao unica", 600, boosts={"poder": 4}, restricoes={"classe": "Clerigo"}),
            CartaEquipamento("Florete da Injustiça", "Arma mao unica", 400, boosts={"poder": 3}, restricoes={"raça": "Elfo"}),
            CartaEquipamento("Rato no Palito", "Arma mao unica", 0, boosts={"poder": 0}),
            CartaEquipamento("Espada dos Cantos e Danças", "Arma mao unica", 400, boosts={"poder": 2}, restricoes={"classe": "Clerigo", "classe": "Guerreiro", "classe": "Mago", "classe": "Comum"}),
            CartaEquipamento("Escudo da Ubiquidade", "Arma mao dupla", 600, boosts={"poder": 4}, restricoes={"classe": "Ladrão", "classe": "Clerigo", "classe": "Mago", "classe": "Comum"}),
            CartaEquipamento("Esapada Sorrateira Bastarda", "Arma mao unica", 200, boosts={"poder": 2}),
            CartaEquipamento("Cetro de Napalm", "Arma mao unica", 800, boosts={"poder": 5}, restricoes={"classe": "Mago"}),
            CartaEquipamento("Arma do Exército Suíço", "Arma mao dupla", 600, boosts={"poder": 4}, restricoes={"raça": "Humano"})
        ]
        for tesouro in tesouros:
            self.cartas_tesouro.append(tesouro)

        classes = [
            Ladrao(), Ladrao(), Ladrao(), Guerreiro(), Guerreiro(), Guerreiro()
        ]
        for classe in classes:
            self.cartas_porta.append(classe)

    def obter_cartas_porta(self):
        return self.cartas_porta

    def obter_cartas_tesouro(self):
        return self.cartas_tesouro


class Jogo:
    def __init__(self):
        self.jogadores = []
        self.gerenciador_de_cartas = GerenciaCartas()
        self.personagens_selecionaveis = []
        self.baralho_porta = BaralhoPorta()
        self.baralho_tesouro = BaralhoTesouro()
        self.baralho_descarte = BaralhoDescarte()
        self.turno_atual = 0

    def criar_personagens(self):
        # Cria os personagens selecionáveis
        Alistair = Personagem("Alistair", "Masculino")
        Erna = Personagem("Erna", "Feminino")
        Galadriel = Personagem("Galadriel", "Feminino")
        Astrid = Personagem("Astrid", "Feminino")
        Skadi = Personagem("Skadi", "Feminino")
        Kali = Personagem("Kali", "Feminino")
        Dakini = Personagem("Dakini", "Feminino")
        Svend = Personagem("Svend", "Masculino")
        Davor = Personagem("Davor", "Masculino")
        Jax = Personagem("Jax", "Masculino")
        Nelian = Personagem("Nelian", "Masculino")
        Ulf = Personagem("Ulf", "Masculino")

        self.personagens_selecionaveis = [Alistair, Astrid, Davor, Erna, Galadriel, Jax, Kali, Nelian, Skadi, Svend, Dakini, Ulf]

    def selecionar_personagem(self):
        # Seleciona o personagem
        print("Escolha um personagem: ")
        for i, personagem in enumerate(self.personagens_selecionaveis):
            print(f"{i + 1}. {personagem}")

        escolha = -1
        while escolha < 0 or escolha >= len(self.personagens_selecionaveis):
            try:
                escolha = int(input("\nDigite o número do personagem que deseja utilizar: ")) - 1
                if escolha < 0 or escolha >= len(self.personagens_selecionaveis):
                    print("Escolha inválida, por favor tente novamente.")
            except ValueError:
                print("Entrada inválida, por favor escolha um número.")

        return self.personagens_selecionaveis[escolha]

    def definir_jogadores(self):
        # Mecânica que define a quantidade de jogadores (min. 3 e max. 6)
        while True:
            try:
                num_jogadores = int(input("Quantos jogadores no jogo? "))
                if 6 >= num_jogadores > 2:
                    break
                else:
                    print("Número de jogadores deve ser entre 3 e 6.")
            except ValueError:
                print("Entrada inválida, por favor escolha um número entre 3 e 6.")

        for i in range(num_jogadores):
            nome = input(f"Nome do jogador {i + 1}: ")
            print("\n")
            jogador = Jogador(nome, self.baralho_descarte, self)
            jogador.personagem = self.selecionar_personagem()

            self.jogadores.append(jogador)

    def iniciar_jogo(self):
        # Inicia o jogo
        print("--------------------------------------------------------------------------")
        print("|                      Seja bem-vindo(a) ao MUNCHKIN!                    |")
        print("--------------------------------------------------------------------------")
        print("\n")
        time.sleep(1)
        input("Pressione ENTER para continuar...")
        print("\n")
        self.criar_personagens()
        self.definir_jogadores()  
        self.gerenciador_de_cartas.criar_cartas()
        self.baralho_porta.cartas = self.gerenciador_de_cartas.obter_cartas_porta()
        self.baralho_tesouro.cartas = self.gerenciador_de_cartas.obter_cartas_tesouro()
        self.baralho_porta.embaralhar()
        self.baralho_tesouro.embaralhar()

        if not self.baralho_porta.cartas:
            print("Erro: O baralho de portas está vazio ao iniciar o jogo!")
            return

        for jogador in self.jogadores:
            cartas_porta = []
            cartas_tesouro = []
            for _ in range(4):
                carta_porta = self.baralho_porta.tirar_carta()
                if carta_porta:
                    cartas_porta.append(carta_porta)

                carta_tesouro = self.baralho_tesouro.tirar_carta()
                if carta_tesouro:
                    cartas_tesouro.append(carta_tesouro)

            jogador.mao.adicionar_cartas(cartas_porta + cartas_tesouro)

    def jogar_turno(self, jogador):
        # Mecânica de turnos pra cada jogador, podendo escolher suas ações
        print(f"\n--- Turno de {jogador.nome} ---")
        time.sleep(1)
        
        print(f"\nInformações do jogador {jogador.nome}:")
        print(f"Nível: {jogador.nivel}")
        
        if jogador.itens_equipados:
            print("Itens Equipados:")
            for item in jogador.itens_equipados:
                print(f"- {item.nome}")
        else:
            print("Nenhum item equipado.")

        if jogador.mao.cartas_na_mao:
            print("Cartas na mão:")
            for carta in jogador.mao.cartas_na_mao:
                print(f"- {carta.nome}")
        else:
            print("Nenhuma carta na mão.")
        
        input("\nPressione ENTER para prosseguir...")

        # Fase 1: Preparação do personagem
        print(f"\nPreparação do personagem de {jogador.nome}.")
        
        while True:
            print("\nEscolha uma opção:")
            print("1. Equipar itens")
            print("2. Usar habilidade")
            print("3. Adicionar classe")
            print("4. Abrir a porta")
            print("\n")
            try:
                escolha = int(input("Escolha o número da ação que deseja realizar: "))
                
                if escolha == 1:
                    jogador.equipar_item()
                elif escolha == 2:
                    jogador.usar_habilidade()
                elif escolha == 3:
                    self.adicionar_classe_jogador(jogador)
                elif escolha == 4:
                    break
            except ValueError:
                print("Escolha inválida, tente novamente.")
        
        # Fase 2: Chutar a porta
        carta_aberta = jogador.abrir_porta(self.baralho_porta)
        
        if carta_aberta is None:
            print(f"\nJogador {jogador.nome} não conseguiu abrir a porta, tentando novamente.")
            return

        print(f"Jogador {jogador.nome} abriu a porta e obteve: {carta_aberta.nome}")
        time.sleep(1)

        if isinstance(carta_aberta, Monstro):
            # Fase 3: Combate
            combate = Combate(jogador, carta_aberta, self.baralho_tesouro, self.jogadores)
            combate.iniciar_combate(jogador)
        elif isinstance(carta_aberta, Maldicao):
            # Fase 3.1: Procurar por encrenca
            jogador.procurar_por_encrenca()
        else:
            # Fase 4: Saquear a sala
            carta_tesouro = self.baralho_tesouro.tirar_carta()
            if carta_tesouro:
                print(f"{jogador.nome} saqueou: {carta_tesouro.nome}")

        # Fase 5: Caridade
        self.caridade(jogador)

    def caridade(self, jogador):
        # Mecânica de caridade (não está funcionando 100% do jeito que eu gostaria)
        total_cartas = len(jogador.mao.cartas_na_mao)

        if total_cartas > 5:
            print(f"{jogador.nome} tem mais de 5 cartas, iniciando a caridade...")
            excedentes = total_cartas - 5

            menor_nivel = None
            for outro_jogador in self.jogadores:
                if outro_jogador != jogador:
                    if menor_nivel is None or outro_jogador.nivel < menor_nivel.nivel:
                        menor_nivel = outro_jogador

            if menor_nivel:
                print(f"Jogador de nível mais baixo: {menor_nivel.nome}")
                time.sleep(1.5)

                if jogador.nivel == menor_nivel.nivel:
                    print(f"Serão descartadas {excedentes} cartas por {jogador.nome}")
                    while excedentes > 0:
                        if jogador.mao.cartas_na_mao:
                            carta_descartada = jogador.mao.cartas_na_mao.pop()
                            print(f"{jogador.nome} descartou {carta_descartada.nome}.")
                            excedentes -= 1
                            time.sleep(1)
                        else:
                            print(f"{jogador.nome} não tem mais cartas para descartar.")
                            break
                else:
                    print(f"{jogador.nome} vai doar {excedentes} cartas para {menor_nivel.nome}.")
                    for _ in range(excedentes):
                        if jogador.mao.cartas_na_mao:
                            carta_doada = jogador.mao.cartas_na_mao.pop()
                            print(f"{jogador.nome} doou {carta_doada.nome} para {menor_nivel.nome}.")
                            menor_nivel.mao.cartas_na_mao.append(carta_doada)
                            time.sleep(1)
                        else:
                            print(f"{jogador.nome} não tem mais cartas para doar.")
                            break
            else:
                print(f"Não há jogadores com nível mais baixo que {jogador.nome}.")

    def verificar_fim_de_jogo(self):
        # Verificador para ver se alguém chegou ao nível 10
        for jogador in self.jogadores:
            if jogador.nivel == 10:
                print(f"{jogador.nome} alcançou o nível máximo e venceu o jogo!")
                return True
        return False

    def executar_turnos(self):
        # Executa o loop do jogo
        while True:
        
            jogador = self.jogadores[self.turno_atual % len(self.jogadores)]
        
            self.jogar_turno(jogador)

            if self.verificar_fim_de_jogo():
                break

            self.turno_atual += 1

    def adicionar_classe_jogador(self, jogador):
        # Equipa a classe no jogador dentro do turno
        print(f"{jogador.nome}, você tem as seguintes cartas na mão:")
        for i, carta in enumerate(jogador.mao.cartas_na_mao, 1):
            print(f"{i}. {carta.nome}")

        try:
            escolha = int(input("Escolha uma carta de classe para adicionar ao seu personagem (0 para não escolher): ")) - 1

            if escolha == -1:
                print(f"{jogador.nome} decidiu não adicionar nenhuma classe.")
                return

            carta_escolhida = jogador.mao.cartas_na_mao[escolha]

            if isinstance(carta_escolhida, Classe):  
                jogador.adicionar_classe(carta_escolhida) 
            else:
                print("Você não escolheu uma carta de classe válida.")
        except (ValueError, IndexError):
            print("Escolha inválida! Tente novamente.")

    def iniciar(self):
        # Inicializa o jogo
        self.iniciar_jogo()
        self.executar_turnos()


# --- Iniciar o jogo --- #
if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar()