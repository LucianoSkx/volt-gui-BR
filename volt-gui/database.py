from typing import Final

from probe import alpha_one_options
from probe import alpha_options
from probe import aniso_options
from probe import call_read_probe
from probe import clamp_options
from probe import frametime_pairs
from probe import gpu_options
from probe import image_count_options
from probe import lod_bias_options
from probe import mip_options
from probe import plain_pairs
from probe import present_options
from probe import shading_options


APP_VERSION: Final[str] = "2.1.1"
APP_AUTHOR: Final[str] = "pythonlover02"
APP_LICENSE: Final[str] = "GPL 3.0 License"
APP_DESCRIPTION: Final[str] = "Minha Alternativa ao AMD Adrenaline / NVIDIA Settings para Linux"
APP_TRANSLATOR: Final[str] = "LucianoSkx (pt-BR)"

DEFAULT_VALUE: Final[str] = "default"
DEFAULT_PROFILE: Final[str] = "default"

PROFILE_TABS: Final[tuple] = ("GPU", "Display", "Textures", "Rendering", "Framerate")
ALL_TABS: Final[tuple] = ("GPU", "Display", "Textures", "Rendering", "Framerate", "Options", "About")

TAB_LABELS: Final[dict] = {
    "GPU": "GPU",
    "Display": "Tela",
    "Textures": "Texturas",
    "Rendering": "Renderização",
    "Framerate": "Taxa de Quadros",
    "Options": "Opções",
    "About": "Sobre",
}


SETTINGS_DB: Final[dict] = {
    "GPU": {
        "device": {
            "section": "gpu",
            "label": "Dispositivo Físico",
            "description": "Qual GPU o jogo enxerga. A camada esconde todos os outros dispositivos da enumeração, então um jogo que pega o primeiro que lhe é oferecido recebe o seu. Se nada coincidir, a lista completa volta e um aviso é registrado.",
            "options": (DEFAULT_VALUE,),
        },
    },
    "Display": {
        "present_mode": {
            "section": "display",
            "label": "VSync / Modo de Apresentação",
            "description": "Como os quadros finalizados chegam à tela. immediate desliga o vsync, mailbox é vsync de baixa latência, fifo é vsync clássico, fifo_relaxed rasga apenas abaixo da taxa de atualização. Todos os outros modos são escondidos do jogo, então seu próprio menu de vsync não pode oferecer um que você descartou. Um modo que a superfície não possui volta para a escolha do jogo com um aviso.",
            "options": (DEFAULT_VALUE,),
        },
        "image_count": {
            "section": "display",
            "label": "Imagens da Swapchain",
            "description": "Quantas imagens a swapchain mantém, que é o controle de quadros em voo e o mais próximo de uma configuração anti-lag aqui. Mais permite que o jogo rode mais à frente da GPU, suavizando a entrega de quadros e custando latência de entrada. Menos o mantém mais próximo da tela. A lista é o que esta superfície permite.",
            "options": (DEFAULT_VALUE,),
        },
        "composite_alpha": {
            "section": "display",
            "label": "Alpha Composto",
            "description": "Como o compositor trata o canal alfa da imagem finalizada. opaque ignora a mesclagem da janela completamente, o caminho mais barato no Wayland. Um valor que a superfície recusa volta para a escolha do jogo com um aviso.",
            "options": (DEFAULT_VALUE,),
        },
        "clipped": {
            "section": "display",
            "label": "Apresentação Recortada",
            "description": "Se o driver pode descartar trabalho em pixels que outra janela cobre. ligado é mais barato e é o que quase todo jogo já pede. desligado mantém esses pixels renderizados, o que só importa se algo lê a imagem apresentada de volta. Vulkan base, então a lista nunca muda.",
            "options": (DEFAULT_VALUE, "off", "on"),
        },
    },
    "Framerate": {
        "frame_limit": {
            "section": "framerate",
            "label": "Limite de Quadros",
            "description": "Limita a taxa de quadros no momento da apresentação, mostrado com o orçamento de tempo que cada taxa oferece. Acima de ~500 o intervalo é menor do que o kernel acorda de forma confiável, então o ritmo sleep desvia acima do limite e manter a taxa exige sliced, precise ou spin.",
            "options": (DEFAULT_VALUE, "20", "24", "30", "36", "40", "45", "48", "50", "60", "72", "75", "90", "100", "120", "144", "165", "180", "240", "300", "360", "540", "600", "720", "900", "1000"),
        },
        "frame_limit_offset": {
            "section": "framerate",
            "label": "Deslocamento do Limite",
            "description": "Desloca o limite de quadros para cima ou para baixo, em passos de dois. Telas VRR querem o limite logo abaixo da taxa de atualização: escolha 144, defina como -6 e você cai em 138. O volt não lê sua taxa de atualização e nunca desloca um limite sozinho, já que a maioria das telas não é VRR. Só faz algo quando Limite de Quadros está definido.",
            "options": (DEFAULT_VALUE, "-10", "-8", "-6", "-4", "-2", "0", "2", "4", "6", "8", "10"),
        },
        "frame_limit_cadence": {
            "section": "framerate",
            "label": "Cadência do Limite",
            "description": "Em qual taxa o limitador ritma. fixed usa seu limite e nada mais. smooth ritma no mais lento dos últimos quadros, então os quadros rápidos esperam pelos lentos e a cadência sai uniforme no que a máquina está sustentando. dynamic lê o mesmo e arredonda para baixo até um quarto de passo do seu limite, então fica em uma taxa fixa: um limite de 60 passa por 60, 48, 40, 34, 30. Ambos trocam quadros por espaçamento uniforme, e nenhum vai mais rápido que seu limite. Use fixed se a máquina sustenta o limite, ou se quer cada quadro possível pela latência. Só faz algo quando Limite de Quadros está definido.",
            "options": (DEFAULT_VALUE, "fixed", "smooth", "dynamic"),
        },
        "frame_limit_method": {
            "section": "framerate",
            "label": "Método do Limite",
            "description": "Quando o limitador espera. early segura o quadro para que as apresentações saiam em cadência fixa. late deixa a apresentação passar e espera antes de devolver o controle, então o jogo lê a entrada mais perto do momento de exibição, que é o que Reflex e Anti-Lag fazem. reactive espera onde early espera mas mede a partir do quadro recém mostrado, então um quadro lento nunca é perseguido com um rápido. Só faz algo quando Limite de Quadros está definido.",
            "options": (DEFAULT_VALUE, "early", "late", "reactive"),
        },
        "frame_pacing": {
            "section": "framerate",
            "label": "Ritmo de Quadros",
            "description": "Como o limitador espera, do mais barato ao mais preciso. sleep entrega toda a espera ao kernel. sliced dorme em passos curtos e re-verifica o relógio, corrigindo quando o kernel acorda atrasado. precise dorme a maior parte do intervalo e então espera ocupada por meio milissegundo. spin espera ocupada o tempo todo, o mais estável e o único que mantém um núcleo acordado. Só faz algo quando Limite de Quadros está definido.",
            "options": (DEFAULT_VALUE, "sleep", "sliced", "precise", "spin"),
        },
    },
    "Textures": {
        "mag_filter": {
            "section": "textures",
            "label": "Filtro de Ampliação",
            "description": "Como uma textura é amostrada quando desenhada maior que seu próprio tamanho, que é qualquer coisa perto da câmera. nearest dá pixels nítidos sem filtro, linear suaviza entre eles. Este é o único filtro que uma captura estática mostra. Vulkan base, então a lista nunca muda.",
            "options": (DEFAULT_VALUE, "nearest", "linear"),
        },
        "min_filter": {
            "section": "textures",
            "label": "Filtro de Redução",
            "description": "Como uma textura é amostrada quando desenhada menor que seu próprio tamanho, que é a maior parte da tela. nearest pega um texel e cintila quando a câmera se move. linear faz média e estabiliza, e é onde mipmaps e filtragem anisotrópica atuam. Vulkan base, então a lista nunca muda.",
            "options": (DEFAULT_VALUE, "nearest", "linear"),
        },
        "mipmap_mode": {
            "section": "textures",
            "label": "Modo Mipmap",
            "description": "Como amostradores se movem entre níveis de mip. nearest corta abruptamente de um mip para o próximo, o que aparece como faixa no chão. linear mistura entre eles, o terceiro linear do trilinear. Vulkan base, então a lista nunca muda. Só afeta texturas que têm mips.",
            "options": (DEFAULT_VALUE, "nearest", "linear"),
        },
        "anisotropy": {
            "section": "textures",
            "label": "Filtragem Anisotrópica",
            "description": "Nitidez em texturas vistas em ângulos acentuados. Valores maiores ficam melhores com pequeno custo. A lista vai em passos de dois até o que sua GPU reporta. O volt nunca ativa o recurso: onde o jogo deixou desligado a configuração é ignorada e uma linha é registrada. Quase todo jogo pede por ele.",
            "options": (DEFAULT_VALUE,),
        },
        "lod_bias": {
            "section": "textures",
            "label": "Viés LOD",
            "description": "Desloca a seleção de mipmap. Negativo nitida ao custo de cintilação, positivo borra mas renderiza mais rápido. Um viés negativo é o mais próximo que o volt chega de nitidez. A lista vai em passos de 0.2 no intervalo que sua GPU reporta.",
            "options": (DEFAULT_VALUE,),
        },
        "mip_floor": {
            "section": "textures",
            "label": "Piso Mip",
            "description": "O nível de mip mais baixo que amostradores podem usar, chamado LOD mínimo no Vulkan. Aumentar força mips menores por toda parte, trocando detalhe por velocidade. A lista vai em passos de dois até a maior imagem que sua GPU endereça, e um nível além do último mip simplesmente cai naquele último.",
            "options": (DEFAULT_VALUE,),
        },
        "mip_ceiling": {
            "section": "textures",
            "label": "Teto Mip",
            "description": "O nível de mip mais alto que amostradores podem usar, chamado LOD máximo no Vulkan. Diminuir mantém texturas distantes mais nítidas do que o jogo pretendia. A lista coincide com Piso Mip, e um teto abaixo do piso é trocado com ele em vez de descartado.",
            "options": (DEFAULT_VALUE,),
        },
    },
    "Rendering": {
        "sample_shading": {
            "section": "rendering",
            "label": "Sombreamento por Amostra",
            "description": "Sombreia na taxa de amostra dentro de alvos MSAA para reduzir cintilação. O valor é a menor fração de amostras sombreadas, e desligado conta como zero. O volt nunca ativa o recurso: a maioria dos renderizadores modernos é diferida e nunca pede, e onde o jogo deixou desligado a configuração é ignorada e uma linha é registrada.",
            "options": (DEFAULT_VALUE,),
        },
        "alpha_to_coverage": {
            "section": "rendering",
            "label": "Alfa para Cobertura",
            "description": "Transforma alfa de fragmento em cobertura, o que suaviza bordas recortadas em folhagem e cercas. Vulkan base, então a lista nunca muda. Só faz algo onde o jogo já renderiza em alvo MSAA.",
            "options": (DEFAULT_VALUE, "on", "off"),
        },
        "alpha_to_one": {
            "section": "rendering",
            "label": "Alfa para Um",
            "description": "Força o alfa do fragmento para 1 após o shader executar. O volt nunca ativa o recurso: onde o jogo deixou desligado a configuração é ignorada e uma linha é registrada. Só faz algo onde o jogo já renderiza em alvo MSAA.",
            "options": (DEFAULT_VALUE,),
        },
        "depth_clamp": {
            "section": "rendering",
            "label": "Limite de Profundidade",
            "description": "Mantém fragmentos fora dos planos próximo e distante e prende sua profundidade no plano em vez de descartá-los. Evita que modelos de armas sejam fatiados quando a câmera encosta na parede. O mesmo controle cobre o plano distante, onde geometria distante achata nele em vez de desaparecer, o que pode ficar pior, então teste por jogo. O volt nunca ativa o recurso, e a maioria dos jogos deixa desligado, então espere que não faça nada na maioria. Execute com VOLT_LOG=info para ver em qual caso você está.",
            "options": (DEFAULT_VALUE,),
        },
    },
}

OPTIONS_DB: Final[dict] = {
    "application_theme": {
        "label": "Tema do Aplicativo",
        "description": "Tema de cores do aplicativo. padrão é cachyos. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "cachyos", "amd", "intel", "nvidia"),
        "fallback": "cachyos",
    },
    "window_transparency": {
        "label": "Transparência da Janela",
        "description": "Transparência do fundo da janela. padrão é desligado. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "on", "off"),
        "fallback": "off",
    },
    "interface_scale_factor": {
        "label": "Fator de Escala da Interface",
        "description": "Multiplicador de escala da interface, em passos de 0.2. padrão é 1.0. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0", "2.2", "2.4", "2.6", "2.8", "3.0"),
        "fallback": "1.0",
    },
    "start_window_maximized": {
        "label": "Iniciar Maximizado",
        "description": "Inicia a janela maximizada. padrão é desligado. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "on", "off"),
        "fallback": "off",
    },
    "start_window_minimized": {
        "label": "Iniciar Minimizado",
        "description": "Inicia a janela minimizada na bandeja. padrão é desligado. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "on", "off"),
        "fallback": "off",
    },
    "system_tray_behavior": {
        "label": "Bandeja do Sistema",
        "description": "Mostrar ícone na bandeja do sistema. padrão é desligado. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "on", "off"),
        "fallback": "off",
    },
    "welcome_message_display": {
        "label": "Mensagem de Boas-vindas",
        "description": "Mostrar a mensagem de boas-vindas ao iniciar. padrão é ligado. Tem efeito após reiniciar o programa.",
        "options": (DEFAULT_VALUE, "on", "off"),
        "fallback": "on",
    },

}


def find_settings_for_tab(tab_name: str) -> dict:
    return SETTINGS_DB.get(tab_name, {})


def get_setting_label(tab_name: str, setting_key: str) -> str:
    return SETTINGS_DB[tab_name][setting_key]["label"]


def get_setting_description(tab_name: str, setting_key: str) -> str:
    return SETTINGS_DB[tab_name][setting_key]["description"]


OPTION_BUILDERS: Final[dict] = {
    "device": gpu_options,
    "present_mode": present_options,
    "image_count": image_count_options,
    "composite_alpha": alpha_options,
    "anisotropy": aniso_options,
    "lod_bias": lod_bias_options,
    "mip_floor": mip_options,
    "mip_ceiling": mip_options,
    "sample_shading": shading_options,
    "alpha_to_one": alpha_one_options,
    "depth_clamp": clamp_options,
    "frame_limit": lambda _: frametime_pairs(
        SETTINGS_DB["Framerate"]["frame_limit"]["options"][1:]),
}


def _static_options(tab_name: str, setting_key: str) -> tuple:
    return plain_pairs(SETTINGS_DB[tab_name][setting_key]["options"])


def find_setting_options(tab_name: str, setting_key: str, data: dict) -> tuple:
    match OPTION_BUILDERS.get(setting_key):
        case None:
            return _static_options(tab_name, setting_key)
        case builder:
            return ((DEFAULT_VALUE, DEFAULT_VALUE),) + builder(data)


def get_setting_options(tab_name: str, setting_key: str) -> tuple:
    return find_setting_options(tab_name, setting_key, call_read_probe())


def get_setting_section(tab_name: str, setting_key: str) -> str:
    return SETTINGS_DB[tab_name][setting_key]["section"]


def build_widget_key(tab_name: str, setting_key: str) -> str:
    return tab_name + ":" + setting_key


def find_cards_for_tab(tab_name: str) -> tuple:
    return tuple(
        (build_widget_key(tab_name, setting_key),
         get_setting_label(tab_name, setting_key),
         get_setting_description(tab_name, setting_key),
         get_setting_options(tab_name, setting_key))
        for setting_key in find_settings_for_tab(tab_name))


def _tab_option_sources(tab_name: str, data: dict) -> tuple:
    return tuple(
        (build_widget_key(tab_name, setting_key),
         find_setting_options(tab_name, setting_key, data))
        for setting_key in find_settings_for_tab(tab_name))


def find_option_sources() -> tuple:
    data = call_read_probe()
    return tuple(
        entry
        for tab_name in PROFILE_TABS
        for entry in _tab_option_sources(tab_name, data))


def find_profile_fields() -> tuple:
    return tuple(
        (build_widget_key(tab_name, setting_key),
         get_setting_section(tab_name, setting_key),
         setting_key)
        for tab_name in PROFILE_TABS
        for setting_key in find_settings_for_tab(tab_name))


def get_option_label(option_key: str) -> str:
    return OPTIONS_DB[option_key]["label"]


def get_option_description(option_key: str) -> str:
    return OPTIONS_DB[option_key]["description"]


def get_option_options(option_key: str) -> tuple:
    return plain_pairs(OPTIONS_DB[option_key]["options"])


def get_option_default_value(option_key: str) -> str:
    return OPTIONS_DB[option_key]["options"][0]


def get_option_fallback(option_key: str) -> str:
    return OPTIONS_DB[option_key]["fallback"]


def _option_is_unset(raw_value: str) -> bool:
    return raw_value in ("", DEFAULT_VALUE)


def resolve_option_value(option_key: str, raw_value: str) -> str:
    match _option_is_unset(raw_value):
        case True:
            return get_option_fallback(option_key)
        case False:
            return raw_value


def get_accent_colors(theme_name: str) -> tuple:
    match theme_name:
        case "amd":
            return ("#E31937", "#FF2D4A", "#B81430")
        case "intel":
            return ("#0068B5", "#1A8CFF", "#004D87")
        case "nvidia":
            return ("#76B900", "#8ED11A", "#5A8F00")
        case _:
            return ("#80dbcb", "#9ae4d8", "#66b0a2")


def get_about_data() -> dict:
    return {
        "Descrição": APP_DESCRIPTION,
        "Licença": APP_LICENSE,
        "Autor": APP_AUTHOR,
        "Tradutor pt-BR": APP_TRANSLATOR,
        "Versão": APP_VERSION,
    }
