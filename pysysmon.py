import psutil
import time
import subprocess
import pwd

# sample the counters at time t1
t1 = time.time()
net_io1 = psutil.net_io_counters()
net_in_bytes1 = net_io1.bytes_recv
net_out_bytes1 = net_io1.bytes_sent

# wait for some interval (e.g. 1 second)
time.sleep(1)

# sample the counters at time t2
t2 = time.time()
net_io2 = psutil.net_io_counters()
net_in_bytes2 = net_io2.bytes_recv
net_out_bytes2 = net_io2.bytes_sent

# calculate the difference in bytes and time
net_in_diff = net_in_bytes2 - net_in_bytes1
net_out_diff = net_out_bytes2 - net_out_bytes1
time_diff = t2 - t1

# calculate the network usage as a rate (bytes per second)
net_in_rate = net_in_diff / time_diff
net_out_rate = net_out_diff / time_diff

# disk usage
disk_usage = psutil.disk_usage('/').percent

# CPU usage
cpu_usage = psutil.cpu_percent(interval=1)

# memory utilization
mem = psutil.virtual_memory()
mem_usage = mem.percent

# themal sensors
tsense = subprocess.run(['sensors'], stdout=subprocess.PIPE).stdout.decode('utf-8')

# user accounts
users = pwd.getpwall()

# processes
processes = psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status'])

# network connections
connections = psutil.net_connections(kind='inet')

# create html file with a table displaying system info
with open('pysysmon.html', 'w') as f:
    f.write('<table>\n')
    f.write('<tr><th>Parameter</th><th>Value</th></tr>\n')
    f.write(f'<tr><td>Disk Usage %</td><td>{disk_usage}</td></tr>\n')
    f.write(f'<tr><td>CPU Usage %</td><td>{cpu_usage}</td></tr>\n')
    f.write(f'<tr><td>Memory Usage %</td><td>{mem_usage}</td></tr>\n')
    f.write(f'<tr><td>Network In Rate</td><td>{net_in_rate:.2f} bytes/s</td></tr>\n')
    f.write(f'<tr><td>Network Out Rate</td><td>{net_out_rate:.2f} bytes/s</td></tr>\n')
    f.write(f'<tr><td>Thermal sensors</td><td><pre>{tsense}</pre></td></tr>\n')
    f.write('<tr><td>User accounts</td><td><pre>')
    for user in users:
        f.write(f'{user.pw_name} ({user.pw_uid}): {user.pw_gecos}\n')
    f.write('</pre></td></tr>\n')
    f.write('<tr><td>Processes</td><td><pre>')
    for process in processes:
        f.write(f'{process.info}\n')
    f.write('</pre></td></tr>\n')
    f.write('<tr><td>Network connections</td><td><pre>')
    for connection in connections:
        f.write(f'{connection}\n')
    f.write('</pre></td></tr>\n')
    f.write('</table>')
    
