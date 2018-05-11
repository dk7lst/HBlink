import time
import cgi

def esc(str):
  # Escape special characters for security. TODO: Might need some more work!
  return cgi.escape(str)

def qrg(freq):
  return '{:7.4f} kHz'.format(float(freq) / 10**6)

def write(logger, config, systemname, clients):
  try:
    filename = config['FILE'].replace('{SYSTEM}', systemname)
    logger.debug('(%s) Updating status file \"%s\".', systemname, filename)
    with open(filename, 'w') as f:
      f.write('<table border=\"1\">\n<tr><td colspan=\"8\" align=\"center\" bgcolor=\"orange\">' + time.asctime() + ' <b>' + esc(systemname) + '</b></td></tr>\n')
      f.write('<tr align=\"center\" bgcolor=\"yellow\"><td>Radio ID:</td><td>ConStat:</td><td>Callsign:</td><td>IP:</td><td>Ping Count:</td><td>Last Ping:</td><td>Rx QRG:</td><td>Tx QRG:</td></tr>\n')
      for client in clients:
        c = clients[client]
        f.write('<tr><td align=\"center\">' + esc(str(c['RADIO_ID']))
          + '</td><td align=\"center\">' + esc(c['CONNECTION'])
          + '</td><td align=\"center\">' + esc(c['CALLSIGN'])
          + '</td><td align=\"center\">' + esc(c['IP'])
          + '</td><td align=\"right\">' + esc(str(c['PINGS_RECEIVED']))
          + '</td><td align=\"right\">{:6.1f} sec ago'.format(time.time() - float(c['LAST_PING']))
          + '</td><td align=\"center\">' + qrg(c['RX_FREQ'])
          + '</td><td align=\"center\">' + qrg(c['TX_FREQ'])
          + '</td></tr>\n');
      f.write('</table>\n')
  except Exception as e: logger.error('(%s) Updating status file failed: %s', systemname, e)
