#-------------------------------------------------------------------#
#                       K-Means Algorithm                           #
#-------------------------------------------------------------------#

class Point:
    """
    Em um k-means existem vários pontos.
    """

    def __init__(self, local:list):
        self.local = local

    def __repr__(self):
        return str(self.local)

    def __getitem__(self, index:int):
        return self.local[index]

    def dist(self, obj):
        """
        Distancia
        """
        resp = 0
        for i in range(len(self.local)):
            resp += abs(self.local[i] - obj.local[i])**2
        resp = resp ** (1/2)
        return resp

class K_means:
    """
    Classe K_means, faz a comparação e diz em que grupo ele está.
    Tem que receber uma lista de listas.
    """

    def __init__(self, dados:list, k:int = 2):
        self.dados = []
        for i in dados:
            self.dados.append(Point(i))
        self.k = k
        self.melhor_caso = None
        self.todos_g = []
        self.var_minima = 0

    def __repr__(self):
        for i in self.dados:
            print(i)
        return str(self.melhor_caso)

    def __getitem__(self, index:int):
        return self.dados[index]

    def carregar(self, int_):
        sleep(1)
        t = 2

        ant = int_
        demora_ant = 0
        media_demora = 0
        val_m = []
        while True:
            cont = 0
            k = len(self.grupos)
            for i in range(k):
                if self.grupos[i] != None:
                    cont += 1

            nov = cont/k * 100/int_ + self.int/int_ * 100
            try:
                demora = (100 - nov)/(nov - ant)#(nov - ant)/t * 100
            except:
                pass
            if (demora+media_demora)/(len(val_m) + 1) > 0 and len(val_m) > int_/(25 * 4):
                print(str(nov)[:5] + "% carregado, tempo estimado " + str(((demora+media_demora)/(len(val_m) + 1) - int_/(25*4))*t)[:str(((demora+media_demora)/(len(val_m) + 1) - int_/(25*4))*t).find(".")] + " segundos")
            else:
                print("Computando estimação")

            if ant == nov:
                print("Concluido")
                return

            else:
                val_m.append(demora)
                if len(val_m) > int(int_/25):
                    del val_m[0]
                media_demora = 0
                for n in val_m:
                    media_demora += n

                ant = cont/k * 100/int_ + self.int/int_ * 100
                sleep(t)

    def salvar(self, nome = "melhor_caso"):
        import json

        if nome.find(".json") == -1:
            nome += ".json"

        dic = {"dados":self.quebrar(), "melhor_caso":self.melhor_caso}

        arq = json.dumps(dic, sort_keys = False, indent = -1)
        with open(nome, "w") as file:
            file.write(arq)

        print("Salvo com o nome",nome)

    def quebrar(self):
        resp = []
        for i in self.dados:
            resp.append(i.local)
        return resp

    def run(self, interacoes = 100, print_ = True):
        """
        Faz a clusterização.
        """
        menor = None

        self.int = 0
        if print_:
            carregamento = Thread(target = self.carregar, args = [interacoes])
            carregamento.start()

        for _ in range(interacoes):
            self.int += 1
            self.grupo_priori()

            for i in range(len(self.dados)):
                if self.grupos[i] == None:
                    d = self.menor_dist(self.dados[i])
                    self.grupos[i] = d

            if menor == None:
                menor = [self.grupos, self.variancia()]

            if self.variancia() <= menor[1]:
                #print(menor[0],menor[1], "-->",self.variancia(),self.grupos)
                menor = [self.grupos, self.variancia()]

        self.melhor_caso = menor[0]
        self.var_minima = menor[1]

    def grupo_priori(self):
        """
        Cria um grupo inicial.
        """
        self.grupos = [None for i in range(len(self.dados))]
        self.grupos_p = []

        for i in range(self.k):
            n = int(random()*len(self.dados))
            while self.grupos[n] != None:
                n = int(random()*len(self.dados))
            self.grupos[n] = i

            self.grupos_p.append(self.dados[n])

        self.todos_g.append(self.grupos_p)

    def menor_dist(self, dado):
        """
        Calcula a menor distância.
        """
        men = dado.dist(self.grupos_p[0])
        men_i = 0
        for i in range(len(self.grupos_p)):
            if dado.dist(self.grupos_p[i]) <= men:
                men = dado.dist(self.grupos_p[i])
                men_i = i
        return men_i

    def media(self,grupos):
        """
        Faz a média do grupo.
        """
        resp = [0 for i in range(len(grupos[0].local))]
        mn = len(grupos)
        for i in range(mn):
            for k in range(len(grupos[0].local)):
                resp[k] += (grupos[i].local[k])/mn
        return resp

    def variancia(self):
        """
        Calcula variância geral do método.
        """
        var = 0
        for i in range(self.k):
            n = []
            for k in range(len(self.dados)):
                if self.grupos[k] == i:
                    n.append(self.dados[k])
            med = self.media(n)
            for h in range(len(med)):
                for j in range(len(n)):
                    var += (med[h] - n[j].local[h]) ** 2

        return var

def abs(a):
    """
    Pega o valor absoluto de um número.
    """
    if a > 0:
        return a
    return -a

def salvar(melhor_caso, nome = "melhor_caso"):
    import json

    if nome.find(".json") == -1:
            nome += ".json"

    dic = {"melhor_caso":melhor_caso}

    arq = json.dumps(dic, sort_keys = False, indent = -1)
    with open(nome, "w") as file:
        file.write(arq)

    print("Salvo com o nome",nome)

def normalizar(dados):
    """
    Normaliza os dados por meio do desvio padrão.
    """
    col = dados.columns
    media = []
    dv = []

    #from sklearn.preprocessing import StandardScaler
    #return StandardScaler().fit_transform(dados[col[3:]])

    for i in col[3:]:
        media.append(dados[i].mean())
        dv.append(dados[i].std())

    dados = dados.values.tolist()
    for j in range(3,len(dados[0])):
        for i in range(len(dados)):
            dados[i][j] = float(dados[i][j])/float(dv[j-3])

    dados = pd.DataFrame(dados, columns = col)

    return dados

def main(dado_, a, v, g, how):
    cluster = K_means(dado_, g)

    cluster.run(how, print_ = False)

    v.value = cluster.var_minima

    for i in range(len(cluster.melhor_caso)):
        a[i] = cluster.melhor_caso[i]

def K_MEANS_APLY(data = None, cpus = 4, groups = 2, how =  400):
    v = []
    a = []
    p_ = []
    for i in range(cpus):
        v.append(Value("f", 9*10**12))
        a.append(Array("d",len(data)))
        p_.append(Process(target = main, args = (data, a[i], v[i], groups, int(how/cpus))))
        p_[-1].start()

    for i in range(cpus):
        p_[i].join()

    mn = min(*[v[i].value for i in range(len(v))])

    for i in range(len(a)):
        if mn == v[i].value:
            salvar(a[i][:])
