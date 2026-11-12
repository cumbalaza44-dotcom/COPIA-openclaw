# Linux Cheatsheet — Data Center Hardware Specialist
> Enfocado en: switches, conectividad, servidores, GPUs, diagnóstico

## 1. Navegación y archivos (base diaria)
```bash
pwd; ls -lah; cd /ruta
cp -r origen destino; mv viejo nuevo; rm -rf ruta  # cuidado
mkdir -p /ruta/sub; touch archivo
cat archivo; less +F archivo; tail -f /var/log/syslog
find / -name "*.log" 2>/dev/null | head -20
grep -Rin "error|fail|link down" /var/log/ | head -30
```

## 2. Switches y red — conexión y diagnóstico
```bash
# Identidad y enlaces
ip -br link show              # estado UP/DOWN rápido
ip -br addr show
ethtool eth0                  # speed/duplex/link
ethtool -S eth0 | grep -i "drop\|err\|crc"   # errores físicos
mii-tool -v 2>/dev/null; dmesg | grep -i "link.*up\|link.*down"

# Conectividad L2/L3
ping -c 4 10.x.x.1
traceroute 10.x.x.1; mtr --report 10.x.x.1
arp -n; ip neigh show         # MAC <-> IP, clave en DC
lldpctl 2>/dev/null || lldpcli show neighbors  # qué switch/puerto te ve

# Puertos, sockets, throughput
ss -tulnp | head -30
iperf3 -s            # en un extremo
iperf3 -c 10.x.x.2 -P 4 -t 30  # prueba real de enlace
```

## 3. Hardware — servidores, FRUs, salud
```bash
# Inventario rápido
dmidecode -t system | grep -E "Manufacturer|Product|Serial"
lscpu | head -20; free -h; lsblk -o NAME,SIZE,TYPE,MODEL,SERIAL
lspci | grep -i "nvidia\|mellanox\|broadcom\|ethernet"
lsusb; lshw -short 2>/dev/null | head -40

# Discos / NVMe
smartctl -a /dev/sda | grep -i "health\|realloc\|temp"
nvme smart-log /dev/nvme0
dmesg | grep -i "ata\|nvme\|scsi.*error" | tail -20

# Fuentes, fans, temperatura, power
sensors; ipmitool sdr list | grep -i "temp\|fan\|ps\|volt"
ipmitool sel list | tail -20   # event log del BMC
ipmitool fru print
```

## 4. GPUs — datacenters IA
```bash
nvidia-smi -L; nvidia-smi
nvidia-smi dmon -s pucvmet -d 2   # power, util, temp en vivo
nvidia-smi nvlink --status
nvidia-smi --query-gpu=index,name,temperature.gpu,power.draw,utilization.gpu,memory.used,memory.total --format=csv
dmesg | grep -i "nvidia\|nvrm\|Xid" | tail -30   # Xid = clave para RMA
```

## 5. NICs / DPUs Mellanox (muy común en IA)
```bash
ibstat; ibv_devices; ibv_devinfo | head -60
mlxlink -d /dev/mst/mt4125_pciconf0 --show_serdes_tx --show_eye 2>/dev/null
ethtool -m eth0  # óptico: potencia TX/RX, temp — clave en "link flapping"
dmesg | grep -i "mlx\|ib\|rdma" | tail -20
```

## 6. Logs y systemd — causa raíz
```bash
journalctl -p err -b --no-pager | tail -40
journalctl -u servicio -f
systemctl status servicio; systemctl restart servicio
dmesg -T | tail -50
uptime; who; last -10
```

## 7. Procesos y carga
```bash
top -o %CPU -b -n1 | head -20; htop  # si existe
ps aux --sort=-%cpu | head -15
ps aux --sort=-%mem | head -15
kill -9 PID; pkill -f nombre
lsof -i :22; fuser -v /dev/nvme0 2>&1 | head
```

## 8. SSH y transferencia (tu día a día)
```bash
ssh user@10.x.x.5
ssh -J jump@bastion user@10.x.x.5   # vía jump host
scp archivo user@host:/ruta/
rsync -avhP origen/ user@host:/destino/
ssh-keygen -t ed25519; ssh-copy-id user@host
```

## 9. One-liners de commissioning
```bash
# Snapshot de un nodo nuevo
hostname; ip -br addr; ip -br link; lscpu | head -5; free -h; lsblk; nvidia-smi -L; ibstat | head -20
# Chequeo pre-entrega
sensors | head; smartctl -a /dev/sda | grep -i health; ethtool eth0 | grep -E "Speed|Link"; ipmitool sel list | tail -5
```

---
Tip: si `link down` + `ethtool -m` con RX bajo → físico (fibra/transceiver). Si RX ok + errores CRC → cable/velocidad/duplex.

## 10. Dell Z9664F-ON (OS10) + S4048-ON (OS9/OS10)
```bash
# --- OS10 (Z9664F-ON, S4048-ON con OS10) ---
show interface status              # estado UP/DOWN todos los puertos
show interface ethernet 1/1/1     # detalle un puerto
show lldp neighbors               # qué hay conectado puerto por puerto
show mac address-table
show interface transceiver         # ópticos: TX/RX/temp (equivale a ethtool -m)
show interface counters errors     # CRC/drops
show version; show system; show inventory
show running-configuration
configure terminal → interface ethernet 1/1/1 → shutdown / no shutdown

# --- OS9 / FTOS (S4048-ON clásico) ---
show interfaces status
show interfaces transceiver
show lldp neighbors
show mac-address-table
show version; show system brief; show inventory
```
> Z9664F-ON = 64x400G spine (OS10). S4048-ON = 48x10G + 6x40G ToR (OS9 u OS10 según versión).
