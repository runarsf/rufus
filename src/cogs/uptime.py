
def ReadableTime(first, last):
    readTime = int(last-first)
    weeks   = int(readTime/604800)
    days    = int((readTime-(weeks*604800))/86400)
    hours   = int((readTime-(days*86400 + weeks*604800))/3600)
    minutes = int((readTime-(hours*3600 + days*86400 + weeks*604800))/60)
    seconds = int(readTime-(minutes*60 + hours*3600 + days*86400 + weeks*604800))
    msg = ''
    if weeks > 0:
        msg += '1 week, ' if weeks == 1 else '{:,} weeks, '.format(weeks)
    if weeks > 0:
        msg += "1 week, " if weeks == 1 else "{:,} weeks, ".format(weeks)
    if days > 0:
        msg += "1 day, " if days == 1 else "{:,} days, ".format(days)
    if hours > 0:
        msg += "1 hour, " if hours == 1 else "{:,} hours, ".format(hours)
    if minutes > 0:
        msg += "1 minute, " if minutes == 1 else "{:,} minutes, ".format(minutes)
    if seconds > 0:
        msg += "1 second, " if seconds == 1 else "{:,} seconds, ".format(seconds)
    if msg == "":
        return "0 seconds"
    else:
        return msg[:-2]
