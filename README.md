> [!NOTE]
> Este fork é mantido apenas para a tradução pt-BR. O projeto original é [pythonlover02/volt-gui](https://github.com/pythonlover02/volt-gui) — reportes de bugs e melhorias da camada devem ser feitos lá. Este fork é responsável somente pela tradução para o Português-BR.

# volt-gui

Painel de controle para jogos Vulkan no Linux. As configurações são aplicadas pelo **volt**, uma camada Vulkan implícita escrita em Rust, então funciona em todo driver: RADV, ANV, NVK, AMDVLK, NVIDIA proprietário.

Apenas Vulkan 1.0. A camada não pede nada além de `VK_KHR_swapchain`, então o comportamento nunca se divide entre drivers.

![](/images/1.png)
![](/images/2.png)
![](/images/3.png)

## Início Rápido

```
git clone https://github.com/pythonlover02/volt-gui.git
cd volt-gui
make
make install-user

volt-gui          # configure o que quiser, pressione Aplicar
volt -- ./jogo
```

Isso cobre nativo, Steam, Wine e Proton. Para instalação em todo o sistema use `sudo make install`. Escolha um, nunca ambos.

Opções de inicialização da Steam:

```
volt -- %command%
```

Jogos Flatpak precisam de trabalho extra, veja [Flatpak](#flatpak).

## Índice

- [Configurações](#configurações)
- [Como Funciona](#como-funciona)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Caminhos de instalação](#caminhos-de-instalação)
- [Desinstalando](#desinstalando)
- [Sistemas Imutáveis](#sistemas-imutáveis)
- [FEX-Emu / Box64](#fex-emu--box64)
- [Compilando Releases](#compilando-releases)
- [Uso](#uso)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Arquivos](#arquivos)
- [Flatpak](#flatpak)
- [Perfis, Predefinições e Opções](#perfis-predefinições--opções)
- [O que o volt nunca fará](#o-que-o-volt-nunca-fará)
- [Contribuindo](#contribuindo)

## Configurações

21 configurações em 5 abas. Cada uma tem padrão `default` (padrão), que deixa a escolha do jogo intacta. Um perfil com tudo em padrão não faz nada.

Cada configuração é um único valor. Sem intervalos, sem ordenação, nada para confundir.

| Aba | Seção | Qtd | Cobre |
|-----|---------|------:|--------|
| GPU | `[gpu]` | 1 | qual dispositivo o jogo enxerga |
| Tela | `[display]` | 4 | modo de apresentação, contagem de imagens, composição, recorte |
| Texturas | `[textures]` | 7 | filtragem, mips, anisotropia, LOD |
| Renderização | `[rendering]` | 4 | sample shading, alpha to coverage, alpha to one, depth clamp |
| Taxa de Quadros | `[framerate]` | 5 | limite, deslocamento, cadência, método, ritmo |

A maioria das listas de opções é lida do seu hardware, não de uma tabela no volt-gui. Modos de apresentação, contagens de imagem, modos alfa, nomes de GPU, anisotropia, níveis de mip e viés LOD vêm de uma sondagem do seu próprio dispositivo. Uma configuração que seu hardware não possui contém apenas `padrão`.

Listas fixas existem onde não há nada para ler. `nearest` e `linear` são Vulkan base sem consulta por trás. As configurações de Taxa de Quadros também não têm nada para ler, já que um jogo nunca diz ao Vulkan qual taxa de quadros quer.

As configurações são lidas uma vez ao iniciar o jogo. Pressione Aplicar e reinicie o jogo.

### A sondagem

O volt-gui executa `volt-probe` sob o perfil que você está editando. Ele abre uma janela de 1px que nunca é mapeada, cria uma superfície, swapchain e amostrador, registra o que o dispositivo reportou e sai. Nada aparece na tela.

```
volt --probe meuperfil -- volt-probe
```

Usa X11, que todo desktop tem via XWayland. Jogos podem abrir superfícies Wayland ou gamescope, e o perfil é gravado antes do volt saber qual. Isso só afeta modos de apresentação, contagens de imagem e modos alfa, e as listas na maioria concordam. Onde não, a camada lida em tempo de execução: contagem de imagens é limitada contra a superfície real, e um modo de apresentação ou alfa rejeitado mantém o valor do jogo com um aviso.

### GPU

**Dispositivo Físico** escolhe qual GPU o jogo enxerga. O volt esconde o resto durante a enumeração. Se nada coincidir, a lista completa volta com um aviso.

Esta é a única configuração que o volt não pode forçar. Nada no Vulkan nomeia o dispositivo em que uma swapchain roda, então um jogo que ignora a ordem de enumeração mantém o que escolheu.

### Tela

**VSync / Modo de Apresentação** `immediate` desligado, `mailbox` vsync de baixa latência, `fifo` vsync clássico, `fifo_relaxed` rasga abaixo da atualização. Modos que você descartou são escondidos do jogo, então seu próprio menu de vsync não pode oferecê-los.

**Imagens da Swapchain** quadros em voo. Mais deixa o jogo rodar à frente da GPU, suavizando a entrega ao custo de latência de entrada. Menos o mantém mais perto da tela. Esta é a configuração anti-lag.

**Alfa Composto** como o compositor trata o alfa da imagem finalizada. `opaque` pula a mesclagem do compositor no Wayland.

**Apresentação Recortada** se o driver pode pular pixels que outra janela cobre.

### Texturas

**Filtro de Ampliação** amostragem onde a textura é desenhada maior que seu próprio tamanho, ou seja, qualquer coisa perto da câmera. `nearest` são pixels nítidos, `linear` suaviza. O único filtro que uma captura de tela mostra.

**Filtro de Redução** o mesmo onde é desenhado menor, que é a maior parte da tela. `nearest` cintila quando a câmera se move, `linear` estabiliza. Deixe em `linear` a menos que queira cintilação.

**Modo Mipmap** corte seco entre níveis de mip, ou mistura.

Três campos de amostrador, três configurações, então toda combinação é alcançável. Retrô é `nearest`/`nearest`/`nearest`. Bilinear é `linear`/`linear`/`nearest`. Trilinear é `linear`/`linear`/`linear`. Pixel art nítido sem cintilação distante é `nearest`/`linear`/`linear`, que nenhum modo nomeado ofereceu.

**Filtragem Anisotrópica** de desligado até o que sua GPU reporta. O volt nunca habilita `samplerAnisotropy`; onde o jogo deixou desligado a configuração é ignorada e registrada. Quase todo jogo habilita.

**Viés LOD** desloca a seleção de mipmap para mais nítido ou mais borrado.

**Piso Mip / Teto Mip** níveis de mip mais baixo e mais alto que amostradores podem usar. Um teto abaixo do piso é trocado em vez de descartado.

### Renderização

**Sombreamento por Amostra** sombreia na taxa de amostra dentro de alvos MSAA para reduzir cintilação. O volt nunca habilita `sampleRateShading`; a maioria dos renderizadores diferidos nunca pede.

**Alfa para Cobertura** transforma alfa de fragmento em cobertura. Suaviza bordas recortadas em folhagem e cercas. Só faz algo onde o jogo já renderiza em MSAA.

**Alfa para Um** força alfa do fragmento para 1 após o shader. O volt nunca habilita o recurso.

**Limite de Profundidade** mantém fragmentos fora dos planos próximo e distante e prende sua profundidade em vez de descartá-los. Evita que modelos de armas sejam fatiados contra paredes. O mesmo controle cobre o plano distante, onde a geometria achata nele em vez de sumir, então teste por jogo. A maioria dos jogos nunca habilita `depthClamp` e o volt não habilitará por eles, então geralmente não faz nada.

### Taxa de Quadros

A maioria dos limitadores oferece um limite e um método. O volt oferece cinco configurações. Nada mais no Linux cobre todas as cinco.

**Limite de Quadros** limite no momento da apresentação. Prazos seguem uma linha do tempo fixa em vez da última apresentação, então jitter do agendador não te arrasta abaixo da taxa pedida. Mantido por swapchain.

**Deslocamento do Limite** desloca o limite em -10 a 10 em passos de dois. Telas VRR querem o limite logo abaixo da atualização: escolha 144, defina -6, caia em 138. O volt nunca desloca um limite sozinho já que a maioria das telas não é VRR.

**Cadência do Limite** em qual taxa o limitador ritma.

- `fixed` é seu limite e nada mais.
- `smooth` ritma no mais lento dos últimos quadros, então quadros rápidos esperam pelos lentos e a cadência sai uniforme no que a máquina sustenta.
- `dynamic` lê o mesmo e arredonda para baixo até um quarto de passo do limite. Um limite de 60 passa por 60, 48, 40, 34, 30. Um limite de 240 passa por 240, 192, 160, 137, 120.

Ambos vêm da ideia de consoles: escolher uma taxa que a máquina sustenta e ficar nela. Nenhum lê a média, porque um limitador só pode atrasar quadros e um quadro mais lento que a média nunca poderia ser ritmado para cima até ela. Ambos sobem sozinhos e nenhum excede seu limite.

Você troca quadros por uniformidade. `fixed` não faz nada quando a máquina cai abaixo do limite, então você recebe o que ela produziu, um quadro longo e o próximo curto. Uma taxa em um dos passos de `dynamic` pode quicar entre dois, que é o custo do arredondamento; `smooth` é a mesma leitura sem ele. Use `fixed` se a máquina sustenta o limite, ou se quer cada quadro possível.

**Método do Limite** `early` segura o quadro para que apresentações saiam em cadência fixa. `late` deixa a apresentação passar e espera depois, então o jogo amostra entrada mais perto do tempo de exibição. Este é o equivalente a Reflex e Anti-Lag. `reactive` espera onde early espera mas mede a partir do quadro recém mostrado, então um quadro lento nunca é perseguido com um rápido.

**Ritmo de Quadros** como o limitador mata tempo. `sleep` entrega a espera ao kernel. `sliced` dorme em passos curtos e re-verifica. `precise` dorme a maior parte e então espera ocupada por meio milissegundo. `spin` espera ocupada o tempo todo, mais estável e o único que mantém um núcleo acordado.

## Como Funciona

O volt se registra como camada implícita (`VK_LAYER_VOLT_settings`). O manifesto declara `enable_environment = VOLT_ENABLE`, então o loader sempre o encontra mas só o ativa quando o lançador `volt` define essa variável no processo filho.

A camada lê `~/.config/volt-gui/<perfil>.toml` uma vez na inicialização e reescreve as chamadas que o jogo faz:

| Aba | Onde a camada atua |
|-----|----------------------|
| GPU | `vkEnumeratePhysicalDevices`, `vkEnumeratePhysicalDeviceGroups(KHR)` |
| Tela | `vkGetPhysicalDeviceSurfacePresentModesKHR`, `...PresentModes2EXT`, `...SurfaceCapabilities(2)KHR`, `vkCreateSwapchainKHR`, `vkCreateSharedSwapchainsKHR` |
| Texturas | `vkCreateSampler`, `vkWriteSamplerDescriptorsEXT` |
| Renderização | `vkCreateGraphicsPipelines`, `vkCmdSetAlphaToCoverageEnableEXT`, `vkCmdSetAlphaToOneEnableEXT`, `vkCmdSetDepthClampEnableEXT` |
| Taxa de Quadros | `vkQueuePresentKHR` |

A criação de dispositivo é lida, nunca modificada. O volt aprende quais recursos o jogo habilitou para que configurações com recurso só se apliquem onde o jogo pediu, e não habilita nada por conta própria.

Cada configuração é interceptada em cada caminho que a alcança. Variantes `2`/`EXT`, grupos de dispositivos, swapchains compartilhadas, escritas de amostrador inline e cobertura alfa dinâmica recebem o mesmo tratamento. Listas de modo de apresentação em cadeia `pNext` também são filtradas no local.

Um ponto de entrada para uma extensão que o jogo nunca habilitou é inalcançável, e a camada só retorna um gancho quando a chamada resolve mais abaixo na cadeia.

O volt-gui é o front-end PySide6. Aplicar apenas salva o perfil. Sem permissões elevadas, sem scripts.

## Requisitos

| Componente | Requisito |
|-----------|-------------|
| Camada | Vulkan 1.0+ com `VK_KHR_swapchain`, Linux x86_64 (mais i686 para jogos 32-bit) |
| Compilação | Rust 1.85.1+ com rustup, GNU make 4.3+ |
| Camada 32-bit | `gcc-multilib`, `libc6-dev-i386` |
| GUI | Python 3.10+, PySide6 |
| Bundles Flatpak | `flatpak`, `ostree` |
| Release em contêiner | `podman` ou `docker` |
| Compilação da sondagem | cabeçalhos `libxcb` |

Sem compilação nativa aarch64. Veja [FEX-Emu / Box64](#fex-emu--box64).

## Instalação

### Arch Linux (AUR)

Existe um pacote não oficial [volt-gui](https://aur.archlinux.org/packages/volt-gui). Não mantenho, mas o empacotador tem sido gente boa, então não vou desencorajar.

Leia o `PKGBUILD` primeiro. Não por causa do empacotador, mas porque o AUR permite que qualquer um envie qualquer coisa.

### Do código-fonte

Todo alvo de compilação é um arquivo, então o make só recompila o que mudou. Tudo cai em `build/`.

| Comando | O que faz |
|---------|--------------|
| `make` | ambas camadas, lançador, GUI, entrada desktop |
| `make layer-64` | camada 64-bit, lançador, sondagem |
| `make layer-32` | camada 32-bit |
| `make gui` | `build/bin/volt-gui` |
| `make flatpak` | `build/bundles/*.flatpak` |
| `make dist` | fontes com `build/` preenchido |
| `make release` | arquivo em `releases/`, toolchain do host |
| `make release-container` | mesmo, dentro da imagem de compilação |
| `sudo make install` | em todo o sistema |
| `make install-user` | em `~/.local`, sem root |
| `sudo make flatpak-install` | bundles de extensão |
| `make flatpak-install-user` | mesmo, `--user` |
| `make setup-user` | `install-user` + `flatpak-install-user` |
| `sudo make uninstall` | tudo |
| `make uninstall-user` | instalação sem root |
| `make clean` | `rm -rf build releases` |
| `make help` | esta lista |

Um `make` puro compila ambas arquiteturas. A camada 32-bit não é opcional, qualquer biblioteca Steam tem títulos 32-bit. `make layer-32` existe para trabalhar naquela peça e adiciona o alvo Rust se faltar.

Bundles Flatpak são o oposto: opcionais, só com `make flatpak`, e nenhum alvo de instalação os toca.

Artefatos de Actions são árvores `make dist`. Descompacte e `sudo make install` instala sem compilar.

Compilar com `sudo` é recusado, então você nunca fica com `build/` de root. Alvos de instalação só copiam o já compilado e nomeiam o que falta se você pulou etapa. O volt-gui também se recusa a iniciar sob `sudo`.

Empacotadores podem preparar sem root:

```
make
make install DESTDIR="$PWD/pkg" PREFIX=/usr
```

Com `DESTDIR` definido a instalação pula `ldconfig`, banco de dados desktop, cache de ícones e verificação de instalação concorrente.

## Caminhos de instalação

| Arquivo | Sistema | Usuário |
|------|--------|------|
| Lançador | `/usr/bin/volt` | `~/.local/bin/volt` |
| Sondagem | `/usr/bin/volt-probe` | `~/.local/bin/volt-probe` |
| GUI | `/usr/bin/volt-gui` | `~/.local/bin/volt-gui` |
| Biblioteca 64 | `/usr/lib/x86_64-linux-gnu/libvolt.so` | `~/.local/lib/volt/x86_64-linux-gnu/libvolt.so` |
| Biblioteca 32 | `/usr/lib/i386-linux-gnu/libvolt.so` | `~/.local/lib/volt/i386-linux-gnu/libvolt.so` |
| Manifesto | `/usr/share/vulkan/implicit_layer.d/VkLayer_volt.json` | `~/.local/share/vulkan/implicit_layer.d/VkLayer_volt.json` |
| Entrada desktop | `/usr/share/applications/volt-gui.desktop` | `~/.local/share/applications/volt-gui.desktop` |
| Ícone | `/usr/share/icons/hicolor/256x256/apps/volt-gui.png` | `~/.local/share/icons/hicolor/256x256/apps/volt-gui.png` |
| Carimbos | `/var/lib/volt` | `~/.local/share/volt` |

O diretório da biblioteca segue o que sua distribuição usa. Como o manifesto cai no diretório de camada implícita e as bibliotecas em caminhos padrão, jogos 32-bit encontram a camada 32-bit e jogos 64-bit a 64-bit sem mapeamento `VK_LAYER_PATH`.

> [!WARNING]
> Não mude `PREFIX` para fora de `/usr` ou `/usr/local`. O loader só varre um conjunto fixo de diretórios de manifesto. Instalar em `/opt/volt` coloca o manifesto onde nada lê e o lançador fora do `$PATH`.

## Desinstalando

```
sudo make uninstall     # sistema
make uninstall-user     # ~/.local
```

Ambos removem binários, bibliotecas, manifesto, entrada desktop, ícone, carimbos, extensão Flatpak do escopo usuário e `~/.config/volt-gui`. Rodando direto como root não há `SUDO_USER`, então passos de escopo usuário são pulados.

Nenhum toca instalação 1.x. 1.x vivia em `/usr/local/bin`, 2.0 vive em `/usr/bin`. Remova 1.x primeiro:

```
sudo rm -f /usr/local/bin/volt /usr/local/bin/volt-gui /usr/local/bin/volt-helper
sudo rm -f /usr/share/applications/volt-gui.desktop
sudo update-desktop-database /usr/share/applications
```

Faça antes de instalar 2.0. `/usr/local/bin` vem primeiro na maioria das distribuições, então um `volt` 1.x restante sobrepõe o novo lançador, nunca define `VOLT_ENABLE`, e toda configuração silenciosamente não faz nada. Se 2.0 parece morto, rode `which volt`.

`make clean` remove `build/` e `releases/` mais diretórios perdidos de layouts antigos.

## Sistemas Imutáveis

No SteamOS, Bazzite, Silverblue e qualquer coisa com `/usr` somente leitura, pule a instalação no sistema:

```
make
make install-user
```

Mais a extensão Flatpak se quiser:

```
make flatpak
make flatpak-install-user
```

`~/.local/bin` tem que estar no seu `PATH`, porque o volt-gui executa `volt` e `volt-probe` para ler seu hardware.

Escolha uma instalação, não ambas. O loader varre diretórios de sistema e usuário, então dois manifestos nomeando a mesma camada deixam indefinido qual é usado, ou se a camada é inserida duas vezes. Ambos alvos recusam rodar enquanto o outro possui a camada.

A GUI é um único binário autocontido, então descompactar um release e clicar duas vezes em `build/bin/volt-gui` abre o editor sem nada instalado. Suficiente para escrever e copiar perfis, não suficiente para usá-los: sem camada no disco a sondagem não roda, então todo card com dispositivo contém só `padrão`.

A extensão Flatpak nunca cobre jogos Steam nativos, que rodam sob o Steam Linux Runtime. A instalação nativa os alcança: a Steam expande `%command%` no host, e o contêiner runtime monta seu diretório home e importa camadas implícitas do host.

## FEX-Emu / Box64

Em aarch64, jogos x86_64 rodam via FEX-Emu ou Box64. Não há compilação nativa aarch64 porque todo jogo Vulkan em Linux tem compilação x86_64.

Camadas de tradução rodam o jogo dentro de sua própria raiz: uma árvore de binários x86_64 separada do host `/usr`. A camada vai para essa árvore.

**Se seu kernel roteia ELFs x86_64 via `binfmt_misc`,** um runtime Flatpak x86_64 se comporta normalmente:

```
flatpak install org.freedesktop.Platform//24.08 --arch=x86_64
make flatpak
make flatpak-install-user
```

**Caso contrário, instale na raiz de tradução:**

```
make
make install DESTDIR=/caminho/para/raiz-de-tradução
```

Não precisa de root e não toca nada no host. Limpe com `make DESTDIR=/caminho/para/raiz-de-tradução uninstall`.

## Compilando Releases

Ambos alvos produzem `releases/volt-gui-<versão>.tar.gz`, uma árvore pronta para instalar. Descompacte e `sudo make install` sem compilar.

`make release` usa sua toolchain e herda seu piso glibc.

`make release-container` compila dentro de `rust:1.85.1-bookworm` (glibc 2.36, Python 3.11), então o piso é fixo. Compila em `build/container/` e roda como seu uid.

```
make release-container CONTAINER_BASE=rust:1.85.1-bullseye
make release-container CONTAINER=docker
```

Bullseye baixa o piso para glibc 2.31 mas traz Python 3.9, abaixo do que a GUI precisa. Use para `make layer-64 layer-32` apenas.

## Uso

```
volt [--probe] [PERFIL] -- COMANDO [ARGS...]
volt -- COMANDO [ARGS...]      # perfil padrão
volt --help
```

Tudo antes de `--` são opções do lançador, tudo depois é o comando:

```
volt -- %command%                # Steam
volt meuperfil -- %command%      # perfil nomeado
volt -- ./jogo
volt -- flatpak run com.example.Jogo
```

O comando de inicialização para o perfil selecionado é mostrado ao lado do botão Aplicar, pronto para copiar.

Nomes de perfil devem ser ASCII imprimível não vazio sem separador de caminho e sem `..`. Qualquer outro cai no padrão com um aviso. O lançador escreve um perfil comentado no primeiro uso.

Para ver o que foi aplicado:

```
VOLT_LOG=info volt -- ./jogo
```

Cada linha é prefixada `[volt]` e vai para stderr.

Em `info` cada configuração ganha uma linha, nomeando o que o jogo pediu e o que o volt escreveu no lugar.

```
[volt] gpu device: pedido 2
[volt] present_mode: pedido fifo, forçado mailbox
[volt] image_count: pedido 3
[volt] mag_filter: pedido linear, forçado nearest
[volt] anisotropy: pedido desligado, forçado 16
[volt] depth_clamp: pedido desligado; o aplicativo não habilitou depthClamp
[volt] frame_limit: forçado 60
[volt] frame_pacing: o perfil não definiu
```

Nenhum valor forçado significa que o volt deixou aquela configuração em paz, seja porque é `padrão` ou porque o jogo já pediu o que você escolheu. O valor forçado é o que o volt escreveu, então uma configuração que o dispositivo limitou mostra o que caiu em vez do que o perfil diz.

As cinco configurações de Taxa de Quadros não têm valor pedido, já que um jogo nunca diz ao Vulkan qual taxa quer. Elas reportam o que o volt forçou, ou dizem que o perfil não as definiu.

A linha da GPU reporta o id do dispositivo como `forçado N` quando o perfil define gpu, e `pedido N` quando não.

Cada configuração imprime uma vez por dispositivo, então no máximo 21 linhas por mais samplers, pipelines ou swapchains que o jogo criar.

## Variáveis de Ambiente

| Variável | Propósito | Valores | Padrão |
|----------|---------|--------|---------|
| `VOLT_CONFIG_NAME` | qual perfil carregar | qualquer nome de perfil | `default` |
| `VOLT_LOG` | verbosidade do log, para stderr | `off`, `error`, `warn`, `info` | `warn` |
| `VOLT_PROBE` | grava `probe.toml` na primeira swapchain | qualquer valor não vazio | não definido |
| `VOLT_ENABLE` | ativa a camada | `1` | não definido |
| `VOLT_DISABLE` | off switch do loader | `1` | não definido |

`HOME` decide onde perfis vivem e cai em `/tmp` com aviso. `LD_LIBRARY_PATH` é estendido pelo lançador com ambos diretórios de camada, preservando o que havia.

Não há override de ambiente para as configurações em si. Um arquivo de perfil é a única forma de defini-las, o que mantém painel e camada descrevendo a mesma coisa.

## Arquivos

| Caminho | O que é |
|------|------------|
| `~/.config/volt-gui/default.toml` | perfil padrão |
| `~/.config/volt-gui/<nome>.toml` | perfis nomeados |
| `~/.config/volt-gui/probe.toml` | o que a última sondagem leu |
| `~/.config/volt-gui/options.toml` | preferências do volt-gui e último perfil ativo |

Perfis são TOML simples, uma seção por aba e uma string por configuração, então você pode editá-los à mão ou manter em repo dotfiles. `probe.toml` é escrito pela camada e vigiado pela GUI, então um dispositivo sondado preenche o painel sem reiniciar. Deletá-lo custa uma nova sondagem.

## Flatpak

Jogos Flatpak não enxergam caminhos do host, então a camada vem como extensão de runtime para `org.freedesktop.Platform` 23.08, 24.08 e 25.08.

Separada e opcional. Nem `make` nem alvos de instalação produzem ou tocam os bundles:

```
make flatpak
make flatpak-install-user     # ou: sudo make flatpak-install
```

Um bundle por runtime. Instale o que combina com o seu, rode `flatpak list` se não souber. Múltiplas versões podem coexistir. Todo bundle carrega a biblioteca 32-bit também.

```
flatpak install --user build/bundles/org.freedesktop.Platform.VulkanLayer.volt-24.08.flatpak
flatpak uninstall --user org.freedesktop.Platform.VulkanLayer.volt
```

O lançador detecta `flatpak run` e roteia pelo wrapper dentro do sandbox:

```
volt -- flatpak run com.example.Jogo
volt -- flatpak run --branch=stable com.example.Jogo
volt meuperfil -- flatpak run com.example.Jogo
```

Não há build Flatpak do próprio volt-gui, só da camada.

### Sem o lançador

Chame o wrapper você mesmo, útil onde só a extensão está instalada:

```
flatpak run --command=/usr/lib/extensions/vulkan/volt/bin/volt-flatpak com.example.Jogo
VOLT_CONFIG_NAME=meuperfil flatpak run --command=/usr/lib/extensions/vulkan/volt/bin/volt-flatpak com.example.Jogo
```

A mesma linha funciona como opção de inicialização Steam para um jogo Flatpak:

```
/usr/lib/extensions/vulkan/volt/bin/volt-flatpak %command%
```

Seu diretório home é montado no sandbox, então perfis se aplicam sem mudanças.

## Perfis, Predefinições e Opções

**Perfis** são arquivos TOML em `~/.config/volt-gui/`, um por configuração. Crie e troque pela GUI, bandeja ou `volt <nome> -- ...`. Trocar salva aquele em que estava e reinicia a sondagem.

**Predefinições** preenchem o perfil ativo com valores curados, de Qualidade (trilinear, anisotropia 16x, mips misturados, vsync clássico) até Batata Baixa Latência (bilinear, anisotropia desligada, cortes duros de mip, present imediato, 2 imagens). Uma predefinição grava todo valor, então qualquer coisa que não define volta ao padrão. Limite de quadros, alfa composto e apresentação recortada são deixados em paz já que dependem da sua tela. Uma predefinição nomeando algo que seu hardware não tem reseta aquele para padrão e diz quais.

**Opções** guarda preferências do próprio volt-gui, não nada que a camada lê: tema, transparência, escala, iniciar maximizado ou na bandeja, ícone da bandeja, janela de boas-vindas. Salvam conforme você muda e têm efeito ao reiniciar. Uma instância por vez.

## O que o volt nunca fará

O volt muda o que o jogo pede ao Vulkan. Ele nunca desenha. Qualquer coisa precisando injeção de shader ou processamento de imagem está fora de escopo.

- **Nitidez, FSR, upscaling, geração de quadros, pós-processamento.**
- **MSAA ou SSAA forçado.** Adicionar amostras significa recriar todo render target, adicionar resolves e reescrever pipelines e shaders. Isso é o grafo de quadros do jogo, não um valor passando.
- **Profundidade de cor, espaço de cor, função de transferência.** Todo formato de superfície 10-bit é UNORM, então forçar 8 para 10 perde codificação sRGB de hardware e lava a imagem, e um jogo que codificou seu formato termina com image views que não batem. Nada disso faz um jogo renderizar conteúdo mais amplo. Um jogo que quer HDR pede via DXVK_HDR, PROTON_ENABLE_HDR ou gamescope.
- **Filtragem cúbica.** Precisa `VK_EXT_filter_cubic`, admitido por formato, enquanto um amostrador não nomeia formato. Não há momento onde o volt pode dizer se seria legal.
- **Sobreposições e HUDs.** Use MangoHud.
- **Overclock, curvas de ventoinha, limites de energia.** Isso é sysfs, não Vulkan. Use LACT, ou CoreCtrl se quiser controles de CPU também.
- **OpenGL.** O labirinto de variável de ambiente por driver é exatamente o que esta reescrita aposentou.
- **Habilitar um recurso ou extensão que o jogo não requisitou.**
- **Requerer uma extensão Vulkan.** Core 1.0 e `VK_KHR_swapchain` é toda a superfície.
- **Escala de resolução.** Precisa `VK_KHR_surface_maintenance1` e `VK_KHR_swapchain_maintenance1`, e o volt não habilita nenhum. Use gamescope.
- **Ritmo de quadros mais apertado que o limitador dá.** Prazos medidos contra a tela precisam `VK_KHR_present_wait` ou `VK_EXT_present_timing`. `late` é o mais perto que Vulkan base alcança.
- **Mudar uma configuração com um jogo rodando.**
- **Escrever em memória que o jogo possui.** O volt corrige as estruturas que repassa e preenche os arrays que uma consulta pede para preencher. Uma cadeia `pNext` que o jogo construiu é lida, nunca escrita.

## Contribuindo

Contribuições bem-vindas. A camada é Rust puro sem scripts de compilação, a GUI é só PySide6. Mantenha mudanças funcionando em Vulkan 1.0 base sem extensões — esse piso é o ponto do projeto.

---
*Tradução pt-BR por [LucianoSkx](https://github.com/LucianoSkx) — fork de [pythonlover02/volt-gui](https://github.com/pythonlover02/volt-gui).*
