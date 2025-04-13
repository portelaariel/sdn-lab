
# Ryu + Mininet Packet Sniffer com Exportação para CSV

## 📁 Estrutura de Diretórios Recomendada

```
~/sdn-lab/
├── ryu-apps/         # Scripts do Ryu
│   └── sniffer_ryu.py  # Controlador com exportação para CSV
├── logs/             # Arquivos .csv de pacotes capturados
└── ryu39-env/        # Ambiente virtual Python 3.9
```

---

## 🔧 Instalação do Mininet e Ferramentas de Captura

```bash
sudo apt update
sudo apt install git python3-pip openvswitch-switch tshark tcpdump net-tools -y

cd ~
git clone https://github.com/mininet/mininet.git
cd mininet
sudo ./util/install.sh -a
```

---

## 🐍 Instalar Python 3.9 + Criar Ambiente Virtual

```bash
sudo apt install python3.9 python3.9-venv python3.9-dev -y

cd ~
python3.9 -m venv ryu39-env
source ryu39-env/bin/activate
```

---

## 📦 Instalar Dependências do Ryu

```bash
pip install setuptools==58.2.0
pip install eventlet==0.30.2
pip install git+https://github.com/faucetsdn/ryu.git
```

---

## ▶️ Executar o Controlador Ryu com Captura para CSV

1. Salve o script `sniffer_ryu.py` em:

```
~/sdn-lab/ryu-apps/sniffer_ryu.py
```

2. **Terminal 1 – Rodar o Ryu**:

```bash
cd ~/sdn-lab/ryu-apps
source ~/sdn-lab/ryu39-env/bin/activate
ryu-manager sniffer_ryu.py
```

3. **Terminal 2 – Rodar o Mininet**:

```bash
sudo mn --controller=remote --switch ovsk,protocols=OpenFlow13 --topo=single,2
```

4. Testar comunicação:

```bash
mininet> h1 ping -c 5 h2
```

📄 O log será salvo em:

```
~/sdn-lab/logs/pacotes.csv
```

---

## 📡 Alternativa: Captura com `tcpdump` e `tshark`

### Dentro do Mininet:

```bash
mininet> h1 tcpdump -i h1-eth0 -w /tmp/h1.pcap &
mininet> h1 ping -c 5 h2
mininet> h1 pkill tcpdump
```

### Fora do Mininet (terminal real):

```bash
sudo tcpdump -i s1-eth1 -w h1.pcap
```

### Converter `.pcap` em `.csv` com `tshark`:

```bash
tshark -r h1.pcap -T fields -e frame.time -e ip.src -e ip.dst -e ip.len \
  -E header=y -E separator=, -E quote=d -E occurrence=f > fluxos.csv
```

---

## 📊 Diferenças entre Métodos de Captura

| Método             | Tipo     | Vantagens                                           |
|--------------------|----------|-----------------------------------------------------|
| `tcpdump` / `tshark` | Passivo  | Acesso completo ao pacote (payload, headers)        |
| `packet_in` (Ryu)   | Ativo    | Programável, leve, ideal para aplicações SDN        |

---

## 🧹 Comandos Úteis

```bash
sudo mn -c      # Limpar rede anterior
exit            # Sair do Mininet
Ctrl+C          # Encerrar o Ryu
```

---

👨‍💻 Projeto para estudos de captura de pacotes e uso de Ryu como controlador SDN com exportação de dados para CSV.
