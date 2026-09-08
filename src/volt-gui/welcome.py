from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from themes import get_standard_button_height
from themes import get_standard_button_width
from ui import create_simple_sidebar_widget
from ui import create_tab_content_widget


def get_welcome_settings() -> dict:
    return {
        "Bem-vindo": {
            "Bem-vindo ao volt-gui": (
                ("text", "O volt-gui é minha Alternativa ao AMD Adrenaline / NVIDIA Settings para Linux.\n\nAs configurações são aplicadas pelo volt, uma camada implícita Vulkan, então funcionam em todo driver Vulkan: RADV, ANV, NVK, AMDVLK, o driver proprietário da NVIDIA e qualquer outro que suporte Vulkan 1.0."),
                ("text", "A camada se atém ao Vulkan 1.0 base e à extensão de swapchain, então nada aqui se comporta diferente de um driver para outro."),
            )
        },
        "Como Funciona": {
            "A Camada volt": (
                ("text", "Cada configuração neste aplicativo é gravada em um arquivo de perfil em ~/.config/volt-gui/. A camada Vulkan do volt lê esse perfil quando um jogo inicia e reescreve as chamadas Vulkan que o jogo faz: amostradores para filtragem de textura e seleção de mip, a swapchain para vsync, contagem de imagens e composição, enumeração de dispositivos para seleção de GPU, presents para o limitador de quadros e pipelines para os controles de renderização."),
                ("text", "As configurações são lidas uma vez quando um jogo inicia e nunca mudam enquanto ele roda. Pressione Aplicar, depois inicie o jogo novamente. A sondagem roda novamente ao Aplicar para que as listas aqui fiquem sincronizadas."),
            ),
            "O Que Não Faz": (
                ("text", "O volt apenas muda o que o jogo pede ao Vulkan. Ele nunca desenha nada por conta própria, então nitidez, upscaling, geração de quadros, MSAA forçado e sobreposições estão fora de escopo. Use MangoHud para sobreposição e LACT para clocks e curvas de ventoinha, ou CoreCtrl se também quiser controles de CPU."),
                ("text", "Também nunca ativa nada que o jogo deixou desligado. O volt não habilita nenhum recurso de dispositivo nem extensão. Onde uma configuração precisa de um recurso, o volt lê o que o jogo pediu e aplica a configuração apenas se o jogo habilitou: é assim que Filtragem Anisotrópica, Sombreamento por Amostra, Alfa para Um e Limite de Profundidade funcionam, e onde o jogo deixou o recurso desmarcado a configuração é ignorada e uma linha é registrada. Uma configuração que não pode ser alcançada dessa forma fica de fora, o que mantém largura de linha e filtragem cúbica fora da mesa, e wireframe forçado fica de fora porque é wallhack. Onde um jogo move estado para um caminho de extensão, o volt o segue até lá: um gancho para uma extensão que o jogo nunca habilitou é simplesmente inalcançável."),
            )
        },
        "Configurações": {
            "Um Valor por Configuração": (
                ("text", "Cada configuração é uma escolha única: o valor que o volt força, ou padrão, que significa que o volt não toca no que o jogo pediu. Não há intervalo, nem ordenação entre valores, e nada para confundir."),
                ("text", "Um valor para o qual o volt não tem nome ainda aparece na lista, ainda salva no perfil e ainda aplica, exatamente como um nomeado."),
                ("text", "Onde a especificação admite apenas o que uma consulta retornou, um valor que seu dispositivo não reportou não é forçado. O volt mantém o valor do jogo e registra um aviso, então um perfil escrito em outra máquina nunca invalida uma chamada."),
                ("text", "Onde a especificação limita um valor, viés LOD contra o limite do seu dispositivo e contagem de imagens contra o que a superfície permite, o volt limita o que repassa. Esse limite é correção, não escolha, então não é mostrado aqui."),
            ),
            "De Onde Vêm as Listas": (
                ("text", "Muitas das caixas são preenchidas a partir do seu próprio hardware em vez de uma lista embutida no volt-gui. Modos de apresentação, contagens de imagem e modos alfa vêm do que a superfície reporta, a lista de GPUs vem do que o driver enumera, e anisotropia, níveis de mip e viés LOD vão até os limites que seu dispositivo oferece. Um cartão sem o recurso por trás contém apenas padrão, e todo cartão baseado em dispositivo também, até a sondagem rodar: o volt-gui não oferece opção que não leu."),
                ("text", "Isso significa que um modo de apresentação que o volt nunca ouviu falar aparece assim que seu driver o suporta. Também significa que um perfil escrito em outra máquina pode nomear algo que esta não consegue fazer, caso em que essa configuração volta ao padrão e o volt-gui diz quais."),
                ("text", "O resto traz listas fixas, porque não há nada para ler. Nearest e linear são Vulkan base sem recurso nem consulta por trás, então todo driver tem ambos e nenhum diz isso. As configurações de Taxa de Quadros não têm nada para ler: um jogo nunca diz ao Vulkan qual taxa de quadros quer, então não há nada no dispositivo para perguntar."),
            ),
            "Os Três Cartões de Filtro": (
                ("text", "Três campos de amostrador, três cartões. Nada sobrescreve nada, e toda combinação é alcançável."),
                ("text", "Na ordem ampliação, redução, mipmap:\n\n- retrô: nearest, nearest, nearest.\n- bilinear: linear, linear, nearest.\n- trilinear: linear, linear, linear.\n- pixel art nítido sem cintilação distante: nearest, linear, linear."),
                ("text", "Ampliação é o que você vê de perto. Redução é a maior parte da tela, e onde mipmaps e filtragem anisotrópica atuam. Modo Mipmap é a mistura entre níveis."),
            ),
            "O Limitador de Quadros": (
                ("text", "Limite de Quadros limita a taxa no momento da apresentação. Deslocamento desloca esse limite, Cadência define em qual taxa o limitador mira, Método define quando ele espera, Ritmo define como, e nenhum dos quatro faz nada até que Limite esteja definido."),
                ("text", "Deslocamento existe para telas com taxa variável, que querem o limite logo abaixo da atualização. Escolha 144, defina o deslocamento para -6 e você cai em 138. O volt não lê sua taxa de atualização e nunca desloca um limite sozinho, já que a maioria das telas não é VRR."),
                ("text", "Cadência é a taxa na qual o limitador mira. fixed é seu limite e nada mais. smooth ritma no mais lento dos últimos quadros, então os quadros rápidos esperam pelos lentos e a cadência sai uniforme no que a máquina está sustentando. dynamic lê exatamente o que smooth lê e então arredonda para baixo até um quarto de passo do seu limite, então fica em uma taxa fixa em vez de seguir a carga. Os passos são quartos do tempo de quadro do seu limite, então ficam próximos embaixo e distantes em cima: um limite de 60 passa por 60, 48, 40, 34, 30, enquanto um de 240 passa por 240, 192, 160, 137, 120. Ambos vêm de como consoles lidam com uma máquina que não sustenta seu alvo, que é escolher uma taxa que consegue sustentar e ficar nela. Um console reduz resolução para chegar lá e o volt não toca em resolução, então tratamento de quadros é o único lugar onde a ideia se encaixa. Um limitador só pode atrasar quadros, por isso nenhum lê a média: um quadro mais lento que a média nunca poderia ser ritmado para cima até ela. Ambos sobem sozinhos, e nenhum vai mais rápido que seu limite. A troca é quadros por uniformidade: fixed não faz nada quando a máquina cai abaixo do limite, então o que você recebe é o que a máquina produziu, um quadro longo e o próximo curto. smooth e dynamic seguram os quadros curtos para coincidir com os longos, o que custa os quadros que você teria visto e compra espaçamento uniforme. A mudança de passo do dynamic é visível, mas é uma mudança em vez de um tempo de quadro diferente a cada quadro. Use fixed se a máquina sustenta o limite, ou se quer cada quadro possível pela latência."),
                ("text", "Cadência e Método são caixas separadas porque respondem perguntas diferentes, e qualquer par funciona junto. dynamic com late mantém uma taxa fixa e ainda lê a entrada o mais próximo possível do momento de exibição."),
                ("text", "Ritmo vai do mais barato ao mais preciso. sleep entrega toda a espera ao kernel e não custa nada. sliced dorme em passos curtos e re-verifica o relógio, o que corrige quando o kernel acorda atrasado. precise dorme a maior parte do intervalo e então espera ocupada por meio milissegundo. spin espera ocupada o intervalo inteiro, o mais estável dos quatro e o único que mantém um núcleo acordado."),
            ),
            "Toda Configuração Força, Exceto Uma": (
                ("text", "O volt grava o valor que você escolheu em sua própria cópia da estrutura que o carrega, então uma configuração se aplica quer o jogo tenha consultado uma query antes ou não. Isso vale para cada cartão aqui exceto um."),
                ("text", "Dispositivo Físico é a exceção, e é um fato sobre Vulkan, não uma escolha. Nada nomeia o dispositivo em que uma swapchain roda: o jogo já possui um dispositivo físico quando o volt vê algo que poderia corrigir. Esconder os outros da enumeração é a única alavanca, então um jogo que ignora a ordem de enumeração mantém o dispositivo que escolheu."),
                ("text", "Onde uma consulta governa o que é legal, o volt também filtra isso. Um modo de apresentação deve ser um que a superfície reportou, então filtrar a consulta significa que um jogo que pega a primeira entrada oferecida recebe o valor certo sem o volt sobrescrever nada, e um jogo que codifica fixo recebe na chamada de criação. Ambas as metades, uma configuração."),
                ("text", "Um valor forçado que o dispositivo não reportou não é forçado. Onde a superfície recusa o modo de apresentação ou o alfa composto que você nomeou, o volt mantém o valor do jogo e registra um aviso. Ele nunca repassa um valor que invalidaria a chamada."),
            )
        },
        "Uso": {
            "Iniciando Jogos": (
                ("text", "Adicione o lançador volt antes do comando do seu jogo. Ele ativa a camada apenas para aquele processo e seleciona o perfil:"),
                ("code", "volt -- %command%", "Steam (Opções de inicialização, perfil padrão):"),
                ("code", "volt meuperfil -- %command%", "Steam (perfil nomeado):"),
                ("code", "volt -- ./jogo", "Terminal:"),
                ("code", "volt -- flatpak run com.example.Jogo", "Flatpak:"),
            ),
            "Comportamento Padrão": (
                ("text", "Toda configuração tem padrão \"default\", o que significa que a camada não toca nesse valor e o aplicativo mantém sua própria escolha. Um perfil com tudo em padrão é um passthrough verdadeiro."),
            ),
            "Vendo o Que Foi Aplicado": (
                ("text", "Execute o jogo por um terminal com VOLT_LOG=info e a camada imprime o que aplicou, o que a superfície ou o dispositivo recusou e quando captou um perfil alterado."),
                ("code", "VOLT_LOG=info volt -- ./jogo", ""),
                ("text", "Cada configuração ganha uma linha, nomeando o valor que o jogo pediu e o valor que o volt escreveu em seu lugar. Nenhum valor forçado significa que o volt deixou essa configuração em paz, seja porque é padrão ou porque o jogo já pediu o que você escolheu. O valor forçado é o que o volt escreveu, então uma configuração que o dispositivo limitou mostra o que foi efetivado em vez do que você escolheu."),
                ("text", "Uma configuração que precisa de um recurso de dispositivo que o jogo deixou desmarcado nomeia esse recurso. As configurações de Taxa de Quadros não têm valor pedido, já que um jogo nunca diz ao Vulkan qual taxa quer, então elas reportam o que o volt forçou ou dizem que o perfil não as definiu."),
                ("text", "A linha da GPU reporta o id do dispositivo como `forçado N` quando você define uma gpu, e `pedido N` quando não."),
                ("text", "Cada configuração imprime uma vez por dispositivo, então no máximo 21 linhas por mais samplers, pipelines ou swapchains que o jogo crie."),
            ),
            "A Sondagem": (
                ("text", "O volt-gui executa o volt-probe sob o perfil que você está editando. É o que preenche as listas de configuração com seu hardware. Pressionar Aplicar o executa novamente para que essas listas coincidam com os valores que você acabou de salvar, e trocar de perfis também o executa."),
                ("text", "Ele abre uma janela de um pixel que nunca é mapeada, cria uma superfície, uma swapchain e um amostrador para que a camada veja cada caminho necessário, registra o que o dispositivo reportou e sai. Nada aparece na tela e nada é desenhado."),
                ("text", "Abre uma superfície X11, que todo desktop tem, já que uma sessão Wayland roda XWayland. Essa não é a única superfície que um jogo abre: Wine e Proton têm drivers Wayland nativos, e gamescope é outro caminho. O perfil é gravado antes de qualquer um existir, então o volt não sabe qual o jogo escolherá, e reportar dois backends ofereceria valores do caminho que o jogo não tomou."),
                ("text", "Modos de apresentação, contagens de imagem e modos alfa são respondidos contra uma superfície em vez de contra a placa, então seu caminho de exibição os limita tanto quanto seu hardware, e uma lista curta ali é a resposta, não falha. Esses três cartões são os únicos que isso toca. As listas na maioria concordam entre backends, e onde não, a camada já lida: contagem de imagens é limitada contra a superfície que o jogo realmente abriu, e um modo de apresentação ou alfa que a superfície recusa deixa o valor do jogo em paz com uma linha no log. Ler uma superfície Wayland nativa diretamente está na lista para depois."),
                ("text", "O volt-probe é compilado pelo make e instalado ao lado do volt e volt-gui, então não há nada extra para buscar. Ele vincula libxcb, que todo desktop já carrega."),
                ("code", "volt --probe meuperfil -- volt-probe", "Execute você mesmo:"),
            )
        },
        "Perfis": {
            "Perfis": (
                ("text", "Crie perfis para alternar entre configurações por jogo.\n\n1. Abra o seletor de perfis e escolha Novo Perfil.\n2. Configure e Aplique as configurações.\n3. Inicie o jogo com o nome daquele perfil, ou troque de perfis pela Bandeja do Sistema."),
                ("text", "O comando de inicialização mostrado ao lado do botão Aplicar sempre corresponde ao perfil selecionado e pode ser copiado direto para a Steam."),
            )
        },
        "Predefinições": {
            "Predefinições": (
                ("text", "Predefinições preenchem o perfil que você tem aberto com um ponto de partida, organizadas em escada do mais bonito ao mais rápido:\n\n- Qualidade: filtragem trilinear, leve viés de nitidez, todos os níveis de mip permitidos, anisotropia 16x, bordas recortadas suavizadas, vsync clássico, swapchain de 4 imagens e ritmo precise em espera early.\n- Equilibrado: ainda trilinear, mailbox para vsync sem latência, anisotropia 8x, ritmo sliced.\n- Desempenho FPS: bilinear, viés de borramento, mailbox, swapchain mantida em 4 imagens e ritmo sleep mais barato.\n- Desempenho Baixa Latência: o mesmo, mirando latência em vez disso, com present immediate, swapchain de 2 imagens, espera late e ritmo spin, o mais estável dos quatro.\n- Batata FPS: bilinear, anisotropia desligada, um passo completo de viés de borramento, os dois mips superiores fora da mesa, suavização de recorte desligada.\n- Batata Baixa Latência: o mesmo novamente com present immediate, swapchain de 2 imagens e espera late.\n\nNenhuma predefinição toca em Alfa Composto ou Apresentação Recortada: esses dependem do seu compositor, então continuam seus."),
                ("text", "Aplicar uma predefinição substitui cada valor no perfil após confirmação, então qualquer coisa que a predefinição não define volta ao padrão. Isso inclui o limite de quadros: o limite certo depende da sua tela, então essa escolha continua sua."),
                ("text", "Uma predefinição pode nomear algo que seu hardware não oferece, mailbox em uma superfície sem ele por exemplo. Essa configuração volta ao padrão e o volt-gui diz quais, então o resto da predefinição ainda se aplica."),
                ("text", "As predefinições de filtro também são a resposta para como os três cartões de filtro devem ser definidos. Qualidade e Equilibrado são trilinear, o resto é bilinear com cortes duros de mip, e cada um deles é explicado cartão por cartão em Os Três Cartões de Filtro acima."),
            )
        },
        "Opções": {
            "Opções": (
                ("text", "Mudanças em Opções são salvas automaticamente mas só têm efeito após reiniciar o volt-gui. Isso inclui o tema, escala, comportamento da bandeja e todas as outras preferências."),
            )
        },
    }


def create_welcome_window_widget() -> QMainWindow:
    window = QMainWindow()
    window.setWindowTitle("Boas-vindas ao volt-gui")
    window.setMinimumSize(620, 380)
    central_widget = QWidget()
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(8, 8, 8, 8)
    main_layout.setSpacing(8)
    content_layout = QHBoxLayout()
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(0)
    welcome_settings = get_welcome_settings()
    stacked_widget = QStackedWidget()
    for section_data in welcome_settings.values():
        stacked_widget.addWidget(create_tab_content_widget("", section_data)["tab"])
    content_layout.addWidget(create_simple_sidebar_widget(tuple(welcome_settings.keys()), stacked_widget))
    content_layout.addWidget(stacked_widget, 1)
    main_layout.addLayout(content_layout, 1)
    button_container = QWidget()
    button_container.setProperty("buttonContainer", True)
    button_layout = QHBoxLayout(button_container)
    button_layout.setContentsMargins(8, 8, 8, 8)
    button_layout.setSpacing(8)
    button_layout.setAlignment(Qt.AlignVCenter)
    close_button = QPushButton("Fechar")
    close_button.setFixedSize(get_standard_button_width(), get_standard_button_height())
    close_button.clicked.connect(window.close)
    button_layout.addStretch(1)
    button_layout.addWidget(close_button, 0, Qt.AlignVCenter)
    button_layout.addStretch(1)
    main_layout.addWidget(button_container)
    window.setCentralWidget(central_widget)
    return window
