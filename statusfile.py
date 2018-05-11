import time
import cgi

def esc(str):
  # Escape special characters for security. TODO: Might need some more work!
  return cgi.escape(str)

def qrg(freq):
  return '{:7.4f} kHz'.format(float(freq) / 10**6)

def abstime(abstime):
  return time.asctime(time.localtime(abstime))

def reltime(abstime):
  t = float(abstime)
  if t <= 0: return 'n/a'
  return '{:6.1f} sec ago'.format(time.time() - t)

def write(logger, config, systemname, clients):
  try:
    filename = config['FILE'].replace('{SYSTEM}', systemname)
    logger.debug('(%s) Updating status file \"%s\".', systemname, filename)
    with open(filename, 'w') as f:
      f.write('<table border=\"1\">\n<tr><td colspan=\"8\" align=\"center\" bgcolor=\"orange\">' + time.asctime() + ': <b>' + esc(systemname) + '</b></td></tr>\n')
      f.write('<tr align=\"center\" bgcolor=\"yellow\"><td>Radio ID</td><td>ConStat</td><td>Callsign</td><td>IP</td><td>Login Time<br>Last Ping</td><td>Last Tx Time<br>Total Tx Time</td><td>QRG</td><td>Version Info</td></tr>\n')
      for client in clients:
        c = clients[client]
        f.write('<tr><td align=\"center\">' + esc(c['RADIO_ID'])
          + '</td><td align=\"center\">' + esc(c['CONNECTION'])
          + '</td><td align=\"center\">' + esc(c['CALLSIGN'])
          + '</td><td align=\"center\">' + esc(c['IP'])
          + '</td><td>' + abstime(c['LOGIN_TIME']) + '<br><div align=\"center\">' + reltime(c['LAST_PING']) + '</div>'
          + '</td><td align=\"center\">' + reltime(c['LAST_TX']) + '<br>' + str(c['TX_PACKETS'] * 0.06) + ' sec'
          + '</td><td align=\"center\">Rx: ' + qrg(c['RX_FREQ']) + '<br>Tx: ' + qrg(c['TX_FREQ'])
          + '</td><td align=\"center\">S: <code>' + esc(c['SOFTWARE_ID']) + '</code><br>P: <code>' + esc(c['PACKAGE_ID']) + '</code>'
          + '</td></tr>\n')
      f.write('</table>\n')
  except Exception as e: logger.error('(%s) Updating status file failed: %s', systemname, e)
